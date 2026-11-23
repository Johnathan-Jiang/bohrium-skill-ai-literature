# Nanopublication Skill

把论文关键结论拆成可独立判断真假的科研断言，绑定最小证据片段与来源，输出可机器读取的结构。

## 文件结构

- `SKILL.md` — Skill 本体。
- `scripts/validate_nanopub.py` — 断言结构校验脚本。
- `references/nanopub-schema.md` — 断言字段、关系受控词表、证据等级。
- `examples/minimal-example.md` — 最小调用示例（标注为示例）。

## 用法

Agent 加载 `SKILL.md`，定位结论段 → 拆断言 → 绑证据 → 补来源元数据 → 导出 JSON。

## 校验脚本

```bash
python3 scripts/validate_nanopub.py result.json
```

检查项：断言必需字段、证据定位、证据等级受控词表。退出码 0=通过。

## 输出

`result.json` 含：`assertions`（id/assertion/subject/relation/object/condition/polarity/evidence/evidence_level/confidence_basis）、`sources`、`uncertainty`、`change_records`。

## 依赖

Python 3 标准库。

## 限制

找不到支撑片段的断言标 `unsupported`；证据与断言冲突时保留双方并说明；不编造来源元数据（缺项标 `unknown`）。
