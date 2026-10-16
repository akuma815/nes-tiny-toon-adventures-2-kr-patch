$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$root=[IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot)).TrimEnd('\')
$boundary=$root+'\'
function Safe([string]$rel) {
    if ([IO.Path]::IsPathRooted($rel)) {throw 'Absolute path refused'}
    $p=[IO.Path]::GetFullPath((Join-Path $root $rel))
    if (-not $p.StartsWith($boundary,[StringComparison]::OrdinalIgnoreCase)) {throw 'Outside project'}
    $walk=$p
    while ($walk.Length -gt $root.Length) {
        if (Test-Path -LiteralPath $walk) {if ((Get-Item -LiteralPath $walk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Reparse target refused'}}
        $walk=Split-Path -Parent $walk
    }
    return $p
}
$p=Safe 'work/cleanup222/deletion_plan.json'
$plan=Get-Content -LiteralPath $p -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($id in @('214','222')) {
    $key='archive'+$id;$h=$key+'_sha256'
    if ((Get-FileHash -LiteralPath (Safe $plan.$key) -Algorithm SHA256).Hash.ToLowerInvariant() -ne $plan.$h) {throw 'Archive SHA mismatch'}
}
$progress=Safe 'work/cleanup222/deletion_progress.jsonl'
$done=@{}
Get-Content -LiteralPath $progress -Encoding UTF8 | ForEach-Object {$entry=$_ | ConvertFrom-Json;if ($entry.state -eq 'REMOVED_RETAINED_RESTORED') {$done[$entry.path]=$true}}
$pending=@($plan.groups | Where-Object {-not $done.ContainsKey($_.path)})
if ($pending.Count -ne 3 -or @($pending | Where-Object kind -ne 'DISPOSABLE_ISOLATED_BROWSER_CACHE').Count) {throw 'Unexpected remainder; inspect before retrying'}
[long]$cacheFiles=0;[long]$cacheBytes=0
foreach ($g in $pending) {
    $path=Safe $g.path
    if (@(Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -and $_.CommandLine.Contains($path)}).Count) {throw "Own renderer still active: $path"}
    $items=@(Get-ChildItem -LiteralPath $path -Recurse -Force)
    if (@($items | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count) {throw 'Reparse child refused'}
    $files=@($items | Where-Object {-not $_.PSIsContainer});[long]$size=0;[long]$latest=0
    foreach ($f in $files) {$size+=$f.Length;[long]$stamp=($f.LastWriteTimeUtc.ToFileTimeUtc()-[long]116444736000000000)*[long]100;if ($stamp -gt $latest) {$latest=$stamp}}
    $g.snapshot.files=$files.Count;$g.snapshot.bytes=$size;$g.snapshot.max_mtime_ns=$latest
    $cacheFiles+=$files.Count;$cacheBytes+=$size
}
$plan.stats.cache_files=$cacheFiles;$plan.stats.cache_bytes=$cacheBytes
$plan | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath (Safe 'work/cleanup222/final_plan.json') -Encoding UTF8
foreach ($g in $pending) {
    $path=Safe $g.path
    # Only the three original disposable targets remain; ownership, inactivity,
    # resolved boundaries and fresh child inventory were checked above.
    Remove-Item -LiteralPath $path -Recurse -Force
    @{path=$g.path;state='REMOVED_RETAINED_RESTORED';files=$g.snapshot.files;retained=0} | ConvertTo-Json -Compress | Add-Content -LiteralPath $progress -Encoding UTF8
}
foreach ($item in $plan.files) {
    $path=Safe $item.path
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256) {throw 'Changed archived large report'}
    Remove-Item -LiteralPath $path -Force
    @{path=$item.path;state='REMOVED_ARCHIVED_REPORT'} | ConvertTo-Json -Compress | Add-Content -LiteralPath $progress -Encoding UTF8
}
foreach ($g in $plan.groups) {foreach ($item in $g.retain) {if ((Get-FileHash -LiteralPath (Safe $item.path) -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256) {throw 'Retained live asset mismatch'}}}
$stage=Safe $plan.staging
Remove-Item -LiteralPath $stage -Recurse -Force
@{work=222;status='DELETED_LOSSLESS_HISTORY_AND_DISPOSABLE_CACHES';groups=@($plan.groups).Count;large_reports=@($plan.files).Count;stats=$plan.stats;archives_unchanged=$true;blocked_folder_skipped=$true;interruption='Snapshot drift in own failed-render browser cache; closed owned browser and refreshed only three cache snapshots'} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Safe 'qa/reports/cleanup222_deletion.json') -Encoding UTF8
Write-Output 'Cleanup222 remainder completed'
