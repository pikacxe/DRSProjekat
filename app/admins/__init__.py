from flask import Blueprint

bp = Blueprint('admins', __name__)

from app.admins import routes
