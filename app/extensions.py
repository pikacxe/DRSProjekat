from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from flask_socketio import SocketIO

db = SQLAlchemy()

mail = Mail()

cors = CORS()

socketio = SocketIO() 

