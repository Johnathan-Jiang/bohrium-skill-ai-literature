# Nanopublication 字段与受控词表

## 断言字段（每条一个可判断真假的命题）

| 字段 | 含义 | 必填 |
|---|---|---|
| `id` | 稳定标识（A1…） | 是 |
| `assertion` | 完整断言句（含条件与限定） | 是 |
| `subject` | 主体 | 是 |
| `relation` | 关系（受控词表见下） | 是 |
| `object` | 客体 | 是 |
| `condition` | 适用条件/范围/区间 | 是 |
| `polarity` | `positive` / `negative` | 是 |
| `evidence.quote` | 支撑断言的最小原文片段 | 是 |
| `evidence.locator` | 原文位置（页码/段落/图表/公式） | 是 |
| `evidence_level` | `direct` / `paraphrase` / `inferred` | 是 |
| `confidence_basis` | 置信度依据 | 否 |

## 关系受控词表（示例，可扩展但须显式声明）

- 因果/机制：`causes` `inhibits` `mediates` `depends_on`
- 比较：`outperforms` `underperforms` `equals`
- 属性：`has_property` `measured_as` `belongs_to`
- 位置/来源：`located_in` `derived_from`

## 拆解与证据规则

1. 一条断言只表达一个命题；复合句拆开，条件保留在断言内。
2. `evidence_level`：`direct`=原句直接支撑；`paraphrase`=原文转述；`inferred`=推断（须在 `confidence_basis` 说明）。
3. 找不到支撑片段：标 `unsupported`，不硬凑、不把推测当证据。
4. 来源元数据（作者/年份/版本/DOI）原文有则记，无则标 `unknown`，不编造。

## 导出

JSON 为规范形态；如需 RDF/N-Quads，把断言映射为 `<assertion> <relation> <object>`，证据与来源作为限定（见 SKILL.md 输出结构）。
