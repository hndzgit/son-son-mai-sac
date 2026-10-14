import os
import glob

BASE_DIR = "/Users/hoainam/Documents/Sơn son mài sắc"

old_bg = "background: var(--site-paper-surface, linear-gradient(#fff3d4ad, #fff3d4ad), url(/story-assets/backgrounds/gold-foundation-v2.webp)) center / 600px 600px repeat !important;"
new_bg = "background: var(--site-paper-surface, linear-gradient(#fff3d4ad, #fff3d4ad), url(/story-assets/backgrounds/gold-foundation-v2.webp)) center / 600px 600px repeat !important;"

# Find all html and py files
files_to_check = []
for root, dirs, files in os.walk(BASE_DIR):
    # skip .git
    if '.git' in root or 'node_modules' in root:
        continue
    for f in files:
        if f.endswith('.html') or f.endswith('.py'):
            files_to_check.append(os.path.join(root, f))

count = 0
for fpath in files_to_check:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_bg in content:
            content = content.replace(old_bg, new_bg)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            print(f"Updated background in: {os.path.relpath(fpath, BASE_DIR)}")
    except Exception as e:
        print(f"Error reading {fpath}: {e}")

print(f"\nTotal files updated: {count}")
