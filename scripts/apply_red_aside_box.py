# -*- coding: utf-8 -*-
"""
Script đổi khung 'Ý NGHĨA TÊN GỌI' trên trang Về dự án sang màu đỏ truyền thống (sơn son):
- Nền đỏ sơn son đặc trưng (#870e0e)
- Viền vàng kim (#c6a663) bo tròn 18px
- Màu chữ chuyển sang vàng ngà và vàng quỳ (#fff0cd, #ffe082, #f1d9aa) tạo độ tương phản cao và thẩm mỹ thủ công truyền thống
- Đường kẻ phân cách vàng kim nhẹ
- Đảm bảo hiển thị hoàn hảo trên mọi thiết bị
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

RED_ASIDE_CSS = """
/* ==================== KHUNG ĐỎ Ý NGHĨA TÊN GỌI ==================== */
.project_projectStory__zaR3l aside {
  background: #870e0e !important;
  color: #f1d9aa !important;
  border: 1px solid #c6a663 !important;
  border-radius: 18px !important;
  box-shadow: 0 14px 36px rgba(84, 14, 14, 0.22) !important;
  padding: clamp(26px, 3.8vw, 42px) !important;
}

.project_projectStory__zaR3l aside .eyebrow {
  color: #e5c987 !important;
  letter-spacing: 0.16em !important;
}

.project_projectStory__zaR3l aside h3 {
  color: #fff0cd !important;
}

.project_projectStory__zaR3l aside > p:not(.project_eyebrow__An6h2) {
  color: #f1d9aa !important;
  line-height: 1.8 !important;
}

.project_nameMeaning__2ZB26 dt {
  color: #ffe082 !important;
  font-weight: 700 !important;
}

.project_nameMeaning__2ZB26 dd {
  color: #f4dfb2 !important;
  line-height: 1.7 !important;
}

.project_projectStory__zaR3l .project_projectStoryClose__dBA7g {
  border-top: 1px solid rgba(229, 201, 135, 0.35) !important;
  color: #fff0cd !important;
}

@media (max-width: 760px) {
  .project_projectStory__zaR3l aside {
    padding: 24px 20px !important;
  }
}
"""

def apply_to_css(rel_path):
    fpath = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if "/* ==================== KHUNG ĐỎ Ý NGHĨA TÊN GỌI ==================== */" in content:
            idx = content.find("/* ==================== KHUNG ĐỎ Ý NGHĨA TÊN GỌI ==================== */")
            content = content[:idx]
        content = content.rstrip() + "\n\n" + RED_ASIDE_CSS + "\n"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CSS: {rel_path}")

css_targets = [
    '_next/static/css/f7d6d17d52efcb3d.css',
    'ma_nguon_css_js/css/f7d6d17d52efcb3d.css'
]

for ct in css_targets:
    apply_to_css(ct)

# Update cachebuster in ve-du-an/index.html and other relevant html files
html_targets = [
    've-du-an/index.html',
    'trang_html_goc/08_ve_du_an.html'
]

for ht in html_targets:
    fpath = os.path.join(BASE_DIR, ht)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'f7d6d17d52efcb3d.css?v=' in content:
            content = re.sub(r'f7d6d17d52efcb3d\.css\?v=\d+', 'f7d6d17d52efcb3d.css?v=21', content)
        else:
            content = re.sub(r'f7d6d17d52efcb3d\.css', 'f7d6d17d52efcb3d.css?v=21', content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML & cachebuster: {ht}")

print("DONE APPLYING RED ASIDE BOX!")
