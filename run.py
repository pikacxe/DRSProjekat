from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app
from os import environ as env
from app.transaction_processor import start_transaction_process, emit_transactions


if __name__ == "__main__":
    # Configure app
    port = int(env.get("FLASK_RUN_PORT", 5000))
    host = env.get("FLASK_RUN_HOST", "localhost")
    app_env = env.get("FLASK_ENV", "development")
    debug = app_env == "development"
    t_period = int(env.get("TRANSACTION_PERIOD", 10))

    scheduler = BackgroundScheduler()
    try:
        # Create app
        app, socketio = create_app(config="config.Config")

        # Start transaction processing
        with app.app_context():
            start_transaction_process()

        # Start emitting transactions to socket
        scheduler.add_job(emit_transactions, "interval", seconds=t_period, args=[app])
        scheduler.start()

        # Run app
        socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)
    except Exception as e:
        if debug:
            print(e)
        else:
            print("Error while starting the app")
