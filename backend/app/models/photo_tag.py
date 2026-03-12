from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin


class PhotoTag(db.Model, TimestampMixin):
    __tablename__ = "photo_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    photo_id: Mapped[int] = mapped_column(ForeignKey("photos.id", ondelete="CASCADE"), index=True, nullable=False)

    key: Mapped[str] = mapped_column(String(64), index=True, nullable=False)  # e.g. event, location
    value: Mapped[str] = mapped_column(String(255), index=True, nullable=False)  # e.g. Diwali

    photo = relationship("Photo", back_populates="tags")

