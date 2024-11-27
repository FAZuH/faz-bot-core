from __future__ import annotations

from argparse import Namespace
from enum import Enum

from alembic.config import Config

from . import fazcord, fazwynn


class AlembicConfig(Config):
    FAZCORD_ENV_PATH = fazcord.__path__[0]  # type: ignore
    FAZWYNN_ENV_PATH = fazwynn.__path__[0]  # type: ignore

    def __init__(self, section_name: str | None = None, cmd_opts: Namespace | None = None) -> None:
        if section_name is None:
            super().__init__()
        else:
            super().__init__(ini_section=section_name, cmd_opts=cmd_opts)

        self.set_main_option("prepend_sys_path", ".")
        self.set_main_option("version_path_separator", "os")

        section = self.Section
        self.set_section_option(
            section.FAZCORD.value,
            "sqlalchemy.url",
            "mysql+pymysql://faz:password@localhost/faz-cord",
        )
        self.set_section_option(section.FAZCORD.value, "script_location", self.FAZCORD_ENV_PATH)

        self.set_section_option(
            section.FAZWYNN.value,
            "sqlalchemy.url",
            "mysql+pymysql://faz:password@localhost/faz-wynn",
        )
        self.set_section_option(section.FAZWYNN.value, "script_location", self.FAZWYNN_ENV_PATH)

        self.set_section_option(
            section.FAZCORD_TEST.value,
            "sqlalchemy.url",
            "mysql+pymysql://faz:password@localhost/faz-cord_test",
        )
        self.set_section_option(
            section.FAZCORD_TEST.value, "script_location", self.FAZCORD_ENV_PATH
        )

        self.set_section_option(
            section.FAZWYNN_TEST.value,
            "sqlalchemy.url",
            "mysql+pymysql://faz:password@localhost/faz-wynn_test",
        )
        self.set_section_option(
            section.FAZWYNN_TEST.value, "script_location", self.FAZWYNN_ENV_PATH
        )

    class Section(Enum):
        FAZCORD = "faz-cord"
        FAZWYNN = "faz-wynn"
        FAZCORD_TEST = "faz-cord_test"
        FAZWYNN_TEST = "faz-wynn_test"
