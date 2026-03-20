"""Custom Hydra submitit launcher that supports overriding the Python executable.

The stock hydra-submitit-launcher only routes ``max_num_timeout`` to
``SlurmExecutor.__init__``; every other parameter goes through
``update_parameters``, which rejects ``python`` (it is init-only).

``ContainerSlurmLauncher`` adds ``python`` to the init-keys so that a
launcher YAML can set e.g.::

    python: ./bin/python-container

and submitit will call that wrapper instead of ``sys.executable``.
"""

import logging
import os
from pathlib import Path
from typing import Any, List, Sequence

import submitit
from hydra.core.singleton import Singleton
from hydra.core.utils import filter_overrides
from hydra_plugins.hydra_submitit_launcher.config import BaseQueueConf
from hydra_plugins.hydra_submitit_launcher.submitit_launcher import SlurmLauncher
from omegaconf import OmegaConf

log = logging.getLogger(__name__)


class ContainerSlurmLauncher(SlurmLauncher):
    """SlurmLauncher that forwards ``python`` to SlurmExecutor.__init__."""

    def launch(
        self,
        job_overrides: Sequence[Sequence[str]],
        initial_job_idx: int,
    ) -> Sequence[Any]:
        """Launch SLURM jobs with optional custom Python executable.

        Note: Hydra launchers are only invoked in ``--multirun``
        mode. For a single SLURM job, use ``--multirun`` with one
        config value (e.g. ``--multirun seed=42``) or call
        ``bin/python-container`` directly.
        """
        assert self.config is not None

        num_jobs = len(job_overrides)
        assert num_jobs > 0

        params = dict(self.params)

        # Keys that must go to __init__, not update_parameters.
        specific_init_keys = {"max_num_timeout", "python"}

        init_params: dict = {"folder": params["submitit_folder"]}
        init_params.update(
            **{
                f"{self._EXECUTOR}_{key}": val
                for key, val in params.items()
                if key in specific_init_keys
            }
        )
        init_keys = specific_init_keys | {"submitit_folder"}

        executor = submitit.AutoExecutor(cluster=self._EXECUTOR, **init_params)

        baseparams = set(OmegaConf.structured(BaseQueueConf).keys())
        update_params = {
            key if key in baseparams else f"{self._EXECUTOR}_{key}": val
            for key, val in params.items()
            if key not in init_keys
        }
        executor.update_parameters(**update_params)

        log.info(
            "Submitit '%s' sweep output dir : %s",
            self._EXECUTOR,
            self.config.hydra.sweep.dir,
        )
        sweep_dir = Path(str(self.config.hydra.sweep.dir))
        sweep_dir.mkdir(parents=True, exist_ok=True)
        if "mode" in self.config.hydra.sweep:
            mode = int(str(self.config.hydra.sweep.mode), 8)
            os.chmod(sweep_dir, mode=mode)

        job_params: List[Any] = []
        for idx, overrides in enumerate(job_overrides):
            idx = initial_job_idx + idx
            lst = " ".join(filter_overrides(overrides))
            log.info("\t#%d : %s", idx, lst)
            job_params.append(
                (
                    list(overrides),
                    "hydra.sweep.dir",
                    idx,
                    f"job_id_for_{idx}",
                    Singleton.get_state(),
                )
            )

        jobs = executor.map_array(self, *zip(*job_params))
        return [j.results()[0] for j in jobs]
