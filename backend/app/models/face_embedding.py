from __future__ import annotations

from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin


class FaceEmbedding(db.Model, TimestampMixin):
    __tablename__ = "face_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    model_name: Mapped[str] = mapped_column(String(128), nullable=False)  # e.g. Facenet512
    detector_backend: Mapped[str] = mapped_column(String(128), nullable=False)  # e.g. RetinaFace
    vector_dim: Mapped[int] = mapped_column(nullable=False)

    # Encrypted embedding bytes (float32 array serialized)
    embedding_encrypted: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    face = relationship("Face", back_populates="embedding", uselist=False)

