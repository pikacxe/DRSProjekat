from datetime import datetime
from app.extensions import db


class Transaction(db.Model):
    __tablename__ = 'Transaction'
    id = db.Column(db.String, primary_key=True, name='ID')
    sender_id = db.Column(db.String, name='SenderID')
    sender_card_number = db.Column(db.String, name='SenderCardNumber')
    currency = db.Column(db.String, name='Currency')
    amount = db.Column(db.Float, name='Amount')
    recipient_card_number = db.Column(db.String, name='RecipientCardNumber')
    recipient_email = db.Column(db.String, name='RecipientEmail')
    recipient_first_name = db.Column(db.String, name='RecipientFName')
    recipient_last_name = db.Column(db.String, name='RecipientLName')
    state = db.Column(db.String, name='State')
    created = db.Column(db.DateTime, default=datetime.utcnow(), name='Created')
    completed = db.Column(db.DateTime, name='Completed')
    is_completed = db.Column(db.Boolean, name='isCompleted')

    # to json
    def to_json(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender_card_number': self.sender_card_number,
            'currency': self.currency,
            'amount': self.amount,
            'recipient_card_number': self.recipient_card_number,
            'recipient_email': self.recipient_email,
            'recipient_first_name': self.recipient_first_name,
            'recipient_last_name': self.recipient_last_name,
            'state': self.state,
            'created': self.created,
            'completed': self.completed,
            'is_completed': self.is_completed
        }
