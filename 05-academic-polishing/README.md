# 学术语言润色 Skill

对学术文本做逐句润色，交付"润色后完整文本 + 逐句修改说明"，保证限定强度、数据、单位、引用编号不改变。

## 文件结构

- `SKILL.md` — Skill 本体。
- `scripts/check_semantics.py` — 语义守恒校验脚本。
- `references/edit-type-taxonomy.md` — 修改类型受控词表与语义守恒清单。
- `examples/minimal-example.md` — 最小调用示例（标注为示例）。

## 用法

Agent 加载 `SKILL.md`，逐句最小编辑，保留原意与限定，输出润色后全文 + 修改清单 + 术语表。

## 校验脚本

```bash
python3 scripts/check_semantics.py result.json
```

检查项：数字、文献编号、图表指向在原文与改文间是否丢失。退出码 0=通过（无丢失）。

## 输出

`result.json` 含：`polished_text`、`edits`（原文/改文/类型/理由）、`term_table`、`sources`、`uncertainty`、`change_records`。

## 依赖

Python 3 标准库。

## 限制

仅做语言层面润色，不改变语义；目标文体不明时按通用学术文体处理并显式标注假设。
