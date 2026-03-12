from __future__ import annotations

from app.workers.celery_app import celery_app


@celery_app.task(name="drishyamitra.ping")
def ping() -> str:
    return "pong"


@celery_app.task(name="drishyamitra.send_email")
def send_email(delivery_log_id: int, user_id: int, to_email: str, photo_ids: list[int]) -> str:
    from sqlalchemy import select

    from app.app_factory import create_app
    from app.extensions import db
    from app.models import DeliveryLog, Photo
    from app.services.delivery_service import send_email_sync

    app = create_app()
    with app.app_context():
        log = db.session.execute(select(DeliveryLog).where(DeliveryLog.id == delivery_log_id)).scalar_one_or_none()
        if not log:
            return "missing_log"
        try:
            photos = list(
                db.session.execute(select(Photo).where(Photo.user_id == user_id, Photo.id.in_(photo_ids))).scalars().all()
            )
            send_email_sync(user_id=user_id, to_email=to_email, photo_paths=[p.file_path for p in photos])
            log.status = "sent"
            db.session.commit()
            return "sent"
        except Exception as e:
            log.status = "failed"
            log.error_message = str(e)
            db.session.commit()
            raise


@celery_app.task(name="drishyamitra.send_whatsapp")
def send_whatsapp(delivery_log_id: int, user_id: int, to_phone: str, photo_ids: list[int]) -> str:
    from sqlalchemy import select

    from config import settings

    from app.app_factory import create_app
    from app.extensions import db
    from app.models import DeliveryLog, Photo
    from app.services.delivery_service import send_whatsapp_sync

    app = create_app()
    with app.app_context():
        log = db.session.execute(select(DeliveryLog).where(DeliveryLog.id == delivery_log_id)).scalar_one_or_none()
        if not log:
            return "missing_log"
        try:
            photos = list(
                db.session.execute(select(Photo).where(Photo.user_id == user_id, Photo.id.in_(photo_ids))).scalars().all()
            )
            base = str(settings.public_base_url or "http://localhost")
            media_urls = [f"{base}/api/photos/{p.id}/file" for p in photos]
            sid = send_whatsapp_sync(to_phone=to_phone, media_urls=media_urls)
            log.status = "sent"
            log.provider_message_id = sid
            db.session.commit()
            return "sent"
        except Exception as e:
            log.status = "failed"
            log.error_message = str(e)
            db.session.commit()
            raise

