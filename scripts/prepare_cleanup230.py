"""Archive superseded posting outputs and derived review/rebuild folders before scoped cleanup."""
from pathlib import Path
import hashlib, json, os, stat, zipfile
from seal_nonplay171 import R

ROOTS=[
 'workspace/publication/TinyToon12_TechnicalGuide_20261009',
 'workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009',
 'workspace/publication/TinyToon2_KR_Worklog_Reader_20261009',
 'qa/publication/author_voice229','qa/publication/author_voice229_final',
 'qa/publication/reader228_worklog','qa/publication/render221',
 'qa/publication/render221_final','qa/publication/render221_v2',
 'qa/publication/render225_final','qa/publication/technical227_final',
 'build/text11_211_rebuild062',
 'dist/TinyToon12_NES_Korean_TechnicalGuide_20261009.zip',
 'dist/TinyToon12_NES_Korean_TechnicalGuide_20261009.zip.sha256',
 'dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip',
 'dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip.sha256',
 'dist/TinyToon2_KR_Worklog_Reader_20261009.zip',
 'dist/TinyToon2_KR_Worklog_Reader_20261009.zip.sha256',
 'dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip',
 'dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip.sha256']
CANONICAL={'README.md','docs/HANDOFF.md','docs/HANDOFF_2026-10-09.md','docs/SURVEY.md','docs/LOCALIZATION_WORK_PLAN.md','docs/journal/2026-10-09.md'}
PLAN=R/'qa/reports/cleanup230_plan.json'
ARCHIVE=R/'qa/archive/cleanup230_superseded.zip'

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as s:
        for chunk in iter(lambda:s.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def safe(p):
    assert p.is_absolute() and p.resolve().is_relative_to(R.resolve()) and p.resolve()!=R.resolve()
    for q in [p,*p.parents]:
        if q.is_relative_to(R) and q.exists():assert not q.stat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT,q
    return p

def files_of(p):
    if p!=R:safe(p)
    if p.is_file():return [p]
    files=[]
    for directory,dirs,names in os.walk(p,followlinks=False):
        for name in dirs:safe(Path(directory)/name)
        for name in names:files.append(safe(Path(directory)/name))
    return sorted(files)

def record(p):
    s=p.stat();return {'sha256':digest(p),'bytes':s.st_size,'mtime_ns':s.st_mtime_ns}

def main():
    assert not PLAN.exists() and not ARCHIVE.exists()
    selected={};roots=[]
    for rel in ROOTS:
        p=safe(R/rel);assert p.exists(),rel;files=files_of(p)
        roots.append({'path':rel,'directory':p.is_dir(),'files':len(files),'bytes':sum(f.stat().st_size for f in files)})
        for f in files:selected[f.relative_to(R).as_posix()]=record(f)
    assert len(selected)>0
    assert digest(R/'build/text11_211_rebuild062/TinyToon2_Text11_Candidate062.nes')==digest(R/'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes')
    print('Selected archive inputs:',len(selected),'files',flush=True)
    kept={}
    for p in files_of(R):
        rel=p.relative_to(R).as_posix()
        if rel not in selected and rel not in CANONICAL:kept[rel]=record(p)
    # Recovery bytes are private: this archive includes a historical ROM rebuild.
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel,meta in selected.items():
            p=R/rel;assert record(p)==meta,rel
            z.write(p,rel)
    checked=0
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and set(z.namelist())==set(selected)
        for rel,meta in selected.items():
            data=z.read(rel);assert len(data)==meta['bytes'] and hashlib.sha256(data).hexdigest()==meta['sha256'],rel;checked+=1
    data={'work':230,'root':str(R),'status':'ARCHIVE_VERIFIED_NOT_DELETED','archive':ARCHIVE.relative_to(R).as_posix(),
      'archive_sha256':digest(ARCHIVE),'archive_bytes':ARCHIVE.stat().st_size,'archive_contains_ROM':True,'public_upload':False,
      'roots':roots,'archived_files':selected,'kept_files':kept,'canonical_docs_will_update':sorted(CANONICAL),
      'stats':{'selected_files':len(selected),'selected_bytes':sum(z['bytes'] for z in selected.values()),'archive_payloads_verified':checked,'kept_files_snapshotted':len(kept)}}
    PLAN.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8')
    literal=lambda value:"'"+value.replace("'","''")+"'"
    script=R/'scripts/execute_cleanup230.ps1';assert not script.exists()
    text='''$ErrorActionPreference = 'Stop'
$taskRoot = 'G:\\Downloads\\Korean Traslate Project\\Games\\Tiny Toon Adventures 2'
$taskPlanPath = Join-Path $taskRoot 'qa\\reports\\cleanup230_plan.json'
$taskPlan = Get-Content -LiteralPath $taskPlanPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($taskPlan.root -ne $taskRoot -or $taskPlan.work -ne 230) { throw 'Unexpected cleanup plan' }
$taskArchive = Join-Path $taskRoot $taskPlan.archive
if ((Get-FileHash -LiteralPath $taskArchive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskPlan.archive_sha256) { throw 'Archive changed' }
$taskAllowed = @(
'''+''.join('  '+literal(str(R/rel))+'\n' for rel in ROOTS)+''')
if ($taskPlan.roots.Count -ne $taskAllowed.Count) { throw 'Target count changed' }
foreach ($taskItem in $taskPlan.roots) {
  $taskPath = Join-Path $taskRoot $taskItem.path
  $taskResolved = (Resolve-Path -LiteralPath $taskPath).Path
  if ($taskResolved -ne $taskPath -or $taskPath -notin $taskAllowed -or -not $taskResolved.StartsWith($taskRoot + '\\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Unexpected resolved target' }
  $taskAncestor = Get-Item -LiteralPath $taskPath -Force
  while ($taskAncestor -and $taskAncestor.FullName.StartsWith($taskRoot, [StringComparison]::OrdinalIgnoreCase)) {
    if ($taskAncestor.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse ancestor' }
    $taskAncestor = if ($taskAncestor.PSIsContainer) { $taskAncestor.Parent } else { $taskAncestor.Directory }
  }
  if ($taskItem.directory) {
    $taskChildren = @(Get-ChildItem -LiteralPath $taskPath -Force -Recurse)
    if (@($taskChildren | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw 'Reparse child' }
    $taskFiles = @($taskChildren | Where-Object { -not $_.PSIsContainer })
  } else { $taskFiles = @(Get-Item -LiteralPath $taskPath -Force) }
  if ($taskFiles.Count -ne $taskItem.files) { throw 'Target file count changed' }
  foreach ($taskFile in $taskFiles) {
    $taskRelative = $taskFile.FullName.Substring($taskRoot.Length + 1).Replace('\\','/')
    $taskExpected = $taskPlan.archived_files.PSObject.Properties[$taskRelative].Value
    if (-not $taskExpected -or $taskFile.Length -ne $taskExpected.bytes -or (Get-FileHash -LiteralPath $taskFile.FullName -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskExpected.sha256) { throw ('Target changed: ' + $taskRelative) }
  }
}
# Every literal target above is fully validated before any deletion.
'''
    for item in roots:
        text+='Remove-Item -LiteralPath '+literal(str(R/item['path']))+(' -Recurse' if item['directory'] else '')+' -Force\n'
    text+='''foreach ($taskPath in $taskAllowed) { if (Test-Path -LiteralPath $taskPath) { throw ('Target remains: ' + $taskPath) } }
[pscustomobject]@{work=230; status='SCOPED_DELETION_COMPLETE'; roots=$taskAllowed.Count; archive_sha256=$taskPlan.archive_sha256; removed_files=$taskPlan.stats.selected_files; removed_bytes=$taskPlan.stats.selected_bytes} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot 'qa\\reports\\cleanup230_execution.json') -Encoding UTF8
Write-Output 'Verified archive exists; only explicit superseded targets removed.'
'''
    script.write_text(text,'utf-8-sig')
    print(json.dumps({'status':data['status'],'roots':len(roots),'archive_bytes':data['archive_bytes'],'archive_sha256':data['archive_sha256'],**data['stats']},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
