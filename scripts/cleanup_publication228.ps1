$ErrorActionPreference = 'Stop'
$taskRoot = 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication'
$taskTargets = @(
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\reader228_worklog\browser_profile',
  'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\reader228_guide\browser_profile'
)
$taskRecords = @()
foreach ($taskPath in $taskTargets) {
  $taskResolved = (Resolve-Path -LiteralPath $taskPath).Path
  if ($taskResolved -ne $taskPath -or -not $taskResolved.StartsWith($taskRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Unexpected cache path' }
  $taskParent = Get-Item -LiteralPath $taskPath -Force
  $taskChildren = @(Get-ChildItem -LiteralPath $taskPath -Force -Recurse)
  if ($taskParent.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse target' }
  if (@($taskChildren | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw 'Reparse child' }
  if (@(Get-CimInstance Win32_Process -Filter "Name = 'msedge.exe'" | Where-Object { $_.CommandLine -and $_.CommandLine.Contains($taskPath) }).Count) { throw 'Own renderer running' }
  $taskFiles = @($taskChildren | Where-Object { -not $_.PSIsContainer })
  $taskRecords += [pscustomobject]@{ path=$taskPath; files=$taskFiles.Count; bytes=($taskFiles | Measure-Object -Property Length -Sum).Sum }
}
# Both targets are literal, existing, validated directories created by this editorial task.
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\reader228_worklog\browser_profile' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\reader228_guide\browser_profile' -Recurse -Force
foreach ($taskRecord in $taskRecords) { if (Test-Path -LiteralPath $taskRecord.path) { throw 'Cache remains' } }
[pscustomobject]@{ work=228; scope='Only current isolated renderer cache, explicit literal paths'; removed=$taskRecords; completed=$true } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\reports\publication228_cache_cleanup.json' -Encoding UTF8
Write-Output 'Removed only two validated temporary renderer profiles; publication sources and screenshots retained.'
