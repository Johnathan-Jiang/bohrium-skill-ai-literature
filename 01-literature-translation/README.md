# 文献翻译 Skill

把真实科研论文（PDF/文本）翻译成可核验的双语对照结果，保证术语一致、段落完整、关系准确、译文可回原文。

## 文件结构

- `SKILL.md` — Skill 本体：触发条件、工作流、四条硬规则、输出契约、异常处理、自查清单。
- `scripts/verify_translation.py` — 译文校验脚本。
- `references/term-table-template.md` — 术语表格式与锁定规则。
- `examples/minimal-example.md` — 最小调用示例（标注为示例，不冒充正式案例结果）。

## 用法

Agent 加载 `SKILL.md` 后，按运行契约读取 `/input/task.md`、`/input/case.json` 与 `resources.yaml` 指向的 PDF，产出双语对照结果到 `/app/output/result.json`。

## 校验脚本

```bash
python3 scripts/verify_translation.py result.json
```

检查项：术语唯一译名、段号—译文一一对应、数字保留、文献编号保留。退出码 0=通过。

## 输出

`result.json` 含：`case_id`、`status`、`term_table`、`segments`（段号/原文/译文/依据/位置）、`verification`、`sources`、`uncertainty`、`change_records`。

## 依赖

Python 3 标准库；读取 PDF 文本层依赖运行时提供的 `pdftotext`/`pdf-text-tool`。

## 限制

不处理扫描件 OCR（无文本层时如实标注）；公式/表格为图片时保留原文符号并标 `[待确认]`，不编造内容。
