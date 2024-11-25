from faz.bot.dev.test.fixtures_api import FixturesApi


def test_fixtures_api_imports_dataset():
    api = FixturesApi()
    api.load_fixtures()
    assert api.guild_stats is not None
    assert api.player_stats is not None
    assert api.online_uuids is not None
