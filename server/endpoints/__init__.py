from fastapi import APIRouter
from . import user

router = APIRouter()
router.include_router(user.router)
