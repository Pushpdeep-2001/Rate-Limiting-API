import jwt
from datetime import datetime, timedelta
import os
from python_dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_EXPIRY_HOURS = int(os.getenv('JWT_EXPIRY_HOURS'))


def generate_jwt(user_id):
    expiry = datetime.now() + timedelta(hours=JWT_EXPIRY_HOURS)
    payload = {
        'user_id': user_id,
        'exp': expiry
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"error": "Token missing"}), 401

        data = decode_jwt(token)
        if not data:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(data["user_id"], *args, **kwargs)
    return decorated       