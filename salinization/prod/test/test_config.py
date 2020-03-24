from salinization.config import get_config


def test_get_config():
    config = get_config

    assert config is not None