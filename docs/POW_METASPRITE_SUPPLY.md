# 작업96 — POW 후보의 native 스프라이트 조립 경로

현재047/CSV를변경하지않았다. ROM82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10, CSVac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556, 원본/1편/모든기존근거유지. [정적분석기](../scripts/analyze_pow_metasprites096.py), [보고서](../qa/reports/pow096_static.json), [selector CPU목록](../work/pow_consumer_096/common_selector_cpu_records.json).

즉시bank61 지정의원본motif A9 3D 85 38은 file5E47/1260D/1F717의3곳이다. 각각CPU9E37/menu초기화, A5FD/스테이지초기화후보, F707/게임오버에해당한다.3곳모두현재047의대응PRG와같다. A5FD의실제실행/게임명은이번정적조사로확정하지않았다. native FD67 mapperwrite를source/047 CPU로재현해274cycles와8포트쓰기 exact를확인했다. RAM38은D000으로가며 historical84 NMItop의PPU1800=0F400 실제매핑으로source61에연결된다. RAM34·35는2KiB반복쌍이고36/37·38/39는각1KiB쌍이라sprite tile 번호에 그대로local bankindex를쓸수없다.

native bank36의9643 조립기는 common1..127/128..191과 stageC0..FF의다른포인터표를선택하고, 음수header는공유geometry포인터+별도tilelist를쓴다. 잠재common selector191개에대해course0..4/source·047의1910 CPUcase가같은cycles/레지스터/OAM으로종료했다. 이는191개모두저작/유효/도달가능함을증명하지않고stage-only인C0..FF와0을포함하지않는다.

frame18/19/3C/3E/7C/9D/9C의7개descriptor를별도geometry/tilelist 해석기로풀어native CPU OAM과exact확인했다. source61을PPU1800에가정했을때18/19와몇회전후보가POW원형그림이되고 **3E는깃발**이된다. [정적조립그림](../work/pow_consumer_096/metasprites_native096_static.png)을직접봤다. 설명팔레트와인위좌표의정적분석그림이며실제게임이미지가아니다. 앞선 [8후보초기분석그림](../work/pow_consumer_096/candidate_metasprites_analysis.png)/[초기기록](../work/pow_consumer_096/candidate_records.json)도보존한다. 의미/번역명을결정한자료가아니다.

기존046네경로/36k카트/현재047골드4성경로의동결RAM snapshot을해시확인하여 RAM38=61+active 해당7ID의조합을찾았으나0개였다. 이것은 제한된end-frame표본검사이며PPU소비/전역미사용증명과구분한다. historical84의 실제PU매핑도046에한정된다. source61에서기존모든그림byte가유지되는것을확인했지만POW의번역/보존 최종사람결정이나생성형수정은하지않았다.

새게임runtime·재빌드·apply는없고정적CPU/과거관측재검토만했다. 게임오버깃발같은동일bank내알려진소비를positive control로새추적해관측기가실제PPU읽기/OAM/제작자조건을연결하는지확인할필요가있다. 전게임완주/전역corpus폐쇄/실기/PCM청음/최종사람검토는미완료,카페완성작업기/외부게시없음.

재현: `python scripts/analyze_pow_metasprites096.py`는동결PNG/보고서가있으면쓰기거부한다. [동결manifest](../manifests/pow096_assets.json).

다음 작업 하나: 현재047 게임오버의source61깃발을positive control로실행해native frame3E→OAM83→PPU패턴읽기·실제PNG를연결하고, 같은관측기에서POW후보frame의생산자도기록한다.
