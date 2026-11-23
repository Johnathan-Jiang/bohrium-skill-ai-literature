# 最小调用示例（方法与实验章节写作）

> 本文件为**示意示例**，不是正式案例结果。

## 输入

- `task.md`：基于 `/input/code/`、`config.yaml`、`train.log` 写方法与实验章节。
- `case.json`：`{"case_id": "demo-008"}`

## 示意输出（片段）

```json
{
  "case_id": "demo-008",
  "status": "success",
  "methods_text": "（示例占位）",
  "parameters": [{"name": "learning_rate", "value": "1e-4", "source": "config.yaml L12", "status": "confirmed"}],
  "gaps": [{"item": "随机种子", "missing": "未记录", "action": "请作者补充"}]
}
```

> 参数与方法为占位示例，不代表任何真实实验。
