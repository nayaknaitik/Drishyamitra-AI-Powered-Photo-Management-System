from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
from sqlalchemy import select

from config import settings

from app.ai.face_detection import decode_image_bytes, detect_faces
from app.ai.face_recognition import compute_embedding, cosine_similarity
from app.ai.photo_indexing import extract_photo_metadata
from app.extensions import db
from app.models import Face, FaceEmbedding, Person, Photo
from app.utils.errors import NotFoundError
from app.utils.security import EmbeddingCrypto
from app.utils.storage import StoragePaths, ensure_dir


@dataclass(frozen=True)
class UploadedFace:
    face_id: int
    x: int
    y: int
    w: int
    h: int
    is_unknown: bool
    person_id: int | None
    person_name: str | None


@dataclass(frozen=True)
class UploadResult:
    photo_id: int
    faces: list[UploadedFace]


class PhotoService:
    def __init__(self) -> None:
        self.paths = StoragePaths(settings.upload_root)
        self.crypto = EmbeddingCrypto.from_secret(settings.secret_key)

    def save_photo_and_process(
        self,
        *,
        user_id: int,
        filename: str | None,
        mime_type: str | None,
        image_bytes: bytes,
    ) -> UploadResult:
        photo = Photo(
            user_id=user_id,
            file_path="",
            original_filename=filename,
            mime_type=mime_type,
        )
        db.session.add(photo)
        db.session.flush()  # allocate ID

        user_dir = self.paths.user_dir(user_id)
        ensure_dir(user_dir)

        ext = _infer_ext(filename, mime_type)
        path = self.paths.photo_path(user_id, photo.id, ext=ext)
        with open(path, "wb") as f:
            f.write(image_bytes)

        meta = extract_photo_metadata(path)
        photo.file_path = path
        photo.taken_at = meta.taken_at
        photo.metadata_json = {"exif": meta.exif} if meta.exif else None
        db.session.commit()

        img = decode_image_bytes(image_bytes)
        detected = detect_faces(img, detector_backend="retinaface", enforce_detection=False)

        known = self._load_known_embeddings(user_id=user_id)

        out_faces: list[UploadedFace] = []
        for d in detected:
            emb_res = compute_embedding(img, d, model_name="Facenet512", detector_backend="retinaface")
            embedding = emb_res.embedding

            person = _best_match_person(embedding, known)

            emb_encrypted = self.crypto.encrypt(embedding.astype(np.float32).tobytes())
            emb_row = FaceEmbedding(
                user_id=user_id,
                model_name=emb_res.model_name,
                detector_backend=emb_res.detector_backend,
                vector_dim=int(embedding.shape[0]),
                embedding_encrypted=emb_encrypted,
            )
            db.session.add(emb_row)
            db.session.flush()

            face_row = Face(
                user_id=user_id,
                photo_id=photo.id,
                person_id=person.id if person else None,
                embedding_id=emb_row.id,
                x=d.x,
                y=d.y,
                w=d.w,
                h=d.h,
                detection_confidence=d.confidence,
                is_unknown=(person is None),
            )
            db.session.add(face_row)
            db.session.flush()

            out_faces.append(
                UploadedFace(
                    face_id=face_row.id,
                    x=face_row.x,
                    y=face_row.y,
                    w=face_row.w,
                    h=face_row.h,
                    is_unknown=face_row.is_unknown,
                    person_id=person.id if person else None,
                    person_name=person.name if person else None,
                )
            )

        db.session.commit()
        return UploadResult(photo_id=photo.id, faces=out_faces)

    def get_photo(self, *, user_id: int, photo_id: int) -> Photo:
        photo = db.session.execute(select(Photo).where(Photo.id == photo_id, Photo.user_id == user_id)).scalar_one_or_none()
        if not photo:
            raise NotFoundError("Photo not found")
        return photo

    def list_photos(self, *, user_id: int, limit: int = 200, offset: int = 0) -> list[Photo]:
        q = (
            select(Photo)
            .where(Photo.user_id == user_id)
            .order_by(Photo.created_at.desc())
            .limit(min(limit, 500))
            .offset(max(offset, 0))
        )
        return list(db.session.execute(q).scalars().all())

    def _load_known_embeddings(self, *, user_id: int) -> list[tuple[np.ndarray, Person]]:
        """
        Loads embeddings that are associated to a labeled person.
        """
        rows = (
            db.session.execute(
                select(FaceEmbedding, Face, Person)
                .join(Face, Face.embedding_id == FaceEmbedding.id)
                .join(Person, Face.person_id == Person.id)
                .where(FaceEmbedding.user_id == user_id)
            )
            .all()
        )
        out: list[tuple[np.ndarray, Person]] = []
        for emb_row, _face_row, person in rows:
            emb = np.frombuffer(self.crypto.decrypt(emb_row.embedding_encrypted), dtype=np.float32)
            out.append((emb, person))
        return out


def _infer_ext(filename: str | None, mime_type: str | None) -> str:
    if filename and "." in filename:
        ext = "." + filename.rsplit(".", 1)[-1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            return ext if ext != ".jpeg" else ".jpg"
    if mime_type == "image/png":
        return ".png"
    if mime_type == "image/webp":
        return ".webp"
    return ".jpg"


def _best_match_person(
    embedding: np.ndarray, known: list[tuple[np.ndarray, Person]], *, threshold: float = 0.72
) -> Person | None:
    best: tuple[float, Person] | None = None
    for known_emb, person in known:
        sim = cosine_similarity(embedding, known_emb)
        if best is None or sim > best[0]:
            best = (sim, person)
    if best and best[0] >= threshold:
        return best[1]
    return None

