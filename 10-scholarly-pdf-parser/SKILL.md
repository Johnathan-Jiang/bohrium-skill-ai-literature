---
name: scholarly-pdf-parser
description: Parse a scientific-paper PDF into a traceable structured result — correct multi-column reading order, section hierarchy, tables, formulas, figures and references, each with page/block evidence.
---

# Scholarly PDF parser

Turn a research-paper PDF into a structured, machine-usable result in which every
extracted item carries its source **page and block**, and unreadable content is
reported honestly instead of being guessed.

## Scope and limits

- Best for born-digital (text-layer) journal PDFs: single- or double-column, English or Chinese.
- Treated as uncertain (still extracted, but flagged): merged-cell tables, scanned
  (image-only) pages, dense formulas, and hyphenated cross-page words.
- Not required here: understanding the scientific *meaning* of figures or formulas;
  only their structural extraction and source location.

## Inputs at runtime

- `/input/case.json` — task description, material path(s), and the `output_contract`
  the result must satisfy.
- `/input/task.md` — this challenge statement.
- The actual PDF file(s) named by `case.json`. Read the real file; do not trust a
  filename label.
- `environment/resources.yaml` — preinstalled tool names and paths
  (pdf-text-tool, pdf-render-tool, ocr-tool, office-renderer, font-discovery, …).
  Read it once and record the paths you actually used.

## Workflow (in order)

### 1. Read the contract first

Open `/input/case.json` and `/input/task.md`. Record:

- `case_id`;
- every field named in `output_contract`;
- the material file path(s);
- any explicit format or language requirement.

If `output_contract` is absent, use the canonical structure emitted by
`scripts/parse_paper.py` and state that choice in `result.json`.

### 2. Locate and inspect the PDF

- Confirm the file exists and opens. A missing, corrupt, or encrypted file is
  `status: failed` with the reason — never fabricate content.
- Determine whether the PDF has a text layer:

```bash
python3 scripts/parse_paper.py --inspect /path/paper.pdf
```

### 3. Parse a text-layer PDF

```bash
python3 scripts/parse_paper.py --pdf /path/paper.pdf --out work/parsed.json
```

The script:

- extracts text per page and block with PyMuPDF;
- detects single- vs double-column layout per page and rebuilds reading order;
- separates running headers/footers from body text;
- detects section headings and builds the section hierarchy;
- extracts tables (`page.find_tables`), figure captions, and reference items;
- attaches `page` and `bbox` evidence to every item;
- reports uncertain parts under `uncertainty`.

Then inspect `work/parsed.json` and fix obvious reading-order mistakes **using the
page/bbox evidence** — never by guessing what the text should say.

### 4. Parse a scanned / image-only PDF

If step 2 shows no text layer:

- render pages with `pdf-render-tool` (or `pdftoppm -r 300`);
- OCR with `ocr-tool`, preferring the language from `case.json`, else `eng` then `chi_sim`;
- re-run the layout logic on the OCR boxes;
- mark the result `ocr: true` and attach `confidence` where the OCR provides it;
- do not present OCR text as exact: record low-confidence items under `uncertainty`.

### 5. Formulas and tables

- Tables: prefer the script's table extraction. For merged or cross-page tables keep
  the raw bbox and mark `needs_manual_check`.
- Formulas: extract the raw line text plus `page`/`bbox`. Use a LaTeX/MathML
  conversion only if one is available; never invent symbols to "repair" a formula —
  mark it `uncertain` instead.

### 6. Write `result.json`

Write `/app/output/result.json` (and keep an editable copy under `/app/output`) with:

- `case_id`;
- every field the case's `output_contract` requires;
- for each field, the extracted value, or an explicit `null` / `missing` plus the reason;
- `evidence` (page + bbox or block id) for each extracted item;
- `status`: `success` | `partial` | `failed`;
- `uncertainty`: items and why they are uncertain;
- `sources`: the PDF path and tool versions actually used.

A missing item is reported as missing — it is never filled with a guess.

### 7. Done

The deliverable is the parsed, traceable `result.json` plus any structured
files the case's `output_contract` requires. There is no slide or Office
export in this challenge; only produce one if the case explicitly asks for it.

## Canonical output structure

`scripts/parse_paper.py` emits (map this onto `case.json.output_contract`):

- `document.title`, `document.authors`, `document.affiliations`, `document.abstract`
- `document.sections[]` — `heading`, `level`, `content_blocks[]` with `text`, `page`, `bbox`
- `document.tables[]` — `caption`, `rows`, `page`, `bbox`
- `document.figures[]` — `caption`, `page`, `bbox`
- `document.formulas[]` — `text`/`latex`, `page`, `bbox`
- `document.references[]` — `text`, `page`
- `document.reading_order[]`, `document.headers_footers[]`, `document.footnotes[]`
- `uncertainty[]`, `status`, `sources`

## Error handling and edge cases

- Encrypted / corrupt PDF → `status: failed`, reason recorded, nothing fabricated.
- No text layer → OCR path; if OCR also fails → `partial` with per-page reasons.
- Ambiguous column boundary → use gap-based split; mark `uncertain`.
- Garbled font / missing glyphs → keep raw text, add an `uncertainty` entry.
- Missing metadata (DOI, year) → `null` + reason, never invented.
- Empty required field → `null` + `missing_reason`, and `status: partial`.

## Self-check before finishing

1. Every extracted item has `page` (and `bbox` when available).
2. `result.json` has `case_id` and every `output_contract` field.
3. No field contains content that is not in the PDF (spot-check 3 items against the rendered page).
4. `status` and `uncertainty` reflect reality; partial work is labelled partial.
5. Editable outputs have a rendered preview beside them.
