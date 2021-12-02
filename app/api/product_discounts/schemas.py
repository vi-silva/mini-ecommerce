from typing import Literal
from pydantic import BaseModel
from app.api.product.schemas import ProductSchema
from app.api.payment_methods.schemas import PaymentMethodSchema

class ProductDiscountsSchema(BaseModel):
    product_id: int
    mode: Literal['value', 'percentage']
    value: float
    payment_method_id: float

class ShowProductDiscountsSchema(ProductDiscountsSchema):
    product: ProductSchema
    payment_method: PaymentMethodSchema

    class Config:
        orm_mode = True
