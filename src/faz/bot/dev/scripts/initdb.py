# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "alembic>=1.14.0",
#   "sqlalchemy>=2.0.36",
# ]
# ///
import os
import re
import subprocess
import sys
from pathlib import Path

# Constants
SCRIPTS_PATH = Path("scripts")
PROJECT_PATH = SCRIPTS_PATH.parent


def load_env() -> None:
    """Load environment variables from .env file."""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()


def check_env() -> None:
    """Check if required environment variables are set."""
    required_vars = [
        "MYSQL_ROOT_PASSWORD",
        "MYSQL_HOST",
        "MYSQL_PORT",
        "MYSQL_USER",
        "MYSQL_PASSWORD",
        "MYSQL_FAZWYNN_DATABASE",
        "MYSQL_FAZCORD_DATABASE",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Error: Required environment variables not set: {', '.join(missing_vars)}")
        sys.exit(1)


def validate_db_name(db_name: str) -> None:
    """Validate database name format."""
    if not re.match(r"^[a-zA-Z0-9_-]+$", db_name):
        print(f"Error: Invalid database name: {db_name}")
        sys.exit(1)


def run_sql(command: str) -> None:
    """Execute SQL command via docker."""
    try:
        subprocess.run(
            [
                "docker",
                "exec",
                "-i",
                "mysql",
                "mariadb",
                "-u",
                "root",
                f"-p{os.environ['MYSQL_ROOT_PASSWORD']}",
                "-h",
                os.environ["MYSQL_HOST"],
                "-P",
                os.environ["MYSQL_PORT"],
                "-e",
                command,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to execute SQL command: {e.stderr}")
        sys.exit(1)


def create_db(db_name: str) -> None:
    """Create main and test databases."""
    validate_db_name(db_name)
    db_name_test = f"{db_name}_test"
    print(f"Creating database: {db_name} and {db_name_test}")
    run_sql(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
    run_sql(f"CREATE DATABASE IF NOT EXISTS `{db_name_test}`;")


def grant_privilege(db_name: str) -> None:
    """Grant privileges for main and test databases."""
    validate_db_name(db_name)
    db_name_test = f"{db_name}_test"
    mysql_user = os.environ["MYSQL_USER"]
    print(f"Granting privileges on {db_name} and {db_name_test} to {mysql_user}")
    run_sql(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{mysql_user}'@'%';")
    run_sql(f"GRANT ALL PRIVILEGES ON `{db_name_test}`.* TO '{mysql_user}'@'%';")


def create_user() -> None:
    """Create MySQL user."""
    mysql_user = os.environ["MYSQL_USER"]
    mysql_password = os.environ["MYSQL_PASSWORD"]
    print(f"Creating user: {mysql_user}")
    run_sql(f"CREATE USER IF NOT EXISTS '{mysql_user}'@'%' IDENTIFIED BY '{mysql_password}';")


def create_dbs() -> None:
    """Create all required databases."""
    create_db(os.environ["MYSQL_FAZWYNN_DATABASE"])
    create_db(os.environ["MYSQL_FAZCORD_DATABASE"])


def grant_privileges() -> None:
    """Grant privileges for all databases."""
    grant_privilege(os.environ["MYSQL_FAZWYNN_DATABASE"])
    grant_privilege(os.environ["MYSQL_FAZCORD_DATABASE"])
    run_sql("FLUSH PRIVILEGES;")


def check_uv() -> None:
    """Check if uv is installed."""
    try:
        subprocess.run(["uv", "--help"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Error: uv command not found.")
        sys.exit(1)


def init_db(name: str) -> None:
    """Initialize database with alembic."""
    name_test = f"{name}_test"
    for db_name in (name, name_test):
        for command in (("ensure_version",), ("upgrade", "head")):
            try:
                subprocess.run(
                    ["uv", "run", "faz-alembic", "-n", db_name, *command],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"Error during alembic {command} for {db_name}: {e.stderr}")
                sys.exit(1)


def init_dbs() -> None:
    """Initialize all databases."""
    init_db("faz-wynn")
    init_db("faz-cord")


def main() -> None:
    """Main function."""

    try:
        load_env()
        check_env()
        check_uv()

        print("Starting database setup...")
        create_user()
        create_dbs()
        grant_privileges()
        init_dbs()
        print("Database setup completed successfully")

    except Exception as e:
        print(f"Error: Script failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
