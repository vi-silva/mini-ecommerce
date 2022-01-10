from pydantic import BaseModel
from pydantic.fields import Field
from sqlalchemy.sql.expression import true

class AdminSchema(BaseModel):
    display_name: str
    email: str
    password: str

class ShowAdminSchema(BaseModel):
    id: int
    display_name: str
    email: str

    class Config:
        orm_mode = True

