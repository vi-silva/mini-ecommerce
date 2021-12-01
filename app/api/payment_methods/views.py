from typing import List
from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app.api.payment_methods.schemas import PaymentMethodSchema, ShowPaymentMethodSchema

from app.db.db import get_db
from app.models.models import PaymentMethods

router = APIRouter()

@router.get('/', response_model=List[ShowPaymentMethodSchema])
def index(db: Session = Depends(get_db)):
    return db.query(PaymentMethods).all()

@router.post('/', status_code= status.HTTP_201_CREATED)
def create(payment_method: PaymentMethodSchema, db: Session = Depends(get_db)):
    db.add(PaymentMethods(**payment_method.dict()))
    db.commit()

@router.get('/{id}', response_model=ShowPaymentMethodSchema)
def show(id: int, db: Session = Depends(get_db)):
    return db.query(PaymentMethods).filter_by(id = id).first()

@router.put('/{id}')
def update(id: int, payment_method: PaymentMethodSchema, db: Session = Depends(get_db)):
    query = db.query(PaymentMethods).filter_by(id=id)
    query.update(payment_method.dict())
    db.commit()