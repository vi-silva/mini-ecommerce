from fastapi.param_functions import Depends
from app.db.db import get_db
from app.models.models import Supplier
from .base_repository import BaseRepository
from sqlalchemy.orm import Session

class SuplierRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Supplier)