from fastapi import FastAPI

from app.routers import posts, users, comments
from app.internal import admin


app = FastAPI()
app.include_router(admin.router, prefix='/admin')
app.include_router(users.router, prefix='/auth', tags=['Auth'])
app.include_router(posts.router, tags=['Blog Posts'])
app.include_router(comments.router, prefix='/comments', tags=['Comments'])
