from pydantic import BaseModel, field_validator


class MessageBase(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("content must not be empty")
        return v


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int

    class Config:
        from_attributes = True


