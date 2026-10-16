$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot)).TrimEnd('\')
$boundary=(Join-Path $root 'dist')+'\'
function Safe([string]$rel) {
    if ([IO.Path]::IsPathRooted($rel)) {throw 'Absolute path refused'}
    $p=[IO.Path]::GetFullPath((Join-Path $root $rel))
    if (-not $p.StartsWith($boundary,[StringComparison]::OrdinalIgnoreCase)) {throw "Outside dist: $p"}
    $walk=$p
    while ($walk.Length -gt $root.Length) {
        if (Test-Path -LiteralPath $walk) {if ((Get-Item -LiteralPath $walk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Reparse refused'}}
        $walk=Split-Path -Parent $walk
    }
    return $p
}
$q=Get-Content -LiteralPath (Join-Path $root 'qa/reports/obsolete_distribution223_archive.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($q.status -ne 'VERIFIED_NOT_DELETED') {throw 'Invalid archive state'}
$archive=[IO.Path]::GetFullPath((Join-Path $root $q.archive))
if (-not $archive.StartsWith((Join-Path $root 'qa/archive')+'\',[StringComparison]::OrdinalIgnoreCase)) {throw 'Outside archive root'}
if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $q.archive_sha256) {throw 'Archive SHA mismatch'}
foreach ($item in $q.files.PSObject.Properties) {
    $p=Safe $item.Name
    if ((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.Value.sha256) {throw "Changed obsolete artifact: $p"}
}
foreach ($target in $q.roots) {
    $p=Safe $target.path
    if ($target.directory) {
        $now=Get-ChildItem -LiteralPath $p -Recurse -Force
        foreach ($child in $now) {
            if ($child.Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Reparse child refused'}
            if (-not $child.PSIsContainer) {
                $name=$child.FullName.Substring($root.Length+1).Replace('\','/')
                if (-not ($q.files.PSObject.Properties.Name -contains $name)) {throw "Unplanned child: $name"}
            }
        }
        # Absolute target remains within dist; every current child was checked.
        Remove-Item -LiteralPath $p -Recurse -Force
    } else {Remove-Item -LiteralPath $p -Force}
}
@{work=223;status='DELETED_SUPERSEDED_DISTRIBUTIONS_ARCHIVED';files=$q.file_count;bytes=$q.selected_bytes;archive_bytes=$q.archive_bytes;archive_sha256=$q.archive_sha256} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'qa/reports/obsolete_distribution223_deletion.json') -Encoding UTF8
Write-Output 'Obsolete223 completed'
