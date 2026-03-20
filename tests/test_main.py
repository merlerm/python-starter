"""Tests for main.py."""

from python_starter.config import Config


def test_config_defaults():
    """Test that the default Config has expected values."""
    cfg = Config()
    assert cfg.seed == 42
