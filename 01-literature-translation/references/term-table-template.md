# 术语表模板（文献翻译）

术语表是翻译过程中的**权威约束**：每次翻译前检索，翻译后回查，全篇锁定同一译名。

## 格式（JSON）

```json
{
  "version": "1",
  "locked": true,
  "entries": [
    {
      "id": "T1",
      "source_term": "solid electrolyte interphase",
      "abbreviation": "SEI",
      "target_term": "固态电解质界面",
      "context": ["electrochemistry"],
      "occurrences": ["p2 摘要", "p5 正文", "p9 结论"],
      "note": ""
    }
  ]
}
```

## 字段说明

| 字段 | 说明 |
|---|---|
| `id` | 稳定标识，翻译段引用用 `T1` |
| `source_term` | 原文术语（规范书写） |
| `abbreviation` | 缩写（如有） |
| `target_term` | 唯一译名 |
| `context` | 语境/学科限定；同词不同语境不同译法时必须填写 |
| `occurrences` | 出现位置清单（页码+位置），用于译法统一验证 |
| `note` | 译法依据或例外说明 |

## 锁定规则

1. 同一 `source_term`（同一语境）全篇只能有一个 `target_term`。
2. 缩写首次出现给"全称（缩写）"，之后只用缩写。
3. 标题、摘要、正文、图注、结论五处译名必须一致。
4. 同词多义：必须新增条目并写明 `context`，不允许无理由漂移。
5. 术语表内部冲突按"标题 → 摘要 → 正文首次出现"优先级裁决，并记录决定。
