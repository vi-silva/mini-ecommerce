from fastapi import Depends
from app.repositories.base_repository import BaseRepository
from app.db.db import Session, get_db
from app.models.models import Customers

class CustomersRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Customers)