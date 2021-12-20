from typing import ClassVar
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime
from app.src.database.engine import Base

class Test(Base):
    __tablename__ = "tb_test"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    deleted_date = Column(DateTime)