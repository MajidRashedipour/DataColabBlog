from datetime import datetime
from pydantic import BaseModel


class CreatePostSchema(BaseModel):
    title: str
    content: str
    tags: list | None = None
    author_id: int | None = None

class ReadPostSchema(BaseModel):
    title: str
    content: str
    tags: str
    created_at: datetime
