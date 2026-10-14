# -*- coding: utf-8 -*-
"""
Script cập nhật toàn diện tiêu đề và mô tả phần LIÊN HỆ:
- Trong DOM HTML:
  <h2>CÙNG NỐI TIẾP<br/>HÀNH TRÌNH SƠN MÀI.</h2>
  <p>Liên hệ với Sơn Son Mài Sắc để cùng kết nối, đồng hành và lan tỏa những giá trị của sơn mài Việt.</p>
- Trong self.__next_f và RSC payload (đảm bảo React hydration không bị đè về text cũ)
- Cập nhật CSS cho .project_contact__MjYrS h2 và p
- Cập nhật cachebuster v=24
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

CONTACT_CSS = """
/* ==================== VỀ DỰ ÁN: TIÊU ĐỀ LIÊN HỆ ĐỒNG HÀNH ==================== */
.project_contact__MjYrS h2 {
  max-width: none !important;
  font-size: clamp(30px, 3.2vw, 46px) !important;
  line-height: 1.15 !important;
  letter-spacing: -0.01em !important;
  font-family: "Project Display", "Playfair Display", Georgia, serif !important;
  margin: 14px 0 18px !important;
}

.project_contact__MjYrS .project_contactIntro__eES4_ p:not(.eyebrow) {
  max-width: 480px !important;
  line-height: 1.7 !important;
  color: #f1d9aa !important;
  font-size: 16px !important;
}

@media (max-width: 760px) {
  .project_contact__MjYrS h2 {
    font-size: clamp(28px, 6.8vw, 36px) !important;
    line-height: 1.2 !important;
  }
}
"""

def apply_css(rel_path):
    fpath = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if "/* ==================== VỀ DỰ ÁN: TIÊU ĐỀ LIÊN HỆ ĐỒNG HÀNH ==================== */" in content:
            idx = content.find("/* ==================== VỀ DỰ ÁN: TIÊU ĐỀ LIÊN HỆ ĐỒNG HÀNH ==================== */")
            content = content[:idx]
        content = content.rstrip() + "\n\n" + CONTACT_CSS.strip() + "\n"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CSS: {rel_path}")

css_targets = [
    '_next/static/css/f7d6d17d52efcb3d.css',
    'ma_nguon_css_js/css/f7d6d17d52efcb3d.css'
]

for ct in css_targets:
    apply_css(ct)

# Update HTML files and RSC payload
targets = [
    've-du-an/index.html',
    'trang_html_goc/08_ve_du_an.html',
    'rsc_payloads/ve-du-an.rsc'
]

OLD_HTML_DOM = '<p class="eyebrow">LIÊN HỆ</p><h2>Hãy cùng<br/>thêm một lớp.</h2><p>Thông tin liên hệ do dự án cung cấp.</p>'
NEW_HTML_DOM = '<p class="eyebrow">LIÊN HỆ</p><h2>CÙNG NỐI TIẾP<br/>HÀNH TRÌNH SƠN MÀI.</h2><p>Liên hệ với Sơn Son Mài Sắc để cùng kết nối, đồng hành và lan tỏa những giá trị của sơn mài Việt.</p>'

OLD_RSC_1 = '["Hãy cùng",["$","br",null,{}],"thêm một lớp."]'
NEW_RSC_1 = '["CÙNG NỐI TIẾP",["$","br",null,{}],"HÀNH TRÌNH SƠN MÀI."]'

OLD_RSC_2 = 'Thông tin liên hệ do dự án cung cấp.'
NEW_RSC_2 = 'Liên hệ với Sơn Son Mài Sắc để cùng kết nối, đồng hành và lan tỏa những giá trị của sơn mài Việt.'

# Also handle escaped versions inside script tags like \"Hãy cùng\"
OLD_RSC_1_ESC = r'[\"Hãy cùng\",[\"$\",\"br\",null,{}],\"thêm một lớp.\"]'
NEW_RSC_1_ESC = r'[\"CÙNG NỐI TIẾP\",[\"$\",\"br\",null,{}],\"HÀNH TRÌNH SƠN MÀI.\"]'

for t in targets:
    fpath = os.path.join(BASE_DIR, t)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # DOM replace
        if OLD_HTML_DOM in content:
            content = content.replace(OLD_HTML_DOM, NEW_HTML_DOM)
            print(f"Replaced HTML DOM in {t}")
            
        # RSC replace unescaped
        if OLD_RSC_1 in content:
            content = content.replace(OLD_RSC_1, NEW_RSC_1)
            print(f"Replaced OLD_RSC_1 in {t}")
        if OLD_RSC_2 in content:
            content = content.replace(OLD_RSC_2, NEW_RSC_2)
            print(f"Replaced OLD_RSC_2 in {t}")
            
        # RSC replace escaped
        if OLD_RSC_1_ESC in content:
            content = content.replace(OLD_RSC_1_ESC, NEW_RSC_1_ESC)
            print(f"Replaced OLD_RSC_1_ESC in {t}")
            
        # Any remaining occurrences of "Hãy cùng", "thêm một lớp."
        content = content.replace('"Hãy cùng"', '"CÙNG NỐI TIẾP"')
        content = content.replace(r'\"Hãy cùng\"', r'\"CÙNG NỐI TIẾP\"')
        content = content.replace('"thêm một lớp."', '"HÀNH TRÌNH SƠN MÀI."')
        content = content.replace(r'\"thêm một lớp.\"', r'\"HÀNH TRÌNH SƠN MÀI.\"')
        content = content.replace(OLD_RSC_2, NEW_RSC_2)

        # Cachebuster
        if t.endswith('.html'):
            if 'f7d6d17d52efcb3d.css?v=' in content:
                content = re.sub(r'f7d6d17d52efcb3d\.css\?v=\d+', 'f7d6d17d52efcb3d.css?v=24', content)
            else:
                content = re.sub(r'f7d6d17d52efcb3d\.css', 'f7d6d17d52efcb3d.css?v=24', content)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved: {t}")

print("DONE APPLYING COMPLETE HYDRATION-SAFE UPDATE!")
