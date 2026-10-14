# -*- coding: utf-8 -*-
"""
Script cân chỉnh ảnh Hero trang Về dự án:
- Ảnh bình hoa chuyển từ position: absolute sunken ở đáy thành relative/grid item ở cột 2
- Căn giữa dọc (align-self: center) với khoảng cách trên dưới đều đặn, cân đối
- Bo góc 20px mềm mại, bóng đổ cao cấp
- Đảm bảo responsive hoàn hảo trên Desktop, Tablet, Mobile
- Cập nhật cachebuster và đồng bộ HTML
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

HERO_ALIGN_CSS = """
/* ==================== CĂN CHỈNH ẢNH HERO VỀ DỰ ÁN CÂN ĐỐI ==================== */
.project_hero__Oebd7 {
  display: grid !important;
  grid-template-columns: 1.15fr 0.85fr !important;
  align-items: center !important;
  padding-right: clamp(24px, 3.5vw, 52px) !important;
  overflow: hidden !important;
}

.project_hero__Oebd7 > div {
  grid-column: 1 !important;
  grid-row: 1 !important;
}

.project_hero__Oebd7 > img {
  position: relative !important;
  grid-column: 2 !important;
  grid-row: 1 !important;
  width: 100% !important;
  max-width: 480px !important;
  height: auto !important;
  max-height: 550px !important;
  aspect-ratio: 2303 / 2759 !important;
  object-fit: contain !important;
  justify-self: end !important;
  align-self: center !important;
  right: auto !important;
  bottom: auto !important;
  border-radius: 20px !important;
  box-shadow: 0 14px 36px rgba(84, 53, 16, 0.16) !important;
  margin: clamp(24px, 3vw, 42px) 0 !important;
  filter: none !important;
}

@media (max-width: 960px) {
  .project_hero__Oebd7 {
    grid-template-columns: 1fr 1fr !important;
    padding-right: 24px !important;
  }
  .project_hero__Oebd7 > img {
    max-height: 480px !important;
  }
}

@media (max-width: 760px) {
  .project_hero__Oebd7 {
    grid-template-columns: 1fr !important;
    padding: 32px 24px 36px !important;
    min-height: 0 !important;
    gap: 20px !important;
  }
  .project_hero__Oebd7 > div {
    grid-column: 1 !important;
    grid-row: 1 !important;
    padding: 0 !important;
    max-width: none !important;
  }
  .project_hero__Oebd7 > img {
    grid-column: 1 !important;
    grid-row: 2 !important;
    justify-self: center !important;
    width: min(100%, 340px) !important;
    height: auto !important;
    max-height: 420px !important;
    margin: 20px auto 0 !important;
    box-shadow: 0 10px 24px rgba(84, 53, 16, 0.14) !important;
  }
}

@media (max-width: 480px) {
  .project_hero__Oebd7 {
    padding: 24px 18px 28px !important;
  }
  .project_hero__Oebd7 > img {
    width: min(100%, 290px) !important;
    margin-top: 16px !important;
  }
}
"""

def apply_to_css(rel_path):
    fpath = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if "/* ==================== CĂN CHỈNH ẢNH HERO VỀ DỰ ÁN CÂN ĐỐI ==================== */" in content:
            idx = content.find("/* ==================== CĂN CHỈNH ẢNH HERO VỀ DỰ ÁN CÂN ĐỐI ==================== */")
            content = content[:idx]
        content = content.rstrip() + "\n\n" + HERO_ALIGN_CSS + "\n"
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
        # Ensure image src is son-son-mai-sac-binh-hoa.webp
        content = re.sub(r'project-ivory-vase-v5\.webp', 'son-son-mai-sac-binh-hoa.webp', content)
        # Update css cachebuster
        if 'f7d6d17d52efcb3d.css?v=' in content:
            content = re.sub(r'f7d6d17d52efcb3d\.css\?v=\d+', 'f7d6d17d52efcb3d.css?v=20', content)
        else:
            content = re.sub(r'f7d6d17d52efcb3d\.css', 'f7d6d17d52efcb3d.css?v=20', content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML & cachebuster: {ht}")

print("DONE APPLYING VỀ DỰ ÁN HERO FIX!")
