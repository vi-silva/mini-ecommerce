from typing import List
from fastapi import APIRouter, status
from fastapi.param_functions import Depends

from app.api.repositories.customers_repository import CustomersRepository
from app.api.customers.schemas import CustomersSchema, ShowCustomersSchema, UpdateCustomersSchema
from app.models.models import Customers

router = APIRouter()

@router.get('/', response_model=List[ShowCustomersSchema])
def index(repository: CustomersRepository = Depends()):
    return repository.get_all()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(customer: CustomersSchema, repository: CustomersRepository = Depends()):
    repository.create(Customers(**customer.dict()))

@router.get('/{id}', response_model=ShowCustomersSchema)
def show(id: int, repository: CustomersRepository = Depends()):
    return repository.get_by_id(id)

@router.put('/{id}')
def update(id: int, customer: UpdateCustomersSchema, repository: CustomersRepository = Depends()):
    repository.update(id, customer.dict())