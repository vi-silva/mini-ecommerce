from fastapi import APIRouter, status, Depends
from app.api.orders.schemas import InputOrderSchema, OrderStatus
from app.models.models import User
from app.services.auth_service import get_user, only_admin
from app.services.orders_service import OrderService

router = APIRouter(dependencies=[Depends(get_user)])

@router.post('/')
def create(input_order_schema: InputOrderSchema, service: OrderService = Depends(), user : User = Depends(get_user)):
    service.create(input_order_schema, user)

@router.patch('/{id}')
def update(id: int, order_status: OrderStatus, service: OrderService = Depends(), user : User = Depends(only_admin)):
    service.update(id,order_status)
