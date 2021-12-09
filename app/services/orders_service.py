from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from app.api.orders.schemas import InputOrderSchema, InputProductSchema, OrderProductsSchema, OrderSchema, OrderStatus, OrderStatusSchema
from app.api.coupons.schemas import CouponType
from app.api.product_discounts.schemas import DiscountMode
from app.models.models import OrderProducts, OrderStatuses, Orders, User
from app.repositories.orders_repository import OrdersRepository
from app.repositories.order_statuses_repository import OrderStatusesRepository
from app.repositories.order_product_repository import OrderProductRepository
from app.repositories.customers_repository import CustomersRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.addresses_repository import AddressesRepository
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.repositories.product_discount_repository import ProductDiscountRepository
from app.services.coupons_service import CouponsService
from random import randint

class OrderService:
    def __init__(self, orders_repository: OrdersRepository = Depends(),
                order_product_repository: OrderProductRepository = Depends(),
                order_statuses_repository : OrderStatusesRepository = Depends(),
                products_repository: ProductRepository = Depends(),
                customers_repository: CustomersRepository = Depends(),
                address_repository: AddressesRepository = Depends(),
                coupons_service: CouponsService = Depends(),
                payment_method_repository: PaymentMethodRepository = Depends(),
                product_discount_repository: ProductDiscountRepository = Depends()) -> None:
        self.orders_repository = orders_repository
        self.order_product_repository = order_product_repository
        self.order_statuses_repository = order_statuses_repository
        self.products_repository = products_repository
        self.customers_repository = customers_repository
        self.addresses_repository = address_repository
        self.coupons_service = coupons_service
        self.payment_method_repository = payment_method_repository
        self.product_discount_repository = product_discount_repository

    def create(self, input_order_schema: InputOrderSchema, user: User):
        order_schema = self.generate_order(input_order_schema, user.id)
        self.validate_address(order_schema.customer_id, order_schema.address_id)
        self.validate_payment(order_schema.payment_form_id)
        self.orders_repository.create(Orders(**order_schema.__dict__))
        self.support_order_table_creations(order_schema, input_order_schema)

    def support_order_table_creations(self, order_schema: OrderSchema, input_order_schema: InputOrderSchema):
        id_order = self.orders_repository.get_by_number(order_schema.number).id
        self.create_order_status(id_order,OrderStatus.ORDER_PLACED)
        self.create_order_products(id_order,input_order_schema.products)

    def generate_order(self, input_order_schema: InputOrderSchema, user_id: int) -> OrderSchema:
        total_value_from_products = self.get_products_value(input_order_schema.products)
        return  OrderSchema(
            number = self.create_order_number(),
            status = OrderStatus.ORDER_PLACED,
            created_at = datetime.now(),
            payment_form_id = input_order_schema.payment_form_id,
            customer_id = self.get_customer_id(user_id),
            address_id = input_order_schema.address_id,
            total_value = total_value_from_products,
            total_discount = self.get_discount_value(input_order_schema.coupon_code, total_value_from_products, input_order_schema.products, input_order_schema.payment_form_id)
        )

    #uuid - gerar str aleatorios nao repetidos - quase impossivel de ser igual - tem 100 caracteres então cuidado ao usar -slice it
    #use timestamp pode ser
    def create_order_number(self)-> int:
        number = randint(0,9999)
        if not self.orders_repository.get_by_number(number):
            return number
        self.create_order_number()

    def create_order_status(self, id_order: int, current_status: OrderStatus):
        self.order_statuses_repository.create(OrderStatuses(**OrderStatusSchema(id_order,current_status,datetime.now()).__dict__))

    def get_discount_value(self, code: str, total_value: float, products: List[InputProductSchema], payment_method_id : int):
        total_discount = self.get_coupon_discount(code, total_value)
        if total_discount != 0:
            return total_discount
        total_discount = self.get_product_payment_discount(total_value,products,payment_method_id)
        if total_discount != 0:
            return total_discount
        return 0

    def get_product_payment_discount(self, total_value: float, products: List[InputProductSchema], payment_method_id: int):
        self.get_coupon_discount
        only_one = self.only_one_product(products)
        if only_one:
            query = self.product_discount_repository.get_by_product_and_payment_method(only_one, payment_method_id)
            if query:
                if query.mode == DiscountMode.VALUE:
                    return float(query.value)
                if query.mode == DiscountMode.PERCENTAGE:
                    return (query.value/100)*total_value
        return 0

    def get_coupon_discount(self, code: str, total_value: float):
        query = self.coupons_service.query_valid_by_code(code)
        if query:
            if query.type == CouponType.VALUE:
                return query.value
            if query.type == CouponType.PERCENTAGE:
                return (query.value/100)*total_value
        return 0

    def only_one_product(self,products: List[InputProductSchema]):
        first_id = products[0].id
        for product in products:
            if product.id != first_id:
                return None
        return first_id
        

    def get_products_value(self, products: List[InputProductSchema]):
        value: float = 0.00
        for product in products:
            query = self.products_repository.get_by_id(product.id)
            if not query:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid product')
            value += (float(query.price) * product.quantity)
        return value

    def validate_address(self, customer_id, address_id):
        query = self.addresses_repository.get_by_id(address_id) 
        if not query or query.customer_id != customer_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inválid address')

    def validate_payment(self, payment_method_id: int):
        if not self.payment_method_repository.get_by_id(payment_method_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inválid payment method')

    def get_address_id(self, id: int):
        return self.addresses_repository.get_by_customer_id(id).id

    def get_customer_id(self, id: int):
        query = self.customers_repository.get_by_user_id(id)
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid user')
        return query.id

    def create_order_products(self, id_order: int, products: List[InputProductSchema]):
        for product in products:
            self.order_product_repository.create(OrderProducts(**OrderProductsSchema(id_order, product.id, product.quantity).__dict__))

    def update(self, id: int, order_status: OrderStatus):
        self.orders_repository.update(id,{'status':f'{order_status}'})
        self.create_order_status(id, order_status)
