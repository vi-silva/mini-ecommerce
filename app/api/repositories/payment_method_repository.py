from app.db.db import Session, get_db
from fastapi import Depends
from app.models.models import PaymentMethods
from app.api.repositories.base_repository import BaseRepository


class PaymentMethodRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, PaymentMethods)