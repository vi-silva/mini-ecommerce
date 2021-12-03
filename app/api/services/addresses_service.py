from fastapi.param_functions import Depends
from app.api.repositories.addresses_repository import AddressesRepository
from app.api.repositories.customers_repository import CustomersRepository
from app.api.addresses.schemas import AddressesSchema
from fastapi import HTTPException, status

from app.models.models import Addresses

class AddressesService:
    def __init__(self, addresses_repository: AddressesRepository = Depends(), customers_repository: CustomersRepository = Depends()) -> None:
        self.addresses_repository = addresses_repository
        self.customers_repository = customers_repository

    def create(self, address: AddressesSchema):
        if not self.customers_repository.get_by_id(address.customer_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid customer')
        if address.primary:
            self.addresses_repository.remove_primary()
        self.addresses_repository.create(Addresses(**address.dict()))


    def update(self,id: int, address: AddressesSchema):
        if not self.customers_repository.get_by_id(address.customer_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid customer')
        if address.primary:
            self.addresses_repository.remove_primary()
        self.addresses_repository.update(id, address.dict())
