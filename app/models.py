from typing import List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, ARRAY, String


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email: str = Field(unique=True, index=True)
    password: int
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now())
    posts: 'Post' = Relationship(back_populates='user')
    comments: 'Comment' = Relationship(back_populates='user')
    access_tokens: 'AccessToken' = Relationship(back_populates='user')
    refresh_tokens: 'RefreshToken' = Relationship(back_populates='user')


class AccessToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    token: str
    token_type: str
    expire_at: datetime
    is_revoke: bool = Field(default=False)
    user_id: int = Field(foreign_key='user.id')
    user: User = Relationship(back_populates='access_tokens')
    refresh_tokens: 'RefreshToken' = Relationship(back_populates='access_token')


class RefreshToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    token: str
    token_type: str
    expire_at: datetime
    is_revoke: bool = Field(default=False)
    user_id: int = Field(foreign_key='user.id')
    access_token_id: int = Field(foreign_key='accesstoken.id')
    user: User = Relationship(back_populates='refresh_tokens')
    access_token: AccessToken = Relationship(back_populates='refresh_tokens')


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    content: str
    tags: str | None = None
    created_at: datetime = Field(default=datetime.now())
    author_id: int = Field(foreign_key='user.id')
    user: User = Relationship(back_populates='posts')
    comments: 'Comment' = Relationship(back_populates='post')


class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default=datetime.now())
    author_id: int = Field(foreign_key='user.id')
    post_id: int = Field(foreign_key='post.id')
    user: User = Relationship(back_populates='comments')
    post: Post = Relationship(back_populates='comments')
