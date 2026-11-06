from pathlib import Path
import json,re,shutil
root=Path(__file__).resolve().parent.parent
original=(root/'public/menu.js').read_text()
# On subsequent builds the original image payloads are kept in authored menu-source.json.
source=root/'worker/menu-source.json'
if not source.exists():
 menu=json.loads(original.split('=',1)[1].strip().rstrip(';'))
 source.write_text(json.dumps(menu,ensure_ascii=False))
else: menu=json.loads(source.read_text())
assets={'/assets/placeholder.svg':{'type':'image/svg+xml','body':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#20291f"/><circle cx="200" cy="145" r="90" fill="none" stroke="#ddc18e" stroke-width="8"/><text x="200" y="160" text-anchor="middle" fill="#ddc18e" font-size="25">GIN SUSHI</text></svg>'}};public_menu=[]
for d in menu:
 m=re.fullmatch(r'data:([^;]+);base64,(.+)',d['image'])
 if not m: raise ValueError('Original image must be embedded')
 path='/assets/'+d['id']+'.jpg';assets[path]={'type':m[1],'body':m[2],'base64':True}
 public_menu.append({**d,'image':path})
(root/'public/menu.js').write_text('window.GIN_MENU='+json.dumps(public_menu,ensure_ascii=False)+';\n')
for f in (root/'public').iterdir():
 if not f.is_file(): continue
 mime='text/html; charset=utf-8' if f.suffix=='.html' else 'text/css; charset=utf-8' if f.suffix=='.css' else 'text/javascript; charset=utf-8'
 assets['/'+f.name]={'type':mime,'body':f.read_text()}
assetcode='const ASSETS='+json.dumps(assets,ensure_ascii=False)+';\nconst INITIAL_MENU='+json.dumps(public_menu,ensure_ascii=False)+';\n'
(root/'worker/assets.js').write_text(assetcode+'export {ASSETS,INITIAL_MENU};\n')
dist=root/'dist'
if dist.exists(): shutil.rmtree(dist)
(dist/'server').mkdir(parents=True)
(dist/'.openai').mkdir()
shutil.copy(root/'.openai/hosting.json',dist/'.openai/hosting.json')
code=(root/'worker/index.js').read_text().replace("import {ASSETS,INITIAL_MENU} from './assets.js';",assetcode)
(dist/'server/index.js').write_text(code)
print(json.dumps({'worker_bytes':len(code.encode()),'dishes':len(public_menu),'assets':len(assets)}))
