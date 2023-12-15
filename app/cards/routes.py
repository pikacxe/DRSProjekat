from flask import jsonify, request
from app.cards import bp
from app.models.card import Card
from app.models.account_balance import AccountBalance
from app.helpers import token_required
from app.extensions import db


@bp.route("/", methods=["GET"])
@token_required
def get_all_cards(curr_user):
    # get all card for user
    user_cards = Card.query.filter_by(user_id=curr_user.id).all()
    if not user_cards or not curr_user.is_verified:
        return jsonify([]), 200
    data = []
    for uc in user_cards:
        # get account balances for each card
        account_balances = AccountBalance.query.filter_by(card_number=uc.card_number).all()
        # get account currencies
        account_currencies = [x.currency for x in account_balances]
        # create a dictionary for each card and its account balances
        el = {
            "card": uc.to_json(),
            "account_balances": [x.to_json() for x in account_balances],
            "account_currencies": account_currencies,
        }

        data.append(el)
    return jsonify(data), 200


@bp.route("/add", methods=["POST"])
@token_required
def add_card(curr_user):
    # add new card
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400
    new_card = Card(card_number=data['card_number'], user_id=curr_user.id)
    # create default acc balance for card
    new_balance = AccountBalance(card_number=new_card.card_number)
    db.session.add(new_card)
    db.session.commit()
    db.session.add(new_balance)
    db.session.commit()

    return jsonify({'message':'Card added successfully'}), 200


@bp.route("/<string:card_number>/", methods=["GET"])
@token_required
def get_card(curr_user, card_number):
    # check if card belongs to user
    card= Card.query.filter_by(card_number=card_number).first()
    if not card:
        return jsonify({'message': 'Card not found!'}), 404
    if card.user_id != curr_user.id:
        return jsonify({'message': 'Card does not belong to user!'}), 401
    # get account balances for card
    account_balances = AccountBalance.query.filter_by(card_number=card_number).all()
    # create a dictionary for each card and its account balances
    data = {
        "card": card.to_json(),
        "account_balances": [x.to_json() for x in account_balances]
    }
    return jsonify(data), 200

@bp.route("/<string:card_number>/deposit", methods=["POST"])
@token_required
def deposit(curr_user, card_number):
    # check if card belongs to user
    card= Card.query.filter_by(card_number=card_number).first()
    if not card:
        return jsonify({'message': 'Card not found!'}), 404
    if card.user_id != curr_user.id:
        return jsonify({'message': 'Card does not belong to user!'}), 401
    # check if account balance with specified currency exists
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid data'}), 400
    currency = data['currency']
    amount = data['amount']
    account_balance = AccountBalance.query.filter_by(card_number=card_number, currency=currency).first()
    if not account_balance:
        # create new account balance
        account_balance = AccountBalance(card_number=card_number, currency=currency, amount=amount)
        db.session.add(account_balance)     
    else:
        # update existing account balance
        account_balance.amount += amount
    db.session.merge(account_balance)
    db.session.commit()
    return jsonify({"message":"Account balance updated successfully"}), 200