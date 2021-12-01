from fastapi import APIRouter
from .product.views import router as product_router
from .supplier.views import router as supplier_router 
from .category.views import router as category_router

router = APIRouter()

router.include_router(product_router, prefix='/product')
router.include_router(supplier_router, prefix='/supplier')
router.include_router(category_router, prefix='/category')
