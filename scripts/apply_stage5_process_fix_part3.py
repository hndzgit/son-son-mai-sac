import subprocess

for filepath in ['_next/static/chunks/840-f19fdd306966b2e5.js', 'ma_nguon_css_js/js/840-f19fdd306966b2e5.js']:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. galleryEyebrow:
    target_eye = 'children:["BẢN PHỐI 3D \\xb7 ",0===n?"CỐT MỘC":1===n?"L\\xc0M V\\xd3C":2===n?"SƠN NỀN":3===n?"TẠO H\\xccNH":"PHỦ SƠN & M\\xc0I NƯỚC"]'
    replace_eye = 'children:["BẢN PHỐI 3D \\xb7 ",0===n?"CỐT MỘC":1===n?"L\\xc0M V\\xd3C":2===n?"SƠN NỀN":3===n?"TẠO H\\xccNH":"PHỦ, M\\xc0I V\\xc0 HO\\xc0N THIỆN"]'
    if target_eye in c:
        c = c.replace(target_eye, replace_eye)
        print(f'{filepath}: patched galleryEyebrow')

    # 2. Stage 3 card title:
    target_s3 = 'children:"PHỦ SƠN & M\\xc0I NƯỚC"'
    replace_s3 = 'children:"PHỦ, M\\xc0I V\\xc0 HO\\xc0N THIỆN"'
    if target_s3 in c:
        c = c.replace(target_s3, replace_s3)
        print(f'{filepath}: patched Stage 3 card title')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)

    subprocess.run(['node', '-c', filepath], check=True)
    print(f'{filepath} node syntax verified OK')
