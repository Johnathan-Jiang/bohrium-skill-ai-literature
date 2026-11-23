---
name: latex-writing-compilation
description: 在指定模板下修改/编写 LaTeX 源码并编译通过，定位报错到文件行号与根因，交付可编辑源码与真实编译产物。用于源码结构、公式、表格、引用、模板适配、编译错误修复与可重复构建等任务；需要"编译得通、改得对、交得可用、复现得了"时触发。
---

# LaTeX 写作与编译：源码可编辑、编译闭环、可复现构建

交付能在指定模板与 TeX 发行版下编译通过的 `.tex` 成果，报错定位到具体文件/行号/根因，保留可编辑源码与真实编译产物。

## 运行契约

- 输入：`/input/task.md`、`/input/case.json`、`resources.yaml` 及 LaTeX 工程（主文件、模板类、bib、图片）。
- 工作目录 `/app/work`；最终结果写入 `/app/output/`。
- 先读真实工程；缺宏包、缺字体、报错级联、模板类缺失、权限不足等如实记录。
- `/app/output/result.json` 必须包含：`case_id`、`status`、`output_contract` 全部字段、`sources`、`uncertainty`、`change_records`。
- 预算 64 次模型请求 / 900 秒：先读工程，再改、编译、定位、修复，循环直到通过或明确卡点。
- 交付物为**可编辑源码**（非截图/片段），附真实编译产物 PDF（及必要的日志）。

## 工作流

1. **识别边界**：读 `task.md`/`case.json`，确认要改动的内容、模板、TeX 发行版、编译命令与轮次。
2. **读工程**：定位主文件、`\documentclass`、导言区宏包加载顺序、`\input/\include` 子文件、`.bib`、`.cls/.sty`。
3. **改源码**：按任务要求改公式符号/编号、表格数值/列宽、交叉引用、参考文献、版式与模板必填项，既符合原文意图又符合模板要求。
4. **编译**：运行 `python3 scripts/latex_build.py main.tex`（引擎/轮次可经 `LATEX_ENGINE`、`LATEX_BIB` 环境变量指定），按模板要求完成编译轮次。
5. **定位报错**：读到**第一条**错误，定位到文件+行号+根因（未定义宏/缺宏包/缺字体/缺失 `\end`/引用未解析/编码等），不停在错误信息表面；级联错误按根因处理；错误分类与构建记录格式见 `references/build-checklist.md`。
6. **修复并复编译**：最小化修复，重复编译直到通过；记录每次改动与原因。
7. **验证**：检查编译产物中公式、表格、交叉引用、参考文献、版式与意图一致。
8. **输出**：可编辑源码 + 编译产物 PDF + 构建记录（模板/版本/宏包/字体/命令），写入 `result.json`。

## 四条硬规则

### 编译得通
- 在指定模板与 TeX 发行版下按预期轮次编译通过；报错定位到文件、行号与根因。

### 改得对
- 公式符号与编号、表格数值与列宽、交叉引用与参考文献、版式与模板必填项既符合原文意图又符合模板要求。

### 交得可用
- 交付结构清楚、可继续编辑和可维护的源码，而非把 PDF/截图/无法编译的片段当结果。

### 复现得了
- 记录模板版本、宏包与字体版本、编译命令与轮次，他人能据此得到同一产物。

## 输出结构

`/app/output/result.json`（合并 task.md 的 `output_contract`）：

```json
{
  "case_id": "...",
  "status": "success|partial|unable",
  "build": {"engine": "xelatex", "passes": ["xelatex","biber","xelatex","xelatex"], "exit_code": 0},
  "errors_fixed": [{"file": "main.tex", "line": 34, "error": "Undefined control sequence \\foo", "root_cause": "缺少宏包", "fix": "\\usepackage{...}"}],
  "deliverables": {"source": "...", "pdf": "...", "log": "..."},
  "template": {"class": "...", "packages": [...], "fonts": [...], "texlive_version": "..."},
  "sources": [...],
  "uncertainty": [{"item": "...", "issue": "缺字体/宏包", "action": "记录并尝试替代，仍缺则标注"}],
  "change_records": [...]
}
```

## 异常处理

- 缺宏包/缺字体：记录并尝试用可用替代；仍缺则 `status="partial"`，列出缺失项与安装命令建议。
- 报错级联：定位第一条错误与根因，不逐个修表象错误。
- 模板类文件缺失：`status="unable"` 或 `partial`，说明缺哪个类文件。
- 权限不足/无法写入或编译：说明原因，交付已完成的源码改动。
- 引用未解析：确认 bib 文件与 `\cite` 键对应，跑足 biber/bibtex 轮次。

## 自查清单

1. 是否在指定模板下编译通过，报错是否定位到文件+行号+根因？
2. 公式/表格/交叉引用/参考文献/版式是否与意图一致？
3. 交付物是否是可编辑源码 + 真实 PDF，而非截图？
4. 是否记录模板/版本/宏包/字体/编译命令，可复现？
5. 每次改动是否有记录与理由？
6. `result.json` 是否字段齐全、状态诚实？

最小调用示例见 `examples/minimal-example.md`（标注为示例）。
