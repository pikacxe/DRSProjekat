from os import environ as env


class Config:
    JWT_SECRET_KEY = env["JWT_SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = env["DB_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = "*"
    CORS_RESOURCES = r"/api/*"
    MAIL_SERVER = "sandbox.smtp.mailtrap.io"
    MAIL_USE_SSL = False
    MAIL_PORT = 2525
    MAIL_USERNAME = "2911d7b4eaaf8a"
    MAIL_PASSWORD = "1d09d3d2c356f4"
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = "drs.projekat.mail@gmail.com"
    TRANSACTION_PERIOD = 5
