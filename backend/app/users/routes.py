from datetime import datetime, timedelta
from os import environ as env
import jwt
from flask import jsonify, request
from app.users import bp
from app.repos.user_repo import UserRepo as ur
from app.helpers import token_required


@bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    print(email, password)
    # get user_id
    user = ur.get_user_by_logon(email, password)
    print(user)
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
    if not ur.change_password(curr_user.id, data["old_password"], data["new_password"]):
        return jsonify({"message": "Password change failed"}), 400
    return jsonify({"message": "Password changed successfully"}), 200


@bp.route("/profile/update", methods=["POST"])
@token_required
def update_user(curr_user):
    # update user data
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Invalid data"}), 400
    if not ur.update_user(curr_user.id, json_data):
        return jsonify({"message": "User was not updated"}), 400
    return jsonify({"message": "User updated successfully"}), 200

