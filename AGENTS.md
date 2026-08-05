# AGENTS.md

Agent instructions for this repository. Extend this file with the project's structure, commands, and domain conventions as it grows.

## Development

- Python managed with `uv`. Install with `uv venv && uv sync --all-extras --dev`.
- Autoformat: `./run_autoformat.sh` (black, isort, docformatter). Run it after every edit.
- CI checks: `./run_ci_checks.sh` (autoformat + mypy + pylint + pytest). Run it before pushing.
- Tests live in `tests/` and are part of the deliverable, not an afterthought. New behavior ships with a test.
- Configuration goes through Hydra (`config/`), with the structured config in `src/<package>/config.py` kept in sync.

## Design rules

- Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.
- Choose the simplest implementation that fully meets the current requirements. Avoid speculative abstractions, configuration, and indirection.
- Grow the system in layers. Start from the smallest version that works end to end, and add each new capability on top of a product that already works. Never trade a working product for unfinished complexity.
- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.

## Pull requests

Ship work as a stack of small pull requests rather than one large branch, using GitHub's [stacked pull requests](https://docs.github.com/en/pull-requests/get-started/about-stacked-prs). The bottom PR targets the default branch and each PR above targets the branch below it, so every layer carries only its own diff, can be reviewed on its own, and the next layer starts while the one under it is still open.

- Install once: `gh extension install github/gh-stack`.
- `gh stack init` starts a stack, `gh stack add <branch>` opens the next layer, `gh stack submit` pushes every branch and creates the linked PRs.
- `gh stack rebase` cascades a change made at a lower layer up through the stack. `gh stack sync` catches the stack up after a layer merges.
- Merging the bottom PR retargets the remaining PRs automatically. Do not rebase and retarget a stack by hand.
- Stacks merge bottom up, and every branch must live in the same repository (cross-fork stacks are not supported).
- `./run_ci_checks.sh` must pass on each layer, not just on the top of the stack.
- Pull requests are squash-merged, so respond to review with plain follow-up commits rather than amending and force-pushing.

## Comments and docs

Write every comment and docstring for its eventual reader, who has no access to the diff or the conversation that produced it.

- Describe what the code does now, on its own terms. No "no longer", "used to", "previously", "as requested", and no references to a prior version or to an alternative that was considered and dropped.
- The rationale for a *change* belongs in the commit message or PR reply, not in the code.
- Keep comments short: one line whenever possible. No multi-line comment blocks explaining simple code.

## Conventions

- Never use em dashes in code, comments, strings, or docs. Use commas, colons, or semicolons.
- Never add AI attribution to commits or PR bodies (no `Co-Authored-By` lines for assistants).
