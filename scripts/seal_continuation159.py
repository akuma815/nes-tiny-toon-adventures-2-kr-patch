from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def seal(work,name,title,body,short,next_action,files):
 doc=R/'docs'/name;mf=R/f'manifests/water{work}_assets.json';assert not doc.exists()and not mf.exists()
 doc.write_text(f'# 작업{work} — {title}\n\n'+body+'\n\n다음 작업 하나: '+next_action+'\n','utf-8')
 entry=f'\n\n## 작업{work} — {title}\n\n'+short+f'\n\n[상세 변경·SHA·검증구분·재현·한계]({name}).\n\n다음 작업 하나: '+next_action+'\n'
 for name2 in ['HANDOFF_2026-10-07.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/name2;s=p.read_text('utf-8')
  if name2=='LOCALIZATION_WORK_PLAN.md':s=re.sub(r'^> \*\*.*?\*\*',f'> **2026-10-07 현재개발049 / 작업{work} 완료.**',s,count=1)
  p.write_text(s+entry,'utf-8')
 p=R/'docs/journal/2026-10-07.md';p.write_text(p.read_text('utf-8')+entry.replace(f'({name})',f'(../{name})'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+f'\n\n[{title}{work}](docs/{name}): '+short+'\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8');s=re.sub(r'작업\d+ 완료',f'작업{work} 완료',s,count=1);s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+next_action+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=list(files)+[doc,Path(__file__)];mf.write_text(json.dumps({'work':work,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8')
