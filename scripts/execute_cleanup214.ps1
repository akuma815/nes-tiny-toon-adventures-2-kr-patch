param([switch]$FinalizeTemporaryFiles)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot)).TrimEnd('\')
$boundary = $root + '\'
function Resolve-SafeTarget([string]$relative) {
    if ([IO.Path]::IsPathRooted($relative)) { throw 'Absolute target refused' }
    $p = [IO.Path]::GetFullPath((Join-Path $root $relative))
    if (-not $p.StartsWith($boundary, [StringComparison]::OrdinalIgnoreCase)) { throw "Outside project: $p" }
    $walk = $p
    while ($walk.Length -gt $root.Length) {
        if (Test-Path -LiteralPath $walk) {
            $i = Get-Item -LiteralPath $walk -Force
            if ($i.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse target refused: $walk" }
        }
        $walk = Split-Path -Parent $walk
    }
    return $p
}
function Get-Snapshot([string]$p) {
    [long]$count = 0; [long]$size = 0; [long]$max = 0
    Get-ChildItem -LiteralPath $p -Recurse -Force | ForEach-Object {
        if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse child refused: $($_.FullName)" }
        if (-not $_.PSIsContainer) {
            $count++; $size += $_.Length
            $ticks = $_.LastWriteTimeUtc.ToFileTimeUtc()
            if ($ticks -gt $max) { $max = $ticks }
        }
    }
    return @{ files = $count; bytes = $size; max_filetime = $max }
}
$planFile = Resolve-SafeTarget 'work/cleanup214/deletion_plan.json'
$plan = Get-Content -LiteralPath $planFile -Raw -Encoding UTF8 | ConvertFrom-Json
if ($plan.root -ne $root -or $plan.status -ne 'VERIFIED_NOT_DELETED') { throw 'Invalid verified cleanup plan' }
$archive = Resolve-SafeTarget $plan.archive_path
if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $plan.archive_sha256) { throw 'Archive SHA mismatch' }
$reportFile = Resolve-SafeTarget 'qa/reports/cleanup214_deletion.json'
if ($FinalizeTemporaryFiles) {
    if (-not (Test-Path -LiteralPath $reportFile)) { throw 'Deletion report missing' }
    $report = Get-Content -LiteralPath $reportFile -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($report.status -ne 'PASS') { throw 'Deletion incomplete' }
    $audit = Get-Content -LiteralPath (Resolve-SafeTarget 'qa/reports/cleanup214_audit.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($audit.status -ne 'PASS') { throw 'Final audit missing' }
    $extra = @()
    foreach ($n in @('work/cleanup214/retained_live','work/cleanup214/inventory.json','work/cleanup214/plan.json')) {
        $p = Resolve-SafeTarget $n
        if (Test-Path -LiteralPath $p) {
            $info = Get-Item -LiteralPath $p
            $snap = if ($info.PSIsContainer) { Get-Snapshot $p } else { @{files=1;bytes=$info.Length} }
            Remove-Item -LiteralPath $p -Recurse -Force
            $extra += @{path=$n;files=$snap.files;bytes=$snap.bytes}
        }
    }
    $out = Resolve-SafeTarget 'qa/reports/cleanup214_temporary_removed.json'
    if (Test-Path -LiteralPath $out) { throw 'Final report exists' }
    @{status='PASS';removed=$extra;reason='Verified staging and verbose temporary inventory; archive index and compact deletion ledger retained'} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $out -Encoding UTF8
    return
}
if (Test-Path -LiteralPath $reportFile) { throw 'Deletion already recorded; do not repeat' }
$journal = Resolve-SafeTarget 'work/cleanup214/deletion_progress.jsonl'
if (Test-Path -LiteralPath $journal) { throw 'Partial run exists; inspect journal before resuming' }
$results = @()
$processes = @(Get-CimInstance Win32_Process)
foreach ($target in $plan.directories) {
    $n = [string]$target.path
    if ($n -notmatch '^(build/[^/]+|dist/[^/]+|work/[^/]+|qa/(dialogue|release|apply|patch)/[^/]+)$') { throw "Invalid run root: $n" }
    if ($n -match '(?i)user|work/cleanup214|build/(text11_candidate_062|text11_211_rebuild062|dialogue_kr_poc_051|ordinary11_candidate_059|opening11_poc_05[35]|homebooth11_candidate_057)$') { throw "Protected root: $n" }
    $p = Resolve-SafeTarget $n
    if ($processes | Where-Object { $_.CommandLine -and $_.CommandLine.IndexOf($p,[StringComparison]::OrdinalIgnoreCase) -ge 0 }) { throw "Active process uses $p" }
    $snap = Get-Snapshot $p
    if ($snap.files -ne $target.files -or $snap.bytes -ne $target.bytes -or $snap.max_filetime -ne $target.max_filetime) { throw "Snapshot changed since archival: $n" }
    $staged = Resolve-SafeTarget ($plan.staging_path + '/' + $n)
    if ($target.restore_files -gt 0) {
        $stage = Get-Snapshot $staged
        if ($stage.files -ne $target.restore_files -or $stage.bytes -ne $target.restore_bytes) { throw "Staging mismatch: $n" }
    }
    @{phase='validated';path=$n} | ConvertTo-Json -Compress | Add-Content -LiteralPath $journal -Encoding UTF8
    Remove-Item -LiteralPath $p -Recurse -Force
    if ($target.restore_files -gt 0) {
        Copy-Item -LiteralPath $staged -Destination (Split-Path -Parent $p) -Recurse -Force
        $restored = Get-Snapshot $p
        if ($restored.files -ne $target.restore_files -or $restored.bytes -ne $target.restore_bytes) { throw "Restored snapshot mismatch: $n" }
    }
    $result = @{phase='completed';path=$n;archived_files=$target.files;archived_bytes=$target.bytes;live_files=[long]$target.restore_files;live_bytes=[long]$target.restore_bytes}
    $result | ConvertTo-Json -Compress | Add-Content -LiteralPath $journal -Encoding UTF8
    $results += $result
    if ($results.Count % 20 -eq 0) { Write-Output "Cleaned run directories: $($results.Count)/$($plan.directories.Count)" }
}
# Only task-created, isolated headless review profiles; never the user's browser profile.
$cacheTargets = @($plan.cache_directory_targets)
Get-ChildItem -LiteralPath (Resolve-SafeTarget 'qa/review') -Directory | ForEach-Object {
    $candidate = Join-Path $_.FullName 'browser_profile'
    if (Test-Path -LiteralPath $candidate) { $cacheTargets += $candidate.Substring($boundary.Length).Replace('\','/') }
}
$caches = @()
foreach ($n in ($cacheTargets | Sort-Object -Unique)) {
    if ($n -notmatch '(^|/)__pycache__$|^qa/review/[^/]+/browser_profile$') { throw "Invalid cache target: $n" }
    $p = Resolve-SafeTarget $n
    if (-not (Test-Path -LiteralPath $p)) { continue }
    if ($processes | Where-Object { $_.CommandLine -and $_.CommandLine.IndexOf($p,[StringComparison]::OrdinalIgnoreCase) -ge 0 }) { throw "Active cache: $p" }
    $snap = Get-Snapshot $p
    Remove-Item -LiteralPath $p -Recurse -Force
    $caches += @{path=$n;files=$snap.files;bytes=$snap.bytes;reason='Regenerable bytecode or isolated QA browser cache'}
}
@{work=214;status='PASS';root=$root;archive_sha256=$plan.archive_sha256;directories=$results;caches=$caches;user_Mesen_and_saves='NOT_TOUCHED';runtime='NOT_RUN'} | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $reportFile -Encoding UTF8
Write-Output "PASS: $($results.Count) archived run directories cleaned; $($caches.Count) cache directories deleted."
