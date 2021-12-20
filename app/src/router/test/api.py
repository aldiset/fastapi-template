from fastapi import APIRouter, Response

from app.src.exception.handler.context import api_exception_handler
from app.src.models.test import Test
from app.src.schemas.test import TestBase
from .object import BaseObject

router = APIRouter()


@router.get("/test/{id}")
async def signup(id:int):
    with api_exception_handler(Response) as response:
        data = await BaseObject(Test).get_object(pk=id)
        response.data = data
        response.status = True

    return response.to_dict()
