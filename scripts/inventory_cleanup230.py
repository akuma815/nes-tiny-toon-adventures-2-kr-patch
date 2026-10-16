"""Read-only file counts and sizes; exclude traversal through reparse points."""
import json, os, stat
from collections import defaultdict
from seal_nonplay171 import R

def main():
    totals=defaultdict(lambda:{'files':0,'bytes':0});reparse=[]
    for directory,dirs,files in os.walk(R,followlinks=False):
        for name in dirs[:]:
            p=os.path.join(directory,name)
            if os.lstat(p).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                reparse.append(os.path.relpath(p,R));dirs.remove(name)
        for name in files:
            p=os.path.join(directory,name);s=os.lstat(p)
            if s.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                reparse.append(os.path.relpath(p,R));continue
            relative=os.path.relpath(p,R).replace('\\','/');parts=relative.split('/')
            for n in range(1,min(3,len(parts))):
                key='/'.join(parts[:n]);totals[key]['files']+=1;totals[key]['bytes']+=s.st_size
    report={'work':230,'root':str(R),'groups':dict(sorted(totals.items())),'reparse_not_traversed':reparse}
    target=R/'qa/reports/cleanup230_inventory.json';assert not target.exists();target.write_text(json.dumps(report,indent=2)+'\n','utf-8')
    for key,value in sorted(totals.items(),key=lambda z:z[1]['bytes'],reverse=True)[:32]:print(f'{key}: {value["files"]} files, {value["bytes"]:,} bytes')
    print('publication/work detail:')
    for key,value in sorted(totals.items()):
        if key.startswith(('workspace/publication/','qa/publication/','work/')):print(key,value)
    print('reparse:',reparse)

if __name__=='__main__':main()
