"""Close only the isolated browser launched by failed article render221."""
import json
from pathlib import Path
import websocket
from seal_nonplay171 import R
p=R/'qa/publication/render221/browser_profile/DevToolsActivePort'
lines=p.read_text('utf-8').splitlines();port=int(lines[0]);endpoint=lines[1]
assert endpoint.startswith('/devtools/browser/') and 1<=port<=65535
c=websocket.create_connection(f'ws://127.0.0.1:{port}{endpoint}',suppress_origin=True,timeout=10)
c.send(json.dumps({'id':1,'method':'Browser.close'}))
try:c.recv()
except websocket.WebSocketConnectionClosedException:pass
c.close()
print('Closed own failed render221 browser')
