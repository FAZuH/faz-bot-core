from sqlalchemy import MetaData

from faz.utils.database.base_model import BaseModel


class BaseFazcordModel(BaseModel):
    __abstract__ = True
    metadata = MetaData(naming_convention=BaseModel._naming_convention)
