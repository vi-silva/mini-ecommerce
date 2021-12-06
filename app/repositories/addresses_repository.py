from fastapi import Depends
from app.repositories.base_repository import BaseRepository
from app.db.db import Session, get_db
from app.models.models import Addresses

class AddressesRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Addresses)

    def remove_primary(self):
        return self.session.query(self.model).filter_by(primary = True).update({"primary": False})

    def delete(self, id):
        self.session.query(self.model).filter_by(id=id).delete()
        self.session.commit()