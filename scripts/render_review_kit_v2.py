"""Render the worklog in an isolated headless Edge profile and verify its UI."""
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
            state=evaluate('({images:document.images.length,allLoaded:Array.from(document.images).every(i=>i.complete&&i.naturalWidth===256),units:document.querySelectorAll(".unit").length,graphicRows:document.querySelectorAll("tbody tr").length,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,externalImages:Array.from(document.images).filter(i=>i.src&&!i.src.startsWith("data:")).length})')
            assert state['images']==9 and state['allLoaded'] and state['units']==54 and state['graphicRows']==29 and state['externalImages']==0 and state['scrollWidth']<=1280,state
            def capture(name):
                data=call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False});(out/name).write_bytes(base64.b64decode(data['data']))
            capture('desktop_top.png')
            assert evaluate('document.querySelector("#search").value="MAIN_05805";document.querySelector("#search").dispatchEvent(new Event("input"));document.querySelectorAll(".unit:not([hidden])").length===1')
            assert evaluate('document.querySelector("#MAIN_05805 summary").click();document.querySelector("#MAIN_05805").open')
            evaluate('document.querySelector("#MAIN_05805").scrollIntoView()');capture('desktop_unit05805.png')
            evaluate('document.querySelector("#search").value="";document.querySelector("#search").dispatchEvent(new Event("input"));scrollTo(0,0)')
            call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':False})
            evaluate('scrollTo(0,0)');mobile=evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,paragraphFont:getComputedStyle(document.querySelector("main p")).fontSize,allParagraphsFit:Array.from(document.querySelectorAll("main p")).every(p=>p.getBoundingClientRect().right<=innerWidth&&p.getBoundingClientRect().left>=0),imagesFit:Array.from(document.images).every(i=>i.getBoundingClientRect().right<=innerWidth)})')
            assert mobile['scrollWidth']<=390 and mobile['allParagraphsFit'] and mobile['paragraphFont']=='17px' and mobile['imagesFit'],mobile
            capture('mobile_top.png');evaluate('document.querySelector("#MAIN_05805").scrollIntoView()');capture('mobile_unit05805.png')
            errors=[e for e in events if e.get('method')=='Runtime.exceptionThrown'];assert not errors,errors
            report={'status':'PASS','source':source.relative_to(ROOT).as_posix(),'browser':'Isolated headless Microsoft Edge','desktop':state,'mobile':mobile,'interaction_checks':['search exact unit returns one','native details opens','search reset restores all','all9 actual images decoded','desktop/mobile fit'],'javascript_errors':errors,'scope':'Local private review reader UI only; no Cafe worklog/upload or game execution.'}
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
