from __future__ import annotations

from datetime import datetime
from typing import Any, TYPE_CHECKING

from faz.utils.database.base_repository import BaseRepository
import pandas
from sqlalchemy import and_
from sqlalchemy import Select
from sqlalchemy import select

from faz.bot.database.fazwynn.model.guild_member_history import GuildMemberHistory

if TYPE_CHECKING:
    from faz.utils.database.base_mysql_database import BaseMySQLDatabase


class GuildMemberHistoryRepository(BaseRepository[GuildMemberHistory, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, GuildMemberHistory)

    def select_between_period_as_dataframe(
        self,
        player_uuid: bytes,
        period_begin: datetime,
        period_end: datetime,
    ) -> pandas.DataFrame:
        """Selects records for a given member within a specified period and returns
        them as a pandas DataFrame. Sorted by datetime.

        Args:
            player_uuid (bytes): The UUID of the player as a byte string.
            period_begin (datetime): The start of the period to filter records.
            period_end (datetime): The end of the period to filter records.

        Returns:
            pandas.DataFrame: A DataFrame containing `PlayerHistory` records matching
            the specified criteria, sorted by `datetime` in ascending order.
        """
        stmt = self.__get_select_between_period_stmt(period_begin, period_end, player_uuid)
        res = pandas.read_sql_query(stmt, self.database.engine)
        return res

    def __get_select_between_period_stmt(
        self, period_begin: datetime, period_end: datetime, player_uuid: bytes
    ) -> Select:
        model = self.model
        stmt = (
            select(model)
            .where(
                and_(
                    model.datetime >= period_begin,
                    model.datetime <= period_end,
                    model.uuid == player_uuid,
                )
            )
            .order_by(self.model.datetime)
        )
        return stmt
