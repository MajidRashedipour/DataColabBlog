from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email: str = Field(unique=True, index=True)
    password: str
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now())


class Token(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    token: str
    token_type: str
    expire_at: datetime
    is_refresh: bool = Field(default=False)
    is_revoke: bool = Field(default=False)
    user_id: int = Field(foreign_key='user.id')
