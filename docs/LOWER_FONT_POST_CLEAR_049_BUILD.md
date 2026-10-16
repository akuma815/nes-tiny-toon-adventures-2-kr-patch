# 작업128 — native clear 이후 폰트 선택049 후보

[048 전환 실패](SHORTAGE048_LIFETIME_REJECTION.md)를 해결하는 code후보049다. [ASM009](../workspace/asm/dialogue_page_font_009.asm), [빌더v2](../scripts/build_clear128_v2.py), [빌드보고](../build/dialogue_kr_poc_049/build_report.json), [독립 검증](../qa/reports/clear128_validation.json). 본문/CSV/모든CHR·native macro·reader·native clear 함수는048과그대로다. helper bank2의slot29/2B만06DF00에서는이전active06F3을C6/6F3에유지하고,이미존재하는post-clear06DF03 초기화에서table226/196으로선택한다. 두번pre-init되는native pointer/행buffer/cursor는기존처럼초기화한다. 다른slot/phase와odd top-tag 계약을보존한다.

font dispatch 세경로의cycle을균등하게38cycles 추가했으며19cycle nativeidle주기의배수다. 48slot×5phase×4active×4flags=3840CPU모델사례(대상32보류포함), intro setup16사례의레지스터/스택복귀/계약RAM/nativebanks를확인했다. 모든page추가38, intro setup과IRQ코드·쓰기주소/시점은기존과같다. CPU모델은비동기IRQ/실제PPU증거가아니며, nativeidle반복수2회와RAM22 RNGcounter가page init마다달라질가능성이있다. 실제경로QA에서이효과를별도로대조한다. 게임전체동일을주장하지않는다.

190byte helper와intro_setup연결주소만이바뀌며048대비165byte다. [Expected Writes](../build/dialogue_kr_poc_049/expected_writes.json)의원본9범위기대바이트·비중첩·전체ROM재구성을확인했고 별도재빌드11파일·한국어공백경로의실제WindowsIPS적용결과가byte exact다. 초기[v1](../scripts/build_clear128.py)의CPU→file범위guard는nativebank32copy의4010base를빠뜨려output전실패했다. [관찰](../qa/reports/clear128_v1_observation.json)을보존하고v2의실제file5440/25440·4E98/24E98범위로해결했다. ASM·실제mutation주소는처음부터올바르게기존빌더의주소를썼다.

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 후보049SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, IPS `01a78be85a8a3a007ba45d039275b0f5fd231b0096b830e75ac28f33f66edbc9`, CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. 499728B/PRG256/CHR232헤더보존. 현재채택047/048거부/049아직후보이며SSOT는후보문장이다. 원본·1편·실패048과기존QA를보존했다.

변경은ASM009/빌더v1,v2/검증기/049및재빌드11파일/한글경로apply3파일/실패관찰·보고/본문서·인계·journal·canonical/manifest다. 이번검증은정적/CPU/build/apply이며새runtime/직접장면은아직없다. 최종사람승인/전역corpus/자연전체/실기/PCM/정식배포미완료. 전체작업후카페작업기를작성한다.

재현: `python scripts/build_clear128_v2.py --output build/새폴더`, IPSCLI는049패치와새결과경로를쓴다. [동결자산](../manifests/clear128_assets.json), 감사경로 `qa/reports/clear128_session.json`.

다음 작업 하나: 049 실제부족3·성공4 입장과다른page경로를같은입력으로실행해 native clear 전후의글꼴수명·타이밍·의도밖픽셀/상태변화를검증한다.
