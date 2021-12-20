from pydantic import BaseModel, validator

from app.src.database.session import session_manager
from app.src.models.test import Test

class TestBase(BaseModel):
    name: str
    description: str