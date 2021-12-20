from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_mixins import AllFeaturesMixin

from app.src.core import config

engine = create_engine(config.DB_DSN)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


session = scoped_session(Session)
BaseModel.set_session(session)
