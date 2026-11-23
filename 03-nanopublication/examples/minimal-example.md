# 最小调用示例（Nanopublication）

> 本文件为**示意示例**，不是正式案例结果。

## 输入

- `task.md`：将 `/input/paper.pdf` 结论段的结论拆成断言并绑定证据，导出 JSON。
- `case.json`：`{"case_id": "demo-003"}`

## 示意输出（片段）

```json
{
  "case_id": "demo-003",
  "status": "success",
  "assertions": [
    {"id": "A1", "assertion": "（示例占位：单主体、单关系、含条件）", "subject": "（示例占位）", "relation": "outperforms", "object": "（示例占位）", "condition": "（示例占位）", "polarity": "positive", "evidence": {"quote": "（示例占位）", "locator": "p5 ¶3"}, "evidence_level": "direct", "confidence_basis": "原句直接支撑"}
  ]
}
```

> 断言内容为占位示例，不代表任何真实论文。
