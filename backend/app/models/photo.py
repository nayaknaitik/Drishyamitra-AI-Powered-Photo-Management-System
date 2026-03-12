from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin


class Photo(db.Model, TimestampMixin):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    original_filename: Mapped[str | None] = mapped_column(String(512), nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(128), nullable=True)

    taken_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # For SQLite, SQLAlchemy will fall back to JSON.
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    user = relationship("User", back_populates="photos")
    faces = relationship("Face", back_populates="photo", cascade="all, delete-orphan")
    tags = relationship("PhotoTag", back_populates="photo", cascade="all, delete-orphan")

