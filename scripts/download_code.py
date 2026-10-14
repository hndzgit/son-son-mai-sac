import urllib.request
import os

BASE_URL = 'https://son-son-mai-sac-orpin.vercel.app'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

css_files = [
    '/_next/static/css/58e70d5489b56972.css',
    '/_next/static/css/3d939b8161363d36.css',
    '/_next/static/css/a2d064b9694e6000.css',
    '/_next/static/css/033bcc6eb475b3ab.css',
    '/_next/static/css/61d7e631d8473667.css',
    '/_next/static/css/7d5ed180c1fe36fd.css',
    '/_next/static/css/e133a03ebd4e8d3a.css',
    '/_next/static/css/f7d6d17d52efcb3d.css',
    '/_next/static/css/7ec32e8ce89c4e93.css'
]

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
    '/_next/static/chunks/polyfills-42372ed130431b0a.js',
    '/_next/static/chunks/dcaa24afa7b9551d.js',
    '/_next/static/chunks/013156edff3e7a3c.js',
    '/_next/static/chunks/2c7bdfb3.9270a99e55a10c68.js',
    '/_next/static/chunks/2e273063009e2330.js',
    '/_next/static/chunks/4f4cbe31c8981f4a.js',
]

os.makedirs('ma_nguon_css_js/css', exist_ok=True)
os.makedirs('ma_nguon_css_js/js', exist_ok=True)

for c in css_files:
    fname = os.path.basename(c)
    dest = os.path.join('ma_nguon_css_js/css', fname)
    try:
        data = urllib.request.urlopen(urllib.request.Request(BASE_URL + c, headers=HEADERS)).read()
        with open(dest, 'wb') as f:
            f.write(data)
        print(f"Downloaded CSS: {fname} ({len(data)} bytes)")
    except Exception as e:
        print(f"Error CSS {c}: {e}")

for j in js_files:
    fname = j.replace('/_next/static/chunks/', '').replace('/', '_')
    dest = os.path.join('ma_nguon_css_js/js', fname)
    try:
        data = urllib.request.urlopen(urllib.request.Request(BASE_URL + j, headers=HEADERS)).read()
        with open(dest, 'wb') as f:
            f.write(data)
        print(f"Downloaded JS: {fname} ({len(data)} bytes)")
    except Exception as e:
        print(f"Error JS {j}: {e}")
