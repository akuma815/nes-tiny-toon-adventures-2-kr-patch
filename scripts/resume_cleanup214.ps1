$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot)).TrimEnd('\')
$boundary = $root + '\'
function Resolve-SafeTarget([string]$relative) {
    if ([IO.Path]::IsPathRooted($relative)) { throw 'Absolute target refused' }
    $p = [IO.Path]::GetFullPath((Join-Path $root $relative))
    if (-not $p.StartsWith($boundary,[StringComparison]::OrdinalIgnoreCase)) { throw "Outside project: $p" }
    $walk=$p
    while ($walk.Length -gt $root.Length) {
        if (Test-Path -LiteralPath $walk) {
            if ((Get-Item -LiteralPath $walk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse target: $walk" }
        }
        $walk=Split-Path -Parent $walk
    }
    return $p
}
# Read-only Windows directory-entry traversal avoids a PowerShell object pipeline per file.
Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Collections.Generic;
public static class Cleanup214Snapshot {
 public static long[] Read(string root) {
  long count=0,size=0,max=0;
  var dirs=new Stack<DirectoryInfo>();dirs.Push(new DirectoryInfo(root));
  while(dirs.Count>0) {
   foreach(var item in dirs.Pop().EnumerateFileSystemInfos()) {
    if((item.Attributes & FileAttributes.ReparsePoint)!=0) throw new IOException("Reparse child: "+item.FullName);
    if((item.Attributes & FileAttributes.Directory)!=0) dirs.Push((DirectoryInfo)item);
    else {var f=(FileInfo)item;count++;size+=f.Length;max=Math.Max(max,f.LastWriteTimeUtc.ToFileTimeUtc());}
   }
  }
  return new long[]{count,size,max};
 }
}
'@
function Assert-Snapshot([string]$p,$expected,[bool]$time) {
    $s=[Cleanup214Snapshot]::Read($p)
    if ($s[0] -ne $expected.files -or $s[1] -ne $expected.bytes -or ($time -and $s[2] -ne $expected.max_filetime)) { throw "Snapshot mismatch: $p" }
}
$plan=Get-Content -LiteralPath (Resolve-SafeTarget 'work/cleanup214/deletion_plan.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$resume=Get-Content -LiteralPath (Resolve-SafeTarget 'work/cleanup214/resume_verified.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($root -ne $plan.root -or $resume.status -ne 'PASS' -or $resume.archive_sha256 -ne $plan.archive_sha256) { throw 'Invalid continuation evidence' }
if ((Get-FileHash -LiteralPath (Resolve-SafeTarget $plan.archive_path) -Algorithm SHA256).Hash.ToLowerInvariant() -ne $plan.archive_sha256) { throw 'Archive SHA mismatch' }
$journal=Resolve-SafeTarget 'work/cleanup214/deletion_progress.jsonl'
$reportFile=Resolve-SafeTarget 'qa/reports/cleanup214_deletion.json'
if (Test-Path -LiteralPath $reportFile) { throw 'Deletion already recorded' }
$events=@(Get-Content -LiteralPath $journal -Encoding UTF8 | ForEach-Object { $_ | ConvertFrom-Json })
$results=@($events | Where-Object {$_.phase -eq 'completed'})
$done=@{};foreach($e in $results){if($done.ContainsKey($e.path)){throw 'Duplicate completion'};$done[$e.path]=$true}
if ($done.Count -ne $resume.completed_directories) { throw 'Journal changed after continuation verification' }
$processes=@(Get-CimInstance Win32_Process)
foreach($target in $plan.directories) {
    $n=[string]$target.path
    if ($done.ContainsKey($n)) {continue}
    if ($n -notmatch '^(build/[^/]+|dist/[^/]+|work/[^/]+|qa/(dialogue|release|apply|patch)/[^/]+)$' -or $n -match '(?i)user|work/cleanup214|build/(text11_candidate_062|text11_211_rebuild062|dialogue_kr_poc_051|ordinary11_candidate_059|opening11_poc_05[35]|homebooth11_candidate_057)$') {throw "Unsafe run root: $n"}
    $p=Resolve-SafeTarget $n
    if ($processes | Where-Object {$_.CommandLine -and $_.CommandLine.IndexOf($p,[StringComparison]::OrdinalIgnoreCase) -ge 0}) {throw "Active target: $p"}
    $partial=@($resume.partial | Where-Object {$_.path -eq $n})
    if($partial.Count -gt 0) {
        if($partial[0].exists) {Assert-Snapshot $p $partial[0] $true}
        elseif(Test-Path -LiteralPath $p) {throw 'Absent partial root reappeared'}
    } else {Assert-Snapshot $p $target $true}
    $staged=Resolve-SafeTarget ($plan.staging_path+'/'+$n)
    if($target.restore_files -gt 0){Assert-Snapshot $staged @{files=$target.restore_files;bytes=$target.restore_bytes} $false}
    @{phase='validated';path=$n;method='native_dotnet_from_same_PowerShell'} | ConvertTo-Json -Compress | Add-Content -LiteralPath $journal -Encoding UTF8
    # The exact absolute target and every child have been checked above. No shell delegation.
    if(Test-Path -LiteralPath $p){[IO.Directory]::Delete($p,$true)}
    if($target.restore_files -gt 0) {
        Copy-Item -LiteralPath $staged -Destination (Split-Path -Parent $p) -Recurse -Force
        Assert-Snapshot $p @{files=$target.restore_files;bytes=$target.restore_bytes} $false
    }
    $result=@{phase='completed';path=$n;archived_files=$target.files;archived_bytes=$target.bytes;live_files=[long]$target.restore_files;live_bytes=[long]$target.restore_bytes}
    $result | ConvertTo-Json -Compress | Add-Content -LiteralPath $journal -Encoding UTF8
    $results += $result
    if($results.Count % 20 -eq 0){Write-Output "Cleaned run directories: $($results.Count)/$($plan.directories.Count)"}
}
$cacheTargets=@($plan.cache_directory_targets)
Get-ChildItem -LiteralPath (Resolve-SafeTarget 'qa/review') -Directory | ForEach-Object {
    $candidate=Join-Path $_.FullName 'browser_profile'
    if(Test-Path -LiteralPath $candidate){$cacheTargets+=$candidate.Substring($boundary.Length).Replace('\','/')}
}
$caches=@()
foreach($n in ($cacheTargets | Sort-Object -Unique)) {
    if($n -notmatch '(^|/)__pycache__$|^qa/review/[^/]+/browser_profile$'){throw "Unsafe cache: $n"}
    $p=Resolve-SafeTarget $n
    if(-not(Test-Path -LiteralPath $p)){continue}
    if($processes | Where-Object {$_.CommandLine -and $_.CommandLine.IndexOf($p,[StringComparison]::OrdinalIgnoreCase) -ge 0}){throw "Active cache: $p"}
    $s=[Cleanup214Snapshot]::Read($p)
    Remove-Item -LiteralPath $p -Recurse -Force
    $caches+=@{path=$n;files=$s[0];bytes=$s[1];reason='Regenerable bytecode or isolated QA browser cache'}
}
@{work=214;status='PASS';root=$root;archive_sha256=$plan.archive_sha256;directories=$results;caches=$caches;user_Mesen_and_saves='NOT_TOUCHED';runtime='NOT_RUN';continuation='Verified interrupted root before native directory deletion'} | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $reportFile -Encoding UTF8
Write-Output "PASS: $($results.Count) archived run directories cleaned; $($caches.Count) cache directories deleted."
