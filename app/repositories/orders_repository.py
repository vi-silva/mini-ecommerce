from app.db.db import Session, get_db
from app.models.models import Orders
from app.repositories.base_repository import BaseRepository
from fastapi import Depends

class OrdersRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Orders)

    def get_by_number(self, number: int):
        return self.session.query(self.model).filter_by(number=number).first()

    