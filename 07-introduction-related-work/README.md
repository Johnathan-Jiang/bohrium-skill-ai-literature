# 引言与相关工作写作 Skill

撰写可进入论文的引言与相关工作：研究背景、相关工作、研究空白、贡献四部分齐全，引用落在具体论断，空白由已引文献缺口推出。

## 文件结构

- `SKILL.md` — Skill 本体。
- `scripts/check_evidence.py` — 证据表完整性校验脚本。
- `references/evidence-table.md` — 论断—引用—来源证据表模板。
- `examples/minimal-example.md` — 最小调用示例（标注为示例）。

## 用法

Agent 加载 `SKILL.md`，先建证据表，再按四部分写作，后核验引用覆盖与贡献对照。

## 校验脚本

```bash
python3 scripts/check_evidence.py result.json
```

检查项：正文每条引用在证据表登记、研究空白有依据。退出码 0=通过。

## 输出

`result.json` 含：`introduction_text`、`evidence_table`、`gap_derivation`、`contribution_mapping`、`sources`、`uncertainty`、`change_records`。

## 依赖

Python 3 标准库。

## 限制

文献库为空/引用查不到原文时只写有证据支撑的部分并标"材料不足"；无文献支撑的空白显式标为"作者判断"。
