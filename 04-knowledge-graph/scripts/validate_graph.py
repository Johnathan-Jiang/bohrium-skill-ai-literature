#!/usr/bin/env python3
"""校验知识图谱：节点带位置、边端点存在、每条边有证据。

用法：python3 validate_graph.py [result.json]
默认读 /app/output/result.json；退出码 0=通过。
"""
import json, sys


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    checks = []

    nodes = d.get('nodes', [])
    ids = {n.get('id') for n in nodes}
    badn = [n.get('id') for n in nodes if not (n.get('label') and n.get('mentions'))]
    checks.append({'check': '节点字段+位置', 'result': 'pass' if not badn else 'fail',
                   'detail': (str(badn)) if badn else f'{len(nodes)} 节点均带位置'})

    edges = d.get('edges', [])
    dangling = [e.get('id') for e in edges if e.get('source') not in ids or e.get('target') not in ids]
    bade = [e.get('id') for e in edges if not (e.get('evidence') or {}).get('locator')]
    checks.append({'check': '边端点存在', 'result': 'pass' if not dangling else 'fail',
                   'detail': (str(dangling)) if dangling else '无悬挂边'})
    checks.append({'check': '边证据绑定', 'result': 'pass' if not bade else 'fail',
                   'detail': (str(bade)) if bade else '每条边有证据'})

    passed = all(c['result'] == 'pass' for c in checks)
    print(json.dumps({'passed': passed, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/app/output/result.json'))
