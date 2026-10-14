import os, subprocess

FILES = [
    "_next/static/chunks/840-f19fdd306966b2e5.js",
    "ma_nguon_css_js/js/840-f19fdd306966b2e5.js"
]

for fpath in FILES:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Make the big heading "Phủ sơn & Mài nước" so it matches the 05 badge
    old_str = '["Phủ then & M\\xe0i nước","Phủ lớp sơn đen (sơn then)'
    new_str = '["Phủ sơn & M\\xe0i nước","Phủ lớp sơn đen (sơn then)'
    if old_str in content:
        content = content.replace(old_str, new_str)
        print(f"[{fpath}] Updated sidebar big heading to Phủ sơn & Mài nước!")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    res = subprocess.run(["node", "-c", fpath], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[{fpath}] Syntax error:", res.stderr)
    else:
        print(f"[{fpath}] Syntax OK!")
