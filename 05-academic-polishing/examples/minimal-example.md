# 最小调用示例（学术语言润色）

> 本文件为**示意示例**，不是正式案例结果。

## 输入

- `task.md`：润色 `/input/draft.md` 摘要段，术语统一，逐句给修改说明。
- `case.json`：`{"case_id": "demo-005"}`

## 示意输出（片段）

```json
{
  "case_id": "demo-005",
  "status": "success",
  "polished_text": "（示例占位：润色后文本）",
  "edits": [
    {"id": "E1", "locator": "¶1 第2句", "original": "（示例占位）", "revised": "（示例占位）", "type": "grammar", "reason": "主谓一致"}
  ]
}
```

> 润色文本为占位示例，不代表任何真实稿件。
