# 方法与实验章节写作 Skill

把散落的实验记录（代码/配置/日志/数据说明）整理成可执行、可复现的方法与实验章节，参数逐条对齐来源。

## 文件结构

- `SKILL.md` — Skill 本体。
- `scripts/check_parameters.py` — 参数来源校验脚本。
- `references/element-checklist.md` — 六类要素清单与参数表模板。
- `examples/minimal-example.md` — 最小调用示例（标注为示例）。

## 用法

Agent 加载 `SKILL.md`，抽要素 → 对齐校验 → 写章节 → 补复现细节 → 找缺口 → 写限制。

## 校验脚本

```bash
python3 scripts/check_parameters.py result.json
```

检查项：参数有来源、状态标注合法、缺口清单可执行。退出码 0=通过。

## 输出

`result.json` 含：`methods_text`、`elements`、`parameters`（值/来源/状态）、`gaps`、`sources`、`uncertainty`、`change_records`。

## 依赖

Python 3 标准库。

## 限制

无来源的数值不补造，列入"待作者确认"；配置冲突并列取值并标注。
