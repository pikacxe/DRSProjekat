from datetime import datetime, timedelta
from os import environ as env
import jwt
from flask import jsonify, request
from app.users import bp
from app.models.user import User
from app.models.transaction import Transaction
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

    return jsonify({"access_token": token}), 200


@bp.route("/profile", methods=["GET"])
@token_required
def get_user(curr_user):
    if not curr_user:
        return jsonify({"message": "Please log in!"}), 401
    return jsonify(curr_user.to_json())


@bp.route("/profile/update", methods=["POST"])
@token_required
def update_user(curr_user):
    # update user data
    data = request.form
    # update curr_user with data
    # TODO map form data to User model

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200


@bp.route("/transaction/add", methods=["POST"])
@token_required
def add_transaction(curr_user):
    # add new transaction
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid data"}), 400
    # TODO add new transaction to db
    # map form data to Transaction model
    # add transaction to db
    # update user balance
    return jsonify({"message": "Transaction added successfully"}), 200
