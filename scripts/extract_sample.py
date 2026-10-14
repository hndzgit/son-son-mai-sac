import urllib.request
import re

routes = ['/ve-du-an', '/san-pham', '/tin-tuc-su-kien', '/cau-chuyen-son-mai', '/kham-pha']
headers = {'User-Agent': 'Mozilla/5.0'}

for r in routes:
    u = f'https://son-son-mai-sac-orpin.vercel.app{r}'
    req = urllib.request.Request(u, headers=headers)
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    # strip tags
    clean = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', '\n', clean)
    lines = [line.strip() for line in clean.split('\n') if line.strip()]
    text = '\n'.join(lines)
    print(f"==================== {r} ====================")
    print(text[:1200])
    print("...\n")
