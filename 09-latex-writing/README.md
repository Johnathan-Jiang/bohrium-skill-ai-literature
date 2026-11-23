# LaTeX 写作与编译 Skill

在指定模板下修改/编写 LaTeX 源码并编译通过，报错定位到文件+行号+根因，交付可编辑源码与真实编译产物。

## 文件结构

- `SKILL.md` — Skill 本体。
- `scripts/latex_build.py` — 编译闭环脚本。
- `references/build-checklist.md` — 错误分类与构建记录模板。
- `examples/minimal-example.md` — 最小调用示例（标注为示例）。

## 用法

Agent 加载 `SKILL.md`，读工程 → 改源码 → 编译 → 定位第一条错误 → 修复 → 复编译 → 验证产物。

## 编译脚本

```bash
python3 scripts/latex_build.py main.tex
# 可指定引擎与 bib 工具：
LATEX_ENGINE=pdflatex LATEX_BIB=bibtex python3 scripts/latex_build.py main.tex
```

存在 `.bbl` 时自动跑「引擎 → biber → 引擎 → 引擎」轮次；失败时定位第一条错误到行号。退出码 0=编译通过。

## 输出

`result.json` 含：`build`（引擎/轮次/退出码）、`errors_fixed`、`deliverables`、`template`、`sources`、`uncertainty`、`change_records`。

## 依赖

Python 3 标准库 + 系统 TeX 发行版（`xelatex`/`pdflatex`、`biber`/`bibtex`）。

## 限制

缺宏包/缺字体时尝试可用替代，仍缺则 `status=partial` 并列出缺失项；交付物始终是可编辑源码 + 真实 PDF，而非截图。
