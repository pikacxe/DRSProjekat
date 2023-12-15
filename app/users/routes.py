from datetime import datetime, timedelta
from os import environ as env
import jwt
from flask import jsonify, request
from app.users import bp
from app.models.user import User, UserForm
from app.helpers import token_required
from app.extensions import db


@bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    # get user_id
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    # generate token
    payload = {"id": user.id, "exp": datetime.utcnow() + timedelta(days=1)}
    key = env["JWT_SECRET_KEY"]
    token = jwt.encode(payload, key, algorithm="HS256")
    res = {
        "access_token": token,
        "is_admin": user.is_admin,
        "is_verified": user.is_verified,    
    }
    return jsonify(res), 200


@bp.route("/profile", methods=["GET"])
@token_required
def get_user(curr_user):
    if not curr_user:
        return jsonify({"message": "Please log in!"}), 401
    return jsonify(curr_user.to_json())

@bp.route("/profile/change-password", methods=["POST"])
@token_required
def change_password(curr_user):
    # change user password
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid data"}), 400
    # check if old password matches
    if curr_user.password != data["old_password"]:
        return jsonify({"message": "Old password does not match user password"}), 401
    # update password
    curr_user.password = data["new_password"]
    db.session.merge(curr_user)
    db.session.commit()
    return jsonify({"message": "Password changed successfully"}), 200


@bp.route("/profile/update", methods=["POST"])
@token_required
def update_user(curr_user):
    # update user data
    json_data = request.get_json()
    data = UserForm(formdata=None, **json_data, meta={"csrf": False})
    if not data or not data.validate():
        return jsonify({"message": "Invalid data"}), 400
    # update curr_user with data using constructor
    curr_user = User(data, curr_user.id)
    # update user in db
    db.session.merge(curr_user)
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

