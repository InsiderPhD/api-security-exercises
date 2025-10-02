from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    display_name: str
    role_id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    # VULNERABILITY: allows client to set any field, including role_id
    email: str | None = None
    display_name: str | None = None
    role_id: int | None = None


