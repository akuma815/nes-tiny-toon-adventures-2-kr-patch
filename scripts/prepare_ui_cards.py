"""Freeze29-draft SSOT and register11 native-card drafts; no source field changes."""
import csv,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 path=ROOT/'workspace/translation/text_ja.csv';before=path.read_bytes();assert sha(before)=='ba881bbffdaf4f5fa84d43f941d9166914e156358a7337c3b1bb66be8af33c86';backup=ROOT/'backups/translation/text_ja_before_ui_cards_001.csv';planpath=ROOT/'workspace/translation/ui_cards_plan_001.json';assert not backup.exists() and not planpath.exists()
 plan=json.loads((ROOT/'work/card_group_001/draft_plan.json').read_text('utf-8'));rows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));assert len(rows)==54
 for p in plan['profiles']:
  row=next(x for x in rows if x['entry_id']==p['entry_id']);assert row['status']=='untranslated' and not row['translation_ko'];scene='Native ride card: rule9E8B/title9E9B/cost9417, RAM34 NMI top plus profile2 lower IRQ; five observed routes'
  row.update(translation_ko=p['text'],status='draft',scene=scene,speaker='Buster',notes='Shared card font193/194. Preserve all macros/variables/control positions/FD padding/literal00 and per-call timing. Macro84..88 shared forced glyphs;83 absent, codes1..3 reused only inside this font. Native_FA keeps leading-zero blank/digit4,1,2,3,50 by actual ride. Train rule keeps native macro width with internal spacing. Final name/tone review pending.')
  p.update(scene=scene,speaker='Buster',screen_kind='cost_lower' if p['slot']==29 else 'rules_top' if 30<=p['slot']<=34 else 'title_top',NT=0x22a8 if p['slot']==29 else 0x2125 if 30<=p['slot']<=34 else 0x20a6,screen_x=64 if p['slot']==29 else 40 if 30<=p['slot']<=34 else 48,screen_y=163 if p['slot']==29 else 72 if 30<=p['slot']<=34 else 40)
 buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows);after=buf.getvalue().encode('utf-8-sig');assert sum(x['status']=='draft' for x in rows)==40
 plan.update(date='2026-10-05',source_sha256='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d',prior_build='dialogue_kr_poc_032',prior_ROM_sha256='c4b40639bafba6a25a1c186c82005963ec4fecdf8d3a22308eaf1ab6643a7d67',backup_CSV_sha256=sha(before),CSV_sha256=sha(after),scope='11 title/rule/cost card drafts; all29 previous drafts retained; no release',review='Draft; final proper names and tone review pending')
 backup.write_bytes(before);path.write_bytes(after);planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'draft':40,'untranslated':14,'CSV_sha256':sha(after),'plan_sha256':sha(planpath.read_bytes())},indent=2))
if __name__=='__main__':main()
