"""Render each ad's Ad Library snapshot in a real browser and save its creative.

The snapshot page builds the creative in JS, so a plain fetch returns a shell.
cmux drives a headless-ish surface; we take the largest rendered image and
download it, so the mockup ships real files and no access token.
"""
import json,subprocess,sys,os,time,urllib.request

SURFACE=os.environ.get('SCRAPE_SURFACE','surface:33')
OUT=os.path.expanduser('~/Desktop/projects/sightline-mockup/assets')
JS_PICK=('(()=>{const i=[...document.querySelectorAll("img")]'
         '.map(x=>({s:x.currentSrc||x.src,a:x.naturalWidth*x.naturalHeight}))'
         '.filter(x=>x.a>90000 && /scontent|fbcdn/.test(x.s))'
         '.sort((p,q)=>q.a-p.a);return i.length?i[0].s:""})()')

def cmux(*args, timeout=60):
    r=subprocess.run(['cmux','browser','--surface',SURFACE,*args],
                     capture_output=True,text=True,timeout=timeout,
                     env={**os.environ,'CMUX_QUIET':'1'})
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''

def grab(snap, dest):
    cmux('goto', snap, timeout=90)
    src=''
    for _ in range(12):
        time.sleep(1.0)
        src=cmux('eval', JS_PICK)
        if src.startswith('http'): break
    if not src.startswith('http'): return False
    req=urllib.request.Request(src, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=45) as r, open(dest,'wb') as f:
        f.write(r.read())
    return os.path.getsize(dest) > 4000

if __name__=='__main__':
    todo=[('ds_huel.json','huel'),('ds_specsavers.json','specsavers'),('ds_layahealthcare.json','laya')]
    got={}
    for f,slug in todo:
        d=json.load(open(f)); got[slug]=[]
        for n,ad in enumerate(d['ads'][:12]):
            name=f'{slug}-{n:02d}.jpg'; dest=os.path.join(OUT,name)
            if os.path.exists(dest) and os.path.getsize(dest)>4000:
                got[slug].append(name); print('cached',name); continue
            ok=False
            try: ok=grab(ad['snap'], dest)
            except Exception as e: print('ERR',name,e)
            print(('ok    ' if ok else 'MISS  ')+name, ad['h'][:40])
            got[slug].append(name if ok else None)
        json.dump(got,open('images.json','w'),indent=1)
    print(json.dumps({k:sum(1 for x in v if x) for k,v in got.items()}))
