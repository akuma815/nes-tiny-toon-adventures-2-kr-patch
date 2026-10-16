# 홈·매표소·놀이기구 문단별 글꼴 기반 — 작업17/18

채택 빌드는 [dialogue_kr_poc_017](../build/dialogue_kr_poc_017/TinyToon2_dialogue_kr_poc.nes)이다. 타이틀003과 도입부9문단·홈 초안은 그대로이며, 새 번역 문장은 없다. SSOT는54원천/10draft/44untranslated다. [독립 검증](../qa/reports/latch017_validation.json), [실제 세 장면](../qa/dialogue/latch017_actual_scenes.png), [자산 해시](../manifests/ui_font_latch_assets.json), [세션 감사](../qa/reports/ui_font_latch_session_20261005.json).

## 구현과 원인

도입 IRQ FB97과 홈 IRQ FB0D는 다르다. 홈 IRQ는 원래06EA의 화면 프로파일로 C6를 매 프레임 덮어썼다. 문단별 선택한 실제 CHR 뱅크를 RAM06F3에 저장하고, FB12의 `LDA FB34,Y` 한 명령만 `LDA 06F3`로 바꾼다. 원래의 PPU2002 읽기, C7의 상단 그림 뱅크, 나머지 명령과 쓰기 위치를 유지한다. 기존 문단 헬퍼는 STA06F3의4사이클을 NOP 패딩에서 상쇄한다. 홈 슬롯0A는 기존 한글 뱅크130을 지정한다.

홈 첫 문단 전에 IRQ가 실행되므로, 홈 초기화 블록9B0F의8바이트에서 별도 헬퍼9800을 호출해 기본 글꼴90을 먼저 저장한다. 헬퍼가 native CBF0→bank32→CBFF를 호출하고 다시 헬퍼로 돌아오도록 임시 bank2의 식별 바이트만02로 고친다. 정식 bank18의 식별32/소스 데이터는 유지한다. 헬퍼는 원래92/2B=32를 복원하고 FDDB를 통해 원래 bank32로 돌아온다. 초기화 추가 시간76사이클은 기존19사이클 대기 루프의4회에 해당한다. PRG/RNG22 관련 기존 한계는 계속 남는다.

[문단 헬퍼005](../workspace/asm/dialogue_page_font_005.asm), [홈 초기화002](../workspace/asm/home_font_init_002.asm), [빌더](../scripts/build_ui_native_latch.py). 헬퍼 bank2의 코드/테이블과 원래 문자열을 쓰는 정식 bank18을 구별한다. CPU9800에 추가한 코드는 임시 bank2에만 존재한다. CHR152KiB/ROM417808과 전체 글꼴·문자열·macro·헤더는014와 같다. 변경 허용 모델은 원본 전체 및014 전체에 대해 독립 구성하여 일치시켰다.

## 검증을 구분한 결과

- 정적: 원본 SHA 및1편 참조 보존, ExpectedWrites7영역 비중첩,014 전체 이미지에서 지정 코드·헬퍼 식별·홈 글꼴 슬롯만 변경. 새 코드가 원래 문자열을 사용하는 정식 bank18을 덮지 않는다. 등록54행과10초안 내용은 불변이다.
- CPU/빌드/적용: 공식6502 ISA604벡터, 문단 ABI1408조건(초기 글꼴624포함), 홈 IRQ36프로파일·글꼴 조건, 홈 초기화16조건. CPU 레지스터/SP/2B/92와 RAM은 허용 글꼴 슬롯·스택을 제외하고 일치. 초기화 추가76사이클, 문단/도입 설정은014와 같은 시간. 독립 재빌드와 실제 한글·공백 경로 IPS 적용 결과가 같음.
- 런타임: 자연 도입6000프레임848화면, 홈·카트 경로3600프레임390화면, 매표소3000프레임289화면, 편지 중 Start1950/악당 중 Start2760 각3600프레임497화면. 총2521화면의 전체 픽셀 차이0. PPU800..3FFF·nametable·팔레트·OAM·원래 문단 ID/포인터 및 상단 C7 일치. 홈에서 사용하지 않는 하단 CHR가 바뀐 표본은 각각212/87이나, 각 실제 매핑의 CHR 내용은 해당 ROM 바이트와 일치한다.
- 실제 IRQ/PPU/mapper 시점: 홈·카트37173, 매표소37146, 도입41034, 합115353행의 frame/PC/scanline/dot/CPU cycle 정확히 일치. 홈에서 기본 글꼴130 대신90을 사용하는 정상 레지스터 값 변경2566건만 존재하고 상단 뱅크는 동일하다.
- 직접 화면:017 홈990, 매표소1620, 카트2310 확인. 홈 초안은 한글이며, 매표소/카트의 아직 번역하지 않은 일본어와 영문 그림은 정상이다. CPU 검증과 화면 검증은 서로 대체하지 않는다.

