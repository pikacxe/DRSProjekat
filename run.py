from app import create_app


if __name__ == "__main__":
    app, socketio = create_app(config="config.Config")
    socketio.run(app, debug=True)