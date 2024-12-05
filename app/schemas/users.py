from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    email: str
    password: str
    confirm_password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str
