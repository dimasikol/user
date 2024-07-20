from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, )
    last_updated = Column(DateTime, nullable=False,)




