from __future__ import annotations

from typing import TYPE_CHECKING, Any

from faz.utils.database.base_repository import BaseRepository

from faz.bot.database.fazwynn.model.guild_member_history import GuildMemberHistory

if TYPE_CHECKING:
    from faz.utils.database.base_mysql_database import BaseMySQLDatabase


class GuildMemberHistoryRepository(BaseRepository[GuildMemberHistory, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, GuildMemberHistory)
