from fastapi import APIRouter

from . import level, user

router = APIRouter()
router.include_router(user.router)
router.include_router(level.router)
