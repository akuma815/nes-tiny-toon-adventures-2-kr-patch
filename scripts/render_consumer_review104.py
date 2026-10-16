"""Work104 isolated headless Edge consumer supplement UI/render/download verification."""
from pathlib import Path
import subprocess,json,time,urllib.request,base64,hashlib
import websocket
R=Path(__file__).resolve().parents[1]
def main():
 source=R/'workspace/review/consumer047_104_20261005/review.html';out=R/'qa/review/consumer104_047';assert source.exists()and not out.exists();out.mkdir(parents=True);profile=out/'browser_profile';profile.mkdir();downloads=out/'synthetic_download';downloads.mkdir();exe=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe');assert exe.is_file();events=[];conn=None
 with (out/'edge_stdout.txt').open('wb')as log:
  proc=subprocess.Popen([str(exe),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+str(profile),'about:blank'],stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
  try:
   marker=profile/'DevToolsActivePort'
   for _ in range(100):
    if marker.exists():break
    time.sleep(.1)
   assert marker.exists();port=int(marker.read_text().splitlines()[0]);tabs=json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list'));conn=websocket.create_connection(next(t['webSocketDebuggerUrl']for t in tabs if t['type']=='page'),suppress_origin=True,timeout=20);serial=0
   def call(method,params=None):
    nonlocal serial
    serial+=1;ident=serial;conn.send(json.dumps({'id':ident,'method':method,'params':params or{}}))
    while True:
     answer=json.loads(conn.recv())
     if answer.get('id')==ident:assert'error'not in answer,answer;return answer.get('result',{})
     events.append(answer)
   def ev(js):
    answer=call('Runtime.evaluate',{'expression':js,'returnByValue':True,'awaitPromise':True});assert'exceptionDetails'not in answer,answer;return answer['result'].get('value')
   def capture(name,selector=None):
    params={'format':'png','captureBeyondViewport':bool(selector)}
    if selector:
     clip=ev('(()=>{const r=document.querySelector('+json.dumps(selector)+').getBoundingClientRect();return{x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height,scale:1}})()');params['clip']=clip
    (out/name).write_bytes(base64.b64decode(call('Page.captureScreenshot',params)['data']))
   call('Page.enable');call('Runtime.enable');call('Browser.setDownloadBehavior',{'behavior':'allow','downloadPath':str(downloads)});call('Emulation.setDeviceMetricsOverride',{'width':1280,'height':1000,'deviceScaleFactor':1,'mobile':False});call('Page.navigate',{'url':source.as_uri()})
   for _ in range(100):
    if ev('document.readyState')=='complete':break
    time.sleep(.1)
   assert ev('(async()=>{await document.fonts.ready;await Promise.all(Array.from(document.images).map(i=>i.decode()));return true})()')
   desktop=ev('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,candidates:document.querySelectorAll(".candidate").length,images:document.images.length,sizes:Array.from(document.images).map(i=>[i.naturalWidth,i.naturalHeight]),externalImages:Array.from(document.images).filter(i=>!i.src.startsWith("data:")).length,pending:Array.from(document.querySelectorAll("select")).every(s=>s.value==="pending")})');assert desktop['width']==1280 and desktop['scrollWidth']<=1280 and desktop['candidates']==3 and desktop['images']==6 and desktop['externalImages']==0 and desktop['pending'];assert desktop['sizes']==[[56,8],[256,240],[48,32],[256,240],[480,360],[256,240]]
   initial=ev('decisions()');assert initial['human_approved']is False and initial['release_eligible']is False and len(initial['review_input'])==3
   capture('desktop_top.png')
   for candidate in('HOWTO','PAUSE','POW'):capture('desktop_'+candidate+'.png','#'+candidate)
   ev('document.querySelector("[data-id=HOWTO]").value="investigate";document.querySelector("[data-note=HOWTO]").value="합성 UI 저장 검사 — 사람 검토 의견 아님";document.querySelector("#export").click()')
   downloaded=downloads/'TinyToon2_047_consumer_review_input.json'
   for _ in range(100):
    if downloaded.exists():break
    time.sleep(.1)
   assert downloaded.exists();saved=json.loads(downloaded.read_text('utf-8'));assert saved['human_approved']is False and saved['release_eligible']is False and saved['review_input'][0]['choice']=='investigate'and'합성'in saved['review_input'][0]['note'];ev('document.querySelector("[data-id=HOWTO]").value="pending";document.querySelector("[data-note=HOWTO]").value=""')
   call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':False});ev('scrollTo(0,0)');mobile=ev('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,imagesFit:Array.from(document.images).every(i=>i.getBoundingClientRect().right<=innerWidth),controlsFit:Array.from(document.querySelectorAll("select,textarea")).every(i=>i.getBoundingClientRect().right<=innerWidth),paragraphFont:getComputedStyle(document.querySelector("header p")).fontSize})');assert mobile['scrollWidth']<=390 and mobile['imagesFit']and mobile['controlsFit']and mobile['paragraphFont']=='17px';capture('mobile_top.png')
   for candidate in('HOWTO','PAUSE','POW'):capture('mobile_'+candidate+'.png','#'+candidate)
   assert ev('JSON.stringify(decisions())')==json.dumps(initial,ensure_ascii=False,separators=(',',':'));errors=[x for x in events if x.get('method')=='Runtime.exceptionThrown'];assert not errors
   report={'work':104,'status':'PASS_CONSUMER_REVIEW_RENDER_AND_SYNTHETIC_DOWNLOAD','source':source.relative_to(R).as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'desktop':desktop,'mobile':mobile,'actual_download_test':True,'synthetic_download_path':downloaded.relative_to(R).as_posix(),'synthetic_download_sha256':hashlib.sha256(downloaded.read_bytes()).hexdigest(),'not_human_review_input':True,'restored_all_pending':True,'JS_errors':errors,'screenshots':8,'human_approved':False,'scope':'Local private consumer review UI/render/download only. No game/new translation or human approval/Cafe publication.'};(out/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
   try:call('Browser.close')
   except websocket.WebSocketConnectionClosedException:pass
  finally:
   if conn:
    try:conn.send(json.dumps({'id':999999,'method':'Browser.close'}))
    except websocket.WebSocketConnectionClosedException:pass
    conn.close()
   try:proc.wait(timeout=10)
   except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=10)
if __name__=='__main__':main()