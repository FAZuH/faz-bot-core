# faz-bot-core

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install faz-bot-core
```

## Scripts

This package provides a few scripts to help with development. It is recommended to run the scripts using [uv](https://docs.astral.sh/uv/).

### faz-initdb

```console
uv run faz-initdb
```

Initializes `faz-cord` and `faz-wynn` database. Does not install the database client. Overwrite default configs using environment variables (from .env-example).

### faz-alembic

```console
uv run faz-alembic -n <name> [command]
```

Entry point for [Alembic](https://alembic.sqlalchemy.org/en/latest/), a database migration tool. `<name>` can be: `faz-cord`, `faz-wynn`, `faz-cord_test` or `faz-wynn_test`.

The following are some useful commands:

- `upgrade head`: Upgrade to the latest revision.
- `upgrade <revision>`: Upgrade to a specific revision.
- `downgrade <revision>`: Downgrade to a specific revision.
- `current`: Show the current revision.
- `history`: Show the revision history.
- `ensure_version`: Ensure the version table exists (named `alembic_version`).

## License

`faz-bot-core` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
