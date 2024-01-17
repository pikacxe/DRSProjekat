from flask import jsonify, request
from app.repos.transaction_repo import TransactionRepo as tr
from app.transactions import bp
from app.helpers import token_required

@bp.route('/', methods=['GET'])
@token_required
def get_all_transactions(curr_user):
    # check if user is admin
    if not curr_user.is_admin:
        return jsonify({'message': 'You are not an admin'}), 401
    data = tr.get_all_transactions()
    return jsonify([x.to_json() for x in data]), 200

@bp.route("/add", methods=["POST"])
@token_required
def add_transaction(curr_user):
    # add new transaction
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Invalid data"}), 400
    if not tr.add_transaction(json_data, curr_user.id):
        return jsonify({"message": "Transaction was not created"}), 400
    return jsonify({"message": "Transaction added successfully"}), 200