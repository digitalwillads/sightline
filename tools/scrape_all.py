"""One pass over every creative cluster: grab the image and the ad-unit text
(CTA, description) in a single page load, for the ads we do not have yet."""
import json,os,subprocess,time,urllib.request
S=os.environ.get('SCRAPE_SURFACE','surface:35')
OUT=os.path.expanduser('~/Desktop/projects/sightline-mockup/assets')
CTAS=["Shop Now","Learn More","Sign Up","Book Now","Get Offer","Send Message","Contact Us",
      "Apply Now","Get Quote","Download","Subscribe","See Menu","Order Now","Watch More",
      "Play Game","Get Directions","Call Now","Buy Now","Donate Now","Install Now",
      "Request Time","Listen Now","Book Travel","Open Link","Get Showtimes","Read More",
      "See More","Watch Video","Try It","Get Started","Save","Message Page"]
LOW={c.lower():c for c in CTAS}
JS=('(()=>{const im=[...document.querySelectorAll("img")]'
    '.map(x=>({s:x.currentSrc||x.src,a:x.naturalWidth*x.naturalHeight}))'
    '.filter(x=>x.a>90000&&/scontent|fbcdn/.test(x.s)).sort((p,q)=>q.a-p.a);'
    'const v=document.querySelector("video");'
    'const src=im.length?im[0].s:(v&&v.poster?v.poster:"");'
    'const lines=document.body.innerText.split("\\n").map(s=>s.trim()).filter(Boolean).slice(0,40);'
    'return JSON.stringify({src,lines})})()')

def cmux(*a,t=120):
    r=subprocess.run(['cmux','browser','--surface',S,*a],capture_output=True,text=True,timeout=t,
                     env={**os.environ,'CMUX_QUIET':'1'})
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
def dl(url,dest):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=60) as r,open(dest,'wb') as f: f.write(r.read())

units=json.load(open('ad_units.json'))
files={'huel':'ds_huel.json','specsavers':'ds_specsavers.json','laya':'ds_layahealthcare.json'}
done=miss=0
for slug,f in files.items():
    ads=json.load(open(f))['ads']
    rows=units.get(slug,[])
    while len(rows)<len(ads): rows.append(None)
    for n,ad in enumerate(ads):
        img=f'{OUT}/{slug}-{n:02d}.jpg'
        have_img=os.path.exists(img) and os.path.getsize(img)>4000
        have_unit=isinstance(rows[n],dict) and rows[n].get('cta') is not None
        if have_img and have_unit: continue
        cmux('goto',ad['snap']); got=None
        for _ in range(10):
            time.sleep(1.0); raw=cmux('eval',JS)
            if raw.startswith('{'):
                d=json.loads(raw)
                if len(d['lines'])>6: got=d; break
        if not got: miss+=1; print('MISS',slug,n); continue
        if not have_img and got['src'].startswith('http'):
            try: dl(got['src'],img)
            except Exception as e: print('img fail',slug,n,e)
        if not have_unit:
            lines=got['lines']
            cta=next((LOW[l.lower()] for l in lines if l.lower() in LOW),'')
            desc=''
            if cta:
                i=lines.index(next(l for l in lines if l.lower()==cta.lower()))
                if i>0 and lines[i-1].lower() not in LOW: desc=lines[i-1]
            rows[n]={'cta':cta,'desc':desc,'cap':ad['dom']}
        done+=1
        if done%10==0:
            units[slug]=rows; json.dump(units,open('ad_units.json','w'),indent=1)
            print('...',done,'processed')
    units[slug]=rows
    json.dump(units,open('ad_units.json','w'),indent=1)
    print(slug,'complete')
print('processed',done,'missed',miss)
