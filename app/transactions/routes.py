from flask import jsonify, request
from app.models.transaction import Transaction, TransactionForm
from app.transactions import bp
from app.extensions import db, socketio
from app.helpers import token_required

@bp.route('/', methods=['GET'])
@token_required
def get_all_transactions(curr_user):
    # check if user is admin
    if not curr_user.is_admin:
        return jsonify({'message': 'You are not an admin'}), 401
    data = Transaction.query.all()
    return jsonify([x.to_json() for x in data]), 200

@socketio.on('transaction_complete')
def get_transaction_complete(data):
    # socketio emit
    socketio.emit('completed_transactions', {'data': 'Transaction complete'})
    


@bp.route("/add", methods=["POST"])
@token_required
def add_transaction(curr_user):
    # add new transaction
    json_data = request.get_json()
    data = TransactionForm(formdata=None, **json_data, meta={"csrf": False})
    if not data or not data.validate():
        return jsonify({"message": "Invalid data"}), 400
    # create new transaction
    new_transaction = Transaction(data, curr_user.id)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Transaction added successfully"}), 200