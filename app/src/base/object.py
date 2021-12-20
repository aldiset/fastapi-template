import json
from typing import TypeVar, Type

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.src.base.crud import CRUDBase
from app.src.database import session_manager
from app.src.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseObject:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_objects(self, *args, limit: int = None, offset: int = None, **kwargs):
        data = []
        with session_manager() as db:
            crud_base = CRUDBase(model=self.model)
            data = await crud_base.get_multi(*args, db=db, offset=offset, limit=limit, )
        return json.loads(JSONResponse(content=jsonable_encoder(data)).body)

    async def get_record_count(self, *args):
        with session_manager() as db:
            crud_base = CRUDBase(model=self.model)
            return await crud_base.count(*args, db=db)
        return 0

    async def get_object(self, pk: int = None):
        data = []
        with session_manager() as db:
            crud_base = CRUDBase(model=self.model)
            data = await crud_base.get(db=db, pk=pk)
            return data

    async def remove(self, pk: int = None):
        data = []
        with session_manager() as db:
            crud_base = CRUDBase(model=self.model)
            data = await crud_base.remove(db=db, pk=pk)
            return data
