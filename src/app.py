from urllib.parse import unquote_plus
from flask import Flask, request, jsonify
from flask_cors import CORS
import db_manager
import jwt
import datetime
from os import environ as env
from functools import wraps
from dotenv import load_dotenv


# load env variables
load_dotenv()

# define Flask app
app =  Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.authorization.token
        # token is missing
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            key = env['JWT_SECRET_KEY']
            data = jwt.decode(token, key, algorithms=["HS256"])
            current_user = db_manager.user_exists_by_id(data['id'])
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

@app.route("/api/admin/register", methods=['POST'])
@token_required
def register(user_id):
    if not db_manager.is_admin(user_id):
        return { "message": "Unauthorized" }, 401
    data = request.form
    result = db_manager.add_user(data['fname'], data['lname'], data['address'], data['city'], data['country'], data['phone'], data['email'], data['password'])
    if not result:
        return { "message": "Error while creating user" }, 500
    return { "message": "User successfully added" }, 200


@app.route("/api/admin/transactions", methods=['GET'])
def get_transactions():
    return { "message": "Welcome to test page" }


@app.route("/api/admin/verify", methods=['POST'])
@token_required
def verify(user_id):
    if not db_manager.is_admin(user_id):
        return { "message": "Unauthorized" }, 401
    data = request.get_json()
    print(data)
    if not data:
        return { "message": "Error" }, 404
    result = db_manager.verify_user(data['user_id'])
    if not result:
        return { "message": "Error while verifying user" }, 500
    return { "message": "User successfully verified" }, 200


@app.route("/api/login", methods=['POST'])
def login():
    url_parameters = decode_url_parameters(request.get_data())
    # get user_id 
    user_id = db_manager.user_exists(url_parameters['email'], url_parameters['password'])
    if(user_id == -1):
        return { "message": "Error" }, 404
    # generate token
    payload ={
        'id': user_id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    key = env['JWT_SECRET_KEY']
    token = jwt.encode(payload, key, algorithm = 'HS256')
    
    return jsonify({'access_token' : token})
    


@app.route("/api/profile", methods=['GET'])
@token_required
def profile(user_id:str):
    user= db_manager.get_user_by_id(user_id)
    if not user:
        return { "message": "Error" }, 404
    return jsonify(user), 200


@app.route("/api/profile/update", methods=['POST'])
def update_profile():
    return { "message": "Welcome to test page" }


@app.route("/api/card/add", methods=['POST'])
def add_card():
    return { "message": "Welcome to test page" }


@app.route("/api/card", methods=['GET'])
def get_cards():
    return { "message": "Welcome to test page" }


@app.route("/api/card/<uuid:card_id>",methods=['GET'])
def get_card(card_id):
    return { "message": "Welcome to test page" }


@app.route("/api/card/<uuid:card_id>/deposit", methods=['POST'])
def deposit(card_id):
    return { "message": "Welcome to test page" }


@app.route("/api/transaction/create", methods=['POST'])
def create_transaction():
    return { "message": "Welcome to test page" }


def decode_url_parameters(raw_data):
    # Decode the raw data to a string
    decoded_data = raw_data.decode('utf-8')

    # Parse the URL parameters
    url_parameters = {}
    for param in decoded_data.split('&'):
        key, value = param.split('=')
        url_parameters[key] = unquote_plus(value)
    return url_parameters

# Start Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env['APP_PORT'] or 8080, debug=env['ENV'] == 'DEV')