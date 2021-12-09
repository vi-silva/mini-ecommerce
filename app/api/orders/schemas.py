from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from app.api.customers.schemas import ShowCustomersSchema
from app.api.payment_methods.schemas import ShowPaymentMethodSchema
from app.api.addresses.schemas import ShowAddressesSchema

from app.db.db import Base

class OrderStatus(str, Enum):
    ORDER_PLACED = 'order_placed'
    ORDER_PAID = 'order_paid'
    ORDER_SHIPPED = 'order_shipped'
    ORDER_RECEIVED = 'order_received'
    ORDER_COMPLETED = 'order_completed'
    ORDER_CANCELLED = 'order_cancelled'

class InputProductSchema(BaseModel):
    id: int
    quantity: int

class InputOrderSchema(BaseModel):
    address_id: int
    payment_form_id: int
    coupon_code: Optional[str]
    products: List[InputProductSchema]

class InputOrderStatusSchema(BaseModel):
    status:OrderStatus

class ShowOrderSchema(BaseModel):
    number: str
    status: str
    customer_id: int
    customer: ShowCustomersSchema
    created_at: datetime
    address_id: int
    address: ShowAddressesSchema
    total_value: float
    payment_form_id:int
    payment_form: ShowPaymentMethodSchema
    total_discount:float

    class Config:
        orm_mode = True

class OrderSchema: #TODO converter para um DTO - muda o nome
    def __init__(self,number: str,status: str,customer_id: int,created_at: datetime,address_id: int,total_value: float,payment_form_id:int,total_discount:float) -> None:
        self.number = number
        self.status = status
        self.customer_id = customer_id
        self.created_at = created_at
        self.address_id = address_id
        self.total_value = total_value
        self.payment_form_id = payment_form_id
        self.total_discount = total_discount

class OrderStatusSchema:
    def __init__(self,order_id: int, status:OrderStatus, created_at: datetime) -> None:
        self.order_id = order_id
        self.status = status
        self.created_at = created_at

class OrderProductsSchema:
    def __init__(self, order_id: int, product_id:int , quantity:int ) -> None:
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
    