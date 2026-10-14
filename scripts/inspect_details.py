import urllib.request
import re

urls = [
    'https://son-son-mai-sac-orpin.vercel.app/_next/static/chunks/app/trai-nghiem/page-4cfd64a621149b8e.js',
    'https://son-son-mai-sac-orpin.vercel.app/_next/static/chunks/app/trai-nghiem/hanh-trinh/page-2c74554e92ef9036.js',
    'https://son-son-mai-sac-orpin.vercel.app/_next/static/chunks/app/tu-chinh/page-ad741d4479a4d65b.js'
]

headers = {'User-Agent': 'Mozilla/5.0'}

for u in urls:
    req = urllib.request.Request(u, headers=headers)
    txt = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    filename = u.split('/')[-1]
    print(f"=== {filename} ===")
    glb = re.findall(r'["\'`][^"\'`]+\.(?:glb|gltf|obj|fbx|hdr)["\'`]', txt)
    audio = re.findall(r'["\'`][^"\'`]+\.(?:mp3|wav|ogg|m4a)["\'`]', txt)
    json_files = re.findall(r'["\'`][^"\'`]+\.json["\'`]', txt)
    images = set(re.findall(r'/(?:story-assets|textures|images)/[a-zA-Z0-9_\-\./]+', txt))
    
    print('  3D models:', glb)
    print('  Audio:', audio)
    print('  JSON:', json_files)
    print('  Assets:', images)
