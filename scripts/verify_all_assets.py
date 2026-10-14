import os
import re
import urllib.request
import urllib.parse

ROOT_DIR = os.path.abspath('kiem_tra_2026-10-12/ban_chup_goc')
LIVE_BASE = 'https://sonsonmaisat.site'

assets_found = set()

# Scan all html, css, js files in ROOT_DIR
for root, dirs, files in os.walk(ROOT_DIR):
    for f in files:
        if f.endswith(('.html', '.css', '.js', '.rsc')):
            path = os.path.join(root, f)
            with open(path, 'r', errors='ignore') as fp:
                content = fp.read()
                # Find all /_next/..., /story-assets/..., /models/..., /textures/..., /api/..., etc.
                matches = re.findall(r'/(?:_next|story-assets|models|textures|api|sounds|audio|brand)[\w\-\./%~]+', content)
                for m in matches:
                    clean = m.split('?')[0].split('#')[0].rstrip('\"\'()[]{}<>,;:')
                    assets_found.add(clean)

print(f"Total unique referenced asset paths found: {len(assets_found)}")

missing = []
for a in sorted(assets_found):
    local_p = os.path.join(ROOT_DIR, a.lstrip('/'))
    if not os.path.exists(local_p):
        missing.append(a)

print(f"Missing locally: {len(missing)}")
for m in missing[:30]:
    print("  Missing:", m)

if missing:
    print(f"\nAttempting to download {len(missing)} missing assets from {LIVE_BASE}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    for m in missing:
        url = LIVE_BASE + m
        local_p = os.path.join(ROOT_DIR, m.lstrip('/'))
        os.makedirs(os.path.dirname(local_p), exist_ok=True)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp, open(local_p, 'wb') as out:
                out.write(resp.read())
            print(f"Downloaded: {m} ({os.path.getsize(local_p)} bytes)")
        except Exception as e:
            print(f"Failed {m}: {e}")
