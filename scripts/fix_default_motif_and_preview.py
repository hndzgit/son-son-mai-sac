import os
import subprocess
import sys

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update j initial state in function D: motif: "Hoa sen" instead of "Thêm"
    old_j_init = '[j,C]=(0,r.useState)({...H,shape:"Mặt hộp",motif:"Th\\xeam",engraving:!1,ornament:"Kh\\xf4ng viền"})'
    new_j_init = '[j,C]=(0,r.useState)({...H,shape:"Mặt hộp",motif:"Hoa sen",engraving:!1,ornament:"Viền k\\xe9p"})'

    if old_j_init in content:
        content = content.replace(old_j_init, new_j_init, 1)
        print(f"[{filepath}] Updated j default motif to 'Hoa sen'")
    else:
        print(f"[{filepath}] Warning: old_j_init not found!")

    # 2. Update ey definition: ensure motif is j.motif (fallback to "Hoa sen" if "Thêm" or empty)
    old_ey = 'ey={...j,shape:p||"Mặt hộp",motif:"Th\\xeam",ornament:n<3?"Kh\\xf4ng viền":j.ornament}'
    new_ey = 'ey={...j,shape:p||"Mặt hộp",motif:"Th\\xeam"===j.motif?"Hoa sen":(j.motif||"Hoa sen"),ornament:n<3?"Kh\\xf4ng viền":(j.ornament||"Viền k\\xe9p")}'

    if old_ey in content:
        content = content.replace(old_ey, new_ey, 1)
        print(f"[{filepath}] Updated ey definition to use active motif instead of hardcoded 'Thêm'")
    else:
        print(f"[{filepath}] Warning: old_ey not found!")

    # 3. In the live surface visualizer, make sure img src uses G({...ey, motif:"Thêm"===ey.motif?"Hoa sen":ey.motif}) if k.top is not set
    old_img_src = '(0,a.jsx)("img",{src:(null==k?void 0:k.top)||G(ey),'
    new_img_src = '(0,a.jsx)("img",{src:(null==k?void 0:k.top)||G({...ey,motif:"Th\\xeam"===ey.motif?"Hoa sen":(ey.motif||"Hoa sen")}),'

    if old_img_src in content:
        content = content.replace(old_img_src, new_img_src, 1)
        print(f"[{filepath}] Updated img src to ensure motif is rendered")
    else:
        print(f"[{filepath}] Warning: old_img_src not found!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    res = subprocess.run(['node', '-c', filepath], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[{filepath}] Node syntax error:", res.stderr)
        return False
    else:
        print(f"[{filepath}] Node syntax PASSED!")

    return True

def run():
    files = [
        '_next/static/chunks/840-f19fdd306966b2e5.js',
        'ma_nguon_css_js/js/840-f19fdd306966b2e5.js'
    ]
    for f in files:
        if not patch_file(f):
            return False
    return True

if __name__ == '__main__':
    if not run():
        sys.exit(1)
    print("Done fixing default motif and preview!")
