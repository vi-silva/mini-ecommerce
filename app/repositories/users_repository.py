from fastapi.param_functions import Depends
from app.db.db import get_db
from app.models.models import User
from .base_repository import BaseRepository
from sqlalchemy.orm import Session


class UserRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, User)

    def find_by_email(self, email):
        return self.session.query(self.model).filter_by(email=email).first()

    def get_all_admins(self):
        return self.session.query(self.model).filter_by(role = 'admin').all()

    def get_admin_by_id(self, id: int):
        return self.session.query(self.model).filter_by(role='admin', id=id).first()
    
    def delete_admin(self, id: int):
        self.session.query(self.model).filter_by(role='admin', id=id).delete()
        self.session.commit()

    def get_by_email(self, email: str):
        return self.session.query(self.model).filter_by(email=email).first()
        