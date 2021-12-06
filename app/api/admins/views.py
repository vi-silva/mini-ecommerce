from os import stat
from typing import List
from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from app.api.admins.schemas import AdminSchema, ShowAdminSchema
from app.models.models import User
from app.services.auth_service import only_admin
from app.repositories.users_repository import UserRepository
from app.services.users_service import UsersService

router = APIRouter(dependencies=[Depends(only_admin)])

@router.get('/', response_model=List[ShowAdminSchema])
def index(repository: UserRepository = Depends()):
    return repository.get_all_admins()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(admin_schema: AdminSchema ,service: UsersService = Depends()):
    service.create(admin_schema)

@router.get('/{id}', response_model=ShowAdminSchema)
def show(id: int, repository: UserRepository = Depends()):
    return repository.get_admin_by_id(id)

@router.put('/{id}')
def update(id: int,admin_schema: AdminSchema, service: UsersService = Depends()):
    service.update(id, admin_schema)

@router.delete('/{id}')
def delete(id: int, repository: UserRepository = Depends()):
    repository.delete_admin(id)