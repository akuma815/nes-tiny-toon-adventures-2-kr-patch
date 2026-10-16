$ErrorActionPreference = 'Stop'
$taskRoot = 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2'
$taskPlanPath = Join-Path $taskRoot 'qa\reports\cleanup230_plan.json'
$taskPlan = Get-Content -LiteralPath $taskPlanPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($taskPlan.root -ne $taskRoot -or $taskPlan.work -ne 230) { throw 'Unexpected cleanup plan' }
$taskArchive = Join-Path $taskRoot $taskPlan.archive
if ((Get-FileHash -LiteralPath $taskArchive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskPlan.archive_sha256) { throw 'Archive changed' }
$taskAllowed = @(
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\workspace\publication\TinyToon12_TechnicalGuide_20261009'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\workspace\publication\TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\workspace\publication\TinyToon2_KR_Worklog_Reader_20261009'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229_final'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\reader228_worklog'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\render221'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\render221_final'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\render221_v2'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\render225_final'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\technical227_final'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\build\text11_211_rebuild062'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon12_NES_Korean_TechnicalGuide_20261009.zip'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon12_NES_Korean_TechnicalGuide_20261009.zip.sha256'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip.sha256'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon2_KR_Worklog_Reader_20261009.zip'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon2_KR_Worklog_Reader_20261009.zip.sha256'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip'
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip.sha256'
)
if ($taskPlan.roots.Count -ne $taskAllowed.Count) { throw 'Target count changed' }
foreach ($taskItem in $taskPlan.roots) {
  $taskPath = Join-Path $taskRoot $taskItem.path
  $taskResolved = (Resolve-Path -LiteralPath $taskPath).Path
  if ($taskResolved -ne $taskPath -or $taskPath -notin $taskAllowed -or -not $taskResolved.StartsWith($taskRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Unexpected resolved target' }
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
    $taskRelative = $taskFile.FullName.Substring($taskRoot.Length + 1).Replace('\','/')
    $taskExpected = $taskPlan.archived_files.PSObject.Properties[$taskRelative].Value
    if (-not $taskExpected -or $taskFile.Length -ne $taskExpected.bytes -or (Get-FileHash -LiteralPath $taskFile.FullName -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskExpected.sha256) { throw ('Target changed: ' + $taskRelative) }
  }
}
# Every literal target above is fully validated before any deletion.
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\workspace\publication\TinyToon12_TechnicalGuide_20261009' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\workspace\publication\TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\workspace\publication\TinyToon2_KR_Worklog_Reader_20261009' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229_final' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\reader228_worklog' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\render221' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\render221_final' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\render221_v2' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\render225_final' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\technical227_final' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\build\text11_211_rebuild062' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon12_NES_Korean_TechnicalGuide_20261009.zip' -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon12_NES_Korean_TechnicalGuide_20261009.zip.sha256' -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip' -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip.sha256' -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon2_KR_Worklog_Reader_20261009.zip' -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToon2_KR_Worklog_Reader_20261009.zip.sha256' -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip' -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\dist\TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip.sha256' -Force
foreach ($taskPath in $taskAllowed) { if (Test-Path -LiteralPath $taskPath) { throw ('Target remains: ' + $taskPath) } }
[pscustomobject]@{work=230; status='SCOPED_DELETION_COMPLETE'; roots=$taskAllowed.Count; archive_sha256=$taskPlan.archive_sha256; removed_files=$taskPlan.stats.selected_files; removed_bytes=$taskPlan.stats.selected_bytes} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot 'qa\reports\cleanup230_execution.json') -Encoding UTF8
Write-Output 'Verified archive exists; only explicit superseded targets removed.'
