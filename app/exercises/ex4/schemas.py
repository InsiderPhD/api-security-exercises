from pydantic import BaseModel


class CommentCreate(BaseModel):
    author: str
    content: str


class Comment(BaseModel):
    id: int
    author: str
    content: str

    class Config:
        from_attributes = True


