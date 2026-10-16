"""ROM-free046 human review records/HTML with explicit historical scene provenance."""
from pathlib import Path
import json,hashlib,base64,html,re,csv,zipfile
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 old=R/'workspace/review/translation043_20261005_v2';out=R/'workspace/review/translation046_20261005';assert not out.exists();x=json.loads((old/'review_records.json').read_text('utf-8'));assert len(x['units'])==54 and len(x['graphics'])==29
 ssot=R/'workspace/translation/text_ja.csv';current=list(csv.DictReader(ssot.open(encoding='utf-8-sig')));by={z['entry_id']:z for z in current}
 for z in x['units']:assert z['translation_ko']==by[z['entry_id']]['translation_ko']and z['status']==by[z['entry_id']]['status'];z['notes_scope']='Historical insertion notes; current technical status in project handoff'
 x['ROM_build']='dialogue_kr_poc_046';x['ROM_sha256']=sha(R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes');x['SSOT_sha256']=sha(ssot);x['human_review_complete']=False
 new=[]
 p=R/'workspace/translation/notices_graphics_plan_001.json';plan=json.loads(p.read_text('utf-8'))
 for i,z in enumerate(plan['labels']):new.append({'id':f'notices_graphics_plan_001:{i}','source':z['source_text'],'translation_ko':z['translation_ko'],'status':'draft','plan':p.relative_to(R).as_posix(),'plan_sha256':sha(p)})
 for n in('start','stop'):
  p=R/f'workspace/translation/{n}_graphics_plan_001.json';z=json.loads(p.read_text('utf-8'));new.append({'id':n+'_graphics_plan_001:0','source':z['source_text'],'translation_ko':z['translation_ko'],'status':'draft','plan':p.relative_to(R).as_posix(),'plan_sha256':sha(p)})
 x['graphics']+=new;assert len(x['graphics'])==33
 for z in x['actual_images']:assert sha(R/z['path'])==z['sha256'];z['ROM_build']='dialogue_kr_poc_043';z['evidence_scope']='Historical actual043 PNG. Reused for visually unchanged prior artwork; not newly executed046 scene.'
 additions=[('시작 안내 — 시작!','qa/dialogue/stop081_cart046/frame_02670.png','046'),('다음 라운드!','qa/dialogue/start077_cart045/frame_05010.png','045'),('시간 초과!','qa/dialogue/start077_cart045/frame_19110.png','045'),('기차 정지 표지','qa/dialogue/stop080_train046_v2/frame_03330.png','046')]
 for label,path,build in additions:
  p=R/path;assert p.is_file();env=json.loads((p.parent/'environment.json').read_text('utf-8'));assert sha(p)==env['files'][p.name];x['actual_images'].append({'label':label,'path':path,'sha256':sha(p),'type':'Actual emulator PNG','ROM_build':'dialogue_kr_poc_'+build,'ROM_sha256':env['rom_sha256'],'intervention':env['intervention'],'evidence_scope':'Natural controller-only actual scene; 045 event images explicitly historical, current046 only claimed for named046 scenes'})
 x['limits']=['Human wording/terminology/artwork approval pending; no auto approval','Registered54 units and46 historical native maincalls, not globalcorpus or whole-game closure','Gallery explicitly distinguishes043/045 historical images and current046 images','Whole natural gameplay/all branches/hardware and PCM listening not complete','Audio registers/engine/DMC preservation verified historically but146 output-phase observations differed; PCM identity not claimed','Pause/HOWTOCONTROL remain consumer-unconnected in testedpaths; full unused proof absent','POW and other embedded effect/branding art remain source candidates; not declared globally translated or human-approved preservation']
 x['technical_reports']={n:sha(R/'qa/reports'/n)for n in('stop080_validation.json','stop081_regression.json','start077_validation.json','notices074_runtime.json')}
 source=(old/'review.html').read_text('utf-8');source=source.replace('043 사람 검토자료','046 사람 검토자료').replace('검토자료043','검토자료046')
 gallery='<div class="gallery">'
 for z in x['actual_images']:
  encoded=base64.b64encode((R/z['path']).read_bytes()).decode();gallery+=f'<figure><img alt="{html.escape(z["label"])}" src="data:image/png;base64,{encoded}"><figcaption>{html.escape(z["label"])} · 실제 {html.escape(z["ROM_build"])}<br>{html.escape(z["evidence_scope"])}<br>{html.escape(z["path"])}</figcaption></figure>'
 gallery+='</div>';source,n=re.subn(r'<div class="gallery">.*?</div>',lambda m:gallery,source,count=1,flags=re.S);assert n==1
 body=''.join('<tr><td>'+html.escape(z['id'])+'</td><td>'+html.escape(z['source'])+'</td><td>'+html.escape(z['translation_ko'])+'</td><td>검토 대기</td></tr>'for z in x['graphics']);source,n=re.subn(r'<tbody>.*?</tbody>',lambda m:'<tbody>'+body+'</tbody>',source,count=1,flags=re.S);assert n==1
 source=source.replace('<h2>실제 화면 표본</h2>','<p>현재046에는 본문45초안/9기술공유와 그림33문구가 있습니다. 네 안내(시작·다음 라운드·시간 초과·정지)를 추가했습니다. 아래043/045 화면은 해당 빌드의 과거 실제 증거이며046에서 재촬영했다고 주장하지 않습니다. 사진별 빌드와 개입을 records JSON에 보존했습니다.</p><h2>실제 화면 표본</h2>')
 source=source.replace('<p class="note">','<p class="note">삽입 당시 기술 메모: ')
 source=source.replace('전체 자연플레이/실기/오디오/reset/savestate 검증은 별도 항목입니다.','전체 자연플레이/실기/PCM 청음은 미완료이며 reset/savestate와 오디오 쓰기·DMC는 과거043의 명시된 검증 범위를 따릅니다. 오디오 출력 위상 동일성은 주장하지 않습니다.')
 out.mkdir();(out/'review.html').write_text(source,'utf-8');(out/'review_records.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n','utf-8')
 pending='''# 현재046 사람 검토 — 자동 승인 없음

등록본문45초안/기술공유9와그림33문구를review.html에서확인한다. 변경판단은ID/현재문구/수정안또는승인/이유/장면/검토자·날짜로기록한다. 실제PNG빌드는사진별로표시하며043·045과거화면과046현재표본을구분한다.

- 버스터 바니/애크미 에이커스/몬타나랜드/몬타나의 철도와대사말투·의미·띄어쓰기.
- 일반티켓·골드티켓·HUD금티켓의공간제약과표현.
- 생성형타이틀/지도/매표소/게임오버 실제철자·미감, 기존장식M/PUSHSTART/법적표시/제작진영문이름 보존결정.
- 추가안내:시간초과!/다음라운드!/시작!/정지의6~7pixel세로글자미감.
- HOWTOCONTROL/PAUSE는testedpath 소비미연결이며전역미사용승인아님. POW같은내장효과음/브랜딩그림의전역범위는자동확정하지않는다.
- 본문54/그림33은등록범위이며전게임완주/전역corpus폐쇄/실기/PCM청음검증과구분한다.

수정은원천SSOT에반영하는별도작업이다. 검토자료에서상태를변경해도원본/ROM/SSOT를자동변경하지않는다. 외부게시권한없음. 최종카페작업기는전체작업후작성한다.
''';(out/'DECISIONS_PENDING.md').write_text(pending,'utf-8');(out/'README.txt').write_text('타이니툰2 현재046 사람검토자료\nreview.html을브라우저로열면전체PNG가인라인포함되어오프라인으로볼수있습니다. ROM/패치/폰트/에뮬레이터는이ZIP에없습니다. 본문54/그림33/actual13사진; 실제빌드043·045·046을구분합니다. 최종승인/카페작업기가아닙니다. DECISIONS_PENDING.md에ID별판단을기록합니다.\n','utf-8')
 manifest={'work':82,'ROM_build':x['ROM_build'],'ROM_sha256':x['ROM_sha256'],'SSOT_sha256':x['SSOT_sha256'],'ROM_free':True,'human_review_complete':False,'registered_units':54,'graphics':33,'actual_images':13,'files':{p.name:sha(p)for p in sorted(out.iterdir())if p.is_file()}};(out/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n','utf-8')
 archive=R/'workspace/review/TinyToon2_Translation_Review_046_20261005.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for p in sorted(out.iterdir()):z.write(p,(Path(out.name)/p.name).as_posix())
 with zipfile.ZipFile(archive)as z:
  assert z.testzip()is None and len(z.namelist())==5
  for p in out.iterdir():assert z.read((Path(out.name)/p.name).as_posix())==p.read_bytes()
 proof={'work':82,'status':'PASS_RECORDS_INLINE_ROMFREE_ZIP','archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'registered_units':54,'graphics':33,'actual_images':13,'ROM_free':True,'all_source_records_and_images_hash_verified':True,'human_review_complete':False,'render':'pending separatebrowser check','scope':'Private review only; historical gallery labels explicit; not finalrelease/Cafe/posting'};p=R/'qa/reports/review046_records.json';assert not p.exists();p.write_text(json.dumps(proof,indent=2)+'\n','utf-8');print(json.dumps(proof,indent=2))
if __name__=='__main__':main()