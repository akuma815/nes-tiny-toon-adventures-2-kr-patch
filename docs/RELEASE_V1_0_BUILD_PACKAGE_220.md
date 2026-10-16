# 작업220 — 최종배포 v1.0 빌드·ROM없는 적용패키지

사용자의 최종배포 요청에 따라062와 동일한 데이터를 v1.0로 고정했다. [배포 ZIP](../dist/TinyToonAdventures2_KR_v1.0_20261009.zip) SHA `c78120f4c16c91245535270730087a25ef64ce07531e7bc4164c053018c270ad`. [적용 안내](../dist/TinyToonAdventures2_KR_v1.0_20261009/README_적용방법.txt). [로컬 ROM](../build/release_v1_0_220/TinyToon2_KR_v1.0.nes) SHA `7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce`. publicZIP은ROM없이13파일이다.

build_credits11_211.py의 새 독립출력으로062 ROM/IPS를 재생성하고 기존062와 byte-exact 비교했다. 원본에서ExpectedWrites 10개를 replay해 중첩0/기대원본일치/최종전체동일을 확인했다. 최종IPS를원본에적용한결과도동일하다. source·CSV·기존ROM/보고/ZIP을변경하지않았다. [빌드 보고](../build/release_v1_0_220/release_build.json), [패키지 보고](../qa/reports/release220_verified.json).

Windows 정상적용·기존출력거부·원본=출력거부·동일크기타판본거부·이미패치본거부·손상패치거부·손상도구거부·인자없음8사례를실행했다. 한글/공백경로 최종ZIP 추출본apply.cmd도전체결과byte-exact PASS. CRC/파일목록/페이로드/ROM-free확인. tool·font라이선스포함.

정적/CPU근거는동일062의211/216~218에한정해계승한다. 실제062エ뮬레이터/장면/완주/가독성검수는미기록·사용자담당이며배포요청을완주승인이나CSV사람검토로바꾸지않았다. 원천45draft/9macro-template 상태도보존했다. release_report와플레이어안내가같은한계를명시한다. 이전버전저장상태호환도미확인이다. 사용자요청에따라파일은최종배포용으로구성했으나전게임완료율/최종QA승인을주장하지않는다.

변경: release220.py,새빌드/패키지/ZIP/해시/보고와인계. 재현: python -B scripts/release220.py (고정출력덮어쓰기거부,새경로복제에서실행). 이번시행의에뮬레이터/컨트롤러실행/외부업로드없음. 카페작업기는다음작업에서만든뒤불필요한펼친자료를정리한다.

다음 작업 하나: 네이버 카페 복사용 작업기·근거구분 PNG·오프라인 HTML을 만들고 데스크톱/모바일 렌더를 확인한다.
