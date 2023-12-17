from datetime import datetime
import uuid
from app.extensions import db



class Transaction(db.Model):
    __tablename__ = 'Transaction'
    id = db.Column(db.String, primary_key=True, name='ID')
    sender_id = db.Column(db.String, name='SenderID')
    sender_card_number = db.Column(db.String, name='SenderCardNumber')
    currency = db.Column(db.String, name='Currency')
    amount = db.Column(db.Float, name='Amount')
    recipient_card_number = db.Column(db.String, name='RecipientCardNumber')
    recipient_email = db.Column(db.String, name='RecipientEmail', unique=True)
    recipient_first_name = db.Column(db.String, name='RecipientFName')
    recipient_last_name = db.Column(db.String, name='RecipientLName')
    state = db.Column(db.String, name='State', default='Pending')
    created = db.Column(db.DateTime, default=datetime.utcnow(), name='Created')
    completed = db.Column(db.DateTime, name='Completed')
    is_completed = db.Column(db.Boolean, name='isCompleted')

    # create transaction from json
    def __init__(self, json, sender_id):
        if not Transaction.verify_json(json):
            raise Exception('Invalid JSON')
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.sender_card_number = json['sender_card_number']
        self.currency = json['currency']
        self.amount = json['amount']
        self.recipient_card_number = json['recipient_card_number']
        self.recipient_email = json['recipient_email']
        self.recipient_first_name = json['recipient_first_name']
        self.recipient_last_name = json['recipient_last_name']
        self.state = 'Pending'
        self.is_completed = False

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
            'created': self.created.strftime('%Y-%m-%d %H:%M:%S'),
            'completed': self.completed.strftime('%Y-%m-%d %H:%M:%S') if self.completed else None,
            'is_completed': self.is_completed
        }
    # verify json
    @staticmethod
    def verify_json(json):
        if (
            'sender_card_number' not in json
            or 'currency' not in json
            or 'amount' not in json
            or 'recipient_card_number' not in json
            or 'recipient_email' not in json
            or 'recipient_first_name' not in json
            or 'recipient_last_name' not in json
        ):
            return False
        return True