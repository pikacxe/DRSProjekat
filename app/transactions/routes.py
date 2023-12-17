from flask import jsonify, request
from app.models.account_balance import AccountBalance
from app.models.card import Card
from app.models.transaction import Transaction
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

@bp.route("/add", methods=["POST"])
@token_required
def add_transaction(curr_user):
    # add new transaction
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Invalid data"}), 400
    try:
        data = Transaction(json_data, curr_user.id)
    except Exception as e:
        print(e)
        return jsonify({"message": "Invalid data"}), 400
    # check if card belongs to user
    card = Card.query.filter_by(card_number=data.sender_card_number).first()
    if not card:
        return jsonify({"message": "Card not found"}), 404
    if card.user_id != curr_user.id:
        return jsonify({"message": "Card does not belong to user"}), 401
    # check if account_balance with currency exists
    account_balance = AccountBalance.query.filter_by(card_number=card.card_number, currency=data.currency).first()
    if not account_balance:
        return jsonify({"message": "Account balance not found"}), 404
    '''
    # check if account has enough money
    if account_balance.amount < data.amount:
        return jsonify({"message": "Not enough money in account"}), 400 
    '''
    db.session.add(data)
    db.session.commit()
    return jsonify({"message": "Transaction added successfully"}), 200


# Web Socker
@socketio.on('connect')
def connect():
    print('Client connected')
    socketio.emit('response', {'data': 'Connected'})

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')