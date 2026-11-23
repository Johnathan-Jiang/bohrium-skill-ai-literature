# 最小调用示例（文献翻译）

> 本文件为**示意示例**，不是正式案例结果；正式案例与白板由平台提供。

## 输入

- `task.md`：将 `/input/paper.pdf` 第 2–4 页的方法节翻译为中文，术语锁定，输出双语对照。
- `case.json`：`{"case_id": "demo-001"}`

## 调用方式（评测环境内）

1. 读 `task.md`、`case.json`，用 `pdftotext paper.pdf` 读真实文本层。
2. 抽术语表 → 切段 → 逐段翻译 → 核验 → 输出 `result.json`。

## 示意输出（片段）

```json
{
  "case_id": "demo-001",
  "status": "success",
  "term_table": [
    {"source_term": "solid electrolyte interphase", "abbreviation": "SEI", "target_term": "固态电解质界面", "occurrences": ["p2 摘要"]}
  ],
  "segments": [
    {"id": "S1", "page": "p2", "locator": "p2 ¶1", "source": "The SEI forms during initial cycling.", "translation": "固态电解质界面在初始循环期间形成。", "basis": "T1 复用；因果/时间关系保留", "status": "ok"}
  ],
  "verification": [{"check": "段落总数一致", "result": "pass", "detail": "12==12"}]
}
```

> 上述译文为示例占位，不代表任何真实论文内容。
