import os
import shutil
import json
import re
from bs4 import BeautifulSoup
import html

# 1. Ensure folders
os.makedirs('trang_html_goc', exist_ok=True)
os.makedirs('du_lieu_noi_dung', exist_ok=True)
os.makedirs('hinh_anh_assets', exist_ok=True)
os.makedirs('ma_nguon_css_js', exist_ok=True)

# 2. Move raw html files to trang_html_goc
html_map = {
    'TrangChu_raw.html': '01_trang_chu.html',
    'KhamPha_raw.html': '02_kham_pha.html',
    'TraiNghiem_raw.html': '03_trai_nghiem.html',
    'TraiNghiemHanhTrinh_raw.html': '04_trai_nghiem_hanh_trinh.html',
    'TuChinh_raw.html': '05_tu_chinh.html',
    'CauChuyenSonMai_raw.html': '06_cau_chuyen_son_mai.html',
    'TinTucSuKien_raw.html': '07_tin_tuc_su_kien.html',
    'VeDuAn_raw.html': '08_ve_du_an.html',
    'SanPham_raw.html': '09_san_pham.html'
}

for src, dest in html_map.items():
    if os.path.exists(src):
        shutil.move(src, os.path.join('trang_html_goc', dest))

print("Organized HTML files in trang_html_goc/")
