from typing import List
from fastapi import APIRouter, status
from fastapi import Depends

from app.models.models import Category, Product
from .schemas import ProductSchema, ShowProductSchema
from sqlalchemy.orm import Session
from app.db.db import get_db

router = APIRouter()

@router.post('/', status_code= status.HTTP_201_CREATED)
def create(product: ProductSchema, db: Session = Depends(get_db)):
    db.add(Product(**product.dict())) #cria um dicionario com o product schema e tenta jogar como atributos para o prduct model - PRECISA DE NOMES IGUAIS
    db.commit()

@router.get('/', response_model=List[ShowProductSchema]) #converte os products para ShowProductSchema para mostrar
def index(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.put('/{id}')
def update(id: int, product: ProductSchema, db: Session = Depends(get_db)):
    query = db.query(Product).filter_by(id=id)
    query.update(product.dict())
    db.commit()

@router.get('/{id}', response_model=ShowProductSchema)
def show(id:int, db:Session=Depends(get_db)):
    return db.query(Product).filter_by(id=id).first()

@router.put('/{id}/category/{id_category}', status_code=status.HTTP_201_CREATED)
def category_to_product(id: int, id_category: int, db: Session = Depends(get_db)):
    query = db.query(Product).filter_by(id=id)
    query.update({"category_id":id_category})
    db.commit()