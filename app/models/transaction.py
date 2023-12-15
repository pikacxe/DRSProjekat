from datetime import datetime
import uuid
from app.extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email

class TransactionForm(FlaskForm):
    sender_card_number = StringField('Sender Card Number', validators=[DataRequired()])
    currency = StringField('Currency', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    recipient_card_number = StringField('Recipient Card Number', validators=[DataRequired()])
    recipient_email = StringField('Recipient Email', validators=[DataRequired(), Email()])
    recipient_first_name = StringField('Recipient First Name', validators=[DataRequired()])
    recipient_last_name = StringField('Recipient Last Name', validators=[DataRequired()])

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

    # create transaction form TransactionForm
    def __init__(self, form, sender_id):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.sender_card_number = form.sender_card_number.data
        self.currency = form.currency.data
        self.amount = form.amount.data
        self.recipient_card_number = form.recipient_card_number.data
        self.recipient_email = form.recipient_email.data
        self.recipient_first_name = form.recipient_first_name.data
        self.recipient_last_name = form.recipient_last_name.data
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
            'created': self.created,
            'completed': self.completed,
            'is_completed': self.is_completed
        }
