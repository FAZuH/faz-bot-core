from __future__ import annotations

from typing import TYPE_CHECKING, Any

from faz.utils.database.base_repository import BaseRepository
from faz.bot.database.fazwynn.model.guild_history import GuildHistory

if TYPE_CHECKING:
    from faz.utils.database.base_mysql_database import BaseMySQLDatabase


class GuildHistoryRepository(BaseRepository[GuildHistory, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, GuildHistory)
