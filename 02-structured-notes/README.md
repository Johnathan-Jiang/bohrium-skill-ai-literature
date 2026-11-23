# 文献总结与结构化笔记 Skill

把真实论文整理成跟随论文自身结构、保留证据与限制条件的可复用结构化笔记（章节总结 + 论文卡片 + 知识点 + 锚点回链）。

## 文件结构

- `SKILL.md` — Skill 本体。
- `scripts/validate_notes.py` — 笔记结构校验脚本。
- `references/note-schema.md` — 论文卡片/章节/知识点字段与锚点约定。
- `examples/minimal-example.md` — 最小调用示例（标注为示例）。

## 用法

Agent 加载 `SKILL.md`，按论文原有章节建立骨架，逐章提炼，输出字段化笔记与锚点表到 `/app/output/result.json`。

## 校验脚本

```bash
python3 scripts/validate_notes.py result.json
```

检查项：论文卡片字段齐全、知识点有锚点+引文、章节有页码。退出码 0=通过。

## 输出

`result.json` 含：`paper_card`、`sections`、`knowledge_points`、`sources`、`uncertainty`、`change_records`。

## 依赖

Python 3 标准库；读取 PDF 依赖运行时工具。

## 限制

扫描件/权限受限文档如实标注；不套用通用摘要模板，不臆造论文未报告的内容。
