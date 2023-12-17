from app.models.user import User
from flask import request, jsonify
from functools import wraps
import jwt
from os import environ as env


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.authorization:
            return jsonify({"message": "Please login!"}), 401
        token = request.authorization.token
        # token is missing
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            # Decoding the payload to fetch the stored details
            key = env["JWT_SECRET_KEY"]
            data = jwt.decode(token, key, algorithms=["HS256"])
            current_user_id = data.get("id")

            # Fetch the user from your database using the user_id
            # Replace 'User' and 'query' with your actual User model and query method
            current_user = User.query.filter_by(id=current_user_id).first()

            if not current_user:
                raise Exception("User not found")

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"message": f"Token is invalid: {str(e)}"}), 401
        except Exception as e:
            return jsonify({"message": f"Error decoding token: {str(e)}"}), 401

        return f(current_user, *args, **kwargs)

    return decorated



