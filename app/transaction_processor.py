from os import environ as env
import atexit
from multiprocessing import Event, Process
import time
from app.extensions import socketio
from app.repos.transaction_repo import TransactionRepo as tr

# emit transactions periodically
def emit_transactions(app):
    with app.app_context():
        print("[Info] Emitting transactions...")
        transactions = tr.get_all_transactions()
        socketio.emit("transaction_processing", [x.to_json() for x in transactions])
        # socketio.emit("transaction_processing","test")
        print(f"[Info] Transactions emitted")


# Transaction processing
def process_transactions(exit_event):
    period = int(env["TRANSACTION_PERIOD"])
    try:
        while not exit_event.is_set():
            print("[Info] Processing transactions from the database...")
            tr.process_pending_transactions()
            time.sleep(period)
    except KeyboardInterrupt:
        pass  # Ignore the KeyboardInterrupt exception
    print("[Info] Transaction processing stopped")


# Create transaction process
def start_transaction_process():
    if not env.get("TRANSACTION_PROCESS_STARTED"):
        env["TRANSACTION_PROCESS_STARTED"] = "1"
        print("[Info] Custom process started")
        exit_event = Event()
        process = Process(
            target=process_transactions,
            args=(exit_event,),
        )
        process.start()
        # Register a function to be called at exit
        atexit.register(lambda: exit_event.set())

