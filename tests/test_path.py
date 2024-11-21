def test_source_path():
    """Test if the source path is configured correctly."""
    from faz.utils.cache_util import CacheUtil

    cache = CacheUtil()

    @cache.decorator
    def foo():
        return None

    assert foo() is None


def test_tests_path():
    """Test if the tests path is configured correctly."""
    from tests.test_placeholder import test_placeholder

    assert test_placeholder()
