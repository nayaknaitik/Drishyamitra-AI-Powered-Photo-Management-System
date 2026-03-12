from __future__ import annotations

import logging

from flask import Flask, jsonify
from flask_cors import CORS

from config import settings

from .extensions import cache, db, jwt, limiter, migrate
from .utils.errors import AppError
from .utils.logging import configure_logging


def create_app() -> Flask:
    configure_logging("INFO")
    app = Flask(__name__)

    app.config.update(
        ENV=settings.flask_env,
        DEBUG=settings.flask_debug,
        SECRET_KEY=settings.secret_key,
        JWT_SECRET_KEY=settings.jwt_secret_key,
        JWT_ACCESS_TOKEN_EXPIRES=settings.jwt_access_token_expires_minutes * 60,
        SQLALCHEMY_DATABASE_URI=_resolve_database_uri(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAX_CONTENT_LENGTH=settings.max_content_length_mb * 1024 * 1024,
    )

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

    db.init_app(app)
    # Ensure models are registered for migrations
    from app import models as _models  # noqa: F401
    migrate.init_app(app, db)
    jwt.init_app(app)

    limiter.init_app(app)

    _init_cache(app)

    _register_error_handlers(app)
    _register_health(app)
    _register_api(app)

    return app


def _resolve_database_uri() -> str:
    url = (settings.database_url or "").strip()
    if url:
        return url
    sqlite_path = settings.sqlite_fallback_path
    return f"sqlite:///{sqlite_path}"


def _init_cache(app: Flask) -> None:
    if settings.redis_url:
        app.config["CACHE_TYPE"] = "RedisCache"
        app.config["CACHE_REDIS_URL"] = settings.redis_url
    cache.init_app(app)


def _register_health(app: Flask) -> None:
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(err: AppError):
        return jsonify({"error": str(err)}), err.status_code

    @app.errorhandler(413)
    def handle_413(_err):
        return jsonify({"error": "File too large"}), 413

    @app.errorhandler(Exception)
    def handle_unhandled(err: Exception):
        logging.exception("Unhandled error")
        return jsonify({"error": "Internal server error"}), 500


def _register_api(app: Flask) -> None:
    from app.api.blueprints import api_blueprint

    app.register_blueprint(api_blueprint())

