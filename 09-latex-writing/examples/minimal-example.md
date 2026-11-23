# 最小调用示例（LaTeX 写作与编译）

> 本文件为**示意示例**，不是正式案例结果。

## 输入

- `task.md`：修改 `/input/tex/main.tex`（模板 acmart），修公式与引用并编译通过。
- `case.json`：`{"case_id": "demo-009"}`

## 示意输出（片段）

```json
{
  "case_id": "demo-009",
  "status": "success",
  "build": {"engine": "xelatex", "passes": ["xelatex","biber","xelatex","xelatex"], "exit_code": 0},
  "errors_fixed": [{"file": "main.tex", "line": 34, "error": "Undefined control sequence", "root_cause": "缺宏包", "fix": "\\usepackage{...}"}],
  "deliverables": {"source": "main.tex", "pdf": "main.pdf"}
}
```

> 源码与报错为占位示例，不代表任何真实工程。
