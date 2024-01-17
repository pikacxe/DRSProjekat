import uuid
from app.extensions import db


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.String, primary_key=True, name="ID")
    first_name = db.Column(db.String, name="FirstName")
    last_name = db.Column(db.String, name="LastName")
    address = db.Column(db.String, name="Address")
    city = db.Column(db.String, name="City")
    country = db.Column(db.String, name="Country")
    phone_number = db.Column(db.String, name="PhoneNumber")
    email = db.Column(db.String, unique=True, nullable=False, name="Email")
    password = db.Column(db.String, name="Password")
    is_verified = db.Column(db.Boolean, default=False, name="isVerified")
    is_admin = db.Column(db.Boolean, default=False, name="isAdmin")

    # create user from json
    def __init__(self, json, id=None):
        if not User.verify_json(json):
            raise Exception("Invalid JSON")
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
            self.is_verified = False
            self.is_admin = False
        self.first_name = json["first_name"]
        self.last_name = json["last_name"]
        self.address = json["address"]
        self.city = json["city"]
        self.country = json["country"]
        self.phone_number = json["phone_number"]
        self.email = json["email"]
        self.password = json["password"]

    # verify json
    @staticmethod
    def verify_json(json):
        if (
            "first_name" not in json
            or "last_name" not in json
            or "address" not in json
            or "city" not in json
            or "country" not in json
            or "phone_number" not in json
            or "email" not in json
        ):
            # TODO add better validation
            return False
        return True

    # verify password
    @staticmethod
    def verify_password(password):
        # TODO add better validation
        return True

    # to json
    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "phone_number": self.phone_number,
            "email": self.email,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
        }
