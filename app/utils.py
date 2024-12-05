from datetime import datetime, timedelta
from sqlmodel import select
from passlib.hash import bcrypt
import jwt
import re

from app.config import Config
from app.models import AccessToken, RefreshToken


def generate_password_hash(password: str) -> str:
    password_hashed = bcrypt.hash(password)
    return password_hashed

def verify_password(password: str, password_hashed: str) -> str:
    return bcrypt.verify(password, password_hashed)

def generate_access_token(user_id, session):
    expiration = datetime.now() + timedelta(hours=Config.ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        'sub': str(user_id),
        'exp': expiration
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    new_token = AccessToken(token=token, token_type=Config.TOKEN_TYPE, expire_at=expiration, user_id=user_id)
    session.add(new_token)
    session.commit()
    session.refresh(new_token)
    return token

def generate_refresh_token(user_id, access_token, session):
    expiration = datetime.now() + timedelta(hours=Config.REFRESH_TOKEN_EXPIRE_HOURS)
    payload = {
        'sub': str(user_id),
        'exp': expiration
    }
    token = session.exec(select(AccessToken).where(AccessToken.token==access_token)).first()
    if token:
        refresh_token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
        new_token = RefreshToken(token=refresh_token, token_type=Config.TOKEN_TYPE, expire_at=expiration, user_id=user_id, access_token_id=token.id)
        session.add(new_token)
        session.commit()
        session.refresh(new_token)
        return refresh_token
    return

def decode_token(token):
    return jwt.decode(token, Config.SECRET_KEY, algorithms=Config.ALGORITHM)

def validation_email(email):
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if valid:
        return True
    return
