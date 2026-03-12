from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.mixins import TimestampMixin


class DeliveryLog(db.Model, TimestampMixin):
    __tablename__ = "delivery_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    channel: Mapped[str] = mapped_column(String(32), nullable=False)  # email|whatsapp
    destination: Mapped[str] = mapped_column(String(255), nullable=False)  # email or phone
    status: Mapped[str] = mapped_column(String(32), nullable=False)  # queued|sent|failed
    provider_message_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

