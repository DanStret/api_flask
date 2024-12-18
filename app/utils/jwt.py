import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"

def generate_token(data, exp_minutes=60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=exp_minutes)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
