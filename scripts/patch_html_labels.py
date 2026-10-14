import os

def update_file(path):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    if "PHỦ, MÀI VÀ HOÀN THIỆN" in content:
        content = content.replace("PHỦ, MÀI VÀ HOÀN THIỆN", "PHỦ SƠN & MÀI NƯỚC")
        changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")

for p in ['kham-pha/index.html', 'trai-nghiem/index.html', 'index.html']:
    update_file(p)
print("Done updating HTML static templates!")
