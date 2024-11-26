# Necessary to load the models
from typing import override

from sqlalchemy import MetaData

from faz.bot.database.fazwynn.fazwynn_database import FazwynnDatabase
from faz.bot.database.fazwynn.model.base_fazwynn_model import BaseFazwynnModel
from faz.bot.dev.scripts.dbvcs.base_env import BaseEnv

FazwynnDatabase  # type: ignore prevent being removed by linter


class FazdbEnv(BaseEnv):
    def __init__(self) -> None:
        self._metadata = BaseFazwynnModel.metadata
        super().__init__()

    @property
    @override
    def metadata(self) -> MetaData:
        return self._metadata

    @property
    @override
    def default_schema_env_name(self) -> str:
        return "MYSQL_FAZWYNN_DATABASE"


env = FazdbEnv()
env.run()
