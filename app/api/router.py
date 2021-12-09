from fastapi import APIRouter
from .product.views import router as product_router
from .supplier.views import router as supplier_router 
from .category.views import router as category_router
from .payment_methods.views import router as payment_methods_router
from .product_discounts.views import router as product_discount_router
from .coupons.views import router as coupons_router
from .customers.views import router as customers_router
from .addresses.views import router as addresses_router
from .users.views import router as users_router
from .auth.views import router as auth_router
from .admins.views import router as admins_router
from .orders.views import router as orders_router
from .catalog.views import router as catalog_router

router = APIRouter()

router.include_router(product_router, prefix='/product', tags=['product'])
router.include_router(supplier_router, prefix='/supplier', tags=['supplier'])
router.include_router(category_router, prefix='/category', tags=['category'])
router.include_router(payment_methods_router, prefix='/payment-method', tags=['payment-method'])
router.include_router(product_discount_router, prefix='/product-discount', tags=['product-discount'])
router.include_router(coupons_router, prefix='/coupons', tags=['coupons'])
router.include_router(customers_router, prefix='/customers', tags=['customers'])
router.include_router(addresses_router, prefix='/addresses', tags=['addresses'])
router.include_router(users_router, prefix='/users', tags=['users'])
router.include_router(auth_router, prefix='/auth', tags=['auth'])
router.include_router(admins_router, prefix='/admins', tags=['admins'])
router.include_router(orders_router, prefix='/orders', tags=['orders'])
router.include_router(catalog_router, prefix='/catalog', tags=['catalog'])
