#!/usr/bin/env python3
"""校验 Nanopublication：断言必需字段、证据定位、证据等级受控词表。

用法：python3 validate_nanopub.py [result.json]
默认读 /app/output/result.json；退出码 0=通过。
"""
import json, sys

REQ = ['id', 'assertion', 'subject', 'relation', 'object', 'condition', 'polarity']
LEVELS = {'direct', 'paraphrase', 'inferred'}


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    checks = []

    asserts = d.get('assertions', [])
    badf = [a.get('id') for a in asserts if any(not a.get(k) for k in REQ)]
    checks.append({'check': '断言必需字段', 'result': 'pass' if not badf else 'fail',
                   'detail': (str(badf)) if badf else f'{len(asserts)} 条字段齐全'})

    bade = [a.get('id') for a in asserts if not (a.get('evidence') or {}).get('locator')]
    checks.append({'check': '证据定位', 'result': 'pass' if not bade else 'fail',
                   'detail': (str(bade)) if bade else '每条证据有位置'})

    badl = [a.get('id') for a in asserts if a.get('evidence_level') not in LEVELS]
    checks.append({'check': '证据等级受控', 'result': 'pass' if not badl else 'fail',
                   'detail': (str(badl)) if badl else '等级合法'})

    passed = all(c['result'] == 'pass' for c in checks)
    print(json.dumps({'passed': passed, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/app/output/result.json'))
