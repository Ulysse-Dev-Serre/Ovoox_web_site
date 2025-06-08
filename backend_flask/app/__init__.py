# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from app import models # Importe tes modèles
    from app.routes_blog import blog_bp

    # ENREGISTRE LE BLUEPRINT SUR L'APPLICATION
    app.register_blueprint(blog_bp)

    return app