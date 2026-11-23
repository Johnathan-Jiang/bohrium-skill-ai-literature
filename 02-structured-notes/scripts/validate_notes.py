#!/usr/bin/env python3
"""校验结构化笔记：论文卡片字段齐全、知识点有锚点+引文、章节有页码。

用法：python3 validate_notes.py [result.json]
默认读 /app/output/result.json；退出码 0=通过。
"""
import json, sys

REQ_CARD = ['research_question', 'data', 'methods', 'findings', 'conclusion', 'limitations', 'premises']


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    checks = []

    card = d.get('paper_card', {})
    miss = [k for k in REQ_CARD if not card.get(k)]
    checks.append({'check': '论文卡片字段', 'result': 'pass' if not miss else 'fail',
                   'detail': f'缺失 {miss}' if miss else '字段齐全'})

    kps = d.get('knowledge_points', [])
    bad = [k.get('id') for k in kps if not (k.get('anchor') and k.get('quote'))]
    checks.append({'check': '知识点锚点+引文', 'result': 'pass' if not bad else 'fail',
                   'detail': f'{len(kps)} 条，缺锚点/引文 {len(bad)}' + (f': {bad}' if bad else '')})

    secs = d.get('sections', [])
    bads = [s.get('section') for s in secs if not s.get('pages')]
    checks.append({'check': '章节页码', 'result': 'pass' if not bads else 'fail',
                   'detail': (str(bads)) if bads else f'{len(secs)} 章均有页码'})

    passed = all(c['result'] == 'pass' for c in checks)
    print(json.dumps({'passed': passed, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/app/output/result.json'))
