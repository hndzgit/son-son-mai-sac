import urllib.request
import re
import json

routes = [
    '/',
    '/kham-pha',
    '/trai-nghiem',
    '/trai-nghiem/hanh-trinh',
    '/tu-chinh',
    '/cau-chuyen-son-mai',
    '/tin-tuc-su-kien',
    '/ve-du-an',
    '/san-pham'
]

headers = {'User-Agent': 'Mozilla/5.0'}

for r in routes:
    u = f'https://son-son-mai-sac-orpin.vercel.app{r}'
    req = urllib.request.Request(u, headers=headers)
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    
    # Extract __next_f payloads
    f_matches = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html)
    total_rsc = sum(len(m) for m in f_matches)
    print(f"Route: {r} -> HTML: {len(html)} bytes, RSC payload parts: {len(f_matches)}, RSC size: {total_rsc} chars")
