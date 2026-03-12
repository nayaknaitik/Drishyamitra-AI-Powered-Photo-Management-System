from __future__ import annotations

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.face_service import FaceService

bp = Blueprint("persons", __name__)
svc = FaceService()


@bp.get("")
@jwt_required()
def list_persons():
    user_id = int(get_jwt_identity())
    persons = svc.list_persons(user_id=user_id)
    return jsonify({"items": [{"id": p.id, "name": p.name} for p in persons]})

