import os
from abc import ABC, abstractmethod

from alembic import context
from alembic.config import Config
from sqlalchemy import MetaData, engine_from_config


class BaseEnv(ABC):
    def __init__(self) -> None:
        self._config = context.config

        db_name = os.getenv(self.default_schema_env_name, None)
        if db_name is not None:
            self._db_name = db_name
        else:
            self._db_name = self.config.config_ini_section

        self._setup_test_dburl()

    def run(self) -> None:
        if context.is_offline_mode():
            self._run_migrations_offline()
        else:
            self._run_migrations_online()

    def _setup_test_dburl(self) -> None:
        """Override sqlalchemy.url with environment variables if set"""
        user = os.getenv("MYSQL_USER", None)
        password = os.getenv("MYSQL_PASSWORD", None)
        host = os.getenv("MYSQL_HOST", None)

        if None in {user, password, host}:
            # If any of the environment variables are not set, do nothing
            return

        self.section["sqlalchemy.url"] = f"mysql+pymysql://{user}:{password}@{host}/{self._db_name}"

    def _run_migrations_offline(self) -> None:
        """Run migrations in 'offline' mode."""
        context.configure(
            url=self.section["sqlalchemy.url"],
            target_metadata=self.metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()

    def _run_migrations_online(self) -> None:
        """Run migrations in 'online' mode."""
        engine = engine_from_config(self.section, prefix="sqlalchemy.")

        with engine.connect() as connection:
            context.configure(connection=connection, target_metadata=self.metadata)

            with context.begin_transaction():
                context.run_migrations()

    @property
    def config(self) -> Config:
        return self._config

    @property
    def section(self) -> dict[str, str]:
        ret = self.config.get_section(self.config.config_ini_section)
        assert ret is not None
        return ret

    @property
    @abstractmethod
    def default_schema_env_name(self) -> str: ...

    @property
    @abstractmethod
    def metadata(self) -> MetaData: ...
