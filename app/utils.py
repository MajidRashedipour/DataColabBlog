from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
import re

from app.database import SessionDep
from app.config import settings
from app.models.users import Token


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def generate_password_hash(password: str):
    password_hashed = pwd_context.hash(password)
    return password_hashed

def verify_password(password: str, password_hashed: str):
    return pwd_context.verify(password, password_hashed)

def generate_token(user_id, session: SessionDep, is_refresh: bool = False):
    expire_time = settings.REFRESH_TOKEN_EXPIRE_HOURS if is_refresh else settings.ACCESS_TOKEN_EXPIRE_HOURS
    expiration = datetime.now() + timedelta(hours=expire_time)
    payload = {
        'sub': str(user_id),
        'exp': expiration
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    new_token = Token(token=token, token_type=settings.TOKEN_TYPE, expire_at=expiration, user_id=user_id, is_refresh=is_refresh)
    session.add(new_token)
    session.commit()
    session.refresh(new_token)
    return token

def decode_token(token):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except InvalidTokenError:
        return

def validation_email(email):
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if valid:
        return True
    return
