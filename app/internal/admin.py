from fastapi import status, HTTPException, APIRouter
from sqlmodel import select
from app.database import SessionDep
from app.models.users import User
from app.schemas.users import AdminRegisterSchema
from app.utils import generate_password_hash, validation_email


router = APIRouter(include_in_schema=False)

@router.post("/register/", status_code=status.HTTP_201_CREATED)
def create_admin(user_data: AdminRegisterSchema, session: SessionDep):
    user_email = user_data.email
    user = session.exec(select(User).where(User.email==user_email)).first()
    if user and user.email == user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Email already exist')
    if not validation_email(user_email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Email')
    user_password = user_data.password
    user_confirm_password = user_data.confirm_password
    if user_password == user_confirm_password:
        new_user = User(email=user_email, is_admin=user_data.is_admin)
        new_user.password = generate_password_hash(user_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {'success': True}
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Password and confirm password does not match')