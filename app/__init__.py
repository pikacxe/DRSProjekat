from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, mail, cors
from os import environ as env


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    # register blueprints
    from app.users import bp as users_bp

    app.register_blueprint(users_bp, url_prefix="/api")

    from app.admins import bp as admins_bp

    app.register_blueprint(admins_bp, url_prefix="/api/admin")

    from app.cards import bp as cards_bp

    app.register_blueprint(cards_bp, url_prefix="/api/card")

    from app.transactions import bp as transactions_bp

    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")

    return app
