
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
@token_required
def get_transactions(user_id):
    if not db_manager.is_admin(user_id):
        return { "message": "Unauthorized" }, 401
    # TODO add transactions with socketio
    return { "message": "Not implemented" }, 500

@app.route("/api/admin/users", methods=['GET'])
@token_required
def get_users(user_id):
    if not db_manager.is_admin(user_id):
        return { "message": "Unauthorized" }, 401
    users = db_manager.get_unverified_users()
    if not users:
        return { "message": "No users found" }, 404
    return jsonify(users), 200

@app.route("/api/admin/verify", methods=['POST'])
@token_required
def verify(user_id):
    if not db_manager.is_admin(user_id):
        return { "message": "Unauthorized" }, 401
    data = request.get_json()
    print(data)
    if not data:
        return { "message": "User not found" }, 404
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
        return { "message": "User not found" }, 404
    # generate token
    payload ={
        'id': user_id,
        'isAdmin': db_manager.is_admin(user_id),
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
        return { "message": "User not found" }, 404
    return jsonify(user), 200


@app.route("/api/profile/update", methods=['POST'])
@token_required
def update_profile(user_id):
    data = request.form
    if not data:
        return { "message": "User not found!" }, 404
    result = db_manager.update_user(user_id, data['fname'], data['lname'], data['address'], data['city'], data['country'], data['phone'], data['email'])
    if not result:
        return { "message": "Error while updating user" }, 500
    return { "message": "User successfully updated" }, 200


@app.route("/api/card/add", methods=['POST'])
@token_required
def add_card(user_id):
    data = request.form
    if not data:
        return { "message": "Invalid form data" }, 400
    result = db_manager.add_card(user_id)
    if not result:
        return { "message": "Error while adding card" }, 500
    return { "message": "Card successfully added" }, 200


@app.route("/api/card", methods=['GET'])
@token_required
def get_cards(user_id):
    cards = db_manager.get_cards(user_id)
    if not cards:
        return { "message": "No card found!" }, 404
    return jsonify(cards), 200
    


@app.route("/api/card/<uuid:card_id>",methods=['GET'])
@token_required
def get_card(user_id, card_id):
    card = db_manager.get_card_by_id(user_id, card_id)
    if not card:
        return { "message": "Card not found" }, 404
    return jsonify(card), 200


@app.route("/api/card/<uuid:card_id>/deposit", methods=['POST'])
@token_required
def deposit(user_id, card_id):
    data = request.form
    if not data:
        return { "message": "Invalid form data" }, 400
    result = db_manager.deposit_balance(user_id, card_id, data['amount'])
    if not result:
        return { "message": "Error while depositing" }, 500
    return { "message": "Deposit successful" }, 200


@app.route("/api/transaction/create", methods=['POST'])
@token_required
def create_transaction(user_id):
    data = request.form
    if not data:
        return { "message": "Invalid form data" }, 400
    result = db_manager.create_transaction(user_id,data['sender_card_number'], data['currency'],
                                           data['amount'], data['recipient_card_number'], data['recipient_email'],
                                           data['recipient_fname'], data['recipient_lname'])
    if not result:
        return { "message": "Error while creating transaction" }, 500
    return { "message": "Transaction successful" }, 200


def decode_url_parameters(raw_data):
    # Decode the raw data to a string
    decoded_data = raw_data.decode('utf-8')

    # Parse the URL parameters
    url_parameters = {}
    for param in decoded_data.split('&'):
        key, value = param.split('=')
        url_parameters[key] = unquote_plus(value)
    return url_parameters


#### db_manager #####
import random
import uuid
from os import environ as env
from dotenv import load_dotenv

# load env variables
load_dotenv()


# connect to database
def connect():
    try:
        return psycopg2.connect(database=env['DB_NAME'],
                                user=env['DB_USER'],
                                password=env['DB_PASS'],
                                host=env['DB_HOST'],
                                port=env['DB_PORT'])
    except Exception as e:
        print(f"[ERROR] Cannot connect to database!")
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - connect] {e}")

# check if user exists
# /api/login
def user_exists(email:str, password:str)->str:
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT "ID" FROM public."User" WHERE "Email"=%s AND "Password"=%s', (email, password))
            data = cur.fetchone()
            return data[0]
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - user-exists] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1
# check if user exists by id
# jwt auth
def user_exists_by_id(user_id:str)->str:
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT "ID" FROM public."User" WHERE "ID"=%s', (user_id,))
            data = cur.fetchone()
            return data[0]
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - exists-by-id] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1

# check if user is admin
# auth
def is_admin(user_id:str)->str:
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT "isAdmin" FROM public."User" WHERE "ID"=%s', (user_id,))
            data = cur.fetchone()
            if not data or not data[0]:
                return None
            return data[0]
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - is-admin] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1


# get user by id
# /api/profile
def get_user_by_id(user_id:str):
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM public."User" WHERE "ID"=%s', (user_id,))
            data = cur.fetchone()
            if not data:
                return -1
            # append column names from cur.description to data
            # so we can return json object
            data = dict(zip([col[0] for col in cur.description], data))
            return data
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - get-uset-by-id] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1

# verify user
# /api/admin/verify
def verify_user(user_id:str)->int:
    try:
        with connect() as conn:
            cur = conn.cursor()
            # check if user exists
            cur.execute('SELECT "ID" FROM public."User" WHERE "ID"=%s', (user_id,))
            data = cur.fetchone()
            if not data:
                return -1
            cur.execute('UPDATE public."User" SET "isVerified" = TRUE WHERE "ID"=%s', (user_id,))
            conn.commit()
            return 1
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - veriy-user] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1

