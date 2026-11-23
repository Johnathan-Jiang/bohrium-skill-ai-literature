#!/usr/bin/env python3
"""LaTeX 编译闭环：按正确轮次编译，定位第一条错误到文件+行号。

用法：python3 latex_build.py [main.tex]
环境变量：LATEX_ENGINE（默认 xelatex）、LATEX_BIB（默认 biber）。
退出码 0=编译通过；非 0=编译失败（输出定位信息）。
"""
import json, os, re, subprocess, sys

ENGINE = os.environ.get('LATEX_ENGINE', 'xelatex')
BIB = os.environ.get('LATEX_BIB', 'biber')


def run(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def first_error(log):
    lines = log.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith('!'):
            ctx = ''
            for j in range(i + 1, min(i + 3, len(lines))):
                m = re.match(r'l\.(\d+)\s*(.*)', lines[j])
                if m:
                    ctx = f'line {m.group(1)}: {m.group(2)[:80]}'
                    break
            return ln.strip(), ctx
    return None, None


def main(main_tex='main.tex'):
    out = {'engine': ENGINE, 'passes': [], 'exit_code': 0, 'errors_fixed': [], 'status': 'success'}
    stem = os.path.splitext(main_tex)[0]
    jobs = []
    if os.path.exists(main_tex):
        jobs = [f'{ENGINE} -interaction=nonstopmode -halt-on-error {main_tex}']
        if os.path.exists(stem + '.bbl'):
            jobs = [f'{ENGINE} -interaction=nonstopmode -halt-on-error {main_tex}',
                    f'{BIB} {stem}',
                    f'{ENGINE} -interaction=nonstopmode -halt-on-error {main_tex}',
                    f'{ENGINE} -interaction=nonstopmode -halt-on-error {main_tex}']
    for cmd in jobs:
        rc, so, se = run(cmd)
        out['passes'].append(cmd.split()[0])
        if rc != 0:
            err, ctx = first_error(so + se)
            out['exit_code'] = rc
            out['status'] = 'failed'
            out['errors_fixed'].append({'command': cmd, 'error': err, 'location': ctx})
            break
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out['exit_code'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'main.tex'))
