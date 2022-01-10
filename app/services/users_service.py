from typing import Union
import bcrypt

from fastapi.exceptions import HTTPException
from app.models.models import User
from app.repositories.users_repository import UserRepository
from fastapi import Depends, status
from app.api.users.schemas import UserSchema
from app.api.admins.schemas import AdminSchema

class UsersService:
    def __init__(self, users_repository: UserRepository = Depends()) -> None:
        self.users_repository = users_repository

    def create(self, schema: UserSchema):
        self.unique_email(schema.email)
        schema.password = bcrypt.hashpw(schema.password.encode('utf8'), bcrypt.gensalt())
        user = User(**schema.dict())
        user.role = 'customer'
        self.users_repository.create(user)

    def create_admin(self, schema: AdminSchema):
        self.unique_email(schema.email)
        schema.password = bcrypt.hashpw(schema.password.encode('utf8'), bcrypt.gensalt())
        user = User(**schema.dict())
        user.role = 'admin'
        self.users_repository.create(user)

    def update(self, id: int, schema: Union[UserSchema, AdminSchema]):
        self.unique_email_update(schema.email, id)
        schema.password = bcrypt.hashpw(schema.password.encode('utf8'), bcrypt.gensalt()) # encriptando a senha
        self.users_repository.update(id, schema.dict())

    def unique_email(self, email: str): 
        if self.users_repository.get_by_email(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already on use")

    def unique_email_update(self, email: str, id: int):
        query = self.users_repository.get_by_email(email)
        if query and query.id != id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already on use")

    