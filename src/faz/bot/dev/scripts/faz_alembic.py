# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "alembic>=1.14.0",
#   "sqlalchemy>=2.0.36",
# ]
# ///

from typing import Optional, Sequence

from alembic.config import CommandLine

from faz.bot.dev.scripts.dbvcs.alembic_config import AlembicConfig


class FazAlembic(CommandLine):
    def main(self, argv: Optional[Sequence[str]] = None) -> None:
        options = self.parser.parse_args(argv)
        if not hasattr(options, "cmd"):
            # see http://bugs.python.org/issue9253, argparse
            # behavior changed incompatibly in py3.3
            self.parser.error("too few arguments")
        else:
            cfg = AlembicConfig(section_name=options.name, cmd_opts=options)
            self.run_cmd(cfg, options)


def main() -> None:
    alembic = FazAlembic("main")
    alembic.main()


if __name__ == "__main__":
    main()
