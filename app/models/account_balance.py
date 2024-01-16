from app.extensions import db


class AccountBalance(db.Model):
    __tablename__ = "AccountBalance"
    card_number = db.Column(db.String, primary_key=True, name="CardNumber")
    currency = db.Column(db.String,default='RSD', primary_key=True, name="Currency")
    balance = db.Column(db.Float,default=0, name="Balance")
    # to json
    def __init__(self, card_number, currency) -> None:
        super().__init__()
        self.card_number = card_number
        self.currency = currency
        self.balance = 0

    def to_json(self):
        return {
            "card_number": self.card_number,
            "currency": self.currency,
            "balance": self.balance,
        }
