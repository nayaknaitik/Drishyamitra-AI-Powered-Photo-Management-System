from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.search_service import SearchService

bp = Blueprint("search", __name__)
svc = SearchService()


@bp.post("")
@jwt_required()
def search():
    user_id = int(get_jwt_identity())
    payload = request.get_json(force=True) or {}
    query = str(payload.get("query", "")).strip()
    parsed, photos = svc.search(user_id=user_id, query_text=query)
    return jsonify(
        {
            "parsed": {
                "intent": parsed.intent,
                "person_name": parsed.person_name,
                "event": parsed.event,
                "year": parsed.year,
                "raw": parsed.raw,
            },
            "items": [{"id": p.id, "taken_at": p.taken_at.isoformat() if p.taken_at else None} for p in photos],
        }
    )

