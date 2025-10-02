from pydantic import BaseModel


class Document(BaseModel):
    id: int
    author_uuid: str
    title: str
    content: str

    class Config:
        from_attributes = True


