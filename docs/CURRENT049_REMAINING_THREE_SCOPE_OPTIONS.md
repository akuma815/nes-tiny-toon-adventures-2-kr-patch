# 작업172 — 미연결3원천 현재 근거·범위 선택지

현재049의미연결3원천을 [판단 자료](../workspace/review/remaining049_172/DECISION_OPTIONS.md)와 [JSON 선택지](../workspace/review/remaining049_172/scope_options.json)로 정리했다. [정적 보고](../qa/reports/nonplay172_remaining_facts.json)는 원본/현재PRG 확장에따른bank주소를계산하고 native확인구간6개·NT호출지점10개·NT1C의포인터/99바이트/1024셀·CHR95의1024바이트보존을대조했다. source32/3E/3F의뱅크값은hex기준이며 sourcePRG8개16KiB/current16개16KiB의각8KiB계산을사용했다. source/현재오프셋을보고에기록했다.

이검사는 기존047의자연/진단소비관측을049런타임검증으로바꾸지않는다. 기존112는명명한19공급경로에1C가없다는범위이며전역CFG부재증명이아니다. CD49/CD73/CE37 root3대상과CD4F→CE37은현재049에서도보존돼CD52 STAGE SELECT 초기화를일반경로에서건너뛴다. RYO51은지정한타이틀숫자2/OAM에없을뿐다른표시나작성자는미확정이다. 동등한부재관측/CPU사례/에뮬레이터반복을추가하지않았다.

선택지는(1)세원천이번범위원문유지:ROM변경없음·추가소비조사없음·표시될경우원문남음가능,(2)소비확인뒤번역:계산호출/상태/폰트및필요시사용자관측조사·추가번역가능하지만비용/개선여부미확정이다. 기존HOWTO/PAUSE/POW 보존승인을이세건으로확대하지않는다. 답변은pending이며최종배포/전역원천완결성도false다. 현재구현결과와추가작업선택은분리한다.

171감사에서과거 [성 통화문서](CASTLE_CURRENCY_QA.md)의외부환경 스킬3.3.0캐시파일이플러그인3.4.0갱신으로없어져기존전체링크검사가실패했다. 원본/1편/171동결자산은일치했다. [실패 보고](../qa/reports/nonplay171_audit_v1_failure.json)와새감사기를보존했다. [171감사v2](../qa/reports/nonplay171_session.json)는모든프로젝트내부링크/자산SHA를엄격히검사하고그정확한옛외부캐시참조1건만별도누락으로보고했다. 역사문서·옛지침을덮어쓰거나가짜복원하지않았고전체외부링크존재를PASS로표현하지않았다. 새증거와문서검증에3.4.0의실제경로/SHA를기록했다.

ROM `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. 변경은172정적기/판단자료/보고/인계·현재계획/journal/canonical·manifest와171감사보완산출물이다. 신규CPU/빌드/적용/에뮬레이터/장면시각/플레이/청음없음.171최종ZIP의실제적용/170문서표시PASS는해당범위근거로재사용한다. 실제플레이사용자담당이며카페완성작업기는전체완료뒤작성한다. 재현 `python scripts/prepare_remaining172.py`; 감사 `python scripts/audit_project_links171_v2.py --manifest manifests/nonplay172_assets.json --output qa/reports/nonplay172_session.json`. 기존출력보호와각산출물SHA는manifest를따른다.

다음 작업 하나: 남은3원천에 대한 사용자의 범위 선택을 기록하고 그 결정 범위만 현재 검토자료와 적용 패키지 설명에 반영한다.
