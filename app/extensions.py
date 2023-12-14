from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_cors import CORS

db = SQLAlchemy()

mail = Mail()

cors = CORS()

