
import os

from flask import Flask, jsonify
from sqlalchemy import event

from server.extensions import db, migrate


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=(
            "sqlite:///" + os.path.join(app.instance_path, "workout.db")
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        engine = db.engine

        def enable_foreign_keys(connection, record):
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        event.listen(engine, "connect", enable_foreign_keys)

        from server import models

    from server.app import register_routes
    register_routes(app)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal server error."}), 500

    return app
