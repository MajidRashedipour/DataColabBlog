from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlmodel import select, or_

from app.database import SessionDep
from app.models.users import User
from app.models.posts import Post
from app.schemas.posts import CreatePostSchema, ReadPostSchema
from app.routers import users


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(user: Annotated[User, Depends(users.get_current_user)], post_data: CreatePostSchema, session: SessionDep):
    new_post = Post(title=post_data.title, content=post_data.content, tags=str(post_data.tags), author_id=user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return {'success': True}


@router.put("/{post_id}/", status_code=status.HTTP_200_OK)
def update_post(post_id: int, post_data: CreatePostSchema, user: Annotated[User, Depends(users.get_current_user)], session: SessionDep):
    post = session.get(Post, post_id)
    if post and ((int(post.author_id) == int(user.id)) or user.is_admin):
        post.title = post_data.title
        post.content = post_data.content
        post.tags = str(post_data.tags)
        session.add(post)
        session.commit()
        session.refresh(post)
        return {'success': True}
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User not allowed')


@router.delete("/{post_id}/", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, user: Annotated[User, Depends(users.get_current_user)], session: SessionDep):
    if user.is_admin:
        post = session.get(Post, post_id)
        if post:
            session.delete(post)
            session.commit()
            return {'success': True}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User not allowed')


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
