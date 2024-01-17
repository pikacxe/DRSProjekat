from app.models.card import Card
from app.repos.accbal_repo import AccountBalanceRepo as abr
from app.extensions import db


class CardRepo:
    def __init__(self):
        pass

    def get_all_cards() -> list:
        data = Card.query.all()
        return [x.to_json() for x in data]

    def get_card(card_number: str):
        return Card.query.filter_by(card_number=card_number).first()

    def get_card_with_balances(card_number: str) -> list:
        card = Card.query.filter_by(card_number=card_number).first()
        if not card:
            return None
        account_balances = abr.get_all_by_card(card_number)
        return {
            "card": card.to_json(),
            "account_balances": account_balances,
        }

    def get_all_cards_for_user(user_id: str) -> list:
        cards = Card.query.filter_by(user_id=user_id).all()
        data = []
        for c in cards:
            # get account balances for each card
            account_balances = abr.get_all_by_card(c.card_number)
            # create a dictionary for each card and its account balances
            el = {
                "card": c.card_number,
                "account_balances": account_balances,
            }
            data.append(el)

        return data

    def get_card_numbers_for_user(user_id: str) -> list:
        cards = Card.query.filter_by(user_id=user_id).all()
        return [x.card_number for x in cards]

    def card_belongs_to_user(card_number: str, user_id: str) -> bool:
        card = Card.query.filter_by(card_number=card_number, user_id=user_id).first()
        if not card:
            return False
        return True

    def add_card(user_id: str, card_number: str) -> bool:
        if not user_id or not card_number:
            return False
        card = Card(card_number=card_number, user_id=user_id)
        # create default account balance for card
        db.session.add(card)
        db.session.commit()
        abr.add_account_balance(card_number)
        return True

    def deposit(card_number: str, currency: str, amount: float) -> bool:
        card = Card.query.filter_by(card_number=card_number).first()
        if not card or not amount:
            return False
        return abr.deposit_to_ballance(card_number, currency, amount)
