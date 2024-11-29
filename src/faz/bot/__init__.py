from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

try:
    __version__ = version("faz-bot-core")
except PackageNotFoundError:
    __version__ = "development"
