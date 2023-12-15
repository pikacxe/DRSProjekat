import atexit
from flask import Flask
from config import Config
from app.extensions import db, mail, cors, socketio
from os import environ as env


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Function to run before the first request is processed
    def before_first_request():
        # Add your startup code or process here
        print("Starting the application...")

    # Function to run when the application is being torn down
    def on_exit():
        # Add your cleanup or process-ending code here
        print("Tearing down the application...")

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # register blueprints
    from app.users import bp as users_bp

    app.register_blueprint(users_bp, url_prefix="/api")

    from app.admins import bp as admins_bp

    app.register_blueprint(admins_bp, url_prefix="/api/admin")

    from app.cards import bp as cards_bp

    app.register_blueprint(cards_bp, url_prefix="/api/card")

    from app.transactions import bp as transactions_bp

    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")

    # Run before_first_request function when the application context is pushed
    with app.app_context():
        before_first_request()

    # Teardown function when the application context is popped
    atexit.register(on_exit)

    return app, socketio
