from typing import List
from fastapi import APIRouter, status, Depends
from app.api.orders.schemas import InputOrderSchema, OrderStatus, ShowOrderSchema
from app.models.models import User
from app.services.auth_service import get_user, only_admin
from app.services.orders_service import OrderService
from app.repositories.orders_repository import OrdersRepository

router = APIRouter()

@router.get('/', response_model=List[ShowOrderSchema])
def index(repository: OrdersRepository = Depends(), user:User = Depends(only_admin)):
    return repository.get_all()

@router.get('/{id}', response_model=ShowOrderSchema)
def show(id: int ,repository: OrdersRepository = Depends(), user:User = Depends(only_admin)):
    return repository.get_by_id(id)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(input_order_schema: InputOrderSchema, service: OrderService = Depends(), user : User = Depends(get_user)):
    service.create(input_order_schema, user)

@router.patch('/{id}')
def update(id: int, order_status: OrderStatus, service: OrderService = Depends(), user : User = Depends(only_admin)):
    service.update(id,order_status)

