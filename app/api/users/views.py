from fastapi import APIRouter
from fastapi.param_functions import Depends
from .schemas import UserSchema
from app.models.models import User
from app.repositories.users_repository import UserRepository
import bcrypt

router = APIRouter()


@router.post('/')
def create(user: UserSchema, repository: UserRepository = Depends()):
    user.password = bcrypt.hashpw(user.password.encode('utf8'), bcrypt.gensalt()) # encriptando a senha
    repository.create(User(**user.dict()))
    
