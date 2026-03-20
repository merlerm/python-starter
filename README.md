# Python Starter Repo

![workflow](https://github.com/tomsilver/python-starter/actions/workflows/ci.yml/badge.svg)

A basic template for building Python packages.

## Features
A package built from this starter code will have the following features:
- **Easy to install** with `pip install -e ".[develop]"` (see `pyproject.toml`)
- **Continuous integration** with GitHub Actions (see `.github/workflows/ci.yml` and `run_ci_checks.sh`)
- **Autoformatting** with black, isort, and docformatter (see `run_autoformat.sh`)
- **Linting** with pytest-pylint (see `.pylintrc`)
- **Type checking** with mypy (see `pyproject.toml`)
- **Unit tests** with pytest (see `tests/`)
- **Config management** with [Hydra](https://hydra.cc/) (see `config/` and `src/python_starter/main.py`)

## Instructions

### Create an Empty Repository on GitHub
1. Go to https://github.com/new and follow the instructions on the first page. No need to include a .gitignore, README, or LICENSE; these will be added later. After clicking "Create repository", stop -- don't follow the command line instructions. Remember the NAME of the repository and then go on to step 2.

### Set Up the Code
2. **Clone this repository** and give it the name of your repo: `git clone git@github.com:tomsilver/python-starter.git <NAME>`. You now have a directory called NAME. **Enter** it: `cd <NAME>`.
3. **Configure the repository:** Make changes to `config.json` and then save.
4. **Apply the configuration**: Make sure that your changes to `config.json` are finalized because they can only be applied once. When you are ready, run `python apply_configuration.py`.
5. **Push your changes**: For example, run `git add . && git commit -m "First commit" && git push -u origin main`.

:tada: **That's it! Your code is ready to use** :tada: You should see your code back on GitHub where you previously had an empty repository.

### Common Next Steps
6. **Make changes** to `pyproject.toml`, especially in the dependencies section.
7. **Set up a virtual environment and install**: Using [uv](https://docs.astral.sh/uv/) (recommended): `uv venv && uv sync --all-extras --dev`. Alternatively: `python -m venv .venv && source .venv/bin/activate && pip install -e ".[develop]"`.
8. **Replace the starter files** (`README.md`, `LICENSE`, `config.json`, `apply_configuration.py`, `main.py`, `config.py`, `structs.py`, `utils.py` and the analogous files in `tests/`) with some of your own.

### Configure GitHub (Optional but Recommended)
9. **Set up branch protections** to prevent accidental changes to your main branch. In `https://github.com/<USER>/<NAME>/settings/branches`:
    - Click `Add classic branch protection rule`.
    - The branch pattern name is `main`.
    - Check "Require a pull request before merging (optionally: uncheck "Require approvals").
    - Check "Require status checks to pass before merging".
    - Check "Require branches to be up to date before merging".
    - Then type in `autoformat`, `static-type-checking`, `linting`, `unit-tests`.
    - Check "Do not allow bypassing the above settings".
10. **Set up repository settings** in `https://github.com/<USER>/<NAME>/settings`:
    - Check "Allow auto-merge".
    - Check "Automatically delete head branches".
    - Uncheck "Allow merge commits".
    - Uncheck "Allow rebase merging".
11. **Set up contributor settings** to lower the barrier for external contributions. In `https://github.com/<USER>/<NAME>/settings/actions`:
    - Update "Fork pull request workflows from outside collaborators" to "Require approval for first-time contributors who are new to GitHub".


## Hydra Config Management

This starter includes [Hydra](https://hydra.cc/) for configuration management with launcher plugins for parallel and cluster execution. Configs are type-checked at runtime via [structured configs](https://hydra.cc/docs/tutorials/structured_config/schema/).

### Config Structure
- `config/config.yaml` — Main config file. Add your parameters here.
- `config/launcher/joblib.yaml` — [Joblib launcher](https://hydra.cc/docs/plugins/joblib_launcher/) for parallel local jobs.
- `config/launcher/slurm.yaml` — [Submitit launcher](https://hydra.cc/docs/plugins/submitit_launcher/) for SLURM cluster jobs.
- `src/python_starter/config.py` — Structured config dataclass for type checking. Keep this in sync with `config.yaml`.

### Usage

Run with the default config:
```bash
python src/python_starter/main.py
```

Override a parameter:
```bash
python src/python_starter/main.py seed=123
```

Run a sweep with parallel local execution (joblib):
```bash
python src/python_starter/main.py --multirun +launcher=joblib seed=1,2,3
```

Run a sweep on a SLURM cluster:
```bash
python src/python_starter/main.py --multirun +launcher=slurm seed=1,2,3
```

### Adding Nested Config Groups

To organize configs into groups (e.g., `model`), create a subdirectory under `config/` with one YAML file per variant:

```text
config/
  config.yaml
  model/
    small.yaml
    large.yaml
```

Each YAML file defines the values for that variant and references a group schema for type checking. In `config/model/small.yaml`:
```yaml
defaults:
  - model_schema

hidden_size: 128
num_layers: 2
```

In `config/model/large.yaml`:
```yaml
defaults:
  - model_schema

hidden_size: 512
num_layers: 8
```

Reference a default variant in `config/config.yaml`:
```yaml
defaults:
  - config_schema
  - model: small
  - _self_

seed: 42
```

Add structured configs in `src/python_starter/config.py` and register both the top-level and group schemas. The structured config defines the schema (field names and types); the YAML files provide the actual values:
```python
@dataclass
class ModelConfig:
    hidden_size: int = MISSING
    num_layers: int = MISSING

@dataclass
class Config:
    seed: int = 42
    model: ModelConfig = MISSING

def register_configs() -> None:
    config_store = ConfigStore.instance()
    config_store.store(name="config_schema", node=Config)
    config_store.store(group="model", name="model_schema", node=ModelConfig)
```

Switch between variants from the command line:
```bash
python src/python_starter/main.py model=large
```

## Notes
- Branch protections only work if you have a public repository or an Enterprise account.
- You can include your repository as a dependency if it's hosted on GitHub. For example, alongside requirements like `numpy` or `matplotlib` in a `pyproject.toml` or `requirements.txt` or `setup.py`, you can list `"<PACKAGE-NAME>@git+https://github.com/<USER>/<NAME>.git"`.
- Feel free to open pull requests to improve this repository.
- You can use this code and modify it in any way without any attributions or acknowledgements (see `LICENSE`).
