"""Apply explicit scope answer and connect page0F PUSH START to existing title049 evidence."""
from pathlib import Path
import copy, csv, json
from analyze_pow_metasprites096 import run, parse
from seal_nonplay166 import R, sha, seal

def main():
    decision=R/'workspace/translation/scope_decisions_20261007_169.json'
    inventory_path=R/'workspace/translation/nonplay_inventory049_169.json'
    report=R/'qa/reports/nonplay169_scope_title_consumer.json'
    assert not any(p.exists()for p in [decision,inventory_path,report])
    prior=R/'workspace/translation/nonplay_inventory049_166.json'
    inventory=json.loads(prior.read_text('utf-8'))
    source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
    rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
    ssot=R/'workspace/translation/text_ja.csv';s=source.read_bytes();c=rom.read_bytes()
    assert sha(source)==inventory['source_sha256']and sha(rom)==inventory['ROM_sha256']and sha(ssot)==inventory['SSOT_sha256']
    explicit={'work':169,'date':'2026-10-07','question':'사용 경로가 미확정인 HOWTO·PAUSE·POW 그림은 현재 원문을 보존했습니다. 이번 한글화에서는 어느 범위로 진행할까요?',
        'user_answer':'이번 범위에서는 원문 유지','approved_by':'user','source':'Explicit user reply to scope question in this session',
        'decisions':[{'id':i,'decision':'preserve_original_for_this_scope','human_approved':True,'consumer_closed':False,'unused_proven':False}for i in ['HOWTO','PAUSE','POW']],
        'limit':'Only these three graphics in this localization scope. Not global English retention, unused proof, gameplay or overall final approval.',
        'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot)}
    decision.write_text(json.dumps(explicit,ensure_ascii=False,indent=2)+'\n','utf-8')
    # Native title setup and blinker contain an explicit63 sprite-bank supplier and8E actor.
    assert s[0x1cc99:0x1cc9d]==bytes.fromhex('a93f8537')
    assert s[0x1ccbe:0x1ccc3]==bytes.fromhex('a98e8d0404')
    assert s[0x1cc70:0x1cd26]==c[0x3cc70:0x3cd26]
    assert s[0x2fc10:0x30010]==c[0x4fc10:0x50010]
    cases=[];reference=None
    for course in range(5):
        m,a,o,steps=run(s,0x8e,course);n,b,p,steps2=run(c,0x8e,course)
        expected,descriptor=parse(m,0x8e)
        assert o==p==expected
        assert (a.a,a.x,a.y,a.p,a.sp,a.processorCycles)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles)
        assert sorted(o[1::4])==list(range(0x41,0x50,2))
        if reference is None:reference=(o,descriptor)
        else:assert reference==(o,descriptor)
        cases.append({'course':course,'source_current049_OAM_and_CPU_equal':True,'sprites':8,'cycles':a.processorCycles})
    q=R/'qa/dialogue/pages130_intro049';e=json.loads((q/'environment.json').read_text('utf-8'))
    assert e['exit_code']==0and e['rom_sha256']==sha(rom)
    paths=[q/f'frame_00720{x}'for x in ['.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv']]
    for p in paths:assert sha(p)==e['files'][p.name]
    ram=paths[1].read_bytes();ppu=paths[2].read_bytes();oam=paths[3].read_bytes()
    assert ram[0x37]==63and ram[0x404]==0x8e and ram[0x405]==0x31
    mappings=list(csv.DictReader(paths[4].open(encoding='utf-8')))
    at1400=[r for r in mappings if r['kind']=='chr'and r['cpu_or_ppu_address']=='1400']
    assert len(at1400)==1and int(at1400[0]['relative_offset'],16)==63*1024
    assert ppu[0x1400:0x1800]==s[0x2fc10:0x30010]
    selected=[list(oam[i:i+4])for i in range(0,256,4)if oam[i]<240and oam[i+1]in range(0x41,0x50,2)]
    assert len(selected)==8and sorted(v[1]for v in selected)==list(range(0x41,0x50,2))
    assert all(v[0]==156and v[2]==2for v in selected)
    assert sorted(v[3]for v in selected)==list(range(96,160,8))
    # Check the signature bank only in this named title actor/OAM context; no global-unused conclusion.
    _,_,number_oam,_=run(s,0x31,0)
    number_local_tiles=sorted({v for t in number_oam[1::4]for v in [t&0xfe,(t&0xfe)+1]})
    assert max(number_local_tiles)==21 and not set(number_local_tiles).intersection(range(48,64))
    title95_tiles=sorted({v for i in range(0,256,4)if oam[i]<240and(oam[i+1]&1)and oam[i+1]<0x40
                         for v in [oam[i+1]&0xfe,(oam[i+1]&0xfe)+1]})
    assert title95_tiles==number_local_tiles
    for item in inventory['outside_registered_candidates']:
        if item['id']in ['HOWTO','PAUSE','POW']:
            item.update(state='retained_by_explicit_scope',decision='preserve_original_for_this_scope',human_approved=True,
                decision_source=decision.relative_to(R).as_posix(),scope_work_closed=True)
            item['limit']+=' User retention decision closes localization scope work, not consumer investigation or unused proof.'
        elif item['id']=='PUSH_START_PAGE0F':
            item.update(state='connected_title_prompt_retained',decision='preserve_existing_title_scope',human_approved=False,
                scope_work_closed=True,consumer_connected=True,evidence_works=[166,169])
            item['facts']='Native CC89/CC8B supplies bank63 to RAM37; CCAE/CCB0 initializes actor8E. Native9643 descriptor emits eight8x16 sprites41..4F. Frozen049 title frame720 maps63 atPPU1400 and contains exact bank/OAM pixels.'
            item['limit']='Existing130 screenshot/PPU/OAM reused; no new emulator. This is the preserved title PUSH START, not a new unlinked string.'
            item['proposal']='기존 타이틀 보존 범위에 연결. 별도 신규 번역 건으로 중복 집계하지 않음.'
        elif item['id']=='RYO51_PAGE17':
            item['facts']+=' Title number2 actor31 uses bank95 local tiles0..21. Signature-containing last row48..63 is absent from the selected title720 OAM.'
            item['limit']+=' Bounded title context only; no global unused or authorship decision.'
            item['evidence_works']=[166,169]
    inventory['work']=169
    inventory['scope_decisions_file']=decision.relative_to(R).as_posix()
    inventory['scope_decisions_sha256']=sha(decision)
    inventory['outside_population_summary']={'discovery_records':7,'explicit_user_retention':3,'connected_existing_title_retention':1,
        'still_unresolved':['RYO51_PAGE17','NT1C','DIAGNOSTIC_STAGE_SELECT'],'still_unresolved_count':3}
    inventory['global_corpus_closed']=False;inventory['human_approved']=False
    inventory_path.write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n','utf-8')
    result={'work':169,'status':'PASS_EXPLICIT_THREE_SCOPE_DECISIONS_AND_TITLE_PROMPT_CONNECTION',
        'approved_retention':['HOWTO','PAUSE','POW'],'unused_proven':False,'global_English_policy':False,
        'title_prompt_source_bank':63,'native_setup_CPU':['CC89','CC8B','CCAE','CCB0'],
        'metasprite_lookup_CPU_hex':f"{reference[1]['lookup_table']:04X}",
        'metasprite_descriptor_CPU_hex':f"{reference[1]['descriptor_pointer']:04X}",
        'source_current049_native_CPU_case_pairs':5,'actual049_evidence_reused_frame':720,'actual_title_OAM':selected,
        'title_source63_PPU_bytes_exact':True,'signature_bank95_title_number2_local_tiles':number_local_tiles,
        'signature_last_row_not_used_by_selected_title_OAM':True,'signature_globally_unused':False,
        'inventory':inventory_path.relative_to(R).as_posix(),'inventory_sha256':sha(inventory_path),
        'still_unresolved_candidates':3,'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),
        'new_emulator_or_gameplay':False,'overall_human_approved':False,'release_eligible':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''사용자가 후보 HOWTO·PAUSE·POW 범위 질문에 **‘이번 범위에서는 원문 유지’**라고 답했다. [명시적 결정 원장](../{decision.relative_to(R).as_posix()})에 세 후보의 현재 한글화 범위 원문 유지만 승인으로 기록했다. 이세건의 범위 작업은 닫고, 미사용 증명·소비 폐쇄·전역 영어 보존·전체 사람 검수는 승인으로 처리하지 않는다. 원본 픽셀을 이미 보존했으므로 ROM을 새로 고칠 필요가 없다.

추가 기술 진전: CHR0F PUSH START는 별도 미연결 문구가 아니라 현재 타이틀의 기존 보존 시작 안내였다. native CC89/CC8B→RAM37=63, CCAE/CCB0→actor8E, bank36/9643 descriptorA19C의8개8x16 sprite41..4F 경로를 연결했다. 원본/현재049의5course CPU조건쌍에서 OAM/레지스터/cycle이 동일했다. 기존 [049 타이틀130 PNG](../qa/dialogue/pages130_intro049/frame_00720.png) 및 종료된QA의RAM/PPU/OAM/mapping/환경SHA를 확인했다. frame720에서 bank63→PPU1400의1024바이트와8개 OAM(y156,x96..152,attr2)을 확인했다. 기존 실제 PNG를 직접 열어 PUSH START 표시를 확인했으며 새게임 실행은 하지 않았다. 기존 타이틀 POC의 PUSH START 보존 범위와 연결하고 신규 번역 건으로 중복 집계하지 않는다.

RYO51 포함 CHR17 마지막 행은 bank95 local48..63이다. 타이틀 숫자2의 actor31은local0..21만 사용하며 지정된720 OAM도 동일하다. 해당타이틀 조건에서 서명행을 사용하지 않는다는 제한된 근거다. 전역 미사용/서명 작성자를 확정하지 않는다. 나머지 미해결은 RYO51, NT1C, 진단STAGE SELECT의3건이다. [현재 원장](../{inventory_path.relative_to(R).as_posix()})은 발견7=사용자보존3+기존타이틀연결보존1+미해결3으로 정리했다. 전역원천완결성과전체사람검수는false.

[검증 보고](../{report.relative_to(R).as_posix()}), 재현 `python scripts/resolve_scope169.py`는기존출력을보호한다. 신규정적/한정CPU와기존완료QA해시·PPU/OAM·PNG 직접확인만수행했다. 신규ROM빌드/적용/게임런타임/플레이/청음없음. ROM `{sha(rom)}`,CSV `{sha(ssot)}` 불변. 변경은결정원장/현재inventory/분석기/보고/인계문서/manifest이며사용근거SHA를고정한다. 실제플레이검수는사용자담당이다.'''
    files=[decision,inventory_path,report,Path(__file__),prior,source,rom,ssot,R/'scripts/analyze_pow_metasprites096.py',
        R/'docs/POC_TITLE.md',q/'environment.json',R/'extracted/chr/survey_20261004_001/chr_page_0F.png',
        R/'extracted/chr/survey_20261004_001/chr_page_17.png',*paths]
    seal(169,'SCOPE_RETENTION_AND_TITLE_PROMPT_CONNECTION.md','보존 범위 확정·PUSH START 타이틀 소비 연결',body,
        '사용자HOWTO/PAUSE/POW 원문유지확정.별도PUSH START는기존타이틀sprite8E/CHR63 소비에연결. 발견7중3보존승인+1기존보존연결+3미해결. ROM/CSV불변.',
        '사용자 원문 유지 결정과 타이틀 소비 연결을 비플레이 검토자료·검수용 적용 패키지의 새 버전에 반영하고 현재 상태를 인계한다.',files)
    print(json.dumps({k:v for k,v in result.items()if k not in ['actual_title_OAM','signature_bank95_title_number2_local_tiles']},indent=2))

if __name__=='__main__':main()
