# Necessary to load the models
from typing import override

from scripts.dbvcs.base_env import BaseEnv
from sqlalchemy import MetaData

from faz.bot.database.fazcord.fazcord_database import FazcordDatabase
from faz.bot.database.fazcord.model.base_fazcord_model import BaseFazcordModel

FazcordDatabase  # type: ignore prevent being removed by linter lol


class FazcordEnv(BaseEnv):
    def __init__(self) -> None:
        self._metadata = BaseFazcordModel.metadata
        super().__init__()

    @property
    @override
    def metadata(self) -> MetaData:
        return self._metadata

    @property
    @override
    def default_schema_env_name(self) -> str:
        return "MYSQL_FAZCORD_DATABASE"


env = FazcordEnv()
env.run()
