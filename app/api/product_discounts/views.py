from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import query

from app.models.models import PaymentMethods, Product, ProductDiscounts
from .schemas import ProductDiscountsSchema
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from app.db.db import get_db

router = APIRouter()

@router.get('/')
def index(db:Session = Depends(get_db)):
    return db.query(ProductDiscounts).all()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(discount: ProductDiscountsSchema, db: Session = Depends(get_db)):
    validate_discount(discount, db)
    db.add(ProductDiscounts(**discount.dict()))
    db.commit()

@router.get('/{id}')
def show(id: int, db:Session = Depends(get_db)):
    return db.query(ProductDiscounts).filter_by(id=id).first()

@router.put('/{id}')
def update(id: int, discount: ProductDiscountsSchema, db: Session = Depends(get_db)):
    validate_discount_update(id, discount, db)
    db.query(ProductDiscounts).filter_by(id=id).update(discount.dict())
    db.commit()

@router.delete('/{id}', status_code=status.HTTP_410_GONE)
def delete(id: int, db: Session = Depends(get_db)):
    db.query(ProductDiscounts).filter_by(id=id).delete()
    db.commit()

def validate_discount(discount: ProductDiscountsSchema, db: Session):
    payment_method_query = db.query(PaymentMethods).filter_by(id=discount.payment_method_id).first()
    if db.query(ProductDiscounts).filter_by(product_id=discount.product_id, payment_method_id=discount.payment_method_id).first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Payment method already discounted for this product')  
    elif not payment_method_query or payment_method_query.enabled == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payment method')  
    elif not db.query(Product).filter_by(id=discount.product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid product')
    elif discount.value == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid value')

def validate_discount_update(id:int, discount: ProductDiscountsSchema, db: Session):
    payment_method_query = db.query(PaymentMethods).filter_by(id=discount.payment_method_id).first()
    query_discount = db.query(ProductDiscounts).filter_by(product_id=discount.product_id, payment_method_id=discount.payment_method_id).first()
    if query_discount and query_discount.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Payment method already discounted for this product')  
    elif not payment_method_query or payment_method_query.enabled == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payment method')  
    elif not db.query(Product).filter_by(id=discount.product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid product')
    elif discount.value == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid value')
