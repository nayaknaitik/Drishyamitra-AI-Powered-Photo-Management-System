from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

from sqlalchemy import select
from twilio.rest import Client as TwilioClient

from config import settings

from app.extensions import db
from app.models import DeliveryLog, Photo
from app.utils.errors import NotFoundError
from app.workers.celery_app import celery_app


class DeliveryService:
    def queue_email(self, *, user_id: int, to_email: str, photo_ids: list[int]) -> dict:
        log = DeliveryLog(user_id=user_id, channel="email", destination=to_email, status="queued")
        db.session.add(log)
        db.session.commit()

        celery_app.send_task("drishyamitra.send_email", args=[log.id, user_id, to_email, photo_ids])
        return {"delivery_log_id": log.id, "status": "queued"}

    def queue_whatsapp(self, *, user_id: int, to_phone: str, photo_ids: list[int]) -> dict:
        log = DeliveryLog(user_id=user_id, channel="whatsapp", destination=to_phone, status="queued")
        db.session.add(log)
        db.session.commit()

        celery_app.send_task("drishyamitra.send_whatsapp", args=[log.id, user_id, to_phone, photo_ids])
        return {"delivery_log_id": log.id, "status": "queued"}


def send_email_sync(*, user_id: int, to_email: str, photo_paths: list[str]) -> None:
    if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password or not settings.smtp_from:
        raise RuntimeError("SMTP not configured")

    msg = EmailMessage()
    msg["Subject"] = "Drishyamitra photos"
    msg["From"] = settings.smtp_from
    msg["To"] = to_email
    msg.set_content("Your requested photos are attached.")

    for p in photo_paths[:10]:
        with open(p, "rb") as f:
            data = f.read()
        msg.add_attachment(data, maintype="image", subtype="jpeg", filename=os.path.basename(p))

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.starttls()
        smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(msg)


def send_whatsapp_sync(*, to_phone: str, media_urls: list[str]) -> str:
    if not settings.twilio_account_sid or not settings.twilio_auth_token or not settings.twilio_whatsapp_from:
        raise RuntimeError("Twilio WhatsApp not configured")
    client = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)
    msg = client.messages.create(
        from_=settings.twilio_whatsapp_from,
        to=f"whatsapp:{to_phone}" if not to_phone.startswith("whatsapp:") else to_phone,
        body="Drishyamitra photos",
        media_url=media_urls[:10] if media_urls else None,
    )
    return str(msg.sid)

