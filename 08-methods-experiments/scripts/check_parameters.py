#!/usr/bin/env python3
"""校验方法实验参数表：每个参数有来源、状态标注合法、缺口可执行。

用法：python3 check_parameters.py [result.json]
默认读 /app/output/result.json；退出码 0=通过。
"""
import json, sys


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    checks = []

    params = d.get('parameters', [])
    nosrc = [p.get('name') for p in params if not p.get('source')]
    checks.append({'check': '参数有来源', 'result': 'pass' if not nosrc else 'fail',
                   'detail': (str(nosrc)) if nosrc else f'{len(params)} 个参数均有来源'})

    bads = [p.get('name') for p in params if p.get('status') not in ('confirmed', 'missing')]
    checks.append({'check': '参数状态标注', 'result': 'pass' if not bads else 'fail',
                   'detail': (str(bads)) if bads else '状态均合法'})

    gaps = d.get('gaps', [])
    badg = [g for g in gaps if not (g.get('item') and g.get('action'))]
    checks.append({'check': '缺口清单可执行', 'result': 'pass' if not badg else 'fail',
                   'detail': (str(badg)) if badg else f'{len(gaps)} 条缺口均有动作'})

    passed = all(c['result'] == 'pass' for c in checks)
    print(json.dumps({'passed': passed, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/app/output/result.json'))
