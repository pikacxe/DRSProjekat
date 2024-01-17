from app.models.user import User
from app.repos.card_repo import CardRepo as cr
from app.extensions import db


class UserRepo:
    def __init__(self):
        pass

    def get_all_users() -> list:
        data = User.query.all()
        return [x.to_json() for x in data]

    def get_id_by_email(email: str) -> str:
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        return user.id

    def get_all_unverified_users() -> list:
        unvf_users = User.query.filter_by(is_verified=False).all()
        data = []
        # get cards for each user
        for u in unvf_users:
            cards = cr.get_card_numbers_for_user(u.id)
            data.append({"user": u.to_json(), "cards": cards})
        return data

    def add_user(json: str) -> User|None:
        if not User.verify_json(json):
            return None
        user = User(json)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_id(id: str) -> User | None:
        return User.query.filter_by(id=id).first()

    def get_user_by_logon(email: str, password: str) -> User | None:
        return User.query.filter_by(email=email, password=password).first()

    def verify_user(id: str) -> bool:
        user = User.query.filter_by(id=id).first()
        if not user:
            return False
        user.is_verified = True
        db.session.merge(user)
        db.session.commit()
        return True

    def change_password(id: str, old_password: str, new_password: str) -> bool:
        user = User.query.filter_by(id=id).first()
        if (
            not user
            or user.password != old_password
            or not User.verify_password(new_password)
        ):
            return False
        user.password = new_password
        db.session.merge(user)
        db.session.commit()
        return True

    def update_user(id: str, json: str) -> bool:
        user = User.query.filter_by(id=id).first()
        if not user or not User.verify_json(json):
            return False
        user.first_name = json["first_name"]
        user.last_name = json["last_name"]
        user.address = json["address"]
        user.city = json["city"]
        user.country = json["country"]
        user.phone_number = json["phone_number"]
        user.email = json["email"]
        db.session.merge(user)
        db.session.commit()
        return True
