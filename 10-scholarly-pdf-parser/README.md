# scholarly-pdf-parser

把科研论文 PDF 解析成**可追溯的结构化结果**：按正确阅读顺序抽取正文、章节层级、表格、公式、图与参考文献，每一项都带 **页码 + 区块坐标（bbox）证据**；读不出来的地方如实标注，不猜补。

## 依赖

- Python ≥ 3.9
- `PyMuPDF`（核心，`pip install PyMuPDF`）
- 扫描版 PDF 需 OCR 工具（平台 `ocr-tool` / `tesseract`）

## 调用步骤

```bash
# 1) 检查 PDF（是否有文字层、是否加密）
python3 scripts/parse_paper.py --inspect paper.pdf

# 2) 解析
python3 scripts/parse_paper.py --pdf paper.pdf --out parsed.json
```

## 输入 / 输出

- 输入：一个科研论文 PDF（文字层或扫描版）。
- 输出 `parsed.json`（canonical 结构）：
  - `document.title / authors / affiliations / abstract`
  - `document.sections[]`（`heading`、`level`、`content_blocks[]`，每块带 `page`/`bbox`）
  - `document.tables[]`（`caption`、`rows`、`page`/`bbox`）
  - `document.figures[]`、`document.formulas[]`、`document.references[]`
  - `document.reading_order[]`、`document.headers_footers[]`
  - `uncertainty[]`、`status`、`sources`
- 平台运行时按 `case.json` 的 `output_contract` 映射上述字段，最终写入
  `result.json`（含 `case_id`）。

## 关键方法

1. **版式分类与阅读顺序**：按文本块宽度区分全宽块（标题、摘要、跨栏图表）与
   栏内块，双栏页先按栏（左栏自上而下、再右栏）再按纵坐标，全宽块按纵坐标
   插回，避免串栏错行、丢段。
2. **页眉页脚分离**：靠近页边 + 短行 +（跨页重复文本或纯页码）才判为页眉页脚，
   首页标题不会被误删。
3. **章节层级**：编号（`3.2`、`3.2 Method`）+ 常用标题词（Abstract / Introduction /
   引言 / 方法 / 结果 / 结论 / 参考文献…）+ 短行加粗三类信号识别。
4. **表格**：`page.find_tables()` 抽行列；跨页/合并单元格保留 bbox 并标记
   `needs_manual_check`。
5. **公式**：启发式（含多个数学符号的短行）+ 页码/bbox 证据，不做臆造修复。
6. **证据链**：每个字段都带 `page`/`bbox`，评审可回到原文定位复核。

## 适用场景 / 限制

- 适用：单栏/双栏、中英文、文字层 PDF；扫描版走 OCR 路径。
- 限制：合并单元格表格、密集公式、扫描低清页仍标为不确定；不做图表/公式的
  科学含义理解，只做结构提取与定位。

## 异常处理

- 加密/损坏 PDF → `status: failed` + 原因，不编造。
- 无文字层 → OCR；OCR 也失败 → `partial` + 每页原因。
- 栏界不明 → 用页中线切分并标 `uncertain`。
- 字体乱码/缺字形 → 保留原文 + `uncertainty` 条目。
- 元数据缺失（DOI/年份）→ `null` + 原因。

## 最小调用示例（示意输出，非正式案例）

输入一个 2 页双栏样例 PDF（`example/sample_paper.pdf`）：

```bash
python3 scripts/parse_paper.py --pdf example/sample_paper.pdf --out example/parsed.json
```

示意输出（节选）：

```json
{
  "status": "success",
  "document": {
    "title": "A Sample Two-Column Paper on Reading Order",
    "authors": ["Alice Author, Bob Author"],
    "sections": [
      {"heading": "Abstract", "level": 1, "page": 1, "bbox": [40.0, 160.0, 104.7, 176.5],
       "content_blocks": [{"text": "This paper describes a method ...", "page": 1, "bbox": [40.0, 188.0, 524.6, 218.5]}]}
    ],
    "references": [{"text": "[1] Author A. Title One. Journal of Parsing, 2026.", "page": 2, "bbox": [40.0, 85.0, 320.0, 100.0]}]
  },
  "uncertainty": []
}
```

> 以上 `example/` 内容为**示意示例**，用于说明接口与流程，不是正式案例答案。

## 自查方法

1. 每条结果都有 `page`（和可用时的 `bbox`）。
2. `result.json` 含 `case_id` 与全部 `output_contract` 字段。
3. 抽查 3 条结果，对照渲染页确认原文一致。
4. `status`/`uncertainty` 与事实一致，未完成处明确标注。
