from datetime import date, datetime
from pydantic import BaseModel

class CustomersSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    genre: str
    document_id: int
    birth_date: date

class UpdateCustomersSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    genre: str
    birth_date: date

class ShowCustomersSchema(CustomersSchema):
    id: int

    class Config:
        orm_mode = True