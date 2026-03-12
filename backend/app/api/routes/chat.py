from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.chat_service import ChatService

bp = Blueprint("chat", __name__)
svc = ChatService()


@bp.post("")
@jwt_required()
def chat():
    user_id = int(get_jwt_identity())
    payload = request.get_json(force=True) or {}
    message = str(payload.get("message", "")).strip()
    result = svc.handle_message(user_id=user_id, message=message)
    return jsonify(result)

