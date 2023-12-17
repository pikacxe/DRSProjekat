from os import environ as env
import atexit
from multiprocessing import Event, Process
import time
from app.models.transaction import Transaction
from app.models.account_balance import AccountBalance
from app.extensions import db, mail, socketio
from datetime import datetime
from app.models.user import User

# emit transactions periodically
def emit_transactions(app):
    with app.app_context():
        print("Emitting transactions...")
        transactions = Transaction.query.all()
        socketio.emit("transaction_processing", [x.to_json() for x in transactions])
        # socketio.emit("transaction_processing","test")
        print("Transactions emitted")


# Transaction processing
def process_transactions(exit_event):
    period = int(env["TRANSACTION_PERIOD"])
    try:
        while not exit_event.is_set():
            print("Processing transactions from the database...")
            process_pending_transactions()
            time.sleep(period)
    except KeyboardInterrupt:
        pass  # Ignore the KeyboardInterrupt exception
    print("Transaction processing stopped")


# Create transaction process
def start_transaction_process():
    if not env.get("TRANSACTION_PROCESS_STARTED"):
        env["TRANSACTION_PROCESS_STARTED"] = "1"
        print("Custom process started")
        exit_event = Event()
        process = Process(
            target=process_transactions,
            args=(exit_event,),
        )
        process.start()
        # Register a function to be called at exit
        atexit.register(lambda: exit_event.set())


# process pending transactions from the database
def process_pending_transactions():
    pending_transactions = Transaction.query.filter_by(state="Pending").all()
    for transaction in pending_transactions:
        transaction.state = "Processing"
        db.session.commit()
        # check if the sender has enough money
        account_balance = AccountBalance.query.filter_by(
            card_number=transaction.sender_card_number, currency=transaction.currency
        ).first()
        if not account_balance or account_balance.balance < transaction.amount:
            transaction.state = "Failed"
            db.session.commit()
            print(f"Transaction {transaction.id} failed")
            continue
        # check if the receiver account balance with transaction currency exists
        receiver_account_balance = AccountBalance.query.filter_by(
            card_number=transaction.recipient_card_number, currency=transaction.currency
        ).first()
        if not receiver_account_balance:
            receiver_account_balance = AccountBalance(
                card_number=transaction.recipient_card_number,
                currency=transaction.currency,
                balance=0,
            )
            db.session.add(receiver_account_balance)
            db.session.commit()
        # update sender account balance
        account_balance.balance -= transaction.amount
        db.session.merge(account_balance)
        # update receiver account balance
        receiver_account_balance.balance += transaction.amount
        db.session.merge(receiver_account_balance)
        transaction.state = "Completed"
        transaction.completed = datetime.utcnow()
        transaction.is_completed = True
        db.session.commit()
        # send email to both sender and receiver
        try:
            # send email to sender
            sender = User.query.filter_by(id=transaction.sender_id).first()
            mail.send_message(
                subject="Transaction completed",
                recipients=[sender.email],
                body=f"Your transaction with id {transaction.id} has been completed successfully",
            )
            # send email to receiver
            mail.send_message(
                subject="Transaction completed",
                recipients=[transaction.recipient_email],
                body=f"You have received {transaction.amount} {transaction.currency} from {sender.first_name} {sender.last_name}",
            )
        except Exception as e:
            print(e)
    return pending_transactions
