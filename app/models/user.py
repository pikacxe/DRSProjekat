from app.extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    address = StringField('Address')
    city = StringField('City')
    country = StringField('Country')
    phone_number = StringField('Phone Number')
    email = StringField('Email', validators=[DataRequired()])


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

    # create user form UserForm and id
    def __init__(self, form, id=None):
        if id:
            self.id = id
        self.first_name = form.first_name.data
        self.last_name = form.last_name.data
        self.address = form.address.data
        self.city = form.city.data
        self.country = form.country.data
        self.phone_number = form.phone_number.data
        self.email = form.email.data
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
