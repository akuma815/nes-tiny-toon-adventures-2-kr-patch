"""Strict dated non-play handoffs. Existing frozen artifacts are never rewritten."""
from pathlib import Path
import hashlib, json, re

R = Path(__file__).resolve().parents[1]
DATE = '2026-10-08'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def seal(work, name, title, body, short, next_action, files):
    doc = R / 'docs' / name
    manifest = R / f'manifests/nonplay{work}_assets.json'
    assert not doc.exists() and not manifest.exists()
    assets = sorted(set([*files, Path(__file__)]))
    assert all(p.is_file() and p.resolve().is_relative_to(R) for p in assets)
    doc.write_text(f'# 작업{work} — {title}\n\n{body}\n\n다음 작업 하나: {next_action}\n', 'utf-8')
    entry = (f'\n\n## 작업{work} — {title}\n\n{short}\n\n'
             f'[상세 변경·SHA·검증 구분·제한]({name}).\n\n다음 작업 하나: {next_action}\n')
    for filename in [f'HANDOFF_{DATE}.md', 'SURVEY.md', 'LOCALIZATION_WORK_PLAN.md']:
        p = R / 'docs' / filename
        text = p.read_text('utf-8') if p.exists() else f'# 인계 — {DATE}\n'
        if filename == 'LOCALIZATION_WORK_PLAN.md':
            text = re.sub(r'^> \*\*.*?\*\*', f'> **{DATE} 사용자 재개 / 현재 개발049 / 작업{work} 완료. 실제 플레이 사용자 담당.**', text, count=1)
        p.write_text(text + entry, 'utf-8')
    p = R / 'docs/journal' / f'{DATE}.md'
    text = p.read_text('utf-8') if p.exists() else f'# 작업 기록 — {DATE}\n'
    p.write_text(text + entry.replace(f'({name})', f'(../{name})'), 'utf-8')
    p = R / 'README.md'
    p.write_text(p.read_text('utf-8') + f'\n\n[{title}{work}](docs/{name}): {short}\n', 'utf-8')
    p = R / 'docs/HANDOFF.md'
    text = re.sub(r'^# .*?\n', f'# 진행 중 — {DATE}, 작업{work} 완료\n', p.read_text('utf-8'), count=1)
    text = re.sub(r'\*\*다음 작업 하나:.*?\*\*', '**다음 작업 하나: ' + next_action + '**', text, count=1)
    text = text.replace('[오늘 인계](HANDOFF_2026-10-07.md)', f'[오늘 인계](HANDOFF_{DATE}.md)', 1)
    text = text.replace('[오늘 journal](journal/2026-10-07.md)', f'[오늘 journal](journal/{DATE}.md)', 1)
    p.write_text(text + entry, 'utf-8')
    manifest.write_text(json.dumps({'work':work, 'files':{
        p.relative_to(R).as_posix():sha(p) for p in [*assets, doc]
    }}, indent=2) + '\n', 'utf-8')

