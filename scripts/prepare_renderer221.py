"""Read-only first-game renderer reference, adapted to this eight-figure article."""
from pathlib import Path
from seal_nonplay171 import R
source=(R.parent/'Tiny Toon Adventures/scripts/render_public_worklog.py').read_text('utf-8')
source=source.replace('images\']==16','images\']==8').replace('headings\']==7','headings\']==8')
source=source.replace('spoilerClosed:!document.querySelector(".spoiler").open,','')
source=source.replace(" and state['spoilerClosed']",'')
source='\n'.join(line for line in source.splitlines() if 'document.querySelector(".spoiler summary")' not in line)+'\n'
source=source.replace(",'ending spoiler opens and closes'",'')
source=source.replace("assert state['images']==16","assert state['images']==8")
source=source.replace("state['headings']==7","state['headings']==8")
source='"""Adapted read-only renderer from game1; local article QA only."""\n'+source
out=R/'scripts/render_publication221.py';assert not out.exists();out.write_text(source,'utf-8')
assert '.spoiler' not in source and "state['images']==8" in source and "state['headings']==8" in source
print('Renderer prepared')
