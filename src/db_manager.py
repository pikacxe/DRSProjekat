import random
import traceback
import uuid
import psycopg2
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
def get_cards(user_id:int)->int:
    try:
        with connect() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM public."Card" WHERE "UserID"=%s', (user_id,))
            data = cur.fetchall()
            return data
    except Exception as e:
        if (env['ENV'] == 'DEV'):
            print(f"[ERROR - get-cards] {e}")
        else:
           print(f"[ERROR] Error while retreiving data from database!")
        return -1
    
# add new card
# /api/card/add
def add_card(user_id:int, currency:str = 'RSD', amount:float=0.0)->int:
    try:
        with connect() as conn:
            cur = conn.cursor()
            # generate unique card number
            card_number = generate_card_number()
            # generate new card
            cur.execute('INSERT INTO public."Card" ("CardNumber", "UserID") VALUES (%s, %s)', (card_number,user_id))
            # generate default account balance with RSD currency and 0 balance
            cur.execute('INSERT INTO public."Account" ("CardNumber", "Currency", "Balance") VALUES (%s, %s, %lf)', (card_number, currency, amount))
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
