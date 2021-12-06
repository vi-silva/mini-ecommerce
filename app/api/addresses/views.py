from typing import List
from fastapi import APIRouter, status
from fastapi.param_functions import Depends

from app.api.repositories.addresses_repository import AddressesRepository
from app.api.addresses.schemas import AddressesSchema, ShowAddressesSchema
from app.api.services.addresses_service import AddressesService
from app.models.models import Addresses

router = APIRouter()

@router.get('/', response_model=List[ShowAddressesSchema])
def index(repository: AddressesRepository = Depends()):
    return repository.get_all()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(address: AddressesSchema, service: AddressesService = Depends()):
    service.create(address)

@router.get('/{id}', response_model=ShowAddressesSchema)
def show(id: int, repository: AddressesRepository = Depends()):
    return repository.get_by_id(id)

@router.put('/{id}')
def update(id: int, address: AddressesSchema,  service: AddressesService = Depends()):
    service.update(id, address)

@router.delete('/{id}')
def delete(id: int, repository: AddressesRepository = Depends()):
    repository.delete(id)