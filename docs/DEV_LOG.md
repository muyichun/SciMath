# Development Log

Entries are newest-first. Each entry records what changed, who made the change, and why.

---

## 2026-09-26 — Codex

**Changes:**
- Clarified the README installation guidance for local development.

**Files modified:**
- `README.md` — clarified the local-development installation wording

---

## 2026-06-03 — xujing

**Changes:**
- 重命名插件为 SciMath（科学数学工具），统一 en_US / zh_Hans 双语标签
- 全局替换 author 为 xujing，移除 pt_BR 语言条目
- 替换插件图标为蓝紫渐变 Σ 风格 SVG
- 修正 eval_expression.yaml 中 "an math" 语法错误，统一括号为半角
- 全量重写 README.md、CLAUDE.md、AGENTS.md，以独立作品口吻重新描述项目
- 同步 provider/maths.yaml 与 manifest.yaml 的描述文案

**Files modified:**
- `manifest.yaml` — 作者、名称、描述全量更新
- `provider/maths.yaml` — 作者、名称、描述同步更新
- `tools/eval_expression.yaml` — 移除 pt_BR，修正语法，规范括号
- `_assets/icon.svg` — 全新设计的渐变 Σ 图标
- `README.md` — 重写为 xujing 独立作品风格
- `CLAUDE.md` — 重写项目说明与结构描述
- `AGENTS.md` — 重写为中文规范文档

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
