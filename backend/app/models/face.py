from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin


class Face(db.Model, TimestampMixin):
    __tablename__ = "faces"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    photo_id: Mapped[int] = mapped_column(ForeignKey("photos.id", ondelete="CASCADE"), index=True, nullable=False)

    person_id: Mapped[int | None] = mapped_column(ForeignKey("persons.id", ondelete="SET NULL"), index=True)
    embedding_id: Mapped[int | None] = mapped_column(ForeignKey("face_embeddings.id", ondelete="SET NULL"), index=True)

    # Bounding box (pixels)
    x: Mapped[int] = mapped_column(Integer, nullable=False)
    y: Mapped[int] = mapped_column(Integer, nullable=False)
    w: Mapped[int] = mapped_column(Integer, nullable=False)
    h: Mapped[int] = mapped_column(Integer, nullable=False)

    detection_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_unknown: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    photo = relationship("Photo", back_populates="faces")
    person = relationship("Person", back_populates="faces")
    embedding = relationship("FaceEmbedding", back_populates="face")

