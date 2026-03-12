from __future__ import annotations

from flask import Blueprint


def api_blueprint() -> Blueprint:
    bp = Blueprint("api", __name__)

    from app.api.routes.auth import bp as auth_bp
    from app.api.routes.chat import bp as chat_bp
    from app.api.routes.delivery import bp as delivery_bp
    from app.api.routes.faces import bp as faces_bp
    from app.api.routes.photos import bp as photos_bp
    from app.api.routes.persons import bp as persons_bp
    from app.api.routes.search import bp as search_bp

    bp.register_blueprint(auth_bp, url_prefix="/auth")
    bp.register_blueprint(photos_bp, url_prefix="/photos")
    bp.register_blueprint(faces_bp, url_prefix="/faces")
    bp.register_blueprint(persons_bp, url_prefix="/persons")
    bp.register_blueprint(search_bp, url_prefix="/search")
    bp.register_blueprint(chat_bp, url_prefix="/chat")
    bp.register_blueprint(delivery_bp, url_prefix="/send")

    return bp

