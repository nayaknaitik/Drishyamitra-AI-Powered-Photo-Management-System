from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from flask_limiter import Limiter

from app.extensions import limiter
from app.services.auth_service import AuthService

bp = Blueprint("auth", __name__)
svc = AuthService()


@bp.post("/register")
@limiter.limit("10/minute")
def register():
    payload = request.get_json(force=True) or {}
    email = str(payload.get("email", "")).strip()
    password = str(payload.get("password", "")).strip()
    user = svc.register(email=email, password=password)
    token = create_access_token(identity=str(user.id))
    return jsonify({"user": {"id": user.id, "email": user.email}, "access_token": token})


@bp.post("/login")
@limiter.limit("20/minute")
def login():
    payload = request.get_json(force=True) or {}
    email = str(payload.get("email", "")).strip()
    password = str(payload.get("password", "")).strip()
    user = svc.authenticate(email=email, password=password)
    token = create_access_token(identity=str(user.id))
    return jsonify({"user": {"id": user.id, "email": user.email}, "access_token": token})

