#!/usr/bin/env python3
"""校验文献翻译结果：术语唯一译名、段号一一对应、数字与文献编号保留。

用法：python3 verify_translation.py [result.json]
默认读 /app/output/result.json；退出码 0=通过，1=存在未通过项。
"""
import json, re, sys

NUM_RE = re.compile(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')
CITE_RE = re.compile(r'\[\d+(?:[,-]\d+)*\]')


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main(path):
    d = load(path)
    checks = []

    terms = d.get('term_table', [])
    seen, dup = {}, []
    for t in terms:
        key = (t.get('source_term'), t.get('context', ''))
        if key in seen:
            dup.append(t.get('source_term'))
        seen[key] = t.get('target_term')
    checks.append({'check': '术语唯一译名', 'result': 'pass' if not dup else 'fail',
                   'detail': ('重复: ' + ', '.join(set(dup))) if dup else f'{len(terms)} 条术语锁定'})

    segs = d.get('segments', [])
    missing = [s.get('id') for s in segs if not s.get('translation')]
    checks.append({'check': '段号-译文一一对应', 'result': 'pass' if not missing else 'fail',
                   'detail': f'{len(segs)} 段，缺译文 {len(missing)}' + (f': {missing}' if missing else '')})

    num_loss = []
    for s in segs:
        src = NUM_RE.findall(s.get('source') or '')
        tgt = NUM_RE.findall(s.get('translation') or '')
        if set(src) - set(tgt):
            num_loss.append((s.get('id'), sorted(set(src) - set(tgt))[:5]))
    checks.append({'check': '数字保留', 'result': 'pass' if not num_loss else 'fail',
                   'detail': str(num_loss[:3]) if num_loss else '数字无缺失'})

    cite_loss = []
    for s in segs:
        src = CITE_RE.findall(s.get('source') or '')
        tgt = CITE_RE.findall(s.get('translation') or '')
        if set(src) - set(tgt):
            cite_loss.append(s.get('id'))
    checks.append({'check': '文献编号保留', 'result': 'pass' if not cite_loss else 'fail',
                   'detail': ('缺失段: ' + str(cite_loss)) if cite_loss else '编号无缺失'})

    passed = all(c['result'] == 'pass' for c in checks)
    print(json.dumps({'passed': passed, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '/app/output/result.json'))
