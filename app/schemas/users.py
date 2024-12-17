from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    email: str
    password: str
    confirm_password: str

class AdminRegisterSchema(UserRegisterSchema):
    is_admin: bool

class UserLoginSchema(BaseModel):
    email: str
    password: str
