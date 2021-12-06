from app.repositories.base_repository import BaseRepository
from app.db.db import Session
from fastapi import Depends

from app.models.models import Category

class CategoryRepository(BaseRepository):
    def __init__(self, session: Session = Depends()) -> None:
        super().__init__(session, Category)