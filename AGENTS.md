# AGENTS.md

> 项目作者：**xujing**

本文件面向所有参与本仓库开发的 AI 编码助手（Claude Code、Codex、Cursor 等），说明开发规范与协作流程。

---

## 每次会话结束后必须更新的文件

凡修改了 `tools/` 或 `provider/` 下的 `.py` 或 `.yaml` 文件，必须在本次会话结束前完成以下更新，不得遗漏：

| 文件 | 更新时机 | 写什么 |
|------|---------|--------|
| `docs/DEV_LOG.md` | 每次有代码改动的会话 | 新增条目（见下方格式） |
| `CLAUDE.md` | 文件结构或架构有变化时 | 更新项目结构部分 |
| `README.md` | 新增工具或功能时 | 更新工具列表与使用说明 |
| `AGENTS.md` | 工作流或规范有变化时 | 更新对应章节 |

---

## 开发日志格式（`docs/DEV_LOG.md`）

在文件顶部插入（最新在前）：

```markdown
## YYYY-MM-DD — <操作者>

**Changes:**
- <每个逻辑变更一条>

**Files modified:**
- `path/to/file` — 一句话说明
```

操作者填写：`Claude Code`、`Codex`、`Cursor` 或 `xujing`。

---

## 项目概览

SciMath 是 xujing 独立开发的 Dify 数学计算插件，提供数值计算与符号计算两类工具。每个工具由两个文件组成：

- `tools/<name>.py` — Python 实现，核心为 `Tool._invoke()`
- `tools/<name>.yaml` — Dify 工具 schema（参数、标签、描述）

所有工具在 `provider/maths.yaml` 的 `tools:` 下注册。

完整架构说明见 `CLAUDE.md`。

---

## AI 协作协议

1. 开始前先阅读 `docs/DEV_LOG.md`，了解上次的改动内容。
2. 提交时写清楚变更说明。
3. 结束前追加 DEV_LOG 条目。

---

## 新增工具清单

- [ ] `tools/<name>.py` — 实现 `class <Name>Tool(Tool)` 与 `_invoke()`
- [ ] `tools/<name>.yaml` — 定义 schema（description、identity、parameters）
- [ ] 在 `provider/maths.yaml` 的 `tools:` 下注册
- [ ] 更新 `docs/DEV_LOG.md`
- [ ] 更新 `CLAUDE.md` 项目结构部分
- [ ] 更新 `README.md` 工具列表

---

## 代码规范

- 依赖通过 `uv` 管理（`pyproject.toml`）
- 所有工具同时返回 `create_text_message`（人类可读 + LaTeX）和 `create_json_message`（结构化）
- 共享工具函数放在 `tools/sympy_utils.py`（或类似的 `tools/*_utils.py`）
- 注释只写 WHY，不写 WHAT