# add new user
# /api/admin/register
def add_user(first_name:str, last_name:str, address:str, city:str, country:str, phone:str, email:str, password:str )->int:
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO public."User" ("ID", "FirstName", "LastName", "Address", "City", "Country", "PhoneNumber", "Email", "Password") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(uuid.uuid4()), first_name, last_name, address, city, country, phone, email, password))
            conn.commit()
            return 1
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - add-user] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1

# get all unverified users
# /api/admin/users
def get_unverified_users():
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM public."User" WHERE "isVerified"=FALSE')
            data = cur.fetchall()
            if not data or len(data) == 0:
                return -1
            # append column names from cur.description to data
            # so we can return json object
            data = [dict(zip([col[0] for col in cur.description], row)) for row in data]
            return data
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - get-unverified-users] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1

# update user
# /api/profile/update
def update_user(user_id:int, first_name:str, last_name:str, address:str, city:str, country:str, phone:str, email:str )->int:
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('UPDATE public."User" SET "FirstName"=%s, "LastName"=%s, "Address"=%s, "City"=%s, "Country"=%s, "PhoneNumber"=%s, "Email"=%s WHERE "ID"=%s', (first_name, last_name, address, city, country, phone, email, user_id))
            conn.commit()
            return 1
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - update-user] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1
    
# get all cards with respective account balances
# /api/card/
def get_cards(user_id:int):
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM public."Card" WHERE "UserID"=%s', (user_id,))
            data = cur.fetchall()
            if not data or len(data) == 0:
                return -1
            # append column names from cur.description to data
            # so we can return json object
            data = [dict(zip([col[0] for col in cur.description], row)) for row in data]
            return data
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - get-cards] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1

# get user card by id
# /api/card/<str:card_id>
def get_card_by_id(user_id:str, card_number:str):
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM public."Card" WHERE "UserID"=%s AND "CardNumber"=%s', (user_id, card_number))
            data = cur.fetchone()
            if not data:
                return -1
            # append column names from cur.description to data
            # so we can return json object
            data = dict(zip([col[0] for col in cur.description], data))
            return data
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - get-card-by-id] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1

# add new card
# /api/card/add
def add_card(user_id:int, card_number:str, currency:str = 'RSD', amount:float=0.0)->int:
    try:
        with connect() as conn:
            cur = conn.cursor()
            # generate unique card number if none provided
            if not card_number:
                card_number = generate_card_number()
            # generate new card
            cur.execute('INSERT INTO public."Card" ("CardNumber", "UserID") VALUES (%s, %s)', (card_number,user_id))
            # generate default account balance with RSD currency and 0 balance
            cur.execute('INSERT INTO public."AccountBalance" ("CardNumber", "Currency", "Balance") VALUES (%s, %s, %lf)', (card_number, currency, amount))
            conn.commit()
            return 1
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - add-card] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1

# generate unique string of 16 digits witf format XXXX-XXXX-XXXX-XXXX
def generate_card_number()->str:
    raw_num = str(random.randint(10**15, 10**16-1))
    return '-'.join(raw_num[i:i+4] for i in range(0, len(raw_num), 4))

# deposit money to account balance
# /api/card/<uuid:card_id>/deposit
def deposit_balance(user_id:str, card_number:str,currency:str, amount:float)->int:
    if amount <= 0:
        return -1
    try:
        with connect() as conn:
            cur = conn.cursor()
            # check if card belongs to user
            cur.execute('SELECT "UserID" FROM public."Card" WHERE "CardNumber"=%s', (card_number,))
            data = cur.fetchone()
            if not data or data[0] != user_id:
                return -1
            # check if card has account balance in given currency
            cur.execute('SELECT * FROM public."AccountBalance" WHERE "CardNumber"=%s AND "Currency"=%s', (card_number, currency))
            data = cur.fetchone()
            if not data:
                # create new account balance for given currency
                cur.execute('INSERT INTO public."AccountBalance" ("CardNumber", "Currency", "Balance") VALUES (%s, %s, %lf)', (card_number, currency, amount))
            # update account balance
            cur.execute('UPDATE public."AccountBalance" SET "Balance"=%lf WHERE "CardNumber"=%s AND "Currency"=%s', (amount, card_number, currency))
            conn.commit()
            return 1
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - deposit-balance] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1

# create new transaction
# /api/transaction/create
def create_transaction(sender_id:str, sender_card_number:str, currency:str, amount:float,
                       recipient_card_number:str, recipient_email:str,
                       recipient_fname:str, recipient_lname:str)->int:
    try:
        with connect() as conn:
            cur = conn.cursor()
            # check if provided card is owned by sender user
            cur.execute('SELECT "UserID" FROM public."Card" WHERE "CardNumber"=%s', (sender_card_number,))
            data = cur.fetchone()
            if not data:
                return -1
            # check if user has account balance with provided currency on card
            cur.execute('SELECT "Balance" FROM public."AccountBalance" WHERE "CardNumber"=%s AND "Currency"=%s', (sender_card_number, currency))
            balance = cur.fetchone()[0]
            if (balance < amount):
                return -1
            # check if recipient exists
            cur.execute('SELECT "ID" FROM public."User" WHERE "Email"=%s', (recipient_email,))
            recipient_id = cur.fetchone()[0]
            if not recipient_id:
                return -1
            # create new transaction
            cur.execute('INSERT INTO public."Transaction" ("ID", "SenderID", "SenderCardNumber", "Currency", "Amount", "RecipientCardNumber", "RecipientEmail", "RecipientFName", "RecipientLName") VALUES (%s, %s, %s, %s, %lf, %s, %s, %s, %s)',
                         (str(uuid.uuid4()), sender_id, sender_card_number, currency, amount, recipient_card_number, recipient_email, recipient_fname, recipient_lname))
            cur.commit()
            return 1
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - create-transaction] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1