## 실패한 후보와 보존

015의 XOR5A 인코딩은 CPU 총시간이 같아도 EOR/NOP를 넣고 PPU2002 읽기를 제거하면서 실제 쓰기 시점이 달라졌다. [실패 보고](../qa/reports/latch015_rejection.json), 빌드/ASM/전체 캡처는 보존하고 채택하지 않았다. 원인은 버스 접근·명령 경계와 비동기 간섭의 차이로 의심되며 DMC 원인이라고 확정하지 않는다.

016은 원래 IRQ 읽기를 복원했으나 초기화 추가72사이클 때문에 대기 루프 위상이 달랐다. [실패 보고](../qa/reports/latch016_rejection.json), 원본 후보 및 캡처 보존.017은4사이클을 더해76으로 맞춘 뒤 실제115353시점과 전체2521화면 검증을 통과했다. 실패 기준을 넓혀 통과시키지 않았다.

## 재현

```powershell
$OutputEncoding=[System.Text.UTF8Encoding]::new($false)
$env:PYTHONIOENCODING='utf-8'
python scripts/build_ui_native_latch.py --output build/dialogue_kr_poc_017_reproduce_NEW
python scripts/verify_ui_native_latch_hooks.py --build build/dialogue_kr_poc_017 --report qa/reports/latch017_hooks_NEW.json
python scripts/verify_ui_native_latch.py
python scripts/audit_ui_font_latch_session.py
```

과거 검증/감사 보고를 새 SSOT로 재실행하지 않는다. 실제 캡처 명령·입력·도구·스크립트 해시는 각 environment.json에 고정된다. 새 실행에는 새 QA 폴더를 사용한다.

ROM SHA256 `57be85f5994ae0ebeb605dfc2ea82d920797e6496815f5b67be55e600eac9aa7`  
IPS SHA256 `c3334a9061daa1743299c059724bd23c273317d57fc8339430700df8d9e3f288`  
CSV SHA256 `76bcc0d985c41dff6ce19cf0dd1a8a02e58bbb6814ca0b2f26e9e8239b9e8c48`

## 미해결과 다음 행동

06F3 소유권은 관측한 도입·홈·매표소·카트 경로에 한정해 확인했다. 다른 스테이지/분기, 교환 성공, 골드·일반 티켓 변수, 영문 그림·크레딧, 전체 텍스트 수집은 남는다. 전체 플레이·오디오·reset/savestate·실기·최종 사람의 명칭/번역/디자인 검토는 미수행이며 개발 빌드다. 배포나 외부 게시 없음. 카페 최종 작업기는 전체 작업 완료 후 작성한다.

다음 작업 하나: 홈 선택명과 매표소 안내에 쓰이는 macro83..88의 중복 glyph/00 위치 제약을 native reader로 검사하고, 미번역 소비기에 영향을 주지 않는 한글 인코딩 범위를 확정한다. 검증과 인계 후 즉시 이어간다.
