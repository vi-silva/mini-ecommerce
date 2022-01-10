from typing import List
from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app.api.payment_methods.schemas import PaymentMethodSchema, ShowPaymentMethodSchema

from app.db.db import get_db
from app.models.models import PaymentMethods
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.services.auth_service import only_admin

router = APIRouter(dependencies=[Depends(only_admin)])

@router.get('/', response_model=List[ShowPaymentMethodSchema])
def index(repository: PaymentMethodRepository = Depends()):
    return repository.get_all()

@router.post('/', status_code= status.HTTP_201_CREATED)
def create(payment_method: PaymentMethodSchema, repository: PaymentMethodRepository = Depends()):
    repository.create(PaymentMethods(**payment_method.dict()))

@router.get('/{id}', response_model=ShowPaymentMethodSchema)
def show(id: int, repository: PaymentMethodRepository = Depends()):
    return repository.get_by_id(id)

@router.put('/{id}')
def update(id: int, payment_method: PaymentMethodSchema, repository: PaymentMethodRepository = Depends()):
    repository.update(id, payment_method.dict())