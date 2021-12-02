from pydantic import BaseModel
from app.api.supplier.schemas import ShowSupplierSchema
from app.api.category.schemas import ShowCategorySchema

class ProductSchema(BaseModel):
    description: str
    price: float
    technical_details: str
    image: str
    visible: bool
    supplier_id: int
    category_id: int

class ShowProductSchema(ProductSchema):
    id: int
    category: ShowCategorySchema
    supplier: ShowSupplierSchema
    
    class Config: #classe interna (metaprogramaçao)
        orm_mode = True