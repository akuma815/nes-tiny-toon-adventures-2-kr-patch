"""Seal non-play tasks with strict paths and the established dated handoff set."""
from pathlib import Path
import hashlib, json, re
R = Path(__file__).resolve().parents[1]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def seal(work, name, title, body, short, next_action, files):
    doc = R / 'docs' / name
    manifest = R / f'manifests/nonplay{work}_assets.json'
    assert not doc.exists() and not manifest.exists()
    files = sorted(set([*files, Path(__file__)]))
    assert all(p.is_file() and p.resolve().is_relative_to(R) for p in files)
    doc.write_text(f'# 작업{work} — {title}\n\n{body}\n\n다음 작업 하나: {next_action}\n', 'utf-8')
    entry = (f'\n\n## 작업{work} — {title}\n\n{short}\n\n'
             f'[상세 변경·SHA·검증 구분·제한]({name}).\n\n다음 작업 하나: {next_action}\n')
    for filename in ['HANDOFF_2026-10-07.md', 'SURVEY.md', 'LOCALIZATION_WORK_PLAN.md']:
        p = R / 'docs' / filename
        old = p.read_text('utf-8')
        if filename == 'LOCALIZATION_WORK_PLAN.md':
            old = re.sub(r'^> \*\*.*?\*\*', f'> **2026-10-07 현재 개발049 / 작업{work} 완료. 실제 플레이 사용자 담당.**', old, count=1)
        p.write_text(old + entry, 'utf-8')
    p = R / 'docs/journal/2026-10-07.md'
    p.write_text(p.read_text('utf-8') + entry.replace(f'({name})', f'(../{name})'), 'utf-8')
    p = R / 'README.md'
    p.write_text(p.read_text('utf-8') + f'\n\n[{title}{work}](docs/{name}): {short}\n', 'utf-8')
    p = R / 'docs/HANDOFF.md'
    old = re.sub(r'작업\d+ 완료', f'작업{work} 완료', p.read_text('utf-8'), count=1)
    old = re.sub(r'\*\*다음 작업 하나:.*?\*\*', '**다음 작업 하나: ' + next_action + '**', old, count=1)
    p.write_text(old + entry, 'utf-8')
    manifest.write_text(json.dumps({'work': work, 'files': {
        p.relative_to(R).as_posix(): sha(p) for p in [*files, doc]
    }}, indent=2) + '\n', 'utf-8')

