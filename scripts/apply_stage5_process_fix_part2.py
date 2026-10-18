import subprocess

for filepath in ['_next/static/chunks/840-f19fdd306966b2e5.js', 'ma_nguon_css_js/js/840-f19fdd306966b2e5.js']:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. galleryEyebrow:
    old_eye = r'4===n?"TẠO H\xccNH":"PHỦ SƠN & M\xc0I NƯỚC"'
    new_eye = r'4===n?"TẠO H\xccNH":"PHỦ, M\xc0I V\xc0 HO\xc0N THIỆN"'
    if old_eye in c:
        c = c.replace(old_eye, new_eye)
        print(f'{filepath}: patched galleryEyebrow')

    # 2. Status badge when mài water finishes:
    old_b = r'q>=85?["M\xe0i lộ ho\xe0n tất (",q,"%) · T\xe1c phẩm lộ r\xf5 tr\xean nền sơn m\xe0i"]'
    new_b = r'q>=85?["M\xe0i lộ ho\xe0n tất (",q,"%) · Sẵn s\xe0ng phủ sơn trong & ủ kh\xf4"]'
    if old_b in c:
        c = c.replace(old_b, new_b)
        print(f'{filepath}: patched status badge')

    # 3. Step 3 card next step button in stage 3:
    old_s3 = r'strong",{style:{color:"#22120c",fontSize:"13.5px",fontFamily:"\'Playfair Display\',serif"},children:"PHỦ SƠN & M\xc0I NƯỚC"}'
    new_s3 = r'strong",{style:{color:"#22120c",fontSize:"13.5px",fontFamily:"\'Playfair Display\',serif"},children:"PHỦ, M\xc0I V\xc0 HO\xc0N THIỆN"}'
    if old_s3 in c:
        c = c.replace(old_s3, new_s3)
        print(f'{filepath}: patched stage 3 card title')

    old_s3_btn = r'Bước tiếp theo: Phủ sơn & M\xe0i nước'
    new_s3_btn = r'Bước tiếp theo: Phủ, m\xe0i v\xe0 ho\xe0n thiện'
    if old_s3_btn in c:
        c = c.replace(old_s3_btn, new_s3_btn)
        print(f'{filepath}: patched stage 3 card button')

    old_s3_p = r'children:"Sau khi ho\xe0n th\xe0nh bố cục họa tiết, t\xe1c phẩm được phủ c\xe1c lớp sơn trong (sơn c\xe1nh gi\xe1n), ủ kh\xf4 v\xe0 tiến h\xe0nh m\xe0i nước tỉ mỉ để từng lớp họa tiết ẩn hiện với chiều s\xe2u độc bản."'
    new_s3_p = r'children:"Sau khi ho\xe0n th\xe0nh bố cục họa tiết, t\xe1c phẩm được phủ sơn đen (sơn then) v\xe0 ủ kh\xf4, tiến h\xe0nh m\xe0i nước tỉ mỉ l\xe0m lộ họa tiết, sau đ\xf3 tiếp tục phủ lớp sơn trong, ủ kh\xf4 rồi mới đ\xe1nh b\xf3ng ho\xe0n thiện."'
    if old_s3_p in c:
        c = c.replace(old_s3_p, new_s3_p)
        print(f'{filepath}: patched stage 3 card paragraph')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)

    subprocess.run(['node', '-c', filepath], check=True)
    print(f'{filepath} node syntax verified OK')
