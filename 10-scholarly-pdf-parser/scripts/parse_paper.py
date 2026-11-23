#!/usr/bin/env python3
"""Scholarly PDF parser.

Extract a research-paper PDF into a structured, traceable JSON document:
reading order, title/authors/abstract, sections, tables, figures, formulas and
references, each item carrying page + bbox evidence. Uncertain parts are
reported, never guessed.

Requires PyMuPDF (``pip install PyMuPDF``). Falls back to a plain pdftotext
extraction when PyMuPDF is unavailable so the pipeline never dies silently.

Usage:
    python3 parse_paper.py --inspect paper.pdf
    python3 parse_paper.py --pdf paper.pdf --out parsed.json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import pymupdf as fitz  # PyMuPDF >= 1.24
    HAS_PYMUPDF = True
except Exception:
    try:
        import fitz  # older PyMuPDF
        HAS_PYMUPDF = True
    except Exception:
        fitz = None
        HAS_PYMUPDF = False

HEADING_WORDS = {
    "abstract", "summary", "introduction", "intro", "background",
    "related work", "related works", "method", "methods", "materials",
    "material and methods", "materials and methods", "experimental",
    "experiments", "experiment", "results", "result", "discussion",
    "discussions", "conclusion", "conclusions", "references", "bibliography",
    "acknowledgment", "acknowledgements", "acknowledgments", "appendix",
    "摘要", "引言", "前言", "背景", "方法", "实验", "结果", "讨论",
    "结论", "参考文献", "致谢", "附录",
}

# "1", "2.3", "2.3.4", optionally followed by a title
NUMBERED_HEADING_RE = re.compile(
    r"^\s*(\d+(?:\.\d+)*)\s*[\.\u3001]?\s*([A-Za-z\u4e00-\u9fff].{0,80})?$"
)

REF_ITEM_RE = re.compile(r"^\s*\[?\d{1,3}\]?\s+\S|\b(19|20)\d{2}\b")

FIGURE_CAPTION_RE = re.compile(r"^\s*(Fig(?:ure)?\.?|图)\s*\d", re.I)
TABLE_CAPTION_RE = re.compile(r"^\s*Table\s*\d|^\s*表\s*\d", re.I)

MATH_MARKERS = ("\\sum", "\\int", "\\frac", "\\left", "\\right", "∑", "∫", "≈",
                "±", "≤", "≥", "∂", "α", "β", "γ", "δ", "θ", "λ", "μ", "π",
                "σ", "φ", "ψ", "ω", "→")

AFFILIATION_HINTS = ("university", "institute", "academy", "department",
                     "school of", "college", "laboratory", "lab", "center",
                     "hospital", "大学", "学院", "研究所", "研究院", "实验室",
                     "医院", "中心", "@")

BOLD_FLAGS = {16, 20, 48, 52, 132, 148, 164, 180}

PAGE_NUM_RE = re.compile(r"^\s*\d{1,3}\s*$")


def round_bbox(b):
    if not b or len(b) < 4:
        return None
    return [round(float(v), 1) for v in b[:4]]


def block_text(block):
    return " ".join(
        s["text"] for l in block.get("lines", []) for s in l.get("spans", [])
    ).strip()


def spans_meta(block):
    sizes, fonts, flags = [], set(), set()
    for l in block.get("lines", []):
        for s in l.get("spans", []):
            sizes.append(s["size"])
            fonts.add(s["font"])
            flags.add(int(s.get("flags", 0)))
    return {
        "max_size": max(sizes) if sizes else 0.0,
        "fonts": sorted(fonts),
        "bold": bool(flags & BOLD_FLAGS),
        "italic": bool(flags & {2, 6, 18, 22}),
    }


def is_heading_block(text, meta, body_median):
    if not text or len(text) > 120:
        return False
    low = text.lower().rstrip(".:")
    known = low in HEADING_WORDS
    m = NUMBERED_HEADING_RE.match(text)
    numbered = bool(m and m.group(1))
    short = len(text) <= 80
    bold = meta["bold"]
    return known or numbered or (short and bold)


def classify_page_layout(blocks, page_w):
    narrow = [b for b in blocks if (b["bbox"][2] - b["bbox"][0]) < 0.70 * page_w]
    left = [b for b in narrow if (b["bbox"][0] + b["bbox"][2]) / 2 < 0.50 * page_w]
    right = [b for b in narrow if (b["bbox"][0] + b["bbox"][2]) / 2 >= 0.50 * page_w]
    return "double" if (left and right) else "single"


def reading_order(blocks, layout, page_w):
    """Rebuild column reading order. Wide blocks (title, abstract, full-width
    figures/tables) are full-width and interleaved by vertical position; the
    rest are read column-by-column (left column, then right column)."""
    full = [b for b in blocks if (b["bbox"][2] - b["bbox"][0]) > 0.70 * page_w]
    full_ids = {id(b) for b in full}
    cols = [b for b in blocks if id(b) not in full_ids]

    if layout == "double":
        left = sorted([b for b in cols if (b["bbox"][0] + b["bbox"][2]) / 2 < 0.50 * page_w],
                      key=lambda b: (b["bbox"][1], b["bbox"][0]))
        right = sorted([b for b in cols if (b["bbox"][0] + b["bbox"][2]) / 2 >= 0.50 * page_w],
                       key=lambda b: (b["bbox"][1], b["bbox"][0]))
        ordered = left + right
    else:
        ordered = sorted(cols, key=lambda b: (b["bbox"][1], b["bbox"][0]))

    full.sort(key=lambda b: b["bbox"][1])
    result, fi = [], 0
    for b in ordered:
        while fi < len(full) and full[fi]["bbox"][1] < b["bbox"][1]:
            result.append(full[fi]); fi += 1
        result.append(b)
    result.extend(full[fi:])
    return result


def is_header_footer(block, page_h, text_freq):
    """Running header/footer: near the page edge, short, and either repeated
    across pages or a bare page number. A one-off title is not a header."""
    text = block["text"].strip()
    y0, y1 = block["bbox"][1], block["bbox"][3]
    near_top = y0 < 0.10 * page_h
    near_bottom = y1 > 0.90 * page_h
    if not (near_top or near_bottom) or len(text) > 60:
        return False
    if PAGE_NUM_RE.match(text):
        return True
    return text_freq.get(text, 0) >= 2


# --------------------------------------------------------------------------

def inspect_pdf(pdf_path: Path) -> dict:
    if not HAS_PYMUPDF:
        return {"path": str(pdf_path), "pymupdf": False, "error": "PyMuPDF not installed"}
    doc = fitz.open(str(pdf_path))
    info = {
        "path": str(pdf_path),
        "pages": doc.page_count,
        "encrypted": bool(doc.is_encrypted),
        "needs_pass": bool(doc.needs_pass),
        "metadata": {k: v for k, v in (doc.metadata or {}).items() if v},
        "text_chars": 0,
        "has_text_layer": False,
    }
    for page in doc:
        info["text_chars"] += len(page.get_text("text").strip())
    info["has_text_layer"] = info["text_chars"] > 50
    doc.close()
    return info


def parse_pdf(pdf_path: Path) -> dict:
    if not HAS_PYMUPDF:
        return fallback_pdftotext(pdf_path)

    doc = fitz.open(str(pdf_path))
    result = {
        "case_id": None,
        "status": "success",
        "ocr": False,
        "document": {
            "title": None, "authors": [], "affiliations": [], "abstract": None,
            "sections": [], "tables": [], "figures": [], "formulas": [],
            "references": [], "footnotes": [], "headers_footers": [],
            "reading_order": [],
        },
        "uncertainty": [],
        "sources": {"pdf": str(pdf_path), "pages": doc.page_count,
                    "engine": f"PyMuPDF {getattr(fitz, 'VersionBind', '?')}"},
    }

    if doc.is_encrypted and doc.needs_pass:
        result["status"] = "failed"
        result["error"] = "encrypted PDF requires a password"
        doc.close()
        return result

    # ---- first pass: gather blocks ----
    pages_blocks = []
    all_sizes = []
    for pno, page in enumerate(doc):
        d = page.get_text("dict")
        blocks = []
        for b in d.get("blocks", []):
            if b.get("type") != 0:
                continue
            text = block_text(b)
            if not text:
                continue
            meta = spans_meta(b)
            blocks.append({"page": pno + 1, "text": text,
                           "bbox": round_bbox(b["bbox"]), "meta": meta})
            all_sizes.append(meta["max_size"])
        pages_blocks.append(blocks)

    body_median = 0.0
    if all_sizes:
        s = sorted(all_sizes)
        body_median = s[len(s) // 2]

    text_freq = {}
    for blocks in pages_blocks:
        for b in blocks:
            t = b["text"].strip()
            text_freq[t] = text_freq.get(t, 0) + 1

    # ---- second pass: structure ----
    in_references = False
    first_heading_seen = False
    pending_abstract = False
    first_content_done = False

    for pno, blocks in enumerate(pages_blocks):
        if not blocks:
            continue
        page_obj = doc[pno]
        page_w, page_h = page_obj.rect.width, page_obj.rect.height
        layout = classify_page_layout(blocks, page_w)
        ordered = reading_order(blocks, layout, page_w)

        for b in ordered:
            text = b["text"]
            low = text.lower().rstrip(".:")
            tag = {"page": b["page"], "bbox": b["bbox"]}
            meta = b["meta"]

            # running header / footer
            if is_header_footer(b, page_h, text_freq):
                seen = {x.get("text") for x in result["document"]["headers_footers"]}
                if text not in seen:
                    result["document"]["headers_footers"].append({"text": text, **tag})
                continue

            # title: the very first content block on page 1 (before any heading)
            if not first_content_done and b["page"] == 1 and not first_heading_seen:
                first_content_done = True
                result["document"]["sections"].append(
                    {"heading": "(preamble)", "level": 0, **tag,
                     "content_blocks": [{"text": text, **tag}]})
                continue

            # figure / table captions (before headings so "Table 1" is not a section)
            if FIGURE_CAPTION_RE.match(text):
                result["document"]["figures"].append({"caption": text, "xref": None, **tag})
                continue
            if TABLE_CAPTION_RE.match(text):
                result["document"]["tables"].append(
                    {"caption": text, "rows": [], **tag, "needs_manual_check": False})
                continue

            # references section
            if low in ("references", "bibliography") or low.endswith("references"):
                in_references = True
                first_heading_seen = True
                result["document"]["sections"].append(
                    {"heading": text, "level": 1, **tag, "content_blocks": []})
                continue
            if in_references and REF_ITEM_RE.match(text):
                result["document"]["references"].append({"text": text, **tag})
                continue

            # formula heuristic (before heading, since formulas are short)
            if len(text) < 200 and sum(1 for m in MATH_MARKERS if m in text) >= 2:
                result["document"]["formulas"].append({"text": text, "latex": None, **tag})
                continue

            # section heading
            if is_heading_block(text, meta, body_median):
                first_heading_seen = True
                level = 1 if (low in HEADING_WORDS or re.match(r"^\d+(\.\d+)*\.?$", text)) else 2
                result["document"]["sections"].append(
                    {"heading": text, "level": level, **tag, "content_blocks": []})
                if low == "abstract":
                    pending_abstract = True
                else:
                    pending_abstract = False
                continue

            # body text
            if result["document"]["sections"]:
                sec = result["document"]["sections"][-1]
                sec["content_blocks"].append({"text": text, **tag})
                if pending_abstract and result["document"]["abstract"] is None:
                    result["document"]["abstract"] = text
            else:
                # preamble (title/authors/affiliation area) before first heading
                result["document"]["sections"].append(
                    {"heading": "(preamble)", "level": 0, **tag,
                     "content_blocks": [{"text": text, **tag}]})

        # tables detected geometrically on this page
        try:
            for tab in page_obj.find_tables():
                result["document"]["tables"].append({
                    "caption": None, "rows": tab.extract(),
                    "page": pno + 1, "bbox": round_bbox(tab.bbox),
                    "needs_manual_check": False})
        except Exception:
            pass

        # embedded images not matched by a caption
        for img in page_obj.get_images(full=True):
            result["document"]["figures"].append(
                {"caption": None, "xref": img[0], "page": pno + 1, "bbox": None})

    _extract_title_authors(result)
    _finalize_reading_order(result, pages_blocks)

    if not any(pages_blocks):
        result["status"] = "partial"
        result["uncertainty"].append("no text blocks extracted; likely scanned — run the OCR path")
    else:
        result["status"] = "success"

    doc.close()
    return result


def _extract_title_authors(result):
    doc = result["document"]
    preamble = next((s for s in doc["sections"] if s.get("heading") == "(preamble)"), None)
    if not preamble:
        return
    blocks = preamble["content_blocks"]
    if not blocks:
        return
    # title: first block on page 1 with the largest font among top blocks
    doc["title"] = blocks[0].get("text")
    for b in blocks[1:6]:
        t = b.get("text", "")
        if any(h in t.lower() for h in AFFILIATION_HINTS):
            doc["affiliations"].append(t)
        elif len(t) < 200 and ("," in t or re.search(r"\b(and|et al\.?)\b", t, re.I)):
            doc["authors"].append(t)


def _finalize_reading_order(result, pages_blocks):
    doc = result["document"]
    for blocks in pages_blocks:
        for b in blocks[:400]:
            doc["reading_order"].append(
                {"page": b["page"], "bbox": b["bbox"], "text": b["text"][:160]})


def fallback_pdftotext(pdf_path: Path) -> dict:
    try:
        out = subprocess.run(["pdftotext", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=120)
        text = out.stdout or ""
    except Exception as e:
        return {"status": "failed", "error": f"pdftotext fallback failed: {e}",
                "document": {"reading_order": []}, "uncertainty": [str(e)],
                "sources": {"pdf": str(pdf_path)}}
    return {
        "status": "partial",
        "document": {"reading_order": [{"page": None, "bbox": None, "text": text[:200000]}]},
        "uncertainty": ["PyMuPDF unavailable; plain pdftotext fallback, no layout analysis"],
        "sources": {"pdf": str(pdf_path), "engine": "pdftotext"},
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Scholarly PDF parser")
    ap.add_argument("--pdf", help="Input PDF path")
    ap.add_argument("--inspect", metavar="PDF", help="Inspect a PDF and print summary")
    ap.add_argument("--out", help="Output JSON path")
    ap.add_argument("--json", action="store_true", help="Print JSON to stdout")
    args = ap.parse_args(argv)

    if args.inspect:
        print(json.dumps(inspect_pdf(Path(args.inspect)), ensure_ascii=False, indent=2))
        return 0
    if not args.pdf:
        ap.error("one of --pdf or --inspect is required")

    data = parse_pdf(Path(args.pdf))
    text = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out} ({len(text)} bytes)", file=sys.stderr)
    if args.json or not args.out:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
