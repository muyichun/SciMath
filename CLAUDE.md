# CLAUDE.md

> Author: **xujing**

这份文件是给 Claude Code 的项目说明，用于理解本仓库的结构与开发规范。

## 项目简介

SciMath 是 xujing 独立开发的 [Dify](https://dify.ai) 数学计算插件。插件对外暴露一组数学工具，覆盖数值计算（NumExpr）和符号计算（SymPy）两个方向，解决 LLM 在精确数学计算上不可靠的问题。插件可通过 Dify Marketplace 分发。

## 运行与开发

依赖通过 `uv` 管理：

```bash
uv sync                # 安装依赖到 .venv
uv run python main.py  # 启动插件（连接远程 Dify 实例）
```

格式化与 Lint（配置见 `pyproject.toml`）：

```bash
uv run black . -C -l 100
uv run ruff check --fix
```

## 环境配置

复制 `.env.example` 为 `.env`，填写远程 Dify 调试凭据：

- `REMOTE_INSTALL_HOST` / `REMOTE_INSTALL_PORT` / `REMOTE_INSTALL_KEY`

## 项目结构

```
main.py                     # 插件入口，实例化 Plugin 并调用 .run()
manifest.yaml               # 插件元数据（名称、版本、运行器配置、权限）
provider/
  maths.yaml                # Provider 身份声明 + 工具注册表
  maths.py                  # MathsProvider(ToolProvider)，凭据校验为 no-op
tools/
  eval_expression.yaml/.py  # NumExpr 数值计算工具
  sympy_utils.py            # 共享工具：parse_expr、parse_equation、to_latex
  sympy_solve.yaml/.py      # 符号求解方程 / 方程组
  sympy_diff.yaml/.py       # 求导（任意阶、任意变量）
  sympy_integrate.yaml/.py  # 定积分 / 不定积分
  sympy_limit.yaml/.py      # 极限（单侧、双侧、趋于无穷）
  sympy_simplify.yaml/.py   # 化简 / 因式分解 / 展开 / 部分分式 / 三角化简
  sympy_series.yaml/.py     # 泰勒 / 麦克劳林级数展开
  sympy_dsolve.yaml/.py     # 常微分方程求解（支持初始条件）
docs/
  DEV_LOG.md                # 开发日志，每次会话结束后追加
```

## 新增工具流程

新增一个工具需要：
1. `tools/<name>.py` — 实现 `Tool._invoke()`
2. `tools/<name>.yaml` — 定义工具 schema（description、identity、parameters）
3. 在 `provider/maths.yaml` 的 `tools:` 下注册 yaml 路径

所有 SymPy 工具同时输出 `create_text_message`（人类可读文本 + LaTeX）和 `create_json_message`（结构化结果）。

## 文档维护规范

每次修改源文件后，必须同步更新：

| 文件 | 更新时机 | 写什么 |
|------|---------|--------|
| `docs/DEV_LOG.md` | 每次有代码改动的会话 | 新增条目：日期、操作者、变更摘要 |
| `CLAUDE.md`（本文件） | 文件结构或架构有变化时 | 更新项目结构部分 |
| `README.md` | 新增工具或功能时 | 更新工具列表 |

详细规范见 `AGENTS.md`。
