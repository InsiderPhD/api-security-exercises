from pydantic import BaseModel


class User(BaseModel):
    uuid: str
    name: str

    class Config:
        from_attributes = True


class Document(BaseModel):
    id: int
    owner_uuid: str
    title: str
    content: str

    class Config:
        from_attributes = True


