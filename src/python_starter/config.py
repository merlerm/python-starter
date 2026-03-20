"""Structured config for Hydra type checking."""

from dataclasses import dataclass

from hydra.core.config_store import ConfigStore


@dataclass
class Config:
    """Main experiment config."""

    seed: int = 42


def register_configs() -> None:
    """Register structured configs with the Hydra ConfigStore."""
    config_store = ConfigStore.instance()
    config_store.store(name="config_schema", node=Config)
