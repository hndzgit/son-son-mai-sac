import urllib.request
import re

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

headers = {'User-Agent': 'Mozilla/5.0'}
urls_in_css = set()

for c in css_files:
    u = f'https://son-son-mai-sac-orpin.vercel.app{c}'
    try:
        req = urllib.request.Request(u, headers=headers)
        content = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'url\(([^)]+)\)', content)
        for m in matches:
            cleaned = m.strip('\'"')
            urls_in_css.add(cleaned)
    except Exception as e:
        print(f"Error {c}: {e}")

print("URLs in CSS:")
for u in sorted(urls_in_css):
    print(u)
