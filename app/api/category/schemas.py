from pydantic import BaseModel

class CategorySchema(BaseModel):
    name: str

class ShowCategorySchema(CategorySchema):
    id: int
    class Config:
        orm_mode = True

