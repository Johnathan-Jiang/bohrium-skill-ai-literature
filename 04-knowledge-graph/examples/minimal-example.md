# 最小调用示例（文献知识图谱）

> 本文件为**示意示例**，不是正式案例结果。

## 输入

- `task.md`：从 `/input/papers/` 两篇论文抽取实体/关系，构建图谱并回答查询。
- `case.json`：`{"case_id": "demo-004"}`

## 示意输出（片段）

```json
{
  "case_id": "demo-004",
  "status": "success",
  "nodes": [{"id": "N1", "type": "method", "label": "（示例占位）", "mentions": ["p2 ¶1"], "quote": "（示例占位）", "voice": "author"}],
  "edges": [{"id": "E1", "source": "N1", "target": "N2", "relation": "improves", "condition": "（示例占位）", "evidence": {"quote": "（示例占位）", "locator": "p4 ¶2"}, "evidence_level": "direct"}],
  "query_results": [{"query": "（示例占位）", "answer": "（示例占位）", "nodes": ["N1"], "evidence_locators": ["p4 ¶2"]}]
}
```

> 实体/关系/查询为占位示例，不代表任何真实论文。
