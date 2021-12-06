from sqlalchemy.orm import Session
from fastapi import Depends
from app.repositories.base_repository import BaseRepository
from app.db.db import get_db
from app.models.models import Product

class ProductRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Product) #chama o construtor da classe pai para injetar a sessão e o modelo específico
