from os import name
import pytest
from fastapi.testclient import TestClient
import factory
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from app.db.db import get_db
from app.models.models import Addresses, Base, Category, Coupons, Customers, PaymentMethods, Product, User, Supplier
from app.app import app
from datetime import date, datetime, timedelta
from app.services.auth_service import create_token

@pytest.fixture()
def db_session():
    engine = create_engine('sqlite:///./test.db',connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = Session()
    yield db
    db.close()
    
@pytest.fixture()
def override_get_db(db_session):
    def _override_get_db():
        yield db_session
    return _override_get_db


@pytest.fixture()
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client

@pytest.fixture()
def user_factory(db_session):
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session = db_session
        
        id = factory.Faker('pyint')
        display_name = factory.Faker('name')
        email = factory.Faker('email')
        role = None
        password = '$2b$12$JkLyS1O5KRlXYTidS/hiqutvLWtcxiemxeKJv0CqmL5aSVWL/toDa' #123
    
    return UserFactory

#TODO descobrir uma forma melhor de fazer isso
@pytest.fixture()
def user_customer_factory(db_session):
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session = db_session
        
        id = factory.Faker('pyint')
        display_name = factory.Faker('name')
        email = factory.Faker('email')
        role = 'customer'
        password = '$2b$12$JkLyS1O5KRlXYTidS/hiqutvLWtcxiemxeKJv0CqmL5aSVWL/toDa' #123
    
    return UserFactory


@pytest.fixture()
def category_factory(db_session):
    class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Category
            sqlalchemy_session = db_session
        
        id = factory.Faker('pyint')
        name = factory.Faker('name')

    return CategoryFactory

@pytest.fixture()
def supplier_factory(db_session):
    class SupplierFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Supplier
            sqlalchemy_session = db_session

        id = factory.Faker('pyint')
        name = factory.Faker('name')

    return SupplierFactory

@pytest.fixture()
def address_factory(db_session):
    class AddressFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Addresses
            sqlalchemy_session = db_session

        id = factory.Faker('pyint')
        address = factory.Faker('name')
        city = factory.Faker('name')
        state = factory.Faker('name')
        number = factory.Faker('name')
        zipcode = factory.Faker('name')
        neighbourhood = factory.Faker('name')
        primary = True
        customer_id = None

    return AddressFactory

@pytest.fixture()
def customer_factory(db_session, user_customer_factory):
    class CustomerFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Customers
            sqlalchemy_session = db_session
        
        id = factory.Faker('pyint')
        first_name = factory.Faker('name')
        last_name = factory.Faker('name')
        phone_number = '999999999'
        genre = 'm'
        document_id = factory.Faker('pyint')
        birth_date = date.today()
        user = factory.SubFactory(user_customer_factory)
    
    return CustomerFactory

@pytest.fixture()
def payment_method_factory(db_session):
    class PaymentMethodFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = PaymentMethods
            sqlalchemy_session = db_session
        
        id = factory.Faker('pyint')
        name = factory.Faker('name')
        enabled = True
    
    return PaymentMethodFactory

#TODO achar uma forma melhor de fazer isso
#ter um fixture que aceite parametros opcionais
@pytest.fixture()
def disabled_payment_method_factory(db_session):
    class PaymentMethodFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = PaymentMethods
            sqlalchemy_session = db_session
        
        id = factory.Faker('pyint')
        name = factory.Faker('name')
        enabled = False
    
    return PaymentMethodFactory

@pytest.fixture()
def product_factory(db_session, category_factory, supplier_factory):
    class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Product
            sqlalchemy_session = db_session

        id = factory.Faker('pyint')
        description = factory.Faker('name')
        price = factory.Faker('pyfloat')
        technical_details = factory.Faker('sentence')
        image = factory.Faker('name')
        visible = True
        category = factory.SubFactory(category_factory)
        supplier = factory.SubFactory(supplier_factory)

    return ProductFactory

@pytest.fixture()
def coupon_factory(db_session):
    class CouponFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Coupons
            sqlalchemy_session = db_session

        id = factory.Faker('pyint')
        code = 'TESTE'
        expire_at = datetime.today()+timedelta(days=10)
        limit = None
        type = 'value'
        value = 10
        
    return CouponFactory

@pytest.fixture()
def user_admin_token(user_factory):
    user = user_factory(role='admin')
    token = create_token({'id':user.id})
    return token


@pytest.fixture()
def admin_auth_header(user_admin_token):
    return {'Authorization': f'Bearer {user_admin_token}'}

@pytest.fixture()
def user_customer_data(customer_factory):
    customer = customer_factory()
    token = create_token({'id':customer.user.id})
    return ({'Authorization': f'Bearer {token}'}, customer) 