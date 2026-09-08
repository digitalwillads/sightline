"""Pull a brand's live ads from the Meta Ad Library, cluster creatives into
variants, classify each by persuasion angle, and emit the report dataset."""
import os,sys,json,re,datetime,collections,urllib.parse,urllib.request

TOK=os.environ['TOK']; TODAY=datetime.date(2026,9,8)
API='https://graph.facebook.com/v21.0/ads_archive?'
FIELDS=('id,page_id,page_name,ad_creative_bodies,ad_creative_link_titles,'
        'ad_creative_link_captions,ad_delivery_start_time,publisher_platforms,eu_total_reach,ad_snapshot_url')

def fetch(params):
    with urllib.request.urlopen(API+urllib.parse.urlencode(params)) as r: return json.load(r)

def pull(term,pages=6):
    base={'access_token':TOK,'search_terms':term,'ad_type':'ALL','ad_reached_countries':"['IE']",
          'ad_active_status':'ACTIVE','limit':'100','fields':FIELDS}
    out=[];p=dict(base)
    for _ in range(pages):
        d=fetch(p); out+=d.get('data',[])
        c=d.get('paging',{}).get('cursors',{}).get('after')
        if not c or not d.get('paging',{}).get('next'): break
        p=dict(base); p['after']=c
    return out

NON_EN=re.compile(r'\b(le|les|des|pour|vos|votre|avec|sans|est|une|con|per|und|dein|deine|dich|nicht|mit|für|sie|para|más|tus|del|niet|voor|het|een|il|della|dei)\b',re.I)
EN=re.compile(r'\b(the|your|you|and|with|for|not|our|that|this|from)\b',re.I)
def is_en(t): return len(EN.findall(t))>len(NON_EN.findall(t))

def norm(s): return re.sub(r'\s+',' ',(s or '')).strip()

# Shared taxonomy. Ordered most specific first; the winner is the angle with the
# most distinct pattern hits, ties broken by this order.
ANGLES=[
 ('Urgency',        r'ends (today|sunday|monday|tonight|soon)|last chance|final|hurry|\d+ hours left|today only|while stocks|limited'),
 ('Price anchoring',r'(£|€|\$)\s?\d|% off|half price|save (up to )?[£€$\d]|cheaper|less than|under [€£$]|per (meal|serving|month)|free delivery|deal'),
 ('Social proof',   r'\b(\d[\d,\.]*)\s?(k|m|million|thousand)?\s?(customers|people|members|reviews|shoppers|users|athletes)|rated|★|reviews|loved by|join (over|the)'),
 ('Convenience',    r'meal prep|no prep|ready in|in (seconds|minutes)|just add|no (waiting|queue|hassle|chore)|book in|one tap|delivered|door'),
 ('Performance',    r'\d+\s?g (protein|fibre|fiber)|gains|reps\b|muscle|strength|training|workout|performance|recovery|pb\b'),
 ('Problem agitation',r'hungry again|didn.t do its job|still (spending|paying)|stop (paying|waiting)|tired of|struggling|fails|why (you|your)|sick of'),
 ('Authority',      r'nutritionist|dietitian|scientist|doctor|expert|certified|award|patented|clinically|research|years of'),
 ('Identity',       r'you deserve|become|who you are|confidence|feel like|your era|be the|lifestyle|community'),
 ('Product feature',r'flavou?r|colour|new\b|now available|range|collection|edition|ingredients|vitamins|nutrients|fabric|fit\b'),
]
def classify(text):
    t=text.lower(); best='Product feature'; bs=0
    for name,pat in ANGLES:
        n=len(set(re.findall(pat,t)))
        if n>bs: bs=n; best=name
    return best

def build(term,page_name,domain,label):
    raw=[a for a in pull(term) if a.get('page_name')==page_name]
    groups=collections.defaultdict(list)
    for a in raw:
        t=norm((a.get('ad_creative_link_titles') or [''])[0])
        b=norm((a.get('ad_creative_bodies') or [''])[0])
        if not b or not is_en(t+' '+b): continue
        groups[(t,b[:90])].append(a)
    rows=[]
    for (t,_),g in groups.items():
        starts=[datetime.date.fromisoformat(a['ad_delivery_start_time']) for a in g if a.get('ad_delivery_start_time')]
        if not starts: continue
        first=min(starts)
        body=norm((g[0].get('ad_creative_bodies') or [''])[0])
        cap=norm((g[0].get('ad_creative_link_captions') or [''])[0]) or domain
        rows.append(dict(id=g[0]['id'], snap=g[0].get('ad_snapshot_url',''),
                         days=(TODAY-first).days, first=first.isoformat(), variants=len(g),
                         h=t or body[:48], copy=body, dom=cap.lower(),
                         plats=sorted({p for a in g for p in (a.get('publisher_platforms') or [])}),
                         reach=sum(a.get('eu_total_reach') or 0 for a in g),
                         angle=classify(t+' '+body)))
    rows.sort(key=lambda r:-r['days'])
    ages=[r['days'] for r in rows]
    mix=collections.Counter(r['angle'] for r in rows)
    n=len(rows)
    return dict(term=term,page=page_name,domain=domain,label=label,
                clusters=n, live=sum(r['variants'] for r in rows),
                longest=max(ages), median=sorted(ages)[n//2], last30=sum(1 for a in ages if a<=30),
                reach=sum(r['reach'] for r in rows),
                mix=[(a,c,round(c/n*100)) for a,c in mix.most_common()],
                ads=rows)

if __name__=='__main__':
    term,page,dom,label=sys.argv[1:5]
    d=build(term,page,dom,label)
    json.dump(d,open(f'ds_{dom.split(".")[0]}.json','w'),indent=1)
    print(f"{dom}: {d['live']} live ads / {d['clusters']} creatives, longest {d['longest']}d, median {d['median']}d, +{d['last30']} in 30d, reach {d['reach']:,}")
    for a,c,p in d['mix']: print(f"   {a:20} {c:3} {p:3}%")
    for r in d['ads'][:6]: print('   *',r['days'],'d',r['variants'],'v |',r['angle'],'|',r['h'][:46],'|',r['copy'][:70].replace('\n',' '))
