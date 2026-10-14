"""Reproducible read-only public-site crawl, dependency graph and byte-level audit.
No login, form submission, hidden endpoint brute forcing or remote code execution.
Usage: python3 scripts/audit_recrawl.py [--refresh]
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,urlunsplit,unquote
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import requests,json,re,hashlib,datetime,subprocess,sys,time

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'kiem_tra_2026-10-12'
RAW=OUT/'ban_chup_goc'
BASE='https://son-son-mai-sac-orpin.vercel.app'
HOST=urlsplit(BASE).netloc
EXT=re.compile(r'\.(?:js|css|png|jpe?g|webp|svg|gif|ico|avif|ttf|otf|woff2?|glb|gltf|bin|hdr|exr|mp[34]|wav|ogg|webm|pdf|json|xml|txt|map)(?:\?|$)',re.I)
MANIFEST=OUT/'manifest.json'
seen={r['url']:r for r in json.loads(MANIFEST.read_text())} if MANIFEST.exists() and '--refresh' not in sys.argv else {}
edges=set();pending=set();external=set();rejected=set()
def now():return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
def clean(ref,source):
    ref=ref.strip().replace('\\/','/').replace('\\u0026','&')
    if not ref or ref.startswith(('data:','blob:','javascript:','mailto:','tel:','#')):return None
    if any(x in ref for x in ['${','<','>','{','}','\\','\n']):return None
    u=urlsplit(urljoin(source,ref));
    if u.scheme not in ['http','https']:return None
    if u.netloc!=HOST:external.add(urlunsplit(u));return None
    # Hash states are preserved as graph edges, not separate HTTP requests.
    return urlunsplit(('https',u.netloc,u.path or '/',u.query,''))
def add(ref,source,kind='reference'):
    u=clean(ref,source)
    if not u:return
    edges.add((source,ref,u,kind))
    if u not in seen:pending.add(u)
def local_for(u,ct):
    p=urlsplit(u);rel=unquote(p.path).lstrip('/') or 'index.html'
    if '..' in Path(rel).parts:raise ValueError('unsafe path')
    if 'text/html' in ct and not Path(rel).suffix:rel+='/index.html'
    if p.query:rel+='.__q_'+hashlib.sha256(p.query.encode()).hexdigest()[:12]
    return RAW/rel
class HTML(HTMLParser):
    def __init__(self,url):super().__init__(convert_charrefs=True);self.url=url;self.elements=[];self.texts=[];self.depth=0;self.skip=0;self.scripts=[];self.script=None
    def handle_starttag(self,tag,attrs):
        d=dict(attrs);self.elements.append({'tag':tag,'attributes':d})
        if tag in ['style','script']:self.skip+=1
        if tag=='script':self.script=''
        for k in ['src','href','poster','data-src']:
            if d.get(k):add(d[k],self.url,tag+':'+k)
        if d.get('srcset'):
            for s in d['srcset'].split(','):add(s.strip().split(' ')[0],self.url,'srcset')
        if tag=='meta' and d.get('property',d.get('name','')) in ['og:image','twitter:image','og:video','og:audio']:add(d.get('content',''),self.url,'metadata')
    def handle_endtag(self,tag):
        if tag in ['script','style']:self.skip=max(0,self.skip-1)
        if tag=='script' and self.script is not None:self.scripts.append(self.script);self.script=None
    def handle_data(self,data):
        if self.script is not None:self.script+=data
        if not self.skip and data.strip():self.texts.append(data)
def discover(text,url,ct):
    if 'html' in ct:
        parser=HTML(url);parser.feed(text)
        slug=urlsplit(url).path.strip('/').replace('/','__') or 'trang_chu'
        if urlsplit(url).query:slug+='__query_'+hashlib.sha256(urlsplit(url).query.encode()).hexdigest()[:12]
        slug+='__'+hashlib.sha256(text.encode()).hexdigest()[:12]
        p=OUT/'trich_xuat_html'/(slug+'.json');p.parent.mkdir(exist_ok=True)
        p.write_text(json.dumps({'url':url,'text_nodes':parser.texts,'elements':parser.elements,'inline_scripts':parser.scripts},ensure_ascii=False,indent=2))
    # URLs embedded in HTML RSC payloads and escaped JS strings.
    t=text.replace('\\/','/').replace('\\u0026','&')
    for x in re.findall(r'''https?://[^\s"'<>\\`]+''',t):
        if urlsplit(x).netloc!=HOST:external.add(x)
        elif EXT.search(x) or '/opengraph-image' in x:add(x,url,'absolute')
    for x in re.findall(r'''(?<![\w/])/(?:story-assets|textures|models|images|fonts|_next/static)/[a-zA-Z0-9_./%?=&+-]+''',t):
        if EXT.search(x):add(x,url,'embedded_path')
    for x in re.findall(r'''["'](static/(?:chunks|css|media)/[^"'\\]+)["']''',t):add('/_next/'+x,url,'next_relative_resource')
    for x in re.findall(r'''["'](/[a-zA-Z0-9_/#-]*)["']''',t):
        if len(x)<180:add(x,url,'internal_literal')
    if 'css' in ct:
        for x in re.findall(r'''url\(\s*["']?([^)'"\s]+)''',t):add(x,url,'css_url')
        for x in re.findall(r'''@import\s+["']([^"']+)''',t):add(x,url,'css_import')
    for x in re.findall(r'[#@]\s*sourceMappingURL=([^\s*]+)',t):add(x,url,'source_map')
    if 'xml' in ct:
        for x in re.findall(r'<loc>(.*?)</loc>',t):add(x,url,'sitemap')
    if urlsplit(url).path=='/robots.txt':
        for x in re.findall(r'(?im)^sitemap:\s*(\S+)',t):add(x,url,'robots_sitemap')
    if '/webpack-' in url:
        # Next webpack runtime publishes finite mappings of async chunk ids to hashes.
        names=dict(re.findall(r'(\d+)===[a-z]\?"([a-f0-9]+)"',t))
        for mapping in re.findall(r'\{((?:\d+:"[a-f0-9]+",?)+)\}',t):
            for ident,h in re.findall(r'(\d+):"([a-f0-9]+)"',mapping):add('/_next/static/chunks/'+names.get(ident,ident)+'.'+h+'.js',url,'webpack_chunk_map')
        for fname in re.findall(r'["\']([a-f0-9]{8}\.[a-f0-9]{16}\.js)["\']',t):add('/_next/static/chunks/'+fname,url,'webpack_named_chunk')
    # Build ID published by Next in its RSC boot record.
    for build in set(re.findall(r'"(?:b|buildId)"\s*:\s*"([\w-]{10,})"',t.replace('\\"','"'))):
        for name in ['_buildManifest.js','_ssgManifest.js']:add('/_next/static/'+build+'/'+name,url,'published_build_id')
def fetch(url):
    row={'url':url,'fetched_at':now(),'method':'GET'}
    for attempt in range(3):
        try:
            r=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (compatible; SSMS-Public-Archive/1.0)','Accept-Encoding':'gzip, deflate'},timeout=(10,35))
            row.update(status=r.status_code,final_url=r.url,content_type=r.headers.get('content-type',''),headers=dict(r.headers),bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),redirects=[{'url':h.url,'status':h.status_code,'location':h.headers.get('location')} for h in r.history])
            if r.status_code>=500 and attempt<2:time.sleep(1);continue
            p=local_for(url,row['content_type']) if r.ok else OUT/'http_loi'/(hashlib.sha256(url.encode()).hexdigest()[:16]+'.body')
            p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(r.content);row['local_path']=str(p.relative_to(ROOT));return row
        except Exception as e:
            row['error']=str(e)
            if attempt<2:time.sleep(1)
    return row
def waves():
    while pending:
        batch=sorted(pending);pending.clear();batch=[u for u in batch if u not in seen]
        with ThreadPoolExecutor(max_workers=4) as pool:
            for r in pool.map(fetch,batch):
                seen[r['url']]=r
                if r.get('status')==200 and any(k in r.get('content_type','') for k in ['text/','javascript','json','xml','svg']):
                    discover((ROOT/r['local_path']).read_text(errors='replace'),r['url'],r['content_type'])
        save();print(json.dumps({'fetched':len(seen),'next':len(pending),'errors':sum(r.get('status')!=200 for r in seen.values())}),flush=True)
def save():
    OUT.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(sorted(seen.values(),key=lambda r:r['url']),ensure_ascii=False,indent=2))
    (OUT/'lien_ket_va_nguon.json').write_text(json.dumps([dict(source=a,reference=b,url=c,kind=d) for a,b,c,d in sorted(edges)],ensure_ascii=False,indent=2))
    (OUT/'lien_ket_ngoai.json').write_text(json.dumps(sorted(external),ensure_ascii=False,indent=2))

if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    # Reprocess cached responses so reruns can discover newly supported references.
    for r in list(seen.values()):
        if r.get('status')==200 and any(k in r.get('content_type','') for k in ['text/','javascript','json','xml','svg']):discover((ROOT/r['local_path']).read_text(errors='replace'),r['url'],r['content_type'])
    add(BASE+'/',BASE,'user_requested')
    for p in ['/robots.txt','/sitemap.xml']:add(p,BASE,'standard_discovery')
    for p in (ROOT/'trang_html_goc').glob('*.html'):discover(p.read_text(),BASE+'/','previous_capture:'+p.name)
    for p in (OUT/'trinh_duyet').glob('*.json'):
        d=json.loads(p.read_text());discover(d['html'],d['url'],'text/html')
    # Include previously archived public assets, including lazy/computed filenames.
    for p in (ROOT/'hinh_anh_assets').rglob('*'):
        if p.is_file():add('/'+p.relative_to(ROOT/'hinh_anh_assets').as_posix(),BASE,'previous_asset')
    waves()
    jsout=OUT/'trich_xuat_js_ast.json'
    if (RAW/'_next').exists():
        while True:
            subprocess.run(['node',str(ROOT/'scripts/audit_js_ast.cjs'),str(RAW/'_next'),str(jsout)],check=True)
            for item in json.loads(jsout.read_text()):
                src=BASE+'/_next/'+item['file']
                for s in item['strings']:
                    v=s['value']
                    if v.startswith('/') and (EXT.search(v) or re.fullmatch(r'/[\w/#?=&-]*',v)):add(v,src,'AST_literal')
                    elif v.startswith(('https://','http://')):clean(v,src)
                for tpl in item['templates']:
                    if any('/' in (x or '') for x in tpl['parts']):rejected.add((src,tpl['raw']))
            if not pending:break
            waves()
    (OUT/'bieu_thuc_dong_can_kiem_tra.json').write_text(json.dumps(sorted(rejected),ensure_ascii=False,indent=2))
    save()
