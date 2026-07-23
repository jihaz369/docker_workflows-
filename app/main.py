"""Application factory and entry point for the notes API."""

import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from app.config import config_by_name
from app.database import db
from app.routes import api_bp
from app.utils import setup_logging


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_name: The configuration environment name. Defaults to
            the FLASK_ENV environment variable or 'development'.

    Returns:
        The configured Flask application instance.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    setup_logging()

    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.errorhandler(404)
    def not_found(error: Exception) -> tuple:
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error: Exception) -> tuple:
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(error: Exception) -> tuple:
        return jsonify({"error": "Internal server error"}), 500

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
