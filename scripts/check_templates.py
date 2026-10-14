import os
import re

js_dir = 'ma_nguon_css_js/js'
for f in os.listdir(js_dir):
    if not f.endswith('.js'): continue
    with open(os.path.join(js_dir, f), 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    matches = re.findall(r'`[^`]*(?:story-assets|textures|images|models|audio)[^`]*`', c)
    for m in matches:
        print(f"[{f}] {m}")
print("Done template scan.")
