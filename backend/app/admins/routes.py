from flask import jsonify, request
from app.repos.user_repo import UserRepo as ur
from app.admins import bp
from app.helpers import token_required
from app.services.mail_service import MailService 



# get all users
@bp.route("/users", methods=["GET"])
@token_required
def get_all_unverified_users(curr_user):
    if not curr_user.is_admin:
        return jsonify({"message": "You are not an admin"}), 401
    data = ur.get_all_unverified_users()
    return jsonify(data), 200


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
    u=ur.add_user(data)
    if not u:
        return jsonify({'message': 'User was not created'}), 400
    # send mail to user with login details
    
    if not MailService.send_mail_register(u):
        return jsonify({"message": "Mail was not sent"}), 500

    return jsonify({"message": "User created successfully"}), 200


@bp.route("/verify", methods=["POST"])
@token_required
def verify_user(curr_user):
    if not curr_user.is_admin:
        return jsonify({"message": "You are not an admin"}), 401
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400
    if not ur.verify_user(data['user_id']):
        return jsonify({'message': 'User was not verified'}), 400
    # send mail to user with successful verification
    if not MailService.send_mail_verification(ur.get_user_by_id(data['user_id'])):
        return jsonify({'message': 'Mail was not sent'}), 500 
    
    return jsonify({'message': 'User verified successfully'}), 200 