# 작업78 — 공통 시작 안내 세 놀이기구 회귀

빌드045/원본/기존CSV 변경없이 롤러코스터·기차·급류의044/045를각4,200프레임씩순차coldboot했다. 각컨트롤러입력은같고RAM/ROM/PC/세이브/체력/화폐개입없음. [실행기](../scripts/run_start078_suite.py), [실행 명령/완료](../work/start_regression_078/suite_runs.json), [검증기](../scripts/verify_start078.py), [보고서](../qa/reports/start078_regression.json).

세쌍1,704PNG/10,278런타임파일(환경JSON제외)을확인했다.045의6,816개CHR1KiB조각은ROM과같고OAM/네임테이블/팔레트는044와같다. RAM 차이는34/35/3A/3B의122→222뿐이며420world행의차이도START font값뿐이다. 각쌍15PNG가96×32 시작영역안에서만바뀌고이후nativephase5게임진입을확인했다. 공통초기화의글꼴수명이각기다른배경으로정상복귀한것을검사한다.

직접시각: 각045의2670시작과3330플레이총6장면을확인했다. [롤러코스터](../qa/dialogue/start078_coaster045/frame_03330.png), [기차](../qa/dialogue/start078_train045/frame_03330.png), [급류](../qa/dialogue/start078_water045/frame_03330.png). 카트자연20k/기존두안내는 [77](START_KOREAN.md)을계승한다. 네놀이기구전체완주/모든방·분기/실기·청음/사람최종언어검토는아니다.

직접기차3330검토중도로표지 **STOP**가아직영문인것을새로발견했다. 기존몬타나철도간판font216..219와달리위쪽세계패턴일수있으므로폰트뱅크를가정해수정하지않는다. 실제소비추적/추출후 ‘정지’로옮길계획이다. 검토자료갱신에앞서알려진표시누락을수정한다.

현재ROM SHA15e9f17dcbaaa02778e6a28d5dcf9c318232508ca5fb0346a6e6303a2ff15350. [파일/SHA manifest](../manifests/start078_assets.json). 신규빌드/apply는이번에재실행하지않았으며77증거를유지한다.

재현: `python scripts/run_start078_suite.py` (고정출력없는복제공간) 또는 `python scripts/run_world_qa.py --rom build/dialogue_kr_poc_045/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_train_001.json`. 검증기는새보고서만허용한다.

다음 작업 하나: 실제기차 STOP 도로표지의글꼴/네임테이블/화면소비기를연결하고PNG로추출한다.
