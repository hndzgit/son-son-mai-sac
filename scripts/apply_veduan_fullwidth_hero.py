# -*- coding: utf-8 -*-
"""
Script mở rộng Hero Box trang Về dự án thành Full Width tương tự trang chủ:
- .project_page__UA7p9: padding: 0 0 76px
- .project_page__UA7p9 > section:not(.project_hero__Oebd7): padding-left/right: max(5vw, 20px)
- .project_hero__Oebd7: full width (width: 100%, max-width: 100%), border-left/right: none, border-radius: 0
- Giữ nguyên toàn bộ căn chỉnh ảnh hoa, tỷ lệ font chữ, và khối Ý NGHĨA TÊN GỌI đỏ
- Cập nhật cachebuster CSS v=22 cho ve-du-an/index.html và trang_html_goc/08_ve_du_an.html
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

FULLWIDTH_HERO_CSS = """
/* ==================== VỀ DỰ ÁN: HERO FULL WIDTH NHƯ TRANG CHỦ ==================== */
.project_page__UA7p9 {
  padding: 0 0 76px !important;
}

.project_page__UA7p9 > section:not(.project_hero__Oebd7) {
  padding-left: max(5vw, 20px) !important;
  padding-right: max(5vw, 20px) !important;
  box-sizing: border-box !important;
}

.project_hero__Oebd7 {
  max-width: 100% !important;
  width: 100% !important;
  margin: 0 0 clamp(64px, 8vw, 110px) !important;
  border-left: none !important;
  border-right: none !important;
  border-top: 1px solid #a48757 !important;
  border-bottom: 1px solid #a48757 !important;
  border-radius: 0 !important;
  padding: clamp(28px, 4vw, 56px) clamp(24px, 5vw, 76px) !important;
  box-sizing: border-box !important;
}

@media (max-width: 760px) {
  .project_hero__Oebd7 {
    padding: 32px 20px 36px !important;
  }
}

@media (max-width: 480px) {
  .project_hero__Oebd7 {
    padding: 24px 16px 28px !important;
  }
}
"""

def apply_css(rel_path):
    fpath = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove older version if present
        if "/* ==================== VỀ DỰ ÁN: HERO FULL WIDTH NHƯ TRANG CHỦ ==================== */" in content:
            idx = content.find("/* ==================== VỀ DỰ ÁN: HERO FULL WIDTH NHƯ TRANG CHỦ ==================== */")
            content = content[:idx]
            
        content = content.rstrip() + "\n\n" + FULLWIDTH_HERO_CSS.strip() + "\n"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CSS: {rel_path}")

css_targets = [
    '_next/static/css/f7d6d17d52efcb3d.css',
    'ma_nguon_css_js/css/f7d6d17d52efcb3d.css'
]

for ct in css_targets:
    apply_css(ct)

# Update cachebuster in HTML
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
            content = re.sub(r'f7d6d17d52efcb3d\.css\?v=\d+', 'f7d6d17d52efcb3d.css?v=22', content)
        else:
            content = re.sub(r'f7d6d17d52efcb3d\.css', 'f7d6d17d52efcb3d.css?v=22', content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML cachebuster (v=22): {ht}")

print("DONE APPLYING FULL WIDTH HERO FIX!")
