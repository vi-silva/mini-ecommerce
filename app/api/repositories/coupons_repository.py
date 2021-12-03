from app.api.repositories.base_repository import BaseRepository
from app.db.db import Session, get_db
from app.models.models import Coupons
from fastapi import Depends

class CouponsRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Coupons)

    def delete(self, id: int):
        self.session.query(self.model).filter_by(id=id).delete()
        self.session.commit()

    def query_by_code(self, code: str):
        return self.session.query(self.model).filter_by(code=code).first()
