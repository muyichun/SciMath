# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A [Dify](https://dify.ai) plugin that exposes a single tool — `eval_expression` — which evaluates math expressions locally using [NumExpr](https://numexpr.readthedocs.io/). It is packaged and distributed via the Dify Marketplace.

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
main.py                   # Plugin entrypoint — instantiates Plugin and calls .run()
manifest.yaml             # Plugin metadata (name, version, runner config, permissions)
provider/
  maths.yaml              # Provider identity/label declarations
  maths.py                # MathsProvider(ToolProvider) — no-op credential validation
tools/
  eval_expression.yaml    # Tool schema: single required `expression` string param
  eval_expression.py      # EvaluateExpressionTool(Tool) — calls ne.evaluate(expression)
```

The plugin framework is `dify_plugin`. Each tool lives in `tools/<name>.py` paired with a `tools/<name>.yaml` schema file. The provider in `provider/` groups tools together and declares the plugin identity.

Adding a new tool requires: a `tools/<name>.py` implementing `Tool._invoke()`, a matching `tools/<name>.yaml`, and registering the yaml in `provider/maths.yaml` under `tools:`.
