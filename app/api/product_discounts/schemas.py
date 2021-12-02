from typing import Literal
from enum import Enum
from pydantic import BaseModel
from app.api.product.schemas import ProductSchema
from app.api.payment_methods.schemas import PaymentMethodSchema

class DiscountMode(str, Enum):
    VALUE = 'value'
    PERCENTAGE = 'percentage'

class ProductDiscountsSchema(BaseModel):
    product_id: int
    # mode: Literal['value', 'percentage'] #minha solucao original
    mode: DiscountMode #avisando que precisa ser um daqueles valores
    value: float
    payment_method_id: float

class ShowProductDiscountsSchema(ProductDiscountsSchema):
    product: ProductSchema
    payment_method: PaymentMethodSchema

    class Config:
        orm_mode = True
