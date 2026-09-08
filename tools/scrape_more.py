"""Fetch the creatives the angle strips need, beyond the twelve already saved."""
import json,os,subprocess,time,urllib.request
S=os.environ.get('SCRAPE_SURFACE','surface:35')
OUT=os.path.expanduser('~/Desktop/projects/sightline-mockup/assets')
JS=('(()=>{const i=[...document.querySelectorAll("img")]'
    '.map(x=>({s:x.currentSrc||x.src,a:x.naturalWidth*x.naturalHeight}))'
    '.filter(x=>x.a>90000&&/scontent|fbcdn/.test(x.s)).sort((p,q)=>q.a-p.a);'
    'if(i.length)return i[0].s;'
    'const v=document.querySelector("video");return v&&v.poster?v.poster:""})()')
def cmux(*a,t=120):
    r=subprocess.run(['cmux','browser','--surface',S,*a],capture_output=True,text=True,timeout=t,
                     env={**os.environ,'CMUX_QUIET':'1'})
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
def dl(url,dest):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=60) as r,open(dest,'wb') as f: f.write(r.read())
    return os.path.getsize(dest)
need=json.load(open('need_imgs.json'))
files={'huel':'ds_huel.json','specsavers':'ds_specsavers.json','laya':'ds_layahealthcare.json'}
ok=miss=0
for slug,idxs in need.items():
    ads=json.load(open(files[slug]))['ads']
    for n in idxs:
        dest=f'{OUT}/{slug}-{n:02d}.jpg'
        if os.path.exists(dest) and os.path.getsize(dest)>4000: continue
        cmux('goto',ads[n]['snap']); src=''
        for _ in range(10):
            time.sleep(1.0); src=cmux('eval',JS)
            if src.startswith('http'): break
        if src.startswith('http'):
            try: dl(src,dest); ok+=1; print('ok  ',os.path.basename(dest))
            except Exception as e: miss+=1; print('FAIL',dest,e)
        else: miss+=1; print('MISS',os.path.basename(dest),ads[n]['h'][:34])
print('downloaded',ok,'missing',miss)
