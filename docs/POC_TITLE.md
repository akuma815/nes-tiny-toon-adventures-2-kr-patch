# 타이틀 한글화 — PNG / 생성형 이미지 / NES 재삽입

2026-10-04. **1편과 같은 방식으로 구현 가능하며 실제 ROM에서 동작하는 실험본까지 검증했다.** 채택 빌드는 `title_kr_ai_003`. 전체 게임 한글화나 정식 배포 완료를 뜻하지 않는다.

![실제 Mesen 타이틀 화면](../qa/title/title_kr_ai_003_actual_4x.png)

## 표시 문구와 결과 파일

게임명은 `타이니 툰 / 어드벤처`, 일본어 부제는 `몬타나랜드에 어서 오세요`, 아래 작은 보조 문구는 `타이니 툰 어드벤처`로 처리했다. 원본 숫자 `2`, 붉은 리본 외곽, `PUSH START`, 저작권 문구는 보존했다. 이 결정은 이번 타이틀에 한정하며 2편의 모든 영문을 유지하는 정책을 새로 확정한 것은 아니다.

- [실험 ROM](../build/title_kr_ai_003/TinyToon2_title_kr_poc.nes), [실험 IPS](../build/title_kr_ai_003/TinyToon2_title_kr_poc.ips), [IPS 해시](../build/title_kr_ai_003/TinyToon2_title_kr_poc.json).
- [원본/수정 실제 화면 비교](../qa/title/title_kr_ai_003_comparison.png), [검증 보고서](../qa/reports/title_kr_ai_003_validation.json).
- [입력 원천 manifest](../manifests/title_assets.json), [실제 배치/소비 명세](../manifests/title_layout.json), [Expected Writes](../build/title_kr_ai_003/expected_writes.json).

## 1편에서 계승한 흐름과 2편의 차이

1편 `docs/POC_TITLE.md`, `scripts/extract_title.py`, `scripts/build_title.py`, `scripts/title_ips.py`를 읽기 참고했다. 원본 PNG, AI PNG, NES 변환 PNG, 실제 ROM 캡처를 분리하는 흐름과 해시 기반 IPS 적용기를 계승했다. 1편의 CHR 주소와 RLE 디코더는 이식하지 않았다.

2편은 화면 중간 IRQ로 패턴 뱅크와 네임테이블을 바꾼다. 프레임 끝 PPU 패턴 메모리만 추출하면 상단 로고의 실제 페이지를 놓친다. 숫자 2도 배경과 별도인 8×16 스프라이트다.

| 영역 | 원본 실제 경로 | 편집 및 보호 |
|---|---|---|
| 상단 로고 | CHR page17, ROM `0x37010`, NT `$2000`, 논리 박스 x40..215/y24..111 | PNG176×88; 전용 타일1..AC 중157/172 사용 |
| 부제/보조 문구 | CHR page19, ROM `0x39010`, NT `$2800`, 논리 박스 x32..223/y112..143 | PNG192×32; 타일1..3E 및4F..66의86/86 사용 |
| 리본 화면 위치 | IRQ scanline111/112, 논리 좌표보다 화면 y가2픽셀 위 | 정적 미리보기·비교 마스크에 dy=-2 반영 |
| 숫자2 | OAM, CHR1KiB bank95의 스프라이트 패턴 | 해당 패턴·OAM·겹친 화면 픽셀 보존 |
| 외곽/시작/저작권 | 공유 배경·스프라이트·원본 팔레트 | 전용 타일과 내부 문구만 수정, 타일0 공유 보호 |

전용 타일 판정은 **타이틀 네임테이블 안의 편집 박스 밖 참조**를 기준으로 한다. 모든 미방문 장면에서의 공유 여부까지 증명한 것은 아니다.

### 배치 데이터 소비까지 확인

[CHR 복사 추적](../qa/title/chr_stream_trace_001/chr_stream_copies.csv)은 frame593의 두 복사에서 selector04/06, PPU `$1129..$1197` / `$1197..$11FB`, 실제 CHR 상대 주소`0x4929/0x4997`을 기록했다. `copy_1.bin`, `copy_2.bin`이 아래 원본 구간과 정확히 같다.

| 스트림 | ROM 파일 범위(끝 제외) | 원본 길이 | 수정 유효 길이 |
|---|---|---:|---:|
| main | `0x24939..0x249A7` | 110 | 63 |
| ribbon | `0x249A7..0x24A0B` | 100 | 90 |

