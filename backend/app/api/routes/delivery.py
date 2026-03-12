from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.delivery_service import DeliveryService

bp = Blueprint("delivery", __name__)
svc = DeliveryService()


@bp.post("/email")
@jwt_required()
def send_email():
    user_id = int(get_jwt_identity())
    payload = request.get_json(force=True) or {}
    destination = str(payload.get("to", "")).strip()
    photo_ids = [int(x) for x in (payload.get("photo_ids") or [])]
    job = svc.queue_email(user_id=user_id, to_email=destination, photo_ids=photo_ids)
    return jsonify(job)


@bp.post("/whatsapp")
@jwt_required()
def send_whatsapp():
    user_id = int(get_jwt_identity())
    payload = request.get_json(force=True) or {}
    destination = str(payload.get("to", "")).strip()
    photo_ids = [int(x) for x in (payload.get("photo_ids") or [])]
    job = svc.queue_whatsapp(user_id=user_id, to_phone=destination, photo_ids=photo_ids)
    return jsonify(job)

