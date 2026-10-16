$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$root = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot)).TrimEnd('\')
$boundary = $root + '\'
function Safe([string]$relative) {
    if ([IO.Path]::IsPathRooted($relative)) { throw 'Absolute target refused' }
    $p = [IO.Path]::GetFullPath((Join-Path $root $relative))
    if (-not $p.StartsWith($boundary,[StringComparison]::OrdinalIgnoreCase)) { throw "Outside project: $p" }
    if ($p.StartsWith((Join-Path $root 'qa\dialogue\booth039_font_probe'),[StringComparison]::OrdinalIgnoreCase)) { throw 'Previously blocked folder excluded' }
    $walk=$p
    while ($walk.Length -gt $root.Length) {
        if (Test-Path -LiteralPath $walk) {
            if ((Get-Item -LiteralPath $walk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse target: $walk" }
        }
        $walk=Split-Path -Parent $walk
    }
    return $p
}
function Snapshot([string]$p) {
    [long]$count=0;[long]$bytes=0;[long]$latest=0
    Get-ChildItem -LiteralPath $p -Recurse -Force | ForEach-Object {
        if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse child refused' }
        if (-not $_.PSIsContainer) {
            $count++;$bytes+=$_.Length
            [long]$stamp=($_.LastWriteTimeUtc.ToFileTimeUtc()-[long]116444736000000000)*[long]100
            if ($stamp -gt $latest) {$latest=$stamp}
        }
    }
    return @{files=$count;bytes=$bytes;max_mtime_ns=$latest}
}
$plan=Get-Content -LiteralPath (Safe 'work/cleanup222/deletion_plan.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($plan.root -ne $root -or $plan.status -ne 'VERIFIED_NOT_DELETED') {throw 'Invalid verified plan'}
foreach ($id in @('214','222')) {
    $name='archive'+$id;$digest=$name+'_sha256'
    if ((Get-FileHash -LiteralPath (Safe $plan.$name) -Algorithm SHA256).Hash.ToLowerInvariant() -ne $plan.$digest) {throw 'Archive SHA mismatch'}
}
$progress=Safe 'work/cleanup222/deletion_progress.jsonl'
if (Test-Path -LiteralPath $progress) {throw 'Existing progress: inspect prior run; do not blindly repeat deletion'}
$removed=0;$groups=0
foreach ($group in $plan.groups) {
    $p=Safe $group.path
    if (-not (Test-Path -LiteralPath $p -PathType Container)) {throw "Missing planned folder: $p"}
    $current=Snapshot $p
    foreach ($key in @('files','bytes','max_mtime_ns')) {if ($current[$key] -ne $group.snapshot.$key) {throw "Changed planned folder $($group.path) / $key"}}
    foreach ($item in $group.retain) {
        $saved=Safe ($plan.staging+'/'+$item.path)
        if ((Get-FileHash -LiteralPath $saved -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256) {throw 'Retained staging mismatch'}
    }
    if ($group.kind -eq 'DISPOSABLE_ISOLATED_BROWSER_CACHE') {
        $active=Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -and $_.CommandLine.Contains($p)}
        if ($active) {throw "Isolated renderer still active: $p"}
    }
    @{path=$group.path;state='STARTED'} | ConvertTo-Json -Compress | Add-Content -LiteralPath $progress -Encoding UTF8
    # The resolved absolute recursive target and every child were checked above.
    Remove-Item -LiteralPath $p -Recurse -Force
    foreach ($item in $group.retain) {
        $destination=Safe $item.path;$saved=Safe ($plan.staging+'/'+$item.path)
        [IO.Directory]::CreateDirectory((Split-Path -Parent $destination)) | Out-Null
        Copy-Item -LiteralPath $saved -Destination $destination
        if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256) {throw 'Restored retained file mismatch'}
    }
    @{path=$group.path;state='REMOVED_RETAINED_RESTORED';files=$group.snapshot.files;retained=@($group.retain).Count} | ConvertTo-Json -Compress | Add-Content -LiteralPath $progress -Encoding UTF8
    $groups++;if ($groups%50 -eq 0) {Write-Output "Completed groups: $groups"}
}
foreach ($item in $plan.files) {
    $p=Safe $item.path
    if ((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.sha256) {throw "Changed large report: $p"}
    Remove-Item -LiteralPath $p -Force
    @{path=$item.path;state='REMOVED_ARCHIVED_REPORT'} | ConvertTo-Json -Compress | Add-Content -LiteralPath $progress -Encoding UTF8
}
$stage=Safe $plan.staging
# Staging is an exact project-local target; all retained payloads were restored and checked.
Remove-Item -LiteralPath $stage -Recurse -Force
$report=@{work=222;status='DELETED_LOSSLESS_HISTORY_AND_DISPOSABLE_CACHES';groups=$groups;large_reports=@($plan.files).Count;stats=$plan.stats;archives_unchanged=$true;blocked_folder_skipped=$true}
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Safe 'qa/reports/cleanup222_deletion.json') -Encoding UTF8
Write-Output 'Cleanup222 completed'
