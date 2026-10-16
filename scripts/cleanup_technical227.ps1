$ErrorActionPreference='Stop'
$projectRoot=[IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot)).TrimEnd('\')
$profile=[IO.Path]::GetFullPath((Join-Path $projectRoot 'qa/publication/technical227_final/browser_profile'))
$scope=[IO.Path]::GetFullPath((Join-Path $projectRoot 'qa/publication/technical227_final'))
if (-not $profile.StartsWith($scope+'\',[StringComparison]::OrdinalIgnoreCase) -or (Split-Path -Leaf $profile) -ne 'browser_profile') {throw 'Unexpected cleanup target'}
$walk=$profile
while ($walk.Length -gt $projectRoot.Length) {
    if ((Test-Path -LiteralPath $walk) -and ((Get-Item -LiteralPath $walk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) {throw 'Reparse target refused'}
    $walk=Split-Path -Parent $walk
}
$running=Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -and $_.CommandLine.Contains('--user-data-dir='+$profile)}
if ($running) {throw 'Isolated profile is still in use'}
$items=Get-ChildItem -LiteralPath $profile -Recurse -Force
foreach ($item in $items) {if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Reparse child refused'}}
$files=@($items | Where-Object {-not $_.PSIsContainer})
$bytes=($files | Measure-Object Length -Sum).Sum
# Exact absolute target is checked to remain beneath this render run only.
Remove-Item -LiteralPath $profile -Recurse -Force
@{work=227;status='DELETED_OWN_FINISHED_RENDER_CACHE';target='qa/publication/technical227_final/browser_profile';removed_files=$files.Count;removed_bytes=$bytes;reports_and_png_preserved=$true} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $projectRoot 'qa/reports/technical227_cache_cleanup.json') -Encoding UTF8
Write-Output 'PASS own technical227 render cache cleanup'
