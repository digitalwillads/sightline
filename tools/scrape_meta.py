"""Second pass over each ad snapshot: capture the parts of the ad unit the API
does not return — the call-to-action label, the link description, the link
caption as Meta renders it, and the advertiser's page avatar."""
import json,subprocess,os,time,urllib.request

S=os.environ.get('SCRAPE_SURFACE','surface:33')
OUT=os.path.expanduser('~/Desktop/projects/sightline-mockup/assets')

# Meta's fixed CTA vocabulary. Matching against it is far steadier than
# guessing which line of the render is the button.
CTAS=["Shop Now","Learn More","Sign Up","Book Now","Get Offer","Send Message","Contact Us",
      "Apply Now","Get Quote","Download","Subscribe","See Menu","Order Now","Watch More",
      "Play Game","Get Directions","Call Now","Buy Now","Donate Now","Install Now",
      "Request Time","Listen Now","Book Travel","Open Link","Get Showtimes","Read More",
      "See More","Watch Video","Try It","Get Started","Save","Message Page","Whatsapp"]

JS = ('(()=>{const lines=document.body.innerText.split("\\n").map(s=>s.trim()).filter(Boolean);'
      'const av=[...document.querySelectorAll("img")].map(i=>({s:i.src,w:i.naturalWidth}))'
      '.filter(x=>x.w>20&&x.w<200).sort((a,b)=>b.w-a.w);'
      'return JSON.stringify({lines:lines.slice(0,40),avatar:av.length?av[0].s:""})})()')

def cmux(*a,t=90):
    r=subprocess.run(['cmux','browser','--surface',S,*a],capture_output=True,text=True,
                     timeout=t,env={**os.environ,'CMUX_QUIET':'1'})
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''

def dl(url,dest):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=60) as r, open(dest,'wb') as f: f.write(r.read())
    return os.path.getsize(dest)

def read(snap):
    cmux('goto',snap)
    for _ in range(10):
        time.sleep(1.0)
        raw=cmux('eval',JS)
        if raw.startswith('{'):
            d=json.loads(raw)
            if len(d['lines'])>6: return d
    return {'lines':[],'avatar':''}

def parse(d, caption_hint):
    lines=d['lines']
    low={c.lower():c for c in CTAS}
    cta=next((low[l.lower()] for l in lines if l.lower() in low), '')
    cap=next((l for l in lines if l.isupper() and '.' in l and ' ' not in l), '')
    desc=''
    if cta and cta in lines:
        i=lines.index(cta)
        # Meta stacks caption, headline, description, then the button.
        for back in (1,2):
            if i-back>=0:
                cand=lines[i-back]
                if cand!=cap and cand not in CTAS and len(cand)<90:
                    desc=cand if back==1 else desc
    return dict(cta=cta, cap=(cap or caption_hint).lower(), desc=desc, avatar=d['avatar'])

if __name__=='__main__':
    out={}
    for f,slug in [('ds_huel.json','huel'),('ds_specsavers.json','specsavers'),('ds_layahealthcare.json','laya')]:
        d=json.load(open(f)); rows=[]
        for n,ad in enumerate(d['ads'][:12]):
            try:
                info=parse(read(ad['snap']), ad['dom'])
            except Exception as e:
                info={'cta':'','cap':ad['dom'],'desc':'','avatar':''}; print('ERR',slug,n,e)
            if n==0 and info['avatar']:
                try: print('  avatar',dl(info['avatar'], f'{OUT}/{slug}-avatar.jpg'),'bytes')
                except Exception as e: print('  avatar fail',e)
            rows.append({k:info[k] for k in ('cta','cap','desc')})
            print(f'{slug}-{n:02d}  cta={info["cta"]!r:16} desc={info["desc"][:38]!r}')
        out[slug]=rows
        json.dump(out,open('ad_units.json','w'),indent=1)
    print('done')
