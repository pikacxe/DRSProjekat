from app.models.transaction import Transaction
from app.extensions import db
from app.repos.accbal_repo import AccountBalanceRepo as abr
from app.repos.card_repo import CardRepo as cr
from app.repos.user_repo import UserRepo as ur
from datetime import datetime
from app.services.mail_service import MailService


class TransactionRepo:
    def __init__(self):
        pass

    def get_all_transactions() -> list:
        return Transaction.query.all()
    
    def process_pending_transactions():
        pending = Transaction.query.filter_by(state="Pending").all()
        for t in pending:
            t.state = "Processing"
            db.session.merge(t)
            db.session.commit()
            # check if the sender has enough money
            account_balance = abr.get_by_card_and_currency(
                t.sender_card_number, t.currency
            )
            if not account_balance or account_balance.balance < t.amount:
                t.state = "Failed"
                db.session.commit()
                print(f"[Info] Transaction {t.id} failed")
                continue
            # check if the receiver account balance with transaction currency exists
            receiver_account_balance = abr.get_by_card_and_currency(t.recipient_card_number,t.currency)
            if not receiver_account_balance:
                abr.add_account_balance(t.recipient_card_number, t.currency)
            # update sender account balance
            abr.update_account_balance(t.sender_card_number, t.currency, -t.amount)
            # update receiver account balance
            abr.update_account_balance(t.recipient_card_number, t.currency, t.amount)
            t.state = "Completed"
            t.completed = datetime.utcnow()
            t.is_completed = True
            db.session.merge(t)
            db.session.commit()
            # send info mail to recepient and sender
            MailService.send_mail_transaction(t)
                

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
        # check if sender and recipient are different
        if t.sender_id == t.recipient_id:
            return False
        # check if recipient name matches recipient email
        if not ur.check_name_and_email(t.recipient_first_name,t.recipient_last_name, t.recipient_email):
            return False
        # check if account balance with currency exists
        account_balance = abr.get_by_card_and_currency(
            t.sender_card_number, t.currency
        )
        if not account_balance:
            return False
        db.session.add(t)
        db.session.commit()
        return True
