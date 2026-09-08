"""Turn the pulled + labelled Ad Library data into the mockup's JS dataset."""
import json,collections,datetime,re,os,label
ASSETS=os.path.expanduser('~/Desktop/projects/sightline-mockup/assets')

PLAT={'facebook':'FB','instagram':'IG','audience_network':'Audience Network',
      'messenger':'Messenger','threads':'Threads'}
UNITS=json.load(open('ad_units.json'))
BRANDS=[('ds_huel.json','huel.com','Huel','huel'),
        ('ds_specsavers.json','specsavers.ie','Specsavers Ireland','specsavers'),
        ('ds_layahealthcare.json','layahealthcare.ie','Laya Healthcare','laya')]

def human(n):
    if n>=1_000_000: return f'{n/1_000_000:.1f}M'
    if n>=1_000: return f'{n/1_000:.0f}k'
    return str(n)
def datefmt(iso):
    d=datetime.date.fromisoformat(iso); return d.strftime('%-d %b %Y')
def host(c, fallback):
    # Meta renders the link caption as a bare host. The API sometimes hands
    # back a full URL, so normalise before display.
    c=re.sub(r'^https?://','',(c or '').strip()).split('/')[0]
    c=re.sub(r'^www\.','',c)
    return (c or fallback).lower()

def trim(t,n):
    t=re.sub(r'\s+',' ',t).strip()
    return t if len(t)<=n else t[:n].rsplit(' ',1)[0]+'…'

out={}
for f,dom,page,slug in BRANDS:
    d=json.load(open(f)); L=label.LABELS[dom]
    for r,code in zip(d['ads'],L['seq']): r['angle']=L[code]
    mix=collections.Counter()
    for r in d['ads']: mix[r['angle']]+=r['variants']
    tot=sum(mix.values())
    order=[a for a,_ in mix.most_common()]
    # one real example headline per angle: the longest-running ad carrying it
    ex={}
    for r in d['ads']:
        ex.setdefault(r['angle'], r['h'] or r['copy'][:60])
    # Each angle carries the creatives filed under it, longest-running first,
    # so the share bar can be checked against the ads themselves.
    by=collections.defaultdict(list)
    for i,r in enumerate(d['ads']): by[r['angle']].append(i)
    angles=[]
    for a in order:
        idxs=by[a][:4]
        thumbs=[dict(img=f'assets/{slug}-{i:02d}.jpg', h=trim(d['ads'][i]['h'],52), days=d['ads'][i]['days'])
                for i in idxs if os.path.exists(os.path.join(ASSETS,f'{slug}-{i:02d}.jpg'))]
        top=d['ads'][by[a][0]]
        angles.append(dict(name=a, share=round(mix[a]/tot*100), count=mix[a],
                           ex=trim(ex[a],64), exDays=top['days'],
                           thumbs=thumbs, rest=max(0, mix[a]-len(thumbs))))
    plats=sorted({p for r in d['ads'] for p in r['plats']})
    # Advertisers reuse one link title across many creatives. When a headline
    # repeats, fall back to the ad's own opening line so the grid reads as
    # distinct ads rather than one ad printed nine times.
    seen=set()
    def headline(r):
        t=trim(r['h'] or '',62)
        if t and t.lower() not in seen:
            seen.add(t.lower()); return t
        first=re.split(r'(?<=[.!?])\s|\n', r['copy'].strip())[0]
        return trim(first or t or r['copy'][:50], 62)
    def body(r,h):
        # If the headline was lifted from the copy, don't print that line twice.
        c=re.sub(r'\s+',' ',r['copy']).strip()
        if h.endswith('…'): return trim(c,210)   # headline was cut; keep the copy whole
        head=h.strip()
        if head and c.lower().startswith(head.lower()[:28]):
            rest=c[len(head):].lstrip(' .!?—-')
            if len(rest)>60: c=rest
        return trim(c,210)
    units=UNITS.get(slug,[])
    cards=[]
    for n,r in enumerate(d['ads'][:12]):
        h=headline(r)
        u=units[n] if n<len(units) else {}
        # Meta stacks caption, headline, description, button. When the scraped
        # description is just the headline again, the ad had no description.
        title=trim(r['h'],62)          # the link title Meta actually renders
        desc=u.get('desc','')
        if desc.strip().lower() in (title.strip().lower(), h.strip().lower().rstrip('…')): desc=''
        img=f'assets/{slug}-{n:02d}.jpg'
        vid=f'assets/{slug}-{n:02d}.mp4'
        has_img=os.path.exists(os.path.join(ASSETS,f'{slug}-{n:02d}.jpg'))
        has_vid=os.path.exists(os.path.join(ASSETS,f'{slug}-{n:02d}.mp4'))
        cards.append(dict(h=h, copy=body(r,h), dom=r['dom'],
                          img=img if has_img else '', video=vid if has_vid else '',
                          cta=u.get('cta',''), desc=trim(desc,60), cap=host(r['dom'] or u.get('cap'), dom), title=title,
                          days=r['days'], first=datefmt(r['first']), variants=r['variants'],
                          angle=r['angle'], plats=' · '.join(PLAT.get(p,p) for p in r['plats'][:3]),
                          reach=human(r['reach'])))
    nodes=[dict(x=L['map'][a][0], y=L['map'][a][1], n=mix[a], l=a) for a in order if a in L['map']]
    win=[dict(t=trim(d['ads'][i]['h'],70),
              s=f"{d['ads'][i]['variants']} variant{'s' if d['ads'][i]['variants']>1 else ''} · {human(d['ads'][i]['reach'])} EU reach",
              days=d['ads'][i]['days'], why=w) for i,w in zip(L['winners'],L['why'])]
    out[dom]=dict(
        brand=page, page=page, domain=dom, real=True,
        avatar=f'assets/{slug}-avatar.jpg',
        follow=f"Page {page}", since=f"Oldest live ad {datefmt(d['ads'][-1]['first'] if False else min(r['first'] for r in d['ads']))}",
        total=d['live'],
        stats=[
          dict(v=str(d['live']),k='live ads',dd=f"+{d['last30']} in 30 days"),
          dict(v=str(d['longest']),s='days',k='longest run',dd='still running'),
          dict(v=str(d['clusters']),k='distinct creatives',dd=f"{d['live']} ads grouped"),
          dict(v=str(d['median']),s='days',k='median age',dd='slow rotation' if d['median']>90 else 'fast rotation',hot=d['median']<=90),
          dict(v=human(d['reach']),k='EU reach, live ads',dd='Ad Library reported'),
          dict(v=str(len(plats)),k='platforms',dd='every Meta surface'),
        ],
        ads=cards, angles=angles, nodes=nodes,
        gap=dict(x=L['gap'][0],y=L['gap'][1],l='open'),
        mapNote=L['note'], winners=win)

js=json.dumps(out,ensure_ascii=False,indent=1)
open('library_real.json','w').write(js)
print(js[:600])
for dom,v in out.items():
    print(dom, v['total'],'live |',len(v['ads']),'cards |',len(v['angles']),'angles |',v['stats'][4]['v'],'reach')
