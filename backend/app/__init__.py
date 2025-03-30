from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from app.config import Config
import certifi


mongo = PyMongo()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    mongo.init_app(app, tlsCAFile=certifi.where())
    CORS(app)

    # Register blueprints
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.route("/api/health")
    def health_check():
        return {"status": "healthy"}, 200

    return app
