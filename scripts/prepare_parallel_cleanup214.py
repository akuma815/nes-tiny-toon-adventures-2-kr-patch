"""Generate a four-folder native PS continuation and verify its interrupted boundary."""
from pathlib import Path
import json, os, sqlite3
from archive_cleanup214 import R, digest, safe

def generate():
    source=(R/'scripts/resume_cleanup214.ps1').read_text('utf-8')
    source=source.replace("work/cleanup214/resume_verified.json","work/cleanup214/resume_parallel_verified.json")
    source=source.replace('using System.Collections.Generic;', 'using System.Collections.Generic;\nusing System.Threading.Tasks;')
    source=source.replace(' public static long[] Read(string root) {', ''' public static Task DeleteAsync(string root, string path) {
  string absolute=Path.GetFullPath(path),boundary=Path.GetFullPath(root).TrimEnd(Path.DirectorySeparatorChar)+Path.DirectorySeparatorChar;
  if(!absolute.StartsWith(boundary,StringComparison.OrdinalIgnoreCase)) throw new IOException("Outside project");
  return Task.Run(()=>Directory.Delete(absolute,true));
 }
 public static long[] Read(string root) {''')
    start=source.index('    # The exact absolute target and every child')
    end=source.index('\n}\n$cacheTargets',start)
    source=source[:start]+'''    $job = if(Test-Path -LiteralPath $p){[Cleanup214Snapshot]::DeleteAsync($root,$p)}else{$null}
    $script:pending += @{task=$job;target=$target;n=$n;p=$p;staged=$staged}
    if($script:pending.Count -ge 4){Finish-One}
'''+source[end:]
    marker='foreach($target in $plan.directories) {'
    finish='''$script:pending=@()
function Finish-One {
    while($true) {
        $ready=@($script:pending | Where-Object {$null -eq $_.task -or $_.task.IsCompleted})
        if($ready.Count -gt 0){break}
        [Threading.Thread]::Sleep(50)
    }
    $j=$ready[0]
    if($null -ne $j.task){$j.task.GetAwaiter().GetResult()}
    $target=$j.target
    if($target.restore_files -gt 0) {
        Copy-Item -LiteralPath $j.staged -Destination (Split-Path -Parent $j.p) -Recurse -Force
        Assert-Snapshot $j.p @{files=$target.restore_files;bytes=$target.restore_bytes} $false
    }
    $result=@{phase='completed';path=$j.n;archived_files=$target.files;archived_bytes=$target.bytes;live_files=[long]$target.restore_files;live_bytes=[long]$target.restore_bytes}
    $result | ConvertTo-Json -Compress | Add-Content -LiteralPath $journal -Encoding UTF8
    $script:results += $result
    $script:pending=@($script:pending | Where-Object {$_.n -ne $j.n})
    if($script:results.Count % 20 -eq 0){Write-Output "Cleaned run directories: $($script:results.Count)/$($plan.directories.Count)"}
}
'''
    source=source.replace(marker,finish+marker)
    source=source.replace('$cacheTargets=@($plan.cache_directory_targets)','while($script:pending.Count -gt 0){Finish-One}\n$cacheTargets=@($plan.cache_directory_targets)')
    source=source.replace("continuation='Verified interrupted root before native directory deletion'","continuation='Verified interrupted root; four disjoint native directory tasks, exact root boundaries' ")
    out=R/'scripts/parallel_cleanup214.ps1'
    assert not out.exists();out.write_text(source,'utf-8')
    print('Generated',out.name)

def verify():
    plan=json.loads((R/'work/cleanup214/deletion_plan.json').read_text('utf-8'))
    assert digest(R/plan['archive_path'])==plan['archive_sha256']
    events=[json.loads(x) for x in (R/'work/cleanup214/deletion_progress.jsonl').read_text('utf-8-sig').splitlines() if x.strip()]
    complete={x['path'] for x in events if x['phase']=='completed'}
    partial={x['path'] for x in events if x['phase']=='validated'}-complete
    assert len(partial)<=1, 'Sequential worker must have stopped before parallel continuation'
    db=sqlite3.connect(f'file:{(R/plan["archive_path"]).as_posix()}?mode=ro',uri=True)
    states=[]
    for n in sorted(partial):
        p=safe(n);count=size=max_time=0
        if p.exists():
            for base,dirs,files in os.walk(p,followlinks=False):
                for name in dirs: safe((Path(base)/name).relative_to(R).as_posix())
                for name in files:
                    f=Path(base)/name;rel=f.relative_to(R).as_posix();safe(rel)
                    h=db.execute('SELECT sha256 FROM entries WHERE path=?',(rel,)).fetchone()
                    assert h and digest(f)==h[0],rel
                    st=f.stat();count+=1;size+=st.st_size;max_time=max(max_time,st.st_mtime_ns//100+116444736000000000)
        states.append({'path':n,'files':count,'bytes':size,'max_filetime':max_time,'exists':p.exists(),'remaining_files_SHA256_checked':True})
    out=R/'work/cleanup214/resume_parallel_verified.json'
    assert not out.exists()
    out.write_text(json.dumps({'status':'PASS','archive_sha256':plan['archive_sha256'],'completed_directories':len(complete),'partial':states},indent=2)+'\n','utf-8')
    db.close();print(out.read_text('utf-8'))

if __name__=='__main__':
    import sys
    generate() if sys.argv[1]=='generate' else verify()
