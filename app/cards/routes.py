from flask import jsonify, request
from app.cards import bp
from app.helpers import token_required
from app.repos.card_repo import CardRepo as cr


@bp.route("/", methods=["GET"])
@token_required
def get_all_cards(curr_user):
    # get all card for user
    data = cr.get_all_cards_for_user(curr_user.id)
    if not data or data == []:
        return jsonify({"message": "No cards found"}), 404
    return jsonify(data), 200


@bp.route("/add", methods=["POST"])
@token_required
def add_card(curr_user):
    # add new card
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid data"}), 400
    if not cr.add_card(curr_user.id, data["card_number"]):
        return jsonify({"message": "Card was not created"}), 400
    return jsonify({"message": "Card added successfully"}), 200


@bp.route("/<string:card_number>/", methods=["GET"])
@token_required
def get_card(curr_user, card_number):
    # get card
    data = cr.get_card_with_balances(card_number)
    if not data or data == []:
        return jsonify({"message": "Card not found"}), 404
    return jsonify(data), 200


@bp.route("/<string:card_number>/deposit", methods=["POST"])
@token_required
def deposit(curr_user, card_number):
    # deposit money into account
    if not cr.card_belongs_to_user(card_number, curr_user.id):
        return jsonify({"message": "Card does not belong to user"}), 401
    data = request.get_json()
    if not data or not data["currency"] or not data["amount"]:
        return jsonify({"message": "Invalid data"}), 400
    if not cr.deposit(card_number, data["currency"], data["amount"]):
        return jsonify({"message": "Deposit failed"}), 400
    return jsonify({"message": "Account balance updated successfully"}), 200
