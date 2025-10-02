from pydantic import BaseModel


class Customer(BaseModel):
    id: int
    name: str
    email: str
    ssn: str
    credit_card_number: str
    api_key: str

    class Config:
        from_attributes = True


