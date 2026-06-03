# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Author: **xujing**

## What this is

A [Dify](https://dify.ai) plugin that exposes math tools including `eval_expression` (NumExpr-based numeric evaluator) and a full suite of SymPy symbolic computation tools. Created and maintained by xujing, distributed via the Dify Marketplace.

## Running and developing

Dependencies are managed with `uv`:

```bash
uv sync                # install dependencies into .venv
uv run python main.py  # start the plugin (connects to remote Dify instance)
```

Formatting and linting (from `pyproject.toml`):

```bash
uv run black . -C -l 100
uv run ruff check --fix
```

## Environment setup

Copy `.env.example` to `.env` and fill in the remote Dify debug credentials:

- `REMOTE_INSTALL_HOST` / `REMOTE_INSTALL_PORT` / `REMOTE_INSTALL_KEY` — connect the plugin to a running Dify instance for live testing.

## Architecture

```
main.py                     # Plugin entrypoint — instantiates Plugin and calls .run()
manifest.yaml               # Plugin metadata (name, version, runner config, permissions)
provider/
  maths.yaml                # Provider identity/label declarations + tool registry
  maths.py                  # MathsProvider(ToolProvider) — no-op credential validation
tools/
  eval_expression.yaml/.py  # NumExpr numeric evaluator (original tool)
  sympy_utils.py            # Shared: parse_expr wrapper, parse_equation, to_latex
  sympy_solve.yaml/.py      # Solve equations / systems symbolically
  sympy_diff.yaml/.py       # Differentiation (nth order, any variable)
  sympy_integrate.yaml/.py  # Definite / indefinite integrals
  sympy_limit.yaml/.py      # Limits (one-sided, at infinity)
  sympy_simplify.yaml/.py   # Simplify / factor / expand / apart / trigsimp / …
  sympy_series.yaml/.py     # Taylor / Maclaurin series expansion
  sympy_dsolve.yaml/.py     # Solve ODEs with optional initial conditions
docs/
  DEV_LOG.md                # Development log — append an entry after every session
```

The plugin framework is `dify_plugin`. Each tool lives in `tools/<name>.py` paired with a `tools/<name>.yaml` schema file. The provider in `provider/` groups tools together and declares the plugin identity.

Adding a new tool requires: a `tools/<name>.py` implementing `Tool._invoke()`, a matching `tools/<name>.yaml`, and registering the yaml in `provider/maths.yaml` under `tools:`.

All SymPy tools output both `create_text_message` (human-readable text + LaTeX) and `create_json_message` (structured result for downstream use in Dify workflows).

## Documentation requirements

After every coding session that modifies source files, update:
- `docs/DEV_LOG.md` — append a new entry (see `AGENTS.md` for format)
- `CLAUDE.md` (this file) — update Architecture if files changed
- `README.md` — update Features/Usage if new tools were added

See `AGENTS.md` for the full multi-tool (Claude / Codex / Cursor) workflow and conventions.
