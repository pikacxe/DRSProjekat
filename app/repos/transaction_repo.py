from app.models.transaction import Transaction
from app.extensions import db
from app.repos.accbal_repo import AccountBalanceRepo as abr
from app.repos.card_repo import CardRepo as cr
from app.repos.user_repo import UserRepo as ur


class TransactionRepo:
    def __init__(self):
        pass

    def get_all_transactions() -> list:
        return Transaction.query.all()

    def add_transaction(json: str, user_id: str) -> bool:
        if not user_id or not Transaction.verify_json(json):
            return False
        t = Transaction(json, user_id)
        # check if card belong to user
        if not cr.card_belongs_to_user(t.sender_card_number, user_id):
            return False
        # check if recipient card belongs to recipient user
        recipient_id = ur.get_id_by_email(t.recipient_email)
        if not cr.card_belongs_to_user(t.recipient_card_number, recipient_id):
            return False
        # check if account balance with currency exists
        account_balance = abr.get_by_card_and_currency(
            t.recipient_card_number, t.currency
        )
        if not account_balance:
            return False
        db.session.add(t)
        db.session.commit()
        return True
