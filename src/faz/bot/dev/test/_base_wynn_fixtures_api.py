from abc import ABC
from os.path import dirname, join


class BaseWynnFixturesApi(ABC):
    _ONLINE_PLAYERS_DATASET = join(dirname(__file__), "dataset/online_players.json")
    _PLAYERS_DATASET = join(dirname(__file__), "dataset/players.json")
    _GUILDS_DATASET = join(dirname(__file__), "dataset/guilds.json")
