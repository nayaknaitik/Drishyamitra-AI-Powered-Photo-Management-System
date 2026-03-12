from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.face_service import FaceService

bp = Blueprint("faces", __name__)
svc = FaceService()


@bp.post("/label")
@jwt_required()
def label():
    user_id = int(get_jwt_identity())
    payload = request.get_json(force=True) or {}
    face_id = int(payload.get("face_id"))
    person_id = payload.get("person_id")
    person_id_int = int(person_id) if person_id is not None else None
    person_name = payload.get("person_name")

    face = svc.label_face(
        user_id=user_id,
        face_id=face_id,
        person_name=str(person_name).strip() if person_name else None,
        person_id=person_id_int,
    )
    return jsonify({"face": {"id": face.id, "person_id": face.person_id, "is_unknown": face.is_unknown}})


@bp.get("/persons")
@jwt_required()
def persons():
    user_id = int(get_jwt_identity())
    persons = svc.list_persons(user_id=user_id)
    return jsonify({"items": [{"id": p.id, "name": p.name} for p in persons]})

