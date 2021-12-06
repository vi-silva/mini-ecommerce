from typing import List
from fastapi import APIRouter, status
from fastapi import Depends

from app.models.models import Product
from app.services.auth_service import only_admin
from .schemas import ProductSchema, ShowProductSchema
from app.repositories.product_repository import ProductRepository

router = APIRouter(dependencies=[Depends(only_admin)]) #adicionando a necessidade de estar logado E ser um admin

@router.post('/', status_code= status.HTTP_201_CREATED)
def create(product: ProductSchema, repository: ProductRepository = Depends()):
    #cria um dicionario com o product schema e tenta jogar como atributos para o prduct model - PRECISA DE NOMES IGUAIS
    repository.create(Product(**product.dict()))

@router.get('/', response_model=List[ShowProductSchema]) #converte os products para ShowProductSchema para mostrar
def index(db: ProductRepository = Depends()):
    return db.get_all()

@router.put('/{id}')
def update(id: int, product: ProductSchema, repository: ProductRepository = Depends()):
    repository.update(id, product.dict())

@router.get('/{id}', response_model=ShowProductSchema)
def show(id:int, repository: ProductRepository = Depends()):
    return repository.get_by_id(id)