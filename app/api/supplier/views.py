from typing import List
from fastapi import APIRouter, status
from fastapi.param_functions import Depends

from app.api.supplier.schemas import ShowSupplierSchema, SupplierSchema
from app.models.models import Supplier
from app.services.auth_service import only_admin
from app.repositories.supplier_repository import SuplierRepository



router = APIRouter(dependencies=[Depends(only_admin)])

@router.post('/', status_code= status.HTTP_201_CREATED)
def create(supplier: SupplierSchema, repository: SuplierRepository = Depends()):
    repository.create(Supplier(**supplier.dict()))

@router.get('/', response_model=List[ShowSupplierSchema])
def index(repository: SuplierRepository = Depends()):
    return repository.get_all()

@router.put('/{id}')
def update(id: int, supplier: SupplierSchema, repository: SuplierRepository = Depends()):
    repository.update(id,supplier.dict())

@router.get('/{id}', response_model=ShowSupplierSchema)
def show(id: int, repository: SuplierRepository = Depends()):
    return repository.get_by_id(id)