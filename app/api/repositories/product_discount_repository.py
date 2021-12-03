from app.db.db import Session, get_db
from fastapi import Depends
from app.models.models import ProductDiscounts
from app.api.repositories.base_repository import BaseRepository

class ProductDiscountRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, ProductDiscounts)

    def get_by_product_and_payment_method(self, product_id: int, payment_method_id: int ):
        return self.session.query(self.model).filter_by(product_id=product_id, payment_method_id=payment_method_id).first()

    def delete(self, int: id):
        self.session.query(self.model).filter_by(id=id).delete()
        self.session.commit()