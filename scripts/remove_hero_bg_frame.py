# -*- coding: utf-8 -*-
"""
Script xóa bỏ khung viền trang trí đằng sau ảnh bìa Hero theo yêu cầu:
"bỏ khung đằng sau ảnh này vì thấy thừa quá"
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

REMOVE_HERO_BG_FRAME_CSS = """
/* ==================== BỎ KHUNG ĐẰNG SAU ẢNH HERO ==================== */
.homeHero_gallery__3RgwW::before,
.homeHero_gallery__3RgwW::after,
.homeHero_feature__NRdLI::before,
.homeHero_feature__NRdLI::after {
  content: none !important;
  display: none !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}
"""

def append_to_css(rel_path):
    fpath = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if "/* ==================== BỎ KHUNG ĐẰNG SAU ẢNH HERO ==================== */" in content:
            idx = content.find("/* ==================== BỎ KHUNG ĐẰNG SAU ẢNH HERO ==================== */")
            content = content[:idx]
        content = content.rstrip() + "\n\n" + REMOVE_HERO_BG_FRAME_CSS + "\n"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CSS: {rel_path}")

css_files = [
    '_next/static/css/58e70d5489b56972.css',
    '_next/static/css/3d939b8161363d36.css',
    'ma_nguon_css_js/css/58e70d5489b56972.css',
    'ma_nguon_css_js/css/3d939b8161363d36.css'
]

for cf in css_files:
    append_to_css(cf)

# Bump cachebusters in HTML files
html_files = [
    'index.html',
    'kham-pha/index.html',
    'tin-tuc-su-kien/index.html',
    've-du-an/index.html',
    'san-pham/index.html',
    'cau-chuyen-son-mai/index.html',
    'trai-nghiem/index.html'
]

for hf in html_files:
    fpath = os.path.join(BASE_DIR, hf)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'58e70d5489b56972\.css\?v=\d+', '58e70d5489b56972.css?v=19', html)
        html = re.sub(r'3d939b8161363d36\.css\?v=\d+', '3d939b8161363d36.css?v=19', html)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Bumped cachebuster in {hf}")

print("DONE REMOVING HERO BACKGROUND FRAME!")
