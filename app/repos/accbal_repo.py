from app.models.account_balance import AccountBalance as ab
from app.extensions import db


class AccountBalanceRepo:
    def __init__(self):
        pass

    def get_all_by_card(self, card_number: str) -> list:
        data = ab.query.filter_by(card_number=card_number).all()
        return [x.to_json() for x in data]

    def get_by_card_and_currency(card_number: str, currency: str) -> ab | None:
        return ab.query.filter_by(card_number=card_number, currency=currency).first()

    def deposit_to_ballance(card_number: str, currency: str, amount: float) -> bool:
        if not card_number or not currency or not amount or amount <= 0:
            return False
        account_balance = ab.query.filter_by(
            card_number=card_number, currency=currency
        ).first()
        if not account_balance:
            # create one
            account_balance = ab(card_number=card_number, currency=currency)
        account_balance.balance += amount
        db.session.merge(account_balance)
        db.session.commit()
        return True
    
    def create_default(self, card_number: str) -> bool:
        if not card_number:
            return False
        acc_bal = ab(card_number=card_number, currency="RSD", balance=0)
        db.session.add(acc_bal)
        db.session.commit()
        return True
