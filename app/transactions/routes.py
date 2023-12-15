from flask import jsonify, request
from app.models.account_balance import AccountBalance
from app.models.card import Card
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
    socketio.emit('completed_transactions', {'data': data})
    
@socketio.on('connect')
def test_connect(auth):
    socketio.emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@bp.route("/add", methods=["POST"])
@token_required
def add_transaction(curr_user):
    # add new transaction
    json_data = request.get_json()
    data = TransactionForm(formdata=None, **json_data, meta={"csrf": False})
    if not data or not data.validate():
        return jsonify({"message": "Invalid data"}), 400
    # check if card belongs to user
    card = Card.query.filter_by(card_number=data.sender_card_number).first()
    if not card:
        return jsonify({"message": "Card not found"}), 404
    if card.user_id != curr_user.id:
        return jsonify({"message": "Card does not belong to user"}), 401
    # check if user has enough money in account balance
    account_balances = AccountBalance.query.filter_by(card_number=card.card_number).all()
    if not account_balances:
        return jsonify({"message": "Account balance not found"}), 404
    # check if account_balance with currency exists
    account_balance = None
    for acc in account_balances:
        if acc.currency == data.currency:
            account_balance = acc
            break
    if not account_balance:
        return jsonify({"message": "Account balance not found"}), 404
    # check if account has enough money
    if account_balance.amount < data.amount:
        return jsonify({"message": "Not enough money in account"}), 400 
    # create new transaction
    new_transaction = Transaction(data, curr_user.id)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Transaction added successfully"}), 200