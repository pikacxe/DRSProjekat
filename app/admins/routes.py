import uuid
from flask import jsonify, request
from flask_mail import Message
from app.repos.user_repo import UserRepo as ur
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
    data = ur.get_all_unverified_users()
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
    if not ur.add_user(data):
        return jsonify({'message': 'User was not created'}), 400
    # send mail to user with login details
    msg = Message(
        "Account was created successfully",
        recipients=[data['email']])
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
    if not ur.verify_user(data['id']):
        return jsonify({'message': 'User was not verified'}), 400
    # send mail to user with successful verification
    msg = Message(
        "Account was verified successfully",
        recipients=[data['email']])
    msg.body = f"Hello, your account was verified successfully. You can now login to your account.\n"
    mail.send(msg)
    
    return jsonify({'message': 'User verified successfully'}), 200 