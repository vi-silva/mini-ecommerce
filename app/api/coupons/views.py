from typing import List
from fastapi import APIRouter, status
from fastapi.param_functions import Depends

from app.api.repositories.coupons_repository import CouponsRepository
from app.api.coupons.schemas import CouponsSchema, ShowCouponsSchema, UpdateCouponsSchema
from app.api.services.coupons_service import CouponsService
from app.models.models import Coupons

router = APIRouter()

@router.get('/', response_model=List[ShowCouponsSchema])
def index(repository: CouponsRepository = Depends()):
    return repository.get_all()

@router.post('/', status_code= status.HTTP_201_CREATED)
def create(coupon: CouponsSchema, service: CouponsService = Depends()):
    service.create(coupon)

@router.get('/{id}', response_model=ShowCouponsSchema)
def show(id: int, repository: CouponsRepository = Depends()):
    return repository.get_by_id(id)

@router.put('/{id}')
def update(id: int, coupon: UpdateCouponsSchema, repository: CouponsRepository = Depends()):
    repository.update(id, coupon.dict())

@router.delete('/{id}')
def delete(id: int, repository: CouponsRepository = Depends()):
    repository.delete(id)