import os, subprocess

FILES = [
    "_next/static/chunks/840-f19fdd306966b2e5.js",
    "ma_nguon_css_js/js/840-f19fdd306966b2e5.js"
]

for fpath in FILES:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Section 1 title:
    old_sec1 = '1. PHỦ LỚP SƠN TRONG & Ủ KH\\xd4'
    new_sec1 = '1. PHỦ LỚP SƠN ĐEN (SƠN THEN) & Ủ KH\\xd4'
    if old_sec1 in content:
        content = content.replace(old_sec1, new_sec1)
        print(f"[{fpath}] Replaced Section 1 title!")

    # 2. Polish subtitle:
    old_polish = '"Bóng"===ei?"Đ\\xe3 đ\\xe1nh b\\xf3ng s\\xe1ng gương":"L\\xe0m mịn & s\\xe1ng b\\xf3ng bề mặt"'
    new_polish = '"Bóng"===ei?"Đ\\xe3 phủ sơn trong & đ\\xe1nh b\\xf3ng s\\xe1ng gương":"Lớp phủ trong (sơn c\\xe1nh gi\\xe1n) & đ\\xe1nh b\\xf3ng s\\xe1ng gương"'
    if old_polish in content:
        content = content.replace(old_polish, new_polish)
        print(f"[{fpath}] Replaced Polish subtitle!")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    res = subprocess.run(["node", "-c", fpath], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[{fpath}] Syntax error:", res.stderr)
    else:
        print(f"[{fpath}] Syntax OK!")
