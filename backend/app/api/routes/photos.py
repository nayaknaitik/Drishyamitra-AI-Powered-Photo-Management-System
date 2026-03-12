from __future__ import annotations

import mimetypes

from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.photo_service import PhotoService

bp = Blueprint("photos", __name__)
svc = PhotoService()


@bp.post("/upload")
@jwt_required()
def upload():
    user_id = int(get_jwt_identity())
    if "file" not in request.files:
        return jsonify({"error": "Missing file"}), 400
    file = request.files["file"]
    image_bytes = file.read()
    mime_type = file.mimetype or mimetypes.guess_type(file.filename or "")[0]

    res = svc.save_photo_and_process(
        user_id=user_id,
        filename=file.filename,
        mime_type=mime_type,
        image_bytes=image_bytes,
    )
    return jsonify(
        {
            "photo_id": res.photo_id,
            "faces": [
                {
                    "id": f.face_id,
                    "x": f.x,
                    "y": f.y,
                    "w": f.w,
                    "h": f.h,
                    "is_unknown": f.is_unknown,
                    "person_id": f.person_id,
                    "person_name": f.person_name,
                }
                for f in res.faces
            ],
        }
    )


@bp.get("")
@jwt_required()
def list_photos():
    user_id = int(get_jwt_identity())
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    photos = svc.list_photos(user_id=user_id, limit=limit, offset=offset)
    return jsonify(
        {
            "items": [
                {
                    "id": p.id,
                    "taken_at": p.taken_at.isoformat() if p.taken_at else None,
                    "created_at": p.created_at.isoformat(),
                    "original_filename": p.original_filename,
                }
                for p in photos
            ]
        }
    )


@bp.get("/<int:photo_id>")
@jwt_required()
def get_photo(photo_id: int):
    user_id = int(get_jwt_identity())
    p = svc.get_photo(user_id=user_id, photo_id=photo_id)
    return jsonify(
        {
            "id": p.id,
            "taken_at": p.taken_at.isoformat() if p.taken_at else None,
            "created_at": p.created_at.isoformat(),
            "original_filename": p.original_filename,
            "mime_type": p.mime_type,
        }
    )


@bp.get("/<int:photo_id>/file")
@jwt_required()
def get_photo_file(photo_id: int):
    user_id = int(get_jwt_identity())
    p = svc.get_photo(user_id=user_id, photo_id=photo_id)
    return send_file(p.file_path, mimetype=p.mime_type or "image/jpeg", as_attachment=False)