배치 스트림은 PRG가 아닌 CHR에 들어 있다. bank2의 `$81F8` 경로가 임시 CHR bank18을 PPU로 읽어 RAM `$0400`에 복사하고 `$8216`에서 디코더를 호출한다. 디코더의 PPU 쓰기는 `$806E`, `$808B`, `$80A0`이며 콜백이 보고하는 PC는 다음 명령 주소다. 두 스트림 모두1024바이트를 전개하고 원본 NT 전체/속성64바이트와 일치했다.

2편 규약은 `FF` 종료, `7F` 새 PPU 목적지, 반복/리터럴/증가열이다. `00`은256번 반복이며 padding이 아니다. 빌더는 이 규약에 맞춘 최단 인코딩 후 자체 디코더로1024바이트 전체를 대조한다. 두 스트림의 기존 경계와 ROM`0x4249`의 포인터`97 11`은 이번 빌드에서 바뀌지 않았다. 원래 총210바이트 공간을 넘지 않고 PRG 후크나 ROM 확장도 필요하지 않았다.

## 이미지 원천과 변환

| 단계 | 보존 위치 |
|---|---|
| 원본 추출 | `extracted/title/title_20261004_001/`의 main/ribbon_original.png 및8배 PNG |
| 생성형 게임명 | `workspace/graphics/title/ai_main_001/main_ai_raw.png`, PROMPT.txt |
| 생성형 리본 문구 | `workspace/graphics/title/ai_ribbon_001/ribbon_ai_raw.png`, PROMPT.txt |
| 작은 글자 교정 생성 | `workspace/graphics/title/ai_caption_002/caption_ai_raw.png`, PROMPT.txt |
| NES 최종 픽셀 | `build/title_kr_ai_003/main_nes.png`, ribbon_nes.png 및8배 PNG |
| 정적 미리보기 | `build/title_kr_ai_003/title_static_preview.png` |
| 실제 실행 화면 | `qa/title/title_kr_ai_003_attract/`, title_kr_ai_003_start/ |

내장 `image_gen`으로 생성했고 API/CLI fallback은 쓰지 않았다. 생성 도구의 원본 출력은 프로젝트에 복사했다. PROMPT.txt는 생성 요청 명세이며 작은 글자 교정 파일에는 도구에 전달한 정확한 문구를 보존했다. 외부 한글 폰트는 이번 빌드에 사용하지 않았다.

게임명은176×88으로 BOX 축소하고 실제 원본4색으로 양자화했다. 부제는 원본 리본 외곽을 유지하고 AI 이미지의 흰 글자만 추출해148×14로 변환한다. 작은 문구는 교정한 별도 AI PNG를100×8로 변환한다. 외곽 픽셀 침범, 타일 예산 초과, 압축 예산 초과는 출력 전에 실패시킨다.

작은 문구는8픽셀 높이여서 자소 간격과 가독성에 여유가 적다. 큰 로고와 부제를 주 표시로 확인했고 보조 문구의 최종 미감·가독성은 사용자 디자인 검토 대상으로 남긴다. 자동 검사로 한글 철자나 디자인 승인을 대신하지 않는다.

## 시행착오와 채택 제외

- `data_trace_001`: PRG의 유사 패턴을 좇았지만 타이틀의 실제 데이터 소비 근거를 얻지 못했다. CHR 복사 추적으로 경로를 확정했다.
- `title_kr_ai_001`: 작은 글자를 두 번 축소하면서 획이 손실됐고 리본 정적 합성의 dy=-2도 미반영했다. 채택 제외.
- `title_kr_ai_002`: 고해상도에서 글자를 분리해 축소를 개선했지만 AI 원천의 작은 `툰` 형태가 부정확하고 정적 합성 위치도 수정 전이었다. 채택 제외.
- 작은 문구만 추가 생성해 교정했다.112×8 첫 배치는 원본 리본 외곽`(182,136)` 침범으로 빌드가 **출력 전 거부**했다.100×8/논리 x80으로 조정해 보호 픽셀을 보존했다.
- 화면 합성은 리본 y=-2와 숫자2의 원본 스프라이트 겹침을 반영했다. 최종 정적 미리보기와 실제 frame720이 픽셀 단위로 일치한다.

초기 추출 manifest의 `layout_consumer` 미해결 기록은 당시의 역사로 보존한다. 이후 확정 기준은 `manifests/title_layout.json`이다. 위치 보정한 추출기에서 새 경로`title_repro_002`로 재추출해 두 원본 PNG의 파일 바이트 동일도 확인했다.

## 검증을 구분한 결과

