#!/usr/bin/env python3
"""校验润色语义守恒：数字/文献编号/图表指向在原文与改文间不丢失。

用法：python3 check_semantics.py [result.json]
默认读 /app/output/result.json；退出码 0=通过（无丢失）。
"""
import json, re, sys

NUM = re.compile(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')
CITE = re.compile(r'\[\d+(?:[,-]\d+)*\]')
FIGTAB = re.compile(r'(?:Fig\.|Figure|Table)\s*\d+', re.I)


def toks(s):
    s = s or ''
    return {'nums': set(NUM.findall(s)), 'cites': set(CITE.findall(s)), 'figtab': set(FIGTAB.findall(s))}


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    checks = []

    edits = d.get('edits', [])
    lost = []
    for e in edits:
        a, b = toks(e.get('original')), toks(e.get('revised'))
        delta = {k: sorted(a[k] - b[k]) for k in a if a[k] - b[k]}
        if delta:
            lost.append({'id': e.get('id'), 'lost': delta})
    checks.append({'check': '数字/引用/图表守恒', 'result': 'pass' if not lost else 'fail',
                   'detail': str(lost[:3]) if lost else f'{len(edits)} 处修改未丢失限定/数字/引用'})

    passed = all(c['result'] == 'pass' for c in checks)
    print(json.dumps({'passed': passed, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/app/output/result.json'))
