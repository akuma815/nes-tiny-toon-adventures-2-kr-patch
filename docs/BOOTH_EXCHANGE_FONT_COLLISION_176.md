# 작업176 — 사용자 티켓교환 대사 깨짐 재현·진단

사용자가 티켓교환 후 대사 깨짐을 신고했고 실제 스크린샷을 제공했다. 실행프로세스22308/H:\Mesen\Mesen.exe/MesenCE, 최근ROM경로와 파일SHA는현재049임을 확인했다. Computer Use native pipe 연결2회실패(os error2), emucap 미연결로 현재live메모리/화면을 직접읽지는못했다. CLI의script-only 전달은원문소스에서기존게임에즉시실행되지않으므로사용하지않았다. 대신 사용자MesenCE2.2.1 exe/DLL을격리복사하고해당게임저장상태1/11을프로젝트QA에복사해12프레임씩재현했다. 사용자프로세스/ROM/설정/세이브는수정하지않았다. MSS포맷4는ROM SHA를내장하지않으므로현재파일SHA·사용자신고·같은원천이름/장면으로귀속하며저장상태자체의해시증명과구분한다.

[진단](../qa/reports/issue176_diagnosis.json): 복사한문제장면에서도티켓16/점수30과같은깨진문구를확인했다. 하단NT는 MAIN_05782 ‘포인트를 티켓으로 / 바꿔 드릴게요’의정상코드인데RAM C6/06F3=196, 실제PPU CHR=196/197(놀이기구요금공유폰트)다. 원래이문장의폰트는162/163이다. 그래서그코드가‘요금은장 내티켓을 / 줘아 쉽지만더’로읽힌다. 깨진번역바이트가아니라폰트선택충돌이다.

native bank32 9D63→9CC9는slot23/arg4를9417에넣어925E로상단소지숫자를갱신한다. 전역font table의slot23=196이현재하단폰트를바꾸지만하단NT는기존문구를유지한다. 저장상태의pending15와실제pointer98E0를확정표시15본문으로혼동하지않는다. 다음수정은매표소course6의숫자slot23에서거주하단폰트를보존하는것이며, 기존helper padding을같은cycle 분기로대체해공통요금/다른본문동작을보존한다. 실제cold-entry/교환콜러trace와수정후회귀가완료돼야fixed로닫는다.

[준비/귀속](../qa/issue176_user_booth/provenance.json), [읽기용Lua](../scripts/trace_issue176.lua), [재현runner](../scripts/run_issue176.py). 재현: `python scripts/run_issue176.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --state qa/issue176_user_booth/user_slot11.mss --output qa/dialogue/issue176_slot11_049` (기존출력보호,사본에서새경로사용). 정적코드/바이트·저장상태격리복원/12프레임raw/실제PNG PASS, 현재사용자live직접읽기및교환caller새재생은아직미수행이다. 새게임전장면QA/빌드/적용/청음/최종사람승인 없음. 현재049 ROM `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`/CSV불변. 변경:176준비/observer/runner/진단/인계·사용자상태복사/격리host·QA/environment/manifest·canonical. 이전175의‘확인한기록의새수정없음’은당시한계며이번자연사용자신고로현범위결함을추가했다. 카페완성글/외부게시없음.

포맷/CLI근거: [MesenCE SaveStateManager](https://github.com/nesdev-org/MesenCE/blob/master/Core/Shared/SaveStateManager.cpp), [CLI Script 분류](https://github.com/nesdev-org/MesenCE/blob/master/UI/Utilities/CommandLineHelper.cs), [기존인스턴스 인자처리](https://github.com/nesdev-org/MesenCE/blob/master/UI/Windows/MainWindow.axaml.cs). 이번포맷값과복원성공은별도로실측했다. 감사 `python scripts/audit_project_links171_v2.py --manifest manifests/nonplay176_assets.json --output qa/reports/nonplay176_session.json`.

다음 작업 하나: 매표소 숫자slot23에서 기존 하단폰트를 같은 사이클로 보존하는050 후보를 만들고, 교환 caller와 인접경로의 원인/수정 회귀를 검증한다.
