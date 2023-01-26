from fastapi import APIRouter

from . import level, user, score

router = APIRouter()
router.include_router(user.router)
router.include_router(level.router)
router.include_router(score.router)
