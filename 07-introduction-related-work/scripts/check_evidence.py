#!/usr/bin/env python3
"""校验引言证据表：正文每条引用在证据表登记、研究空白有依据。

用法：python3 check_evidence.py [result.json]
默认读 /app/output/result.json；退出码 0=通过。
"""
import json, re, sys

CITE = re.compile(r'\[(\d+(?:[,-]\d+)*)\]')


def expand(s):
    out = set()
    for grp in CITE.findall(s):
        for p in grp.split(','):
            p = p.strip()
            if '-' in p:
                a, b = p.split('-')
                out.update(range(int(a), int(b) + 1))
            elif p.isdigit():
                out.add(int(p))
    return out


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    checks = []

    text = d.get('introduction_text', '')
    cited = expand(text)
    etable = d.get('evidence_table', [])
    etable_cites = set()
    for e in etable:
        etable_cites |= expand(str(e.get('citation', '')))
    missing = sorted(cited - etable_cites)
    checks.append({'check': '每条引用有证据登记', 'result': 'pass' if not missing else 'fail',
                   'detail': f'正文 {sorted(cited)}，证据表 {sorted(etable_cites)}' + (f'，缺失 {missing}' if missing else '')})

    gaps = d.get('gap_derivation', [])
    badg = [g.get('gap') for g in gaps if not g.get('basis')]
    checks.append({'check': '研究空白有依据', 'result': 'pass' if not badg else 'fail',
                   'detail': (str(badg)) if badg else f'{len(gaps)} 条空白均有依据'})

    passed = all(c['result'] == 'pass' for c in checks)
    print(json.dumps({'passed': passed, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/app/output/result.json'))
