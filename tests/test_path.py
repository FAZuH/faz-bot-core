def test_source_path():
    """Test if the source path is configured correctly.

    This test is added to detect conflict between namespace packages.
    """
    from faz.bot.wynn.util.emeralds import Emeralds

    emerald = Emeralds(emeralds=1)

    assert emerald.emeralds == 1

def test_faz_utils_path():
    """Test if the faz.utils path is configured correctly."""
    from faz.utils.cache_util import CacheUtil

    cache = CacheUtil()

    @cache.decorator
    def foo():
        return "bar"

    assert foo() == "bar"


def test_tests_path():
    """Test if the tests path is configured correctly."""
    from tests.test_placeholder import test_placeholder

    assert test_placeholder()