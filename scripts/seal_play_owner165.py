from pathlib import Path
import json
from seal_continuation159 import R,sha,seal
def main():
 out=R/'qa/reports/play_owner165_handoff.json';assert not out.exists()
 d=R/'qa/dialogue/water165_rope_capture049';e=json.loads((d/'environment.json').read_text('utf-8'))
 for f,v in e['files'].items():assert sha(d/f)==v
 complete=(d/'trace_complete.txt').read_text('utf-8')if(d/'trace_complete.txt').exists()else None
 # End markers and hashes are archival checks, not a new fullplay assessment.
 result={'work':165,'status':'USER_OWNS_ACTUAL_PLAY_QA','user_instruction':'실제 플레이 검수는 내가 할께 그 외에 잔여건이 있어>?','actual_play_owner':'user','new_automated_gameplay_runs_authorized':False,'owned_Mesen_PID':14764,'owned_runner_PID':13464,'owned_process_identity_checked_before_stop':True,'runner_finished_exit_code':e['exit_code'],'observed_complete_marker':complete,'QA_assets_hash_verified':len(e['files']),'natural_clear_assessed':False,'scope':'Pending165 run completed11500 marker at handover. Preserve all output; no new gameplay/visual verdict. User ownership supersedes auto-play stream.','ROM_sha256':e['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'nonplay_remaining':['Global source/graphics corpus closure beyond registered54/33/20 inventories','HOWTO116117/PAUSE120121/POW61 consumer-to-target/exclusion decisions','Final45draft texts and33graphics/name/title human choices','163 singlePNG capture discrepancy: retain FAIL, establish reliable visual evidence or exclude unsupported equivalence','FinalROM-free release notes/support scope/checksums/licenses/packaging after validated corrections','NaverCafe worklog copy/images/HTML/upload guide after project completion; no external posting authorization'],'human_approved':False,'release_eligible':False}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 body=f'''[검수 소유권/남은 일](../qa/reports/play_owner165_handoff.json), [165 실행계획](../work/water165/run_plan.json), [165 준비](../scripts/prepare_water_rope165.py), [정리기](../scripts/seal_play_owner165.py).

사용자가 실제 플레이 검수를 직접 맡겠다고 지시했다. 자동플레이/완주 컨트롤러 실험은 이 시점에 종료한다. 확인한 owned Mesen PID14764(parent13464/정확한전용exe와165명령)만 종료 요청했고 runner는종료했다. 보존된11500 완료마커/exit0 및3644산출물SHA를확인했다. 이는자료보존검증이며새플레이성공/실패/완주판정은추가하지않는다. 첫C9/0541쓰기자료등도보존한다. 실제플레이판정은사용자담당이다. 새에뮬레이터실행없음.

플레이를제외한잔여: (1)등록54문자/33그림/20NT 밖 전역원천누락·제외근거폐쇄, (2)HOWTO116117·PAUSE120121·POW61의실제대상/미사용/원본유지결정, (3)45문장초안과33그림/명칭/타이틀의최종선택, (4)163 PNG4410비교실패의캡처근거정리와지원되지않는전체영상동일주장제외, (5)수정반영후정식ROM없는배포설명·해시·도구라이선스·패키지, (6)모든작업완료뒤네이버카페본문·이미지·읽기HTML·업로드안내. 외부게시권한은없다. CSV9untranslated는기술/공유macro·숫자단위이며9일본어문장미번역이라는뜻이아니다.

현재검수본: [ROM049](../build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes), [ROM없는적용ZIP](../dist/TinyToonAdventures2_KR_Review_049_20261006.zip), [문장/그림검토HTML](../workspace/review/translation049_20261006/review.html). ROM SHA `{result['ROM_sha256']}`,CSV SHA `{result['CSV_sha256']}` 불변. 검수패치ZIP SHA `27404b77f6afc4a6ad8e1e51e357a89aba804b0c5631fbac5193862acb2de42e`; 정식배포판은아니다. 기존132실제적용/133reset-state보고PASS는해당범위의역사검증으로보존하며재실행하지않았다.

변경:165준비/Lua/계획·QA보존·소유권보고·상세/날짜별인계/journal/canonical·프로젝트AGENTS·manifest/audit. 원본·1편·현재빌드·기존실패보존.각산출물SHA는manifest.이번정적SHA/완료마커/소유프로세스정리만수행.새CPU/build/apply/직접장면검토/청음/실기/사람최종없음. 미완료조건은사용자플레이검수와별개로위목록에기록한다.'''
 p=R/'AGENTS.md';s=p.read_text('utf-8');assert '실제 플레이 검수 사용자 담당 — 2026-10-07'not in s
 p.write_text(s+'\n\n## 실제 플레이 검수 사용자 담당 — 2026-10-07\n\n사용자가 실제 플레이 검수를 직접 맡는다. 별도 재요청 전 자동 플레이·완주 컨트롤러 실험을 새로 실행하지 않는다. 기존 실행/실패 증거는 보존하고 인계한다. 정적 원천/그래픽 소비 조사, 번역·삽입·재빌드/적용, 문서·배포·작업기 등 비플레이 작업의 범위는 유지한다. 사용자 플레이 결과를 최종 완료로 추정하지 않는다.\n','utf-8')
 files=[out,Path(__file__),p,R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'scripts/run_menu_qa.py',R/'config/water_first_hazard_steer156.json',R/'scripts/trace_water_hold163.lua',R/'qa/reports/water164_rope_model.json',R/'dist/TinyToonAdventures2_KR_Review_049_20261006.zip',R/'workspace/review/TinyToon2_Translation_Review_049_20261006.zip']
 for pat in ['scripts/*165*','work/water165/*','qa/dialogue/water165_rope_capture049/*']:files.extend(R.glob(pat))
 seal(165,'ACTUAL_PLAY_USER_HANDOFF_AND_REMAINDERS.md','실제 플레이 사용자 이관·잔여 정리',body,'사용자 실제플레이담당.자동플레이종료/165자료보존/ROM·CSV불변.비플레이 잔여6종 정리.','HOWTO/PAUSE/POW 및 등록범위 밖 원천의 기술 잔여를 정적으로 정리해 번역 추가·제외 판단 근거를 작성한다.',files)
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8');s=s.replace('별도 중단 지시 전까지 허가된 개발 작업을 계속한다.','실제 플레이 검수는 2026-10-07 사용자 담당으로 이관했다. 자동 플레이 실험은 종료하며 비플레이 개발 범위를 유지한다.',1);p.write_text(s,'utf-8');print('SEALED165 USER PLAY QA OWNER')
if __name__=='__main__':main()
