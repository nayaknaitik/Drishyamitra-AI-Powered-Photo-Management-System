from __future__ import annotations

from flask.cli import FlaskGroup

from app.app_factory import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)

if __name__ == "__main__":
    cli()

