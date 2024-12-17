from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select

from app.database import SessionDep
from app.models.users import User
from app.models.posts import Post, Comment
from app.routers import users
from app.schemas.comments import CreateCommentSchema, ReadCommentSchema


router = APIRouter()

@router.post("/{post_id}/", status_code=status.HTTP_201_CREATED)
def create_post_comment(post_id: int, comment_data: CreateCommentSchema, user: Annotated[User, Depends(users.get_current_user)], session: SessionDep):
    post = session.get(Post, post_id)
    if post:
        new_comment = Comment(content=comment_data.content, user_id=user.id, post_id=post.id)
        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)
        return {'success': True}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')


# @router.put("/update/{comment_id}/", status_code=status.HTTP_200_OK)
# def update_comment(comment_id: int, post_data: CreateCommentSchema, session: SessionDep, authorization: Annotated[str | None, Header()] = None):
#     if authorization:
#         token_type = authorization.split(' ')[0]
#         token = authorization.split(' ')[1]
#         access_token = session.exec(select(AccessToken).where(AccessToken.token==token)).first()
#         refresh_token = session.exec(select(RefreshToken).where(RefreshToken.token==token)).first()
#         if (access_token and access_token.token_type == token_type and access_token.expire_at >= datetime.now() and not access_token.is_revoke) or (refresh_token and refresh_token.token_type == token_type and refresh_token.expire_at >= datetime.now() and not refresh_token.is_revoke):
#             token = access_token if access_token else refresh_token
#             payload = decode_token(token.token)
#             user_id = payload.get('sub')
#             user = session.get(User, user_id)
#             comment = session.get(Comment, comment_id)
#             if comment and user.is_admin:
#                 comment.content = post_data.content
#                 session.add(comment)
#                 session.commit()
#                 session.refresh(comment)
#                 return {'success': True}
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User not allowed')
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized')


# @router.delete("/delete/{comment_id}/", status_code=status.HTTP_200_OK)
# def delete_comment(comment_id: int, session: SessionDep, authorization: Annotated[str | None, Header()] = None):
#     if authorization:
#         token_type = authorization.split(' ')[0]
#         token = authorization.split(' ')[1]
#         access_token = session.exec(select(AccessToken).where(AccessToken.token==token)).first()
#         refresh_token = session.exec(select(RefreshToken).where(RefreshToken.token==token)).first()
#         if (access_token and access_token.token_type == token_type and access_token.expire_at >= datetime.now() and not access_token.is_revoke) or (refresh_token and refresh_token.token_type == token_type and refresh_token.expire_at >= datetime.now() and not refresh_token.is_revoke):
#             token = access_token if access_token else refresh_token
#             payload = decode_token(token.token)
#             user_id = payload.get('sub')
#             user = session.get(User, user_id)
#             if user and user.is_admin:
#                 comment = session.get(Comment, comment_id)
#                 if comment:
#                     session.delete(comment)
#                     session.commit()
#                     return {'success': True}
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')
#             raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User not allowed')
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User unauthorized')


# @router.get("/", status_code=status.HTTP_200_OK, response_model=list[ReadCommentSchema])
# def read_comments(session: SessionDep):
#     comments = session.exec(select(Comment)).all()
#     if comments:
#         return comments
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')


# @router.get("/{comment_id}/", status_code=status.HTTP_200_OK, response_model=ReadCommentSchema)
# def read_a_comment(comment_id: int, session: SessionDep):
#     comment = session.get(Comment, comment_id)
#     if comment:
#         return comment
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')


@router.get("/{post_id}/", status_code=status.HTTP_200_OK, response_model=list[ReadCommentSchema])
def read_post_comments(post_id: int, session: SessionDep):
    comments = session.exec(select(Comment).where(Comment.post_id==post_id)).all()
    if comments:
        return comments
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')