from fastapi import APIRouter
from app.api.routers.root.root import router as root_router
from app.api.routers.copier.main import router as copier_router
from app.api.routers.trader.main import router as trader_router

router = APIRouter(
    prefix="/api/v1",
)


router.include_router(root_router)
router.include_router(trader_router)
router.include_router(copier_router)