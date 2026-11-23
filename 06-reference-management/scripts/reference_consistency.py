#!/usr/bin/env python3
"""校验引用一致性：文末编号连续、引用-文献映射齐全、去重可解释。

用法：python3 reference_consistency.py [result.json]
默认读 /app/output/result.json；退出码 0=通过。
"""
import json, sys


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    checks = []

    refs = d.get('reference_list', [])
    nums = [r.get('num') for r in refs if isinstance(r.get('num'), int)]
    cont = sorted(nums) == list(range(1, len(refs) + 1))
    checks.append({'check': '文末编号连续', 'result': 'pass' if cont else 'fail',
                   'detail': f'{len(refs)} 条，编号 1..{len(refs)}' if cont else f'编号不连续: {nums}'})

    cmap = d.get('citation_map', [])
    bad = [c.get('citation') for c in cmap if not c.get('source_id')]
    checks.append({'check': '引用-文献映射', 'result': 'pass' if not bad else 'fail',
                   'detail': (str(bad)) if bad else f'{len(cmap)} 条引用均有 source_id'})

    dedup = d.get('dedup', [])
    badr = [x for x in dedup if not (x.get('merged_into') and x.get('reason'))]
    checks.append({'check': '去重可解释', 'result': 'pass' if not badr else 'fail',
                   'detail': (str(badr)) if badr else f'{len(dedup)} 条去重均有依据'})

    passed = all(c['result'] == 'pass' for c in checks)
    print(json.dumps({'passed': passed, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/app/output/result.json'))
