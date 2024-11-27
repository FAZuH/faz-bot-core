import os
from abc import ABC, abstractmethod
from typing import override
from unittest import TestCase
from unittest.mock import MagicMock

from alembic import command
from alembic.environment import EnvironmentContext
from alembic.script.base import ScriptDirectory
from sqlalchemy import engine_from_config, text

from faz.bot.dev.scripts.dbvcs.alembic_config import AlembicConfig


class CommonMigrationTest:
    class Test(TestCase, ABC):
        @override
        def setUp(self) -> None:
            self.config = AlembicConfig(self.section_name)
            self.mock_stdout = self.config.print_stdout = MagicMock()

            self._setup_test_dburl()
            self._drop_all()

            command.ensure_version(self.config)
            command.stamp(self.config, "base")

        def test_upgrade(self):
            # Act
            command.upgrade(self.config, self.target_version)

            # Assert
            command.current(self.config)

            output = self.mock_stdout.call_args_list[-1].args[0]
            self.assertIn(self.target_version, output)

        def test_downgrade(self):
            # Prepare
            command.upgrade(self.config, self.target_version)

            # Act
            command.downgrade(self.config, "base")

            # Assert
            command.current(self.config)
            self.mock_stdout.assert_not_called()

        # def _populate_db(self) -> None:
        #     test = CommonFazdbRepositoryTest.Test
        #     mocks = []
        #     mocks.append(test._get_fazdb_uptime_mock_data())
        #     mocks.append(test._get_guild_info_mock_data())
        #     mocks.append(test._get_guild_member_history_mock_data())
        #     mocks.append(test._get_online_players_mock_data())
        #     mocks.append(test._get_player_activity_history_mock_data())
        #     mocks.append(test._get_worlds_mock_data())
        #     mocks.append(test._get_guild_history_mock_data())
        #     mocks.append(test._get_player_info_mock_data())
        #     mocks.append(test._get_character_info_mock_data())
        #     mocks.append(test._get_player_history_mock_data())
        #     mocks.append(test._get_character_history_mock_data())
        #
        #     with self._db.must_enter_session() as ses:
        #         for mock in mocks:
        #             ses.add_all([mock[0], mock[2]])

        def _setup_test_dburl(self) -> None:
            """Override sqlalchemy.url with environment variables if set"""
            user = os.getenv("MYSQL_USER", None)
            password = os.getenv("MYSQL_PASSWORD", None)
            host = os.getenv("MYSQL_HOST", None)
            db_name = self.section_name

            if None in {user, password, host}:
                return

            self.section["sqlalchemy.url"] = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

        def _drop_all(self):
            engine = engine_from_config(self.section, prefix="sqlalchemy.")
            with engine.connect() as conn:
                # Get environment context
                env = EnvironmentContext(self.config, ScriptDirectory.from_config(self.config))
                env.configure(conn)

                # Create a context manager that provides the connection
                with env.begin_transaction():
                    # First, disable foreign key checks
                    conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))

                    # Get the drop statements
                    result = conn.execute(
                        text(
                            """
                            SELECT 
                                CONCAT('DROP TABLE IF EXISTS `', table_name, '`')
                            FROM information_schema.tables
                            WHERE table_schema = DATABASE()
                            AND table_type = 'BASE TABLE'
                        """
                        )
                    )

                    # Execute each drop statement
                    for (drop_statement,) in result:
                        conn.execute(text(drop_statement))

                    # Re-enable foreign key checks
                    conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))

        @property
        def section(self) -> dict[str, str]:
            ret = self.config.get_section(self.section_name)
            assert ret is not None
            return ret

        @property
        def start_version(self) -> str:
            return "base"

        @property
        @abstractmethod
        def target_version(self) -> str: ...

        @property
        @abstractmethod
        def section_name(self) -> str:
            """Database name to test."""
            ...
