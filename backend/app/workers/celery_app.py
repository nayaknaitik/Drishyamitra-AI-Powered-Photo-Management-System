from __future__ import annotations

from celery import Celery

from config import settings


def make_celery() -> Celery:
    broker = settings.celery_broker_url or settings.redis_url
    backend = settings.celery_result_backend or settings.redis_url
    if not broker or not backend:
        # Celery optional; tasks can be executed synchronously if not configured
        broker = "memory://"
        backend = "cache+memory://"

    celery = Celery(
        "drishyamitra",
        broker=broker,
        backend=backend,
        include=["app.workers.tasks"],
    )
    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )
    return celery


celery_app = make_celery()

