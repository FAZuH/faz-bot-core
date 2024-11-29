from datetime import datetime
from datetime import timedelta
from typing import override

import pandas

from faz.bot.database.fazwynn.repository.guild_member_history_repository import (
    GuildMemberHistoryRepository,
)
from tests.database.fazwynn._common_fazwynn_repository_test import CommonFazwynnRepositoryTest


class TestGuildMemberHistoryRepository(
    CommonFazwynnRepositoryTest.Test[GuildMemberHistoryRepository]
):
    async def test_select_between_period_as_dataframe_returns_within_range(
        self,
    ) -> None:
        # Prepare
        self.__insert_mock_data()
        since = self._get_mock_datetime() - timedelta(days=100)
        until = self._get_mock_datetime() + timedelta(days=100)
        mock = self._get_mock_data()[0]

        # Act
        res = self.repo.select_between_period_as_dataframe(mock.uuid, since, until)

        # Assert
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res, pandas.DataFrame)
        self.assertEqual(res.iloc[0].to_dict(), mock.to_dict())

    async def test_select_between_period_as_dataframe_returns_empty_when_outside_range(
        self,
    ) -> None:
        # Prepare
        self.__insert_mock_data()
        since = datetime.fromtimestamp(0)
        until = datetime.fromtimestamp(100)
        mock = self._get_mock_data()[0]

        # Act
        res = self.repo.select_between_period_as_dataframe(mock.uuid, since, until)

        # Assert
        self.assertEqual(len(res), 0)

    def __insert_mock_data(self):
        mock = self._get_mock_data()[0]
        with self.database.enter_session() as ses:
            ses.add(mock)

    @override
    def _get_mock_data(self):
        return self._get_guild_member_history_mock_data()

    @property
    @override
    def repo(self):
        return self.database.guild_member_history
