from faz.utils.database.base_model import BaseModel
from sqlalchemy import MetaData


class BaseFazwynnModel(BaseModel):
    __abstract__ = True
    metadata = MetaData(naming_convention=BaseModel._naming_convention)
