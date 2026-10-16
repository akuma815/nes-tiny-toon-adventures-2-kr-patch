"""Bound remaining-three facts to current049 and present scope choices without guessing consumers."""
from pathlib import Path
import hashlib, json
from title_codec import unpack
from seal_nonplay171 import R, sha, seal

def h(data): return hashlib.sha256(data).hexdigest()

def prg_offset(data, virtual_bank, address):
    assert 0x8000 <= address < 0x10000
    return 16 + ((virtual_bank & 63) % (data[4] * 2)) * 8192 + (address & 0x1fff)

def main():
    folder=R/'workspace/review/remaining049_172'
    report=R/'qa/reports/nonplay172_remaining_facts.json'
    assert not folder.exists() and not report.exists()
    meta=json.loads((R/'manifests/source_rom.json').read_text('utf-8'))
    source=R/meta['path'];rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
    ssot=R/'workspace/translation/text_ja.csv';s=source.read_bytes();c=rom.read_bytes()
    inventory=json.loads((R/'workspace/translation/nonplay_inventory049_169.json').read_text('utf-8'))
    assert sha(source)==inventory['source_sha256']==meta['sha256']
    assert sha(rom)==inventory['ROM_sha256'] and sha(ssot)==inventory['SSOT_sha256']
    # Verified logical bank names map differently after PRG expansion.
    spans=[('normal_stage_skip',0x3e,0xcd49,0xcd73),
           ('root3_inline_dispatch',0x3e,0xcd3e,0xcd49),
           ('NT_RAM06D0_supplier',0x3e,0xcc02,0xcc20),
           ('NT_RAM06E5_supplier',0x3f,0xf97a,0xf988),
           ('title_number2_and_prompt_setup',0x3e,0xcc7d,0xccb3),
           ('diagnostic_queue_data',0x32,0x81b2,0x81c7)]
    code=[]
    for name,bank,start,end in spans:
        a=prg_offset(s,bank,start);b=prg_offset(c,bank,start)
        before=s[a:a+end-start];after=c[b:b+end-start];assert before==after
        code.append({'ID':name,'logical_bank_hex':f'{bank:02X}','CPU_start_hex':f'{start:04X}','CPU_end_exclusive_hex':f'{end:04X}',
            'source_file_offset_hex':f'{a:X}','current_file_offset_hex':f'{b:X}','bytes':end-start,'sha256':h(before),'equal':True})
    assert prg_offset(s,0x32,0x8bf9)==0x4c09 and prg_offset(c,0x32,0x8bf9)==0x24c09
    assert s[0x1cd53:0x1cd59]==bytes.fromhex('49cd73cd37ce')
    assert c[0x3cd5f:0x3cd62]==bytes.fromhex('4c37ce')
    assert c[0x3cd67:0x3cd6c]==bytes.fromhex('a909201381')
    pointer=int.from_bytes(c[0x240ed:0x240ef],'little');assert pointer==0x8bf9
    raw=s[0x4c09:0x4c6c];assert raw==c[0x24c09:0x24c6c]
    nt,n=unpack(raw);assert n==99 and len(nt)==1024
    assert min(nt)==0x2000 and max(nt)==0x23ff
    assert s[0x37c10:0x38010]==c[0x57c10:0x58010] # source bank95 to current prefix bank95.
    # Existing112 was047: reuse source consumer bounds, do not upgrade its runtime observations to049.
    supplier=R/'qa/reports/nt112_supplier_bounds.json'
    old=json.loads(supplier.read_text('utf-8'));assert old['source_sha256']==sha(source)
    callsite_bytes=[]
    for row in old['direct_JSR8025_sites']:
        a=row['source_file_offset'];before=s[a-3:a+3];after=c[a+0x20000-3:a+0x20000+3]
        assert before==after
        callsite_bytes.append({'source_file_offset_hex':f'{a:X}','current_file_offset_hex':f'{a+0x20000:X}',
            'supplied_selector':row['selector'],'bytes_equal':True})
    facts=[
        {'ID':'RYO51_PAGE17','kind':'原本 타이틀 타일의 서명 모양'.replace('原本','원본'),
         'source_bank':95,'current_source_bytes_preserved':True,
         'confirmed':'RYO51 모양이 있는 마지막 행은 타이틀 숫자2 스프라이트 및 기존049 타이틀720 OAM에서 쓰이지 않았다.169의 실제 자료와 현재 정적 코드가 근거다.',
         'unresolved':'작성자·다른 장면 소비·전역 미사용은 미확정.',
         'ordinary_display_connected':False,'evidence':['qa/reports/nonplay169_scope_title_consumer.json','extracted/chr/survey_20261004_001/chr_page_17.png'],
         'scope_decision':'pending'},
        {'ID':'NT1C','kind':'호출자·폰트 미연결 배경 데이터',
         'source_file_offset_hex':'4C09','current_file_offset_hex':'24C09','encoded_bytes':99,'decoded_NT_cells':1024,
         'source_sha256':h(raw),'current_source_bytes_preserved':True,
         'confirmed':'네임테이블 포인터와 압축 원천은 정상이다. 기존112의 명명된 공급 경로19개는1C를 공급하지 않는다. 현재049의 해당10호출지점 바이트도 보존됐다.',
         'unresolved':'모든 간접 호출·별도 진입·실제 폰트가 폐쇄된 것은 아니다. 문자 또는 장식으로 확정하지 않는다.',
         'ordinary_display_connected':False,'evidence':['qa/reports/nt112_supplier_bounds.json','qa/reports/candidate119_NT1C.json'],
         'scope_decision':'pending'},
        {'ID':'DIAGNOSTIC_STAGE_SELECT','kind':'일반 진입에서 건너뛰는 진단 UI 후보',
         'source_file_offset_hex':'41C2','current_file_offset_hex':'241C2','current_source_bytes_preserved':True,
         'confirmed':'일반root3의 target은CD49/CD73/CE37이며CD4F는CE37로 점프한다. CD52의 STAGE SELECT 후보 호출은 이 초기화 경로에서 건너뛴다. 관련 코드/데이터가현재049에서도보존됐다.',
         'unresolved':'실제 표시 폰트와 계산 진입·다른 state writer의 전역 도달성은 미확정.',
         'ordinary_display_connected':False,'evidence':['qa/reports/stage110_analysis.json','qa/reports/printer113_catalog.json'],
         'scope_decision':'pending'}]
    options=[
        {'ID':'preserve_original_for_this_scope','expected_change':'세 원천을 이번 범위에서 원문 유지. ROM/숨겨진 UI 변화 없음.',
         'gain':'현재 구현을 사용자 플레이 검수에 사용할 수 있게 범위를 확정한다. 알려진 본문/그림54/33에는 변화가 없다.',
         'effort':'결정 원장과 검토/지원 문서 반영. 소비 조사를 추가하지 않음.',
         'limit':'실제로 표시될 경우 해당 원문이 남을 수 있다. 전역 미사용·원천 전체 완결성·최종 배포 승인이 아님.'},
        {'ID':'investigate_consumers_then_translate','expected_change':'소비와 의미를 먼저 연결한 뒤 필요할 때 번역·삽입.',
         'gain':'숨겨진 표시가 존재한다면 추가 문구를 번역할 가능성.',
         'effort':'계산 호출/상태·폰트 공급 조사. 일반 플레이에서 나타나면 사용자 장면/입력 증거도 활용. 소요와 결과는 미확정.',
         'limit':'실제 소비가 연결되기 전에는 추측 패치나 진단 UI 활성화를 하지 않는다. 현재049는 유지.'}]
    result={'work':172,'status':'PASS_BOUNDED_CURRENT049_REMAINING_FACTS_SCOPE_PENDING',
        'source_sha256':sha(source),'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),'code_data_spans':code,
        'ten_named_NT_callsite_bytes_current049_equal':callsite_bytes,'facts':facts,'options':options,
        'explicit_scope_decisions_for_these_three':False,'global_corpus_closed':False,'new_CPU_or_emulator_or_gameplay':False,
        'historical047_consumer_observations_not_promoted_to_current049_runtime':True,'release_eligible':False,
        'auditor171_note':'Old3.3.0 environment skill cache link expired. Audit v2 reports this one historical external reference separately while enforcing every project-local path and all artifact hashes.'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    folder.mkdir()
    (folder/'scope_options.json').write_text(json.dumps({'work':172,'baseline_ROM_sha256':sha(rom),'facts':facts,'options':options,
        'human_decision':'pending','global_unused_proven':False},ensure_ascii=False,indent=2)+'\n','utf-8')
    text='''# 남은 세 원천의 범위 선택 · 현재049

현재 확인된 본문54원천/45초안·9공유 단위와 그림33문구는 동일하다. HOWTO·PAUSE·POW 원문 유지 결정은 이미 확정되어171 적용 패키지에 반영했다. 아래 세 원천은 그 결정에 포함되지 않는다.

| 원천 | 현재 확인한 사실 | 남은 불확실성 |
|---|---|---|
| RYO51 | 원본 타이틀 타일의 서명 모양. 숫자2와 지정한 타이틀 OAM에서는 사용되지 않음 | 작성자·다른 표시 경로 |
| NT1C | 정상 압축99바이트→1024셀. 명명된19공급 경로에없음 | 간접 호출·소비 폰트, 문자/장식 여부 |
| STAGE SELECT | 일반 stage 초기화에서 건너뛰는 별도 printer 후보 | 실제 표시 폰트·다른 진입 |

모두현재049에 원천바이트 그대로 보존했다. 미사용으로 확정한 것이 아니다. 기존170 review.html에서 관련CHR정적자료/근거를볼수있다. 새로운게임실행은하지않았다.

선택A — 이번 범위에서 원문 유지: 세 원천을 추가 번역하지 않고 문서의 범위를 확정한다. 게임/진단 UI는 바뀌지 않는다. 표시될 경우 해당 원문이 남을 수 있다. 전역 미사용·원천 전체 완결성·최종 문구/그림/배포 승인으로 확대하지 않는다.

선택B — 소비 확인 후 번역: 계산 호출·상태·폰트 공급을 추가 조사한다. 일반 플레이 중 나타나면 사용자 장면/입력 증거도 활용한다. 실제 표시가 존재한다면 추가 번역 가능성이 있지만 소요/개선 여부는 미확정이다. 소비 확인 전 추측 패치를 하지 않는다.

결정 양식: 이번 범위 원문 유지 / 소비 확인 후 번역. 세 원천 중 일부만 다르게 선택해도 된다. 현재 상태는pending이다. 실제 플레이 검수와 최종 말투·명칭·그림 결정은 별도로 남는다.
'''
    (folder/'DECISION_OPTIONS.md').write_text(text,'utf-8')
    (folder/'artifact_manifest.json').write_text(json.dumps({'work':172,'files':{p.name:sha(p) for p in folder.iterdir() if p.is_file()}},indent=2)+'\n','utf-8')
    body=f'''현재049의미연결3원천을 [판단 자료](../{folder.relative_to(R).as_posix()}/DECISION_OPTIONS.md)와 [JSON 선택지](../{folder.relative_to(R).as_posix()}/scope_options.json)로 정리했다. [정적 보고](../{report.relative_to(R).as_posix()})는 원본/현재PRG 확장에따른bank주소를계산하고 native확인구간6개·NT호출지점10개·NT1C의포인터/99바이트/1024셀·CHR95의1024바이트보존을대조했다. source32/3E/3F의뱅크값은hex기준이며 sourcePRG8개16KiB/current16개16KiB의각8KiB계산을사용했다. source/현재오프셋을보고에기록했다.

이검사는 기존047의자연/진단소비관측을049런타임검증으로바꾸지않는다. 기존112는명명한19공급경로에1C가없다는범위이며전역CFG부재증명이아니다. CD49/CD73/CE37 root3대상과CD4F→CE37은현재049에서도보존돼CD52 STAGE SELECT 초기화를일반경로에서건너뛴다. RYO51은지정한타이틀숫자2/OAM에없을뿐다른표시나작성자는미확정이다. 동등한부재관측/CPU사례/에뮬레이터반복을추가하지않았다.

선택지는(1)세원천이번범위원문유지:ROM변경없음·추가소비조사없음·표시될경우원문남음가능,(2)소비확인뒤번역:계산호출/상태/폰트및필요시사용자관측조사·추가번역가능하지만비용/개선여부미확정이다. 기존HOWTO/PAUSE/POW 보존승인을이세건으로확대하지않는다. 답변은pending이며최종배포/전역원천완결성도false다. 현재구현결과와추가작업선택은분리한다.

171감사에서과거 [성 통화문서](CASTLE_CURRENCY_QA.md)의외부환경 스킬3.3.0캐시파일이플러그인3.4.0갱신으로없어져기존전체링크검사가실패했다. 원본/1편/171동결자산은일치했다. [실패 보고](../qa/reports/nonplay171_audit_v1_failure.json)와새감사기를보존했다. [171감사v2](../qa/reports/nonplay171_session.json)는모든프로젝트내부링크/자산SHA를엄격히검사하고그정확한옛외부캐시참조1건만별도누락으로보고했다. 역사문서·옛지침을덮어쓰거나가짜복원하지않았고전체외부링크존재를PASS로표현하지않았다. 새증거와문서검증에3.4.0의실제경로/SHA를기록했다.

ROM `{sha(rom)}`,CSV `{sha(ssot)}` 불변. 변경은172정적기/판단자료/보고/인계·현재계획/journal/canonical·manifest와171감사보완산출물이다. 신규CPU/빌드/적용/에뮬레이터/장면시각/플레이/청음없음.171최종ZIP의실제적용/170문서표시PASS는해당범위근거로재사용한다. 실제플레이사용자담당이며카페완성작업기는전체완료뒤작성한다. 재현 `python scripts/prepare_remaining172.py`; 감사 `python scripts/audit_project_links171_v2.py --manifest manifests/nonplay172_assets.json --output qa/reports/nonplay172_session.json`. 기존출력보호와각산출물SHA는manifest를따른다.'''
    files=[Path(__file__),report,source,rom,ssot,R/'workspace/translation/nonplay_inventory049_169.json',supplier,
        R/'qa/reports/nonplay169_scope_title_consumer.json',R/'qa/reports/stage110_analysis.json',R/'qa/reports/printer113_catalog.json',
        R/'qa/reports/candidate119_NT1C.json',R/'qa/reports/nonplay171_final.json',
        R/'qa/reports/nonplay171_audit_v1_failure.json',R/'scripts/audit_project_links171_v2.py',R/'qa/reports/nonplay171_session.json']
    files.extend(p for p in folder.iterdir() if p.is_file())
    seal(172,'CURRENT049_REMAINING_THREE_SCOPE_OPTIONS.md','미연결3원천 현재 근거·범위 선택지',body,
        'RYO51/NT1C/진단STAGE SELECT 현재049 코드/원천보존과한계를분리.원문유지/소비조사후번역 선택지준비·결정pending.171의옛외부스킬캐시링크누락을별도보고/내부자산감사PASS. ROM/CSV불변.',
        '남은3원천에 대한 사용자의 범위 선택을 기록하고 그 결정 범위만 현재 검토자료와 적용 패키지 설명에 반영한다.',files)
    print(json.dumps({'work':172,'status':result['status'],'unresolved':3,'decision_options':2,'ROM_sha256':sha(rom),'new_emulator_or_CPU':False},indent=2))

if __name__=='__main__':main()
