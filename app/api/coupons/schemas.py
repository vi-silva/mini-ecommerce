from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class CouponType(str, Enum):
    VALUE = 'value'
    PERCENTAGE = 'percentage'

class CouponsSchema(BaseModel):
    code: str
    expire_at: datetime
    limit: int
    type: CouponType
    value: float

class ShowCouponsSchema(CouponsSchema):
    id: int
    class Config:
        orm_mode = True

class UpdateCouponsSchema(BaseModel):
    limit: int
    expire_at: datetime