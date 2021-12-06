from fastapi import APIRouter, status
from app.services.auth_service import only_admin
from app.services.product_discount_service import ProductDiscountService

from app.models.models import ProductDiscounts
from .schemas import ProductDiscountsSchema
from fastapi import Depends
from sqlalchemy.orm.session import Session

from app.repositories.product_discount_repository import ProductDiscountRepository

from app.db.db import get_db

router = APIRouter(dependencies=[Depends(only_admin)])

@router.get('/')
def index(repository: ProductDiscountRepository = Depends()):
    return repository.get_all()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(discount: ProductDiscountsSchema, service: ProductDiscountService = Depends()):
    service.create_discount(discount)

@router.get('/{id}')
def show(id: int, repository: ProductDiscountRepository = Depends()):
    return repository.get_by_id(id)

@router.put('/{id}')
def update(id: int, discount: ProductDiscountsSchema, service: ProductDiscountService = Depends()):
    service.update_discount(id, discount)

@router.delete('/{id}')
def delete(id: int, repository: ProductDiscountRepository = Depends()):
    repository.delete(id)