from datetime import datetime
from pydantic import BaseModel


class CreateCommentSchema(BaseModel):
    content: str
    author_id: int | None = None
    post_id: int | None = None

class ReadCommentSchema(BaseModel):
    content: str
    created_at: datetime
