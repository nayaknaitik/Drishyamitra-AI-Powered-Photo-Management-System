from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from deepface import DeepFace

from app.ai.face_detection import DetectedFace


@dataclass(frozen=True)
class FaceEmbeddingResult:
    embedding: np.ndarray  # float32
    model_name: str
    detector_backend: str


def crop_face(img_bgr: np.ndarray, face: DetectedFace) -> np.ndarray:
    h_img, w_img = img_bgr.shape[:2]
    x1 = max(0, face.x)
    y1 = max(0, face.y)
    x2 = min(w_img, face.x + face.w)
    y2 = min(h_img, face.y + face.h)
    return img_bgr[y1:y2, x1:x2]


def compute_embedding(
    img_bgr: np.ndarray,
    face: DetectedFace,
    *,
    model_name: str = "Facenet512",
    detector_backend: str = "retinaface",
) -> FaceEmbeddingResult:
    """
    Computes an embedding for a detected face.

    We pass the cropped face and skip further detection to keep pipeline deterministic.
    """
    face_img = crop_face(img_bgr, face)
    reps = DeepFace.represent(
        img_path=face_img,
        model_name=model_name,
        detector_backend=detector_backend,
        enforce_detection=False,
        align=True,
    )
    emb = np.array(reps[0]["embedding"], dtype=np.float32)
    return FaceEmbeddingResult(embedding=emb, model_name=model_name, detector_backend=detector_backend)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)
    return float(np.dot(a, b) / denom)

