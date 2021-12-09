from typing import List
from fastapi.params import Query
from pydantic.main import BaseModel


class CatalogFilter:
    def __init__(self, description: str = Query(None),
                 category_id: int = Query(None),
                 supplier_id: int = Query(None),
                 min_price: float = Query(None),
                 max_price: float = Query(None),
                 category_name: str = Query(None)):
        self.description = description
        self.category_id = category_id
        self.supplier_id = supplier_id
        self.min_price = min_price
        self.max_price = max_price
        self.category_name = category_name


class ShowCategorySchema(BaseModel):
    name: str
    id: int

    class Config:
        orm_mode = True


class ShowSupplierSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ShowPaymentMethodSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ShowDiscountSchema(BaseModel):
    mode: str
    value: float
    payment_method: ShowPaymentMethodSchema

    class Config:
        orm_mode = True


class ShowProductSchema(BaseModel):
    id: int
    description: str
    price: float
    category: ShowCategorySchema
    supplier: ShowSupplierSchema
    discounts: List[ShowDiscountSchema]

    class Config:
        orm_mode = True