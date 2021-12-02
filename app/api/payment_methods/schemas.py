from pydantic import BaseModel

class PaymentMethodSchema(BaseModel):
    name: str
    enabled: bool

class ShowPaymentMethodSchema(PaymentMethodSchema):
    id: int
    class Config:
        orm_mode = True