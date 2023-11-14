from fastapi import APIRouter
from .copier_basic import router as copier_basic
from .copier_activities import router as copier_activities

router = APIRouter(
    prefix="/copier",
)

router.include_router(copier_basic)
router.include_router(copier_activities)
