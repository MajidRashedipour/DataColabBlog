from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Header, Query
from sqlmodel import select, or_

from app.database import SessionDep
from app.models import Post, User, AccessToken, RefreshToken
from app.schemas.posts import CreatePostSchema, ReadPostSchema
from app.utils import decode_token


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post_data: CreatePostSchema, session: SessionDep, authorization: Annotated[str | None, Header()] = None):
    if authorization:
        token_type = authorization.split(' ')[0]
        token = authorization.split(' ')[1]
        access_token = session.exec(select(AccessToken).where(AccessToken.token==token)).first()
        refresh_token = session.exec(select(RefreshToken).where(RefreshToken.token==token)).first()
        if (access_token and access_token.token_type == token_type and access_token.expire_at >= datetime.now() and not access_token.is_revoke) or (refresh_token and refresh_token.token_type == token_type and refresh_token.expire_at >= datetime.now() and not refresh_token.is_revoke):
            token = access_token if access_token else refresh_token
            payload = decode_token(token.token)
            user_id = payload.get('sub')
            user = session.get(User, user_id)
            if user:
                new_post = Post(title=post_data.title, content=post_data.content, tags=str(post_data.tags), author_id=user.id)
                session.add(new_post)
                session.commit()
                session.refresh(new_post)
                return {'success': True}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Token')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized')


@router.put("/{post_id}/", status_code=status.HTTP_200_OK)
def update_post(post_id: int, post_data: CreatePostSchema, session: SessionDep, authorization: Annotated[str | None, Header()] = None):
    if authorization:
        token_type = authorization.split(' ')[0]
        token = authorization.split(' ')[1]
        access_token = session.exec(select(AccessToken).where(AccessToken.token==token)).first()
        refresh_token = session.exec(select(RefreshToken).where(RefreshToken.token==token)).first()
        if (access_token and access_token.token_type == token_type and access_token.expire_at >= datetime.now() and not access_token.is_revoke) or (refresh_token and refresh_token.token_type == token_type and refresh_token.expire_at >= datetime.now() and not refresh_token.is_revoke):
            token = access_token if access_token else refresh_token
            payload = decode_token(token.token)
            user_id = payload.get('sub')
            user = session.get(User, user_id)
            post = session.get(Post, post_id)
            if post and ((int(post.author_id) == int(user_id)) or user.is_admin):
                post.title = post_data.title
                post.content = post_data.content
                post.tags = str(post_data.tags)
                session.add(post)
                session.commit()
                session.refresh(post)
                return {'success': True}
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User not allowed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized')


@router.delete("/{post_id}/", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, session: SessionDep, authorization: Annotated[str | None, Header()] = None):
    if authorization:
        token_type = authorization.split(' ')[0]
        token = authorization.split(' ')[1]
        access_token = session.exec(select(AccessToken).where(AccessToken.token==token)).first()
        refresh_token = session.exec(select(RefreshToken).where(RefreshToken.token==token)).first()
        if (access_token and access_token.token_type == token_type and access_token.expire_at >= datetime.now() and not access_token.is_revoke) or (refresh_token and refresh_token.token_type == token_type and refresh_token.expire_at >= datetime.now() and not refresh_token.is_revoke):
            token = access_token if access_token else refresh_token
            payload = decode_token(token.token)
            user_id = payload.get('sub')
            user = session.get(User, user_id)
            if user and user.is_admin:
                post = session.get(Post, post_id)
                if post:
                    session.delete(post)
                    session.commit()
                    return {'success': True}
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User not allowed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized')


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ReadPostSchema])
def read_posts(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100, search: str | None = None):
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    if search:
        posts = session.exec(select(Post).where(or_(Post.tags.contains(search), Post.title.contains(search), Post.content.contains(search)))).all()
    if posts:
        return posts
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')


# @router.get("/{post_id}/", status_code=status.HTTP_200_OK, response_model=ReadPostSchema)
# def read_a_post(post_id: int, session: SessionDep):
#     post = session.get(Post, post_id)
#     if post:
#         return post
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
