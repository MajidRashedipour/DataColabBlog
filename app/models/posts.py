from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    content: str
    tags: str | None = None
    created_at: datetime = Field(default=datetime.now())
    author_id: int = Field(foreign_key='user.id')


class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default=datetime.now())
    user_id: int = Field(foreign_key='user.id')
    post_id: int = Field(foreign_key='post.id')
