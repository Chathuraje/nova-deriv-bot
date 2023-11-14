from fastapi import APIRouter
from .trader_basic import router as trader_basic
from .trader_activities import router as trader_activities

router = APIRouter(
    prefix="/trader",
)

router.include_router(trader_basic)
router.include_router(trader_activities)
