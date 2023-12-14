from app.extensions import db


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.String, primary_key=True, name='ID')
    first_name = db.Column(db.String, name='FirstName')
    last_name = db.Column(db.String, name='LastName')
    address = db.Column(db.String, name='Address')
    city = db.Column(db.String, name='City')
    country = db.Column(db.String, name='Country')
    phone_number = db.Column(db.String, name='PhoneNumber')
    email = db.Column(db.String, unique=True, nullable=False, name='Email')
    password = db.Column(db.String, name='Password')
    is_verified = db.Column(db.Boolean, default=False, name='isVerified')
    is_admin = db.Column(db.Boolean, default=False, name='isAdmin')

    # to json
    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'phone_number': self.phone_number,
            'email': self.email,
            'is_verified': self.is_verified,
            'is_admin': self.is_admin
        }
