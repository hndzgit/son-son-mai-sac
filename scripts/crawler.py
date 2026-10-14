import urllib.request
import re
import os

BASE_URL = 'https://son-son-mai-sac-orpin.vercel.app'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_text(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8', errors='ignore')

def discover_assets():
    js_files = [
        '/_next/static/chunks/app/cau-chuyen-son-mai/page-18999a17f9a00aec.js',
        '/_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js',
        '/_next/static/chunks/app/layout-885788913b392875.js',
        '/_next/static/chunks/app/page-1f5c1f7a3dcd2475.js',
        '/_next/static/chunks/app/san-pham/page-2a9f8a05b3d81499.js',
        '/_next/static/chunks/app/tin-tuc-su-kien/page-0044ed8affa87fe5.js',
        '/_next/static/chunks/app/trai-nghiem/hanh-trinh/page-2c74554e92ef9036.js',
        '/_next/static/chunks/app/trai-nghiem/page-4cfd64a621149b8e.js',
        '/_next/static/chunks/app/tu-chinh/page-ad741d4479a4d65b.js',
        '/_next/static/chunks/app/ve-du-an/page-4431fa17e862519b.js',
        '/_next/static/chunks/498-9c99f7a25e206a4c.js',
        '/_next/static/chunks/840-f19fdd306966b2e5.js',
        '/_next/static/chunks/369-2063549c42145b16.js',
        '/_next/static/chunks/945-9b486e563304ccbb.js',
        '/_next/static/chunks/2200cc46-2612da093c775fbc.js',
        '/_next/static/chunks/webpack-f57e898f0a30f96c.js',
        '/_next/static/chunks/main-app-9f81c5509794c70d.js',
        # dynamic chunks mentioned in webpack
        '/_next/static/chunks/dcaa24afa7b9551d.js',
        '/_next/static/chunks/013156edff3e7a3c.js',
        '/_next/static/chunks/2c7bdfb3.9270a99e55a10c68.js',
        '/_next/static/chunks/2e273063009e2330.js',
        '/_next/static/chunks/4f4cbe31c8981f4a.js',
    ]

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

    all_assets = set()
    
    # 1. Check all html pages
    for r in routes:
        html = fetch_text(BASE_URL + r)
        # matches
        m = re.findall(r'(/story-assets/[^\s"\'\)\>]+)', html)
        all_assets.update(m)
        m2 = re.findall(r'(/[^\s"\'\)\>]+\.(?:webp|jpg|jpeg|png|svg|gif|mp4|webm|glb|gltf|hdr|mp3|wav|json))', html)
        all_assets.update([x for x in m2 if not x.startswith('/_next/')])

    # 2. Check all js chunks
    for js in js_files:
        try:
            txt = fetch_text(BASE_URL + js)
            m = re.findall(r'(/story-assets/[^\s"\'\)\>]+)', txt)
            all_assets.update(m)
            m2 = re.findall(r'(/[a-zA-Z0-9_\-\./]+\.(?:webp|jpg|jpeg|png|svg|gif|mp4|webm|glb|gltf|hdr|mp3|wav|json))', txt)
            all_assets.update([x for x in m2 if not x.startswith('/_next/')])
        except Exception as e:
            # print(f"Could not load {js}: {e}")
            pass

    # Clean assets
    cleaned = set()
    for a in all_assets:
        # remove quotes, trailing chars
        a = re.sub(r'[\"\';\)].*$', '', a)
        if '.' in os.path.basename(a):
            cleaned.add(a)

    print(f"Total unique static assets found: {len(cleaned)}")
    for a in sorted(cleaned):
        print(a)

if __name__ == '__main__':
    discover_assets()
