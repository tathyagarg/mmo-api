from datetime import datetime, timedelta

import jwt
import bcrypt
 
def verify_password(plain: str, hashed: str):
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(data: dict, expires: timedelta, secret: str, algorithm: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, secret, algorithm=algorithm)

