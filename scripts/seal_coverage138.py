from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/coverage138_assets.json';assert not m.exists()
 p=R/'workspace/translation/coverage049_138.json';v=json.loads(p.read_text('utf-8'))
 nxt='현재049를094의동결 gold4 입력·초기seed·관측기로9000프레임 실행하고, 과거047과대조해 slot1C/상단22·28/하단2A의출력·폰트수명을확인한다.'
 detail='''# 작업138 — 현재049 등록 원천별 검증 원장

[54원천 원장](../workspace/translation/coverage049_138.json), [재현 스크립트](../scripts/make_coverage138.py).

48 main 슬롯/46 main 고유 원천과8 macro 고유 원천을 SSOT/canonical 추출목록과 대조했다. 완료된049 실행7개 및 정확히 명명한 역사047 성 분기3개만 연결한다. ROM/CSV/추출원천과 소비한 environment/trace/RAM/CHR 매핑 파일은 실제 SHA를 다시 확인했다. 현재 ROM 포인터는 high mirrored main table, 폰트 tag는 실제 helper가 읽는 low table에서 가져왔다. 역사적 plan의 font 값으로 현재 상태를 추정하지 않았다.

현재 init+font15, init only12, font only9, 역사047 init only3, 이 선택된 실행들에 미연결7, 별도 reader 연결이 필요한 shared macro8이다. 이 분류는 문장 완성 또는 전체게임 검증률이 아니다. 9445 beforeRTS 페이지 초기화는 실제 source byte 읽기와 다르다. phase00일 때 기존 글자를 지우기 전 유지되는 font도 원래 값으로 보존한다. intro는 memory observer가 없으므로 실제 tag/CHR font snapshot만 연결한다. native ID는 이후 증가할 수 있으므로 snapshot ID만으로 원천을 지정하지 않는다. 공유193/196/201 및 alias 슬롯의 font만으로 문장을 고르지 않는다.

문장 완성/부분출력/지우기/직접 시각검증 결론은 [129](LOWER_FONT_POST_CLEAR_049_BRANCH_QA.md), [130](DEVELOPMENT049_PAGE_REGRESSION.md), [133](STATE049_SHORTAGE_REGRESSION.md)의 bounded 근거를 유지한다. 이번에 새로운 complete-text 판정을 만들지 않았다. Macro88 등은 삽입되어 있다고 해서 이 원장의 실제 reader 관측을 통과했다고 세지 않았다. 미연결은 전역 unused를 뜻하지 않는다.

MAIN_05824(slot1C)는 현재 선택된049 경로에 init이 없고, 과거047 gold4/normal50 입장에는 있다. 따라서 다음 작업은 gold4 성의 신규049 경로로 선택한다. 상단22/28과 성공2A도 이 경로의 수명 검증 대상으로 삼는다. 기존부족3/idle/DMC 실험을 되풀이하는 단계가 아니다.

변경: make_coverage138.py/seal_coverage138.py,coverage049_138.json,본 문서,dated handoff/journal/README/SURVEY/PLAN/HANDOFF 및 scoped manifest/audit. ROM049 SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. 개별SHA는 원장 및 manifest에 기록한다.

검증 구분: 정적/동결자료 대조 PASS. 신규 build/apply/runtime/직접PNG 검토 없음. 이전장면결론은 별도보고서에만 귀속한다. 원본/1편/역사증거보존. 재현 `python scripts/make_coverage138.py`는 기존원장 덮어쓰기를 거부한다. 글로벌 corpus/자연전체완주/HOWTO·PAUSE·POW 잔여소비경로/하드웨어/PCM청음/사람최종문체·명칭·그림검토/정식배포는 여전히 미완료다. 사람승인false/카페 완성작업기·게시 없음.

'''
 doc=R/'docs/COVERAGE049_REGISTERED_SOURCES.md';doc.write_text(detail+'다음 작업 하나: '+nxt+'\n','utf-8')
 entry='\n\n## 작업138 — 등록54원천 현재/역사 검증 원장\n\n현재init+font15/init12/font9,역사init3/선택실행미연결7/macro별도reader8. 초기화와실제읽기·완성을구분했으며global unused/완료율로해석하지않는다. 원본/1편/049/CSV불변·새runtime없음.\n\n[상세 변경·SHA·검증구분·재현·한계](COVERAGE049_REGISTERED_SOURCES.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(COVERAGE049_REGISTERED_SOURCES.md)','(../COVERAGE049_REGISTERED_SOURCES.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[登録원천 검증138](docs/COVERAGE049_REGISTERED_SOURCES.md): 현재/역사 증거를 구분하고 gold4 성의현재049 미실행분기를 선택.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업137 이후','작업138 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files={**v['verified_inputs']}
 for rel in ['workspace/translation/coverage049_138.json','scripts/make_coverage138.py','scripts/seal_coverage138.py','docs/COVERAGE049_REGISTERED_SOURCES.md',*v['linked_completion_reports']]:files[rel]=sha(R/rel)
 m.write_text(json.dumps({'work':138,'files':files},indent=2)+'\n','utf-8');print('PASS work138 handoff')
if __name__=='__main__':main()
