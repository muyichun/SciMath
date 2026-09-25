# SciMath — Dify Plugin

> Author: **xujing**

SciMath is a scientific math plugin for [Dify](https://dify.ai) workflows. The motivation is straightforward: LLMs are unreliable at precise calculation, yet workflows often need exact results. SciMath delegates the math to dedicated engines — SymPy for symbolic computation, NumExpr for numeric evaluation — so results are deterministic and reproducible.

---

## Tools

### Numeric evaluation

| Tool | Description |
|------|-------------|
| `eval_expression` | Evaluate a math expression locally via NumExpr (fast, supports array operations) |

### Symbolic computation (SymPy)

| Tool | Description | Example input |
|------|-------------|---------------|
| `sympy_solve` | Solve equations or systems symbolically, returns exact solutions | `x**2 - 4 = 0` |
| `sympy_diff` | Differentiate an expression (nth order, partial derivatives supported) | `sin(x)*x**2`, order=2 |
| `sympy_integrate` | Definite or indefinite integral | `exp(-x**2)`, bounds 0 to oo |
| `sympy_limit` | Limit at a point or infinity (one-sided or two-sided) | `sin(x)/x` as x→0 |
| `sympy_simplify` | Simplify / factor / expand / partial fractions / trig simplify | `sin(x)**2 + cos(x)**2` |
| `sympy_series` | Taylor / Maclaurin series expansion | `exp(x)` around 0, order 6 |
| `sympy_dsolve` | Solve ordinary differential equations with optional initial conditions | `f(x).diff(x) - f(x)` |

All SymPy tools return both:
- A human-readable text result with LaTeX notation
- A structured JSON object for downstream use in Dify workflows

---

## Installation

1. Install **SciMath** from the Dify Plugin Marketplace, or load this directory directly when developing locally.
2. Add the desired tool node to your workflow.
3. Wire the expression / equation parameter from your LLM node to the tool input.

---

## Local development

```bash
cp .env.example .env          # fill in REMOTE_INSTALL_HOST / PORT / KEY
uv sync                       # install dependencies
uv run python main.py         # connect to a remote Dify instance for live testing
```

Formatting and lint:

```bash
uv run black . -C -l 100
uv run ruff check --fix
```

---

## Expression syntax

SymPy tools accept standard mathematical notation:

- Powers: `x**2` or `x^2`
- Implicit multiplication: `2x` is equivalent to `2*x`
- Constants: `pi`, `E`, `oo` (infinity), `I` (imaginary unit)
- Functions: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `abs`, `factorial`, …
- ODE notation: `f(x).diff(x)` = f′(x), `f(x).diff(x, 2)` = f″(x)

---

## Development log

See [`docs/DEV_LOG.md`](docs/DEV_LOG.md) for the full change history.

---

## License

Created and maintained by **xujing**. All rights reserved.
