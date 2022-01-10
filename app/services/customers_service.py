from fastapi import Depends
from app.api.users.schemas import UserSchema
from app.models.models import Customers, User
from app.services.users_service import UsersService
from app.repositories.customers_repository import CustomersRepository
from app.api.customers.schemas import CustomersInsertSchema, CustomersSchema, UpdateCustomersSchema
from app.repositories.users_repository import UserRepository

class CustomersService:
    def __init__(self, users_service: UsersService = Depends(), customers_repository: CustomersRepository = Depends(), users_repository: UserRepository = Depends()) -> None:
        self.users_service = users_service
        self.customers_repository = customers_repository
        self.users_repository = users_repository

    def create(self, schema: CustomersInsertSchema):
        user_schema: UserSchema = UserSchema(**{'display_name':schema.display_name,'email':schema.email,'password':schema.password, 'role': 'customer'})
        self.users_service.create(user_schema)
        customer_schema: CustomersSchema = CustomersSchema(**schema.dict())
        customer = Customers(**customer_schema.dict())
        customer.user_id = self.users_repository.get_by_email(user_schema.email).id
        self.customers_repository.create(customer)

    def update(self, id, user: User, schema: UpdateCustomersSchema):
        user = self.users_repository.get_by_id(user.id)
        user_schema = UserSchema(**{'display_name':user.display_name, 'email':schema.email, 'password':schema.password, 'role':user.role})
        self.users_service.update(user.id, user_schema)
        self.customers_repository.update(id, {
            'first_name': schema.first_name,
            'last_name': schema.last_name,
            'phone_number': schema.phone_number,
            'genre': schema.genre,
            'birth_date': schema.birth_date})
        


    