$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot)).TrimEnd('\')
$allowed=@('dist/TinyToonAdventures2_KR_v1.0_20261009.zip','dist/TinyToonAdventures2_KR_v1.0_20261009.zip.sha256','dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009.zip','dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009.zip.sha256','dist/TinyToonAdventures2_KR_v1.zip','dist/TinyToonAdventures2_KR_v1.zip.sha256','qa/release/release224_final_zip','qa/release/release226_final_zip','qa/publication/render225_final/browser_profile')
function Safe([string]$rel) {
    if ([IO.Path]::IsPathRooted($rel)) {throw 'Absolute path refused'}
    $p=[IO.Path]::GetFullPath((Join-Path $root $rel))
    if (-not $p.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase)) {throw 'Outside workspace'}
    $walk=$p
    while ($walk.Length -gt $root.Length) {
        if ((Test-Path -LiteralPath $walk) -and ((Get-Item -LiteralPath $walk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) {throw 'Reparse refused'}
        $walk=Split-Path -Parent $walk
    }
    return $p
}
$q=Get-Content -LiteralPath (Join-Path $root 'qa/reports/cleanup226_plan.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($q.status -ne 'VERIFIED_READY_FOR_SCOPED_CLEANUP') {throw 'Invalid state'}
$archive=Safe $q.archive
if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $q.archive_sha256) {throw 'Archive mismatch'}
$profile=Safe 'qa/publication/render225_final/browser_profile'
$processes=Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -and $_.CommandLine.Contains('--user-data-dir='+$profile)}
if ($processes) {throw 'Own renderer still running; do not remove active profile'}
foreach ($target in $q.roots) {
    if ($allowed -notcontains $target.path) {throw 'Unlisted cleanup root'}
    $p=Safe $target.path
    if ($target.directory) {
        foreach ($child in (Get-ChildItem -LiteralPath $p -Recurse -Force)) {
            if ($child.Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Reparse child refused'}
            if (-not $child.PSIsContainer) {
                $name=$child.FullName.Substring($root.Length+1).Replace('\','/')
                if ($q.files.PSObject.Properties.Name -notcontains $name) {throw 'Snapshot changed'}
            }
        }
    }
}
foreach ($file in $q.files.PSObject.Properties) {
    $p=Safe $file.Name
    if ((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne $file.Value.sha256) {throw "Changed file: $p"}
}
foreach ($target in $q.roots) {
    $p=Safe $target.path
    if ($target.directory) {Remove-Item -LiteralPath $p -Recurse -Force} else {Remove-Item -LiteralPath $p -Force}
}
@{work=226;status='DELETED_ARCHIVED_SUPERSEDED_AND_OWN_TEMP';files=$q.file_count;removed_bytes=$q.selected_bytes;archive_bytes=$q.archive_bytes;archive_sha256=$q.archive_sha256} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'qa/reports/cleanup226_deletion.json') -Encoding UTF8
Write-Output 'PASS final scoped cleanup226'
