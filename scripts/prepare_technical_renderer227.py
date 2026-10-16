"""Reuse the established isolated reader renderer for the technical guide UI."""
from seal_nonplay171 import R
p=R/'scripts/render_technical227.py';assert not p.exists()
s=(R/'scripts/render_publication221.py').read_text('utf-8')
s=s.replace('Adapted read-only renderer from game1; local article QA only.','Technical-guide local reader QA only; no game execution.')
s=s.replace("state['images']==8", "state['images']==2").replace("state['headings']==8", "state['headings']==16")
s=s.replace("state['externalImages']==0", "state['externalImages']==2")
start=s.index("            assert evaluate('document.querySelector(\".zoom\").click();")
end=s.index("            call('Emulation.setDeviceMetricsOverride',{'width':390",start)
s=s[:start]+'''            assert evaluate('document.querySelector("summary").click();document.querySelector("details").open')
            evaluate('document.querySelector("nav a").click()')
            assert evaluate('location.hash')=='#section1'
            evaluate('document.querySelectorAll("h2")[9].scrollIntoView()');capture('desktop_font_section.png')
'''+s[end:]
s=s.replace("document.querySelectorAll(\"h2\")[4].scrollIntoView()", "document.querySelectorAll(\"h2\")[9].scrollIntoView()")
s=s.replace("capture('mobile_bug_section.png')", "capture('mobile_font_section.png')")
s=s.replace("['image zoom opens','Escape closes zoom']", "['contents opens','first contents anchor navigates']")
p.write_text(s,'utf-8');print('Prepared render_technical227.py')
