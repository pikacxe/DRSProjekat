import uuid
from flask import jsonify, request
from flask_mail import Message
from app.models.user import User
from app.admins import bp
from app.helpers import token_required
from app.extensions import db, mail
from os import environ as env  


# get all users
@bp.route("/users", methods=["GET"])
@token_required
def get_all_unverified_users(curr_user):
    if not curr_user.is_admin:
        return jsonify({"message": "You are not an admin"}), 401
    data = User.query.filter_by(is_verified=False).all()
    return jsonify([x.to_json() for x in data]), 200


# register a new user
@bp.route("/register", methods=["POST"])
@token_required
def register(curr_user):
    if not curr_user.is_admin:
        return jsonify({"message": "You are not an admin"}), 401
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400
    # add new user to db
    user = User(id=str(uuid.uuid4()), email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    # send mail to user with login details
    msg = Message(
        "Account was created successfully",
        recipients=[user.email])
    msg.body = f"Hello, your account was created successfully. Your login details are:\nEmail: {user.email}\nPassword: {user.password}\n"
    mail.send(msg)
    return jsonify({"message": "User created successfully"}), 200


@bp.route("/verify", methods=["POST"])
@token_required
def verify_user(curr_user):
    if not curr_user.is_admin:
        return jsonify({"message": "You are not an admin"}), 401
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400
    user_to_verify = User.query.filter_by(id = data['user_id']).first()
    user_to_verify.is_verified = True
    db.session.commit()
    # send mail to user with successful verification
    msg = Message(
        "Account was verified successfully",
        recipients=[user_to_verify.email])
    msg.body = f"Hello, your account was verified successfully. You can now login to your account.\n"
    mail.send(msg)
    
    return jsonify({'message': 'User verified successfully'}), 200 