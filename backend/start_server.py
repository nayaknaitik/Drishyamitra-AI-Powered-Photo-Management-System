"""
Entry point for running the Flask API.

Development entry point (uses Flask built-in server).
"""

def main() -> None:
    from app.app_factory import create_app

    app = create_app()
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()

