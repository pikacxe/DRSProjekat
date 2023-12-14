from flask import jsonify
from app.models.transaction import Transaction
from app.transactions import bp
from app.helpers import token_required

@bp.route('/', methods=['GET'])
#@token_required
def get_all_transactions():
    data = Transaction.query.all()
    return jsonify([x.to_json() for x in data]), 200