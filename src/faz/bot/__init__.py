from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("faz-bot-core")
except PackageNotFoundError:
    __version__ = "development"
