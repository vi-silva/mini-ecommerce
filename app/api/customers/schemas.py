from datetime import date, datetime
from pydantic import BaseModel
from app.api.users.schemas import UserSchema

class CustomersSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    genre: str
    document_id: int
    birth_date: date
    
class CustomersInsertSchema(CustomersSchema):
    user: UserSchema
    

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