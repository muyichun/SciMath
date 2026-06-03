# SciMath — Dify Plugin

> Author: **xujing**

A [Dify](https://dify.ai) plugin providing precise math tools that cover the cases where LLMs are unreliable: symbolic computation, exact arithmetic, and numeric evaluation.

## Tools

### Numeric evaluation
| Tool | Description |
|------|-------------|
| `eval_expression` | Evaluate a numeric math expression locally via NumExpr (fast, supports arrays) |

### Symbolic computation (SymPy)
| Tool | Description | Example input |
|------|-------------|---------------|
| `sympy_solve` | Solve equations / systems symbolically | `x**2 - 4 = 0` |
| `sympy_diff` | Differentiate an expression (nth order) | `sin(x)*x**2`, order=2 |
| `sympy_integrate` | Definite or indefinite integral | `exp(-x**2)`, bounds 0 to oo |
| `sympy_limit` | Limit at a point or infinity | `sin(x)/x` as x→0 |
| `sympy_simplify` | Simplify / factor / expand / partial fractions / trig simplify | `sin(x)**2 + cos(x)**2` |
| `sympy_series` | Taylor / Maclaurin series expansion | `exp(x)` around 0, order 6 |
| `sympy_dsolve` | Solve ordinary differential equations | `f(x).diff(x) - f(x)` |

All SymPy tools return both a human-readable text result (with LaTeX) and a structured JSON object for use in Dify workflows.

## Install

1. Install **Maths** from the Dify Marketplace (or load from this directory for local dev).
2. Add the desired tool to your workflow.
3. Wire the `expression` / `equations` / `ode` parameter from the LLM node.

## Local development

```bash
cp .env.example .env          # fill in REMOTE_INSTALL_HOST/PORT/KEY
uv sync                       # install dependencies
uv run python main.py         # connect to remote Dify instance for live testing
```

## Expression syntax

SymPy tools accept standard mathematical notation:
- Powers: `x**2` or `x^2`
- Implicit multiplication: `2x` or `2*x`
- Constants: `pi`, `E`, `oo` (infinity), `I` (imaginary unit)
- Functions: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `abs`, `factorial`, …
- For ODEs: `f(x).diff(x)` = f′(x), `f(x).diff(x, 2)` = f″(x)

## Development log

See [`docs/DEV_LOG.md`](docs/DEV_LOG.md) for a full history of changes.

## License

Created and maintained by **xujing**.
