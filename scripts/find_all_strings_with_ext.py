import os
import re

js_dir = 'ma_nguon_css_js/js'
found_files = set()

for f in os.listdir(js_dir):
    if not f.endswith('.js'): continue
    path = os.path.join(js_dir, f)
    with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    
    # Matches any quoted string with an extension
    matches = re.findall(r'["\'`]([^"\'`\s\(\)]+\.[a-zA-Z0-9]{2,5})["\'`]', content)
    for m in matches:
        if any(m.endswith('.' + ext) for ext in ['jpg', 'jpeg', 'png', 'webp', 'svg', 'gif', 'mp3', 'wav', 'mp4', 'webm', 'ttf', 'woff', 'woff2', 'json', 'pdf', 'glb', 'gltf', 'obj', 'hdr']):
            found_files.add(m)

print(f"Total matching files found across all JS chunks: {len(found_files)}")
for item in sorted(found_files):
    print(item)