**정적:** 원본 SHA 유지. 원본 PNG→타일→ROM 왕복은 원본 ROM과 완전히 같다. 수정 빌드는244개 Expected Write와 전체3209바이트 diff를 대조했고 중첩·소유 범위 이탈이 없다. 헤더, 전체 PRG, 팔레트, NT 속성, 숫자2 패턴, 편집 외 배경 픽셀을 보존했다. 번역 CSV와 초기 감사에 등록한1편 원본/문서/배포 ZIP 해시도 같다.

**빌드/적용:** 같은 AI PNG3개로 재빌드한 ROM, 별도 Python 프로세스로 한글·공백 경로에 IPS를 실제 적용한 ROM이 모두`d7e8870c98909339486ae6448346d6ba2c65dbaacbe7861fab05bbe35ad8737a`와 같다. IPS SHA는`6f6d7c46409ed1b638cdd0651695d4015ce17b7ca75a2b79320d56341118af39`. 정식 Windows 배포 적용 도구는 아직 만들지 않았다.

**에뮬레이터:** 격리 Mesen2.1.1에서 무입력5400프레임과 Start720..727의3000프레임, 모두 종료0. 같은 실행 파일·설정·입력의 원본 캡처72개와 비교했다. 타이틀7표본만 한글 그림이 달라졌고65표본은 전체 화면 동일, 타이틀 허용 마스크 밖 차이는 전부0픽셀이다. 모든72표본의 OAM과32바이트 팔레트도 원본과 같다. 자연 데모 후 frame3360/3480/3600에서 한글 타이틀로 재진입한다. 별도의 리셋·세이브스테이트 재개 테스트는 하지 않았다.

원본은 Mesen DB의 Famicom/KONAMI-VRC7 설정을 썼고 수정 CRC는 DB에 없어 헤더 mapper85/sub0/Horizontal로 실행됐다. 두 로그를 보존하고 명시적 컨트롤러 설정을 사용했다. 이 차이는72화면 비교에서 이상을 보이지 않았지만 다른 모든 장면/실기 동일성까지 보장하지 않는다.

**직접 장면 시각:** 원본과 한글 게임명/부제 생성 이미지, NES 변환 그림, 실제 타이틀 확대와 비교표의 콜드부팅720·자연 재진입3360·Start 후 홈1080·도입 대사1920을 직접 확인했다. 로고/리본/숫자2 중첩과 홈 화면을 확인했다. 이는 사용자 최종 디자인 승인이나 전체 장면 QA가 아니다.

미수행: 전체 완주, 미방문 장면 공유 타일 QA, 실기, 오디오 청취, 대사 한글 삽입, 사용자 최종 디자인 승인, 정식 배포, 카페 게시.

## 재현 명령

프로젝트 루트에서 실행한다. `_next` 경로는 존재하지 않는 새 경로로 바꾼다. 최종 빌더는 동결한 추출`title_20261004_001`을 사용한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_source.ps1
python .\scripts\extract_title_png.py --output .\extracted\title\title_extract_next
python .\scripts\build_title.py --main-png .\extracted\title\title_20261004_001\main_original.png --ribbon-png .\extracted\title\title_20261004_001\ribbon_original.png --roundtrip --output .\build\title_roundtrip_next
python .\scripts\build_title.py --main-png .\workspace\graphics\title\ai_main_001\main_ai_raw.png --ribbon-png .\workspace\graphics\title\ai_ribbon_001\ribbon_ai_raw.png --caption-png .\workspace\graphics\title\ai_caption_002\caption_ai_raw.png --output .\build\title_kr_next
python .\scripts\title_ips.py apply --source '.\original\rom\Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes' --patch .\build\title_kr_ai_003\TinyToon2_title_kr_poc.ips --output '.\qa\title\한글 적용 다음\TinyToon2_title_kr_applied.nes'
python .\scripts\run_title_qa.py --rom .\build\title_kr_ai_003\TinyToon2_title_kr_poc.nes --output .\qa\title\title_attract_next --frames 5400
python .\scripts\run_title_qa.py --rom .\build\title_kr_ai_003\TinyToon2_title_kr_poc.nes --output .\qa\title\title_start_next --frames 3000 --start 720
python .\scripts\verify_title.py
```

`verify_title.py`는 채택003과 기존 동결 증거를 감사한다. 새로운 캡처를 만들었다고 이 스크립트가 자동으로 신규 경로를 검증하는 것은 아니다. 생성형 이미지는 매번 달라질 수 있으므로 재현은 동결 PNG의 해시를 기준으로 한다.

**다음 작업 하나:** 실제 타이틀 화면을 기준으로 로고와 작은 보조 문구의 최종 디자인을 검토한다.
