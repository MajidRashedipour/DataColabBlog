from typing import Annotated
from fastapi import APIRouter, status, Header
from fastapi.exceptions import HTTPException
from sqlmodel import select
from app.database import SessionDep
from app.models import User, AccessToken, RefreshToken
from app.schemas.users import UserRegisterSchema, UserLoginSchema
from app.utils import generate_password_hash, verify_password, validation_email, generate_access_token, generate_refresh_token


router = APIRouter()

@router.post("/register/", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserRegisterSchema, session: SessionDep):
    user_email = user_data.email
    user = session.exec(select(User).where(User.email==user_email)).first()
    if user and user.email == user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exist')
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
            access_token = generate_access_token(user.id, session)
            refresh_token = generate_refresh_token(user.id, access_token, session)
            if access_token and refresh_token:
                token = {
                    'Access': access_token,
                    'Refresh': refresh_token
                }
                return {'success': True, 'token': token}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password does not match')


@router.post("/logout/", status_code=status.HTTP_200_OK)
def logout_user(session: SessionDep, authorization: Annotated[str | None, Header()] = None):
    if authorization:
        token = authorization.split(' ')[1]
        access_token = session.exec(select(AccessToken).where(AccessToken.token==token)).first()
        refresh_token = session.exec(select(RefreshToken).where(RefreshToken.token==token)).first()
        if access_token:
            access_token.is_revoke = True
            session.add(access_token)
            session.commit()
            refresh_token = session.exec(select(RefreshToken).where(RefreshToken.access_token_id==access_token.id)).first()
            if refresh_token:
                refresh_token.is_revoke = True
                session.add(refresh_token)
                session.commit()
                return {'success': True}
        elif refresh_token:
            access_token = session.exec(select(AccessToken).where(AccessToken.refresh_tokens==refresh_token)).first()
            refresh_token.is_revoke = True
            session.add(refresh_token)
            session.commit()
            if access_token:
                access_token.is_revoke = True
                session.add(access_token)
                session.commit()
                return {'success': True}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized')
