"""Example entry point with Hydra config management."""

import hydra
from omegaconf import DictConfig

from python_starter.config import register_configs

register_configs()


@hydra.main(config_path="../../config", config_name="config", version_base="1.3")
def main(cfg: DictConfig) -> None:
    """Run the main entry point."""
    print(cfg)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
