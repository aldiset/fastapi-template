from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.src.database import Base
from app.src.core.config import PAGINATION_LIMIT

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get(self, db: Session, pk: Any) -> Optional[ModelType]:
        data = db.query(self.model).filter(and_(self.model.id == pk, self.model.deleted_date == None)).first()
        if data:
            return data
        else:
            raise FileNotFoundError("Data not found!")

    async def get_multi(
        self, *args, db: Session, offset: int = 0, limit: int = PAGINATION_LIMIT
    ) -> List[ModelType]:
        return db.query(self.model).filter(self.model.deleted_date == None, *args).order_by(self.model.id.asc()).offset(offset).limit(limit).all()

    async def count(
        self, *args, db: Session
    ) -> int:
        return db.query(self.model).filter(self.model.deleted_date == None, *args).count()

    async def remove(self, db: Session, *, pk: int) -> ModelType:
        obj = await self.get(db=db, pk=pk)
        if obj:
            obj.deleted_date = datetime.now()
            db.commit()
            db.refresh(obj)
            return obj
        else:
            raise FileNotFoundError("Data not found!")
