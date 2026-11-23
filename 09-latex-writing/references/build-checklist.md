# LaTeX 错误分类与构建记录模板

## 错误分类（定位到文件+行号+根因）

| 类别 | 常见表现 | 根因/修复 |
|---|---|---|
| 未定义控制序列 | `Undefined control sequence` | 缺宏包/拼写错误 → `\usepackage` 或改拼写 |
| 缺失环境 | `Missing \end{...}` | 环境未闭合/嵌套错误 |
| 引用未解析 | `Citation 'x' undefined` / `Reference ... undefined` | 未跑 biber/bibtex 或键不匹配 |
| 缺字体 | fontspec 报错 | 换可用字体或装字体 |
| 编码问题 | 中文乱码/编译失败 | 用 xelatex/UTF-8，检查 inputenc |
| 数学模式错误 | `Missing $ inserted` | 公式未进数学环境 |

## 编译轮次（记录实际命令）

- 带 bib：`xelatex → biber/bibtex → xelatex → xelatex`
- 无 bib：`xelatex → xelatex`（至少两轮解析交叉引用）

## 构建记录模板

```json
{
  "engine": "xelatex",
  "passes": ["xelatex", "biber", "xelatex", "xelatex"],
  "exit_code": 0,
  "template": {"class": "acmart", "texlive": "TeX Live 2024"},
  "packages": ["booktabs", "amsmath"],
  "fonts": ["..."],
  "errors_fixed": [{"file": "...", "line": 0, "error": "...", "root_cause": "...", "fix": "..."}]
}
```

## 可复现原则

记录模板版本、宏包与字体版本、编译命令与轮次；他人据此能得到同一产物。
