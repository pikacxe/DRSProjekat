from app.extensions import db


class Card(db.Model):
    __tablename__ = 'Card'
    card_number = db.Column(db.String, primary_key=True, name='CardNumber')
    user_id = db.Column(db.String, db.ForeignKey('User.ID'), nullable=False, name='UserID')
    user = db.relationship('User', backref=db.backref('cards', lazy=True))

    # to json
    def to_json(self):
        return {
            'card_number': self.card_number,
            'user_id': self.user_id
        }
