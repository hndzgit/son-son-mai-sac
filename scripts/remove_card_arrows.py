# -*- coding: utf-8 -*-
"""
Script xóa bỏ hoàn toàn các dấu link mũi tên ↗ trong các thẻ chất liệu (materialGallery cards):
1. Cập nhật CSS để ẩn triệt để .materialGallery_cardCopy__NBeRZ i và .materialGallery_card__sP88f i
2. Cập nhật HTML trong index.html và trai-nghiem/index.html
3. Cập nhật file JS chunk _next/static/chunks/369-2063549c42145b16.js
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

HIDE_ARROW_CSS = """
/* ẨN HOÀN TOÀN CÁC DẤU LINK MŨI TÊN ↗ TRONG CARD CHẤT LIỆU */
.materialGallery_cardCopy__NBeRZ i,
.materialGallery_card__sP88f i {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  width: 0 !important;
  height: 0 !important;
  pointer-events: none !important;
}
"""

def append_to_css(rel_path):
    fpath = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if "/* ẨN HOÀN TOÀN CÁC DẤU LINK MŨI TÊN ↗ TRONG CARD CHẤT LIỆU */" in content:
            idx = content.find("/* ẨN HOÀN TOÀN CÁC DẤU LINK MŨI TÊN ↗ TRONG CARD CHẤT LIỆU */")
            content = content[:idx]
        content = content.rstrip() + "\n\n" + HIDE_ARROW_CSS + "\n"
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

# 2. Xóa trong HTML files
html_files = ['index.html', 'trai-nghiem/index.html']
for hf in html_files:
    fpath = os.path.join(BASE_DIR, hf)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()
        # Tìm các card trong materialGallery và bỏ <i aria-hidden="true">↗</i>
        # Match inside materialGallery_cardCopy__NBeRZ
        pattern = r'(<span class="materialGallery_cardCopy__NBeRZ">.*?)(<i aria-hidden="true">↗</i>)(</span>)'
        new_html = re.sub(pattern, r'\1\3', html)
        if new_html != html:
            print(f"Removed arrow icons from {hf}")
        # Bump cachebuster css
        new_html = re.sub(r'58e70d5489b56972\.css\?v=\d+', '58e70d5489b56972.css?v=16', new_html)
        new_html = re.sub(r'3d939b8161363d36\.css\?v=\d+', '3d939b8161363d36.css?v=16', new_html)
        new_html = re.sub(r'369-2063549c42145b16\.js(\?v=\d+)?', '369-2063549c42145b16.js?v=7', new_html)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"Updated {hf}")

# 3. Xóa trong JS Chunk 369-2063549c42145b16.js
chunk_path = os.path.join(BASE_DIR, '_next/static/chunks/369-2063549c42145b16.js')
if os.path.exists(chunk_path):
    with open(chunk_path, 'r', encoding='utf-8') as f:
        js = f.read()
    target = ',(0,r.jsx)("i",{"aria-hidden":"true",children:"↗"})'
    if target in js:
        js = js.replace(target, '')
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(js)
        print("Removed arrow icon from JS chunk 369-2063549c42145b16.js")
    else:
        print("Target arrow pattern not found in JS chunk (might already be removed)")

print("DONE REMOVING LINK ARROWS!")
