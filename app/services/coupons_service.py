from fastapi.param_functions import Depends
from fastapi import HTTPException, status
from app.repositories.coupons_repository import CouponsRepository
from app.models.models import Coupons
from app.api.coupons.schemas import CouponsSchema

class CouponsService:
    def __init__(self, coupons_repository: CouponsRepository = Depends()) -> None:
        self.coupons_repository = coupons_repository

    def create(self, coupon: CouponsSchema):
        if self.coupons_repository.query_by_code(coupon.code):
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail='Invalid Coupon')
        self.coupons_repository.create(Coupons(**coupon.dict()))
