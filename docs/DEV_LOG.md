# Development Log

Entries are newest-first. Each entry records what changed, who made the change, and why.

---

## 2026-06-03 — xujing

**Changes:**
- Unified author to `xujing` across all YAML schemas and MD files
- Removed `pt_BR` locale entries; only `en_US` and `zh_Hans` are maintained
- Replaced plugin icon with a clean blue-purple gradient Σ (sigma) SVG

**Files modified:**
- `tools/eval_expression.yaml` — removed pt_BR, author already xujing
- `manifest.yaml` — author changed from langgenius to xujing, removed pt_BR
- `provider/maths.yaml` — author changed from Bowen Liang to xujing, removed pt_BR
- `_assets/icon.svg` — new clean gradient sigma icon
- `README.md`, `AGENTS.md`, `docs/DEV_LOG.md` — updated author/attribution to xujing

---

## 2026-06-01 — Claude Code

**Changes:**
- Added SymPy symbolic computation engine (Part 1 of math expansion roadmap)
- 7 new tools: `sympy_solve`, `sympy_diff`, `sympy_integrate`, `sympy_limit`, `sympy_simplify`, `sympy_series`, `sympy_dsolve`
- Shared parsing utility module `tools/sympy_utils.py` (parse_expr with implicit multiplication + `^` support)
- All tools return structured JSON + human-readable text with LaTeX notation

**Files modified:**
- `pyproject.toml` — added `sympy>=1.13.0` dependency
- `provider/maths.yaml` — registered 7 new tool YAML files
- `tools/sympy_utils.py` — new: shared expression parsing, equation parsing, latex output
- `tools/sympy_solve.py` + `tools/sympy_solve.yaml` — solve equations/systems symbolically
- `tools/sympy_diff.py` + `tools/sympy_diff.yaml` — differentiation (nth order, partial)
- `tools/sympy_integrate.py` + `tools/sympy_integrate.yaml` — definite/indefinite integrals
- `tools/sympy_limit.py` + `tools/sympy_limit.yaml` — limits (one-sided, at infinity)
- `tools/sympy_simplify.py` + `tools/sympy_simplify.yaml` — simplify/factor/expand/apart/trigsimp/etc.
- `tools/sympy_series.py` + `tools/sympy_series.yaml` — Taylor/Maclaurin series expansion
- `tools/sympy_dsolve.py` + `tools/sympy_dsolve.yaml` — solve ODEs with optional initial conditions

---

## 2024-09-20 — xujing (initial commit)

**Changes:**
- Initial plugin scaffold with single `eval_expression` tool (NumExpr-based numeric evaluator)

**Files modified:**
- `main.py`, `manifest.yaml`, `provider/maths.yaml`, `provider/maths.py`
- `tools/eval_expression.py` + `tools/eval_expression.yaml`
