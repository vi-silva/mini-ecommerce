from fastapi import APIRouter
from .product.views import router as product_router
from .supplier.views import router as supplier_router 
from .category.views import router as category_router
from .payment_methods.views import router as payment_methods_router
from .product_discounts.views import router as product_discount_router
from .coupons.views import router as coupons_router
from .customers.views import router as customers_router

router = APIRouter()

router.include_router(product_router, prefix='/product', tags=['product'])
router.include_router(supplier_router, prefix='/supplier', tags=['supplier'])
router.include_router(category_router, prefix='/category', tags=['category'])
router.include_router(payment_methods_router, prefix='/payment-method', tags=['payment-method'])
router.include_router(product_discount_router, prefix='/product-discount', tags=['product-discount'])
router.include_router(coupons_router, prefix='/coupons', tags=['coupons'])
router.include_router(customers_router, prefix='/customers', tags=['customers'])
