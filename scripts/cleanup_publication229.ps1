$ErrorActionPreference = 'Stop'
$taskRoot = 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication'
$taskPaths = @(
 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229\browser_profile',
 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229_final\browser_profile',
 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229_verified\browser_profile'
)
$taskRecords = @()
foreach ($taskPath in $taskPaths) {
  $taskResolved = (Resolve-Path -LiteralPath $taskPath).Path
  if ($taskResolved -ne $taskPath -or -not $taskResolved.StartsWith($taskRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Unexpected cache path' }
  $taskParent = Get-Item -LiteralPath $taskPath -Force
  $taskChildren = @(Get-ChildItem -LiteralPath $taskPath -Force -Recurse)
  if ($taskParent.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse target' }
  if (@($taskChildren | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw 'Reparse child' }
  if (@(Get-CimInstance Win32_Process -Filter "Name = 'msedge.exe'" | Where-Object { $_.CommandLine -and $_.CommandLine.Contains($taskPath) }).Count) { throw 'Own renderer running' }
  $taskFiles = @($taskChildren | Where-Object { -not $_.PSIsContainer })
  $taskRecords += [pscustomobject]@{path=$taskPath; files=$taskFiles.Count; bytes=($taskFiles | Measure-Object -Property Length -Sum).Sum}
}
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229\browser_profile' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229_final\browser_profile' -Recurse -Force
Remove-Item -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\publication\author_voice229_verified\browser_profile' -Recurse -Force
foreach ($taskRecord in $taskRecords) { if (Test-Path -LiteralPath $taskRecord.path) { throw 'Cache remains' } }
[pscustomobject]@{work=229; completed=$true; removed=$taskRecords; scope='Only current isolated reader renderer profiles'} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath 'G:\Downloads\Korean Traslate Project\Games\Tiny Toon Adventures 2\qa\reports\publication229_cache_cleanup.json' -Encoding UTF8
Write-Output 'Current isolated renderer profiles removed; article and QA screenshots retained.'
