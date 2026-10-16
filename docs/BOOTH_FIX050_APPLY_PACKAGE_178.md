# 작업178 — 수정050 ROM없는 적용묶음·실Windows 검증

[050 적용ZIP](../dist/TinyToonAdventures2_KR_Review_050_BoothFix_20261008.zip) SHA `7d13c4e1a5214e64b63a9daa72df008b461ed0c594d6c90a28e77b1e30dd7667` / [ROM](../build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes) SHA `49b8e869a232657f88c1810c3319d0f79b0ee23dd1ed993cf2bfc1f48726dc25`. 원본일본판→050 xdelta이며이전049를덮지않는다. [27개포함파일/검증보고](../qa/reports/issue178_package.json), [사용법](../dist/TinyToonAdventures2_KR_Review_050_BoothFix_20261008/README_적용방법.txt). tools/licenses/apply.cmd는이전검증본을그대로복사했다. PS1의패치명·패치SHA·결과SHA·050표시만바꾸고기존출력덮어쓰기금지/원본검증/도구해시/임시파일정리는보존했다.

검증: 실Windows apply.cmd8사례(정상/기존출력/원본=출력/동일크기타판본/이미패치본/손상패치/손상도구/인자없음) PASS. 한글·공백경로 최종ZIP 추출본 apply.cmd 실행 byte-exact050 PASS. ZIP CRC/전체포함파일exact/적용후payload불변/ROM없는ZIP PASS. 원본·1편·이전049적용본·사용자세이브·Mesen untouched. 기존173folder에사용자가만든ROM은복사하지않았다.

049검토HTML/이미지/결정169/173은review049_historical로exact보존하고역사자료임을root사용법/notes/report에명시했다. 새050대상54/33전장면재검증이나결정양식최종승인으로전환하지않았다. issue177에실제같은입력 교환before/afterPNG와집중4분기검증report를넣었다. scope_policy050은원문유지6건의사용자정책을그대로참조하며본문/CHR/별도printer표가049와같음을확인했다. [작업177](BOOTH_EXCHANGE_FONT_FIX_050_177.md)의집중runtime와package적용은구분한다. 전체플레이/최종사람승인/전역원천완결은미완료이고카페완성작업기/게시없음.

재생: 새050 ROM을열고초기화후매표소에다시들어가교환한다. 이미깨진049 강제저장상태의자동복구는보장하지않는다. builder: `python scripts/build_booth177.py --output build/NEW_050`; package: `python scripts/package_booth178.py`는기존최종산출물재작성방지로재실행하지않는다. hashes는위보고와패키지SHA256.txt를따른다.

다음 작업 하나: 사용자가 새050 ROM을 열고 초기화/매표소 재진입 후 티켓 교환 대사를 검수한다.
