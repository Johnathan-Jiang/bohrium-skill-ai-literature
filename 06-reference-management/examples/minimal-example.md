# 最小调用示例（参考文献与引用管理）

> 本文件为**示意示例**，不是正式案例结果。

## 输入

- `task.md`：对 `/input/manuscript.md` 与 `/input/library.bib` 做引用定位、编号更新、去重与核验。
- `case.json`：`{"case_id": "demo-006"}`

## 示意输出（片段）

```json
{
  "case_id": "demo-006",
  "status": "success",
  "citation_map": [{"claim": "（示例占位）", "citation": "[3]", "source_id": "LIB-004", "match_basis": "DOI 一致"}],
  "dedup": [{"merged_into": "LIB-004", "merged": ["LIB-011"], "reason": "预印本与正式版同文"}],
  "verification": [{"citation": "[2]", "check": "元数据", "result": "pass"}]
}
```

> 引用与文献条目为占位示例，不代表任何真实稿件。
