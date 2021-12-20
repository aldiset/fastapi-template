from fastapi import APIRouter

from app.src.router.root import api as root

router = APIRouter()

router.include_router(root.router, tags=["Root"], prefix="")
