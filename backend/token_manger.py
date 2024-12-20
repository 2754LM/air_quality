from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status

SECRET_KEY = "b8c5f4a2e1e0e2e4a4c6c8f4a2e1e0e4a4c6c8f4a2e1e0e4a4c6c8f4a2e1e0e4"
ALGORITHM = "HS256"

def create_access_token(data: dict, timeout: int = 0):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=timeout)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as e:
        return None

if __name__ == '__main__':
    token = create_access_token({"username": "admin", "password" : "admin"})
    print(decode_jwt(token))