from typing import List
from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from app.models.models import User

from app.repositories.customers_repository import CustomersRepository
from app.api.customers.schemas import CustomersInsertSchema, ShowCustomersSchema, UpdateCustomersSchema
from app.services.customers_service import CustomersService
from app.services.auth_service import get_user, only_admin

router = APIRouter()

@router.get('/', response_model=List[ShowCustomersSchema])
def index(repository: CustomersRepository = Depends()):
    return repository.get_all()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(customer: CustomersInsertSchema, service: CustomersService = Depends()):
    service.create(customer)

@router.get('/{id}', response_model=ShowCustomersSchema)
def show(id: int, repository: CustomersRepository = Depends()):
    return repository.get_by_id(id)

@router.put('/{id}', dependencies=[Depends(get_user)])
def update(id: int, customer: UpdateCustomersSchema, service: CustomersService = Depends(), user : User  = Depends(get_user)):
    service.update(id, user, customer)