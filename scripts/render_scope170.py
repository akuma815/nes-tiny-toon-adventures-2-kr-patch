"""Render170 private non-play review; browser artifact QA, no game execution."""
import argparse,base64,json,subprocess,time,urllib.request
from pathlib import Path
import websocket
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    source=a.input.resolve();source.relative_to(ROOT/'workspace/review')
    out=a.output.resolve();out.relative_to(ROOT/'qa/review');out.mkdir(parents=True,exist_ok=False)
    exe=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe');assert exe.is_file()
    profile=out/'browser_profile';profile.mkdir()
    command=[str(exe),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+str(profile),'about:blank']
    with (out/'edge_stdout.txt').open('wb') as log:
        p=subprocess.Popen(command,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
        conn=None
        try:
            marker=profile/'DevToolsActivePort'
            for _ in range(100):
                if marker.exists():break
                time.sleep(.1)
            else:raise AssertionError('No isolated browser port')
            port=int(marker.read_text().splitlines()[0]);tabs=json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list'))
            conn=websocket.create_connection(next(t['webSocketDebuggerUrl'] for t in tabs if t['type']=='page'),suppress_origin=True,timeout=20)
            serial=0;events=[]
            def call(method,params=None):
                nonlocal serial
                serial+=1;ident=serial;conn.send(json.dumps({'id':ident,'method':method,'params':params or {}}))
                while True:
                    r=json.loads(conn.recv())
                    if r.get('id')==ident:
                        assert 'error' not in r,r;return r.get('result',{})
                    events.append(r)
            def evaluate(js):
                r=call('Runtime.evaluate',{'expression':js,'returnByValue':True,'awaitPromise':True});assert 'exceptionDetails' not in r,r;return r['result'].get('value')
            call('Page.enable');call('Runtime.enable')
            call('Emulation.setDeviceMetricsOverride',{'width':1280,'height':1000,'deviceScaleFactor':1,'mobile':False})
            call('Page.navigate',{'url':source.as_uri()})
            for _ in range(50):
                if evaluate('document.readyState')=='complete':break
                time.sleep(.1)
            assert evaluate('(async()=>{await document.fonts.ready;await Promise.all(Array.from(document.querySelectorAll("figure img")).map(i=>i.decode()));return true})()')
            state=evaluate('({images:document.images.length,allLoaded:Array.from(document.images).every(i=>i.complete&&i.naturalWidth===(i.classList.contains("static-source")?128:256)),units:document.querySelectorAll(".unit").length,graphicRows:document.querySelectorAll("tbody tr").length,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,externalImages:Array.from(document.images).filter(i=>i.src&&!i.src.startsWith("data:")).length})')
            assert state['images']==25 and state['allLoaded'] and state['units']==54 and state['graphicRows']==33 and state['externalImages']==0 and state['scrollWidth']<=1280,state
            def capture(name):
                data=call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False});(out/name).write_bytes(base64.b64decode(data['data']))
            capture('desktop_top.png')
            gate=evaluate('({text:document.querySelector("#MAIN_0590C .parallel section:nth-child(2) pre").textContent,caption:document.querySelector("figure:last-child figcaption").textContent})')
            assert evaluate('document.querySelector("#MAIN_0590C .parallel section:nth-child(1) pre").textContent')=='ざんねんだけど\nチケットがたりないよ'
            assert gate['text']=='아쉽지만\n티켓이 부족해!'  and 'dialogue_kr_poc_049'in gate['caption'],gate
            evaluate('document.querySelector("#MAIN_0590C").open=true;document.querySelector("#MAIN_0590C").scrollIntoView()');capture('desktop_shortage049.png')
            assert evaluate('document.querySelector("#search").value="MAIN_05805";document.querySelector("#search").dispatchEvent(new Event("input"));document.querySelectorAll(".unit:not([hidden])").length===1')
            assert evaluate('document.querySelector("#MAIN_05805 summary").click();document.querySelector("#MAIN_05805").open')
            evaluate('document.querySelector("#MAIN_05805").scrollIntoView()');capture('desktop_unit05805.png')
            assert evaluate('document.querySelector("#search").value="";document.querySelector("#search").dispatchEvent(new Event("input"));document.querySelectorAll(".unit:not([hidden])").length===54');evaluate('scrollTo(0,0)')
            call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':False})
            evaluate('scrollTo(0,0)');mobile=evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,paragraphFont:getComputedStyle(document.querySelector("main p")).fontSize,allParagraphsFit:Array.from(document.querySelectorAll("main p")).every(p=>p.getBoundingClientRect().right<=innerWidth&&p.getBoundingClientRect().left>=0),imagesFit:Array.from(document.images).every(i=>i.getBoundingClientRect().right<=innerWidth)})')
            assert mobile['scrollWidth']<=390 and mobile['allParagraphsFit'] and mobile['paragraphFont']=='17px' and mobile['imagesFit'],mobile
            evaluate('document.querySelector("#MAIN_0590C").scrollIntoView()');capture('mobile_shortage049.png');evaluate('scrollTo(0,0)')
            capture('mobile_top.png');evaluate('document.querySelector("#MAIN_05805").scrollIntoView()');capture('mobile_unit05805.png')
            extra=evaluate('({candidates:document.querySelectorAll(".candidate").length,staticImages:document.querySelectorAll(".static-source").length,actualImages:document.querySelectorAll("figure img:not(.static-source)").length,footer:document.body.textContent.includes("작업133은049의"),owner:document.body.textContent.includes("실제 플레이 검수는 사용자 담당")})')
            assert extra['candidates']==7 and extra['staticImages']==4 and extra['actualImages']==21 and extra['footer'] and extra['owner'],extra
            evaluate('document.querySelector("#PAUSE").open=true;document.querySelector("#PAUSE").scrollIntoView()');capture('mobile_candidate_pause.png')
            assert evaluate('document.querySelector("#PAUSE").open')
            scope_states=evaluate('Array.from(document.querySelectorAll(".candidate")).map(c=>c.dataset.state)')
            assert scope_states.count('retained_by_explicit_scope')==3 and scope_states.count('connected_title_prompt_retained')==1 and scope_states.count('preserved_unresolved')==3,scope_states
            records=json.loads((source.parent/'review_records.json').read_text('utf-8'));credits=[u for u in records['units']if 'displayed_original'in u];assert len(credits)==3
            for u in credits:
                expression='document.querySelector("#'+u['entry_id']+' section pre").textContent'
                assert evaluate(expression)==u['displayed_original'],u['entry_id']
            evaluate('document.querySelector("#MAIN_05939").open=true;document.querySelector("#MAIN_05939").scrollIntoView()');capture('mobile_readable_credits.png')
            creditMobile=evaluate('({right:document.querySelector("#MAIN_05939 pre").getBoundingClientRect().right,width:innerWidth,scrollWidth:document.documentElement.scrollWidth})');assert creditMobile['right']<=390 and creditMobile['scrollWidth']<=390,creditMobile
            call('Emulation.setDeviceMetricsOverride',{'width':1280,'height':1000,'deviceScaleFactor':1,'mobile':False});evaluate('document.querySelector("#MAIN_05939").scrollIntoView()');capture('desktop_readable_credits.png')
            errors=[e for e in events if e.get('method')=='Runtime.exceptionThrown'];assert not errors,errors
            report={'status':'PASS','source':source.relative_to(ROOT).as_posix(),'browser':'Isolated headless Microsoft Edge','desktop':state,'mobile':mobile,'readable_credits_exact':3,'credit_mobile_fit':creditMobile,'interaction_checks':['search exact unit returns one','native details opens','search reset restores all','21 reused actual images and4 static atlases decoded','desktop/mobile fit'],'javascript_errors':errors,'nonplay_candidate_UI':extra,'scope_states':scope_states,'current049_shortage_text_and_provenance':gate,'scope':'Local170 review reader browser UI only. Actual play user-owned; no Cafe article/upload or game execution.'}
            (out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
            try:call('Browser.close')
            except websocket.WebSocketConnectionClosedException:pass
        finally:
            if conn:
                try:conn.send(json.dumps({'id':999999,'method':'Browser.close'}))
                except websocket.WebSocketConnectionClosedException:pass
                conn.close()
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=10)
if __name__=='__main__':main()
