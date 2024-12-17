from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from app.database import SessionDep
from app.models.users import User, Token
from app.schemas.users import UserRegisterSchema, UserLoginSchema
from app.utils import generate_password_hash, verify_password, validation_email, generate_token, decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter()

def get_user(user_id, session: SessionDep):
    user = session.get(User, user_id)
    if user:
        return user
    return

def verify_token(jwt_token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    token = session.exec(select(Token).where(Token.token==jwt_token)).first()
    if token and token.expire_at >= datetime.now() and not token.is_revoke:
        return token.token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

def get_current_user(jwt_token: Annotated[str, Depends(verify_token)], session: SessionDep):
    payload = decode_token(token=jwt_token)
    if payload:
        user_id = payload.get('sub')
        user = get_user(user_id, session)
        if user:
            return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')


@router.post("/register/", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserRegisterSchema, session: SessionDep):
    user_email = user_data.email
    user = session.exec(select(User).where(User.email==user_email)).first()
    if user and user.email == user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Email already exist')
    if not validation_email(user_email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Email')
    user_password = user_data.password
    user_confirm_password = user_data.confirm_password
    if user_password == user_confirm_password:
        new_user = User(email=user_email)
        new_user.password = generate_password_hash(user_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {'success': True}
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Password and confirm password does not match')


@router.post("/login/", status_code=status.HTTP_200_OK)
def login_user(user_data: UserLoginSchema, session: SessionDep):
    user_email = user_data.email
    user = session.exec(select(User).where(User.email==user_email)).first()
    if user and user.email == user_email:
        user_password = user_data.password
        verify_pass = verify_password(user_password, user.password)
        if verify_pass:
            access_token = generate_token(user.id, session)
            refresh_token = generate_token(user.id, session, is_refresh=True)
            if access_token and refresh_token:
                token = {
                    'Access': access_token,
                    'Refresh': refresh_token
                }
                return {'success': True, 'token': token}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password does not match')


@router.post("/logout/", status_code=status.HTTP_200_OK)
def logout_user(jwt_token: Annotated[str, Depends(verify_token)], session: SessionDep):
    token = session.exec(select(Token).where(Token.token==jwt_token)).first()
    if token:
        token.is_revoke = True
        session.add(token)
        session.commit()
        return {'success': True}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized')
