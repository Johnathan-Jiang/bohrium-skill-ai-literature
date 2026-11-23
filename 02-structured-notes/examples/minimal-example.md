# 最小调用示例（文献总结与结构化笔记）

> 本文件为**示意示例**，不是正式案例结果。

## 输入

- `task.md`：对 `/input/paper.pdf` 做章节级结构化笔记 + 论文卡片，锚点回链。
- `case.json`：`{"case_id": "demo-002"}`

## 示意输出（片段）

```json
{
  "case_id": "demo-002",
  "status": "success",
  "paper_card": {"research_question": "（示例占位）", "data": "（示例占位）", "methods": "（示例占位）", "findings": "（示例占位）", "limitations": "（示例占位）", "premises": "（示例占位）"},
  "sections": [
    {"section": "Methods", "pages": "p3-p5", "purpose": "（示例占位）", "content": "（示例占位）", "link_next": "（示例占位）"}
  ],
  "knowledge_points": [{"id": "K1", "statement": "（示例占位）", "anchor": "p4 ¶2", "quote": "（示例占位）"}]
}
```

> 字段内容为占位示例，不代表任何真实论文。
