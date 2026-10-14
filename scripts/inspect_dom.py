from bs4 import BeautifulSoup
import json
import re
import html
import os

def clean(t):
    if not t:
        return ""
    t = html.unescape(t)
    return ' '.join(t.split())

def inspect_page_structure(filename):
    print(f"\n==================== {filename} ====================")
    with open(filename, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    main = soup.find('main')
    if not main:
        print("No main tag found!")
        return

    # print sections
    sections = main.find_all(['section', 'article', 'div'], recursive=False)
    for s in main.find_all(['section', 'article']):
        s_id = s.get('id', '')
        s_cls = ' '.join(s.get('class', []))
        heading = s.find(['h1', 'h2', 'h3', 'h4'])
        h_text = clean(heading.get_text()) if heading else 'No heading'
        print(f"Section [id='{s_id}', class='{s_cls[:30]}']: {h_text}")

files = [
    'TrangChu_raw.html',
    'KhamPha_raw.html',
    'TraiNghiem_raw.html',
    'TraiNghiemHanhTrinh_raw.html',
    'TuChinh_raw.html',
    'CauChuyenSonMai_raw.html',
    'TinTucSuKien_raw.html',
    'VeDuAn_raw.html',
    'SanPham_raw.html'
]

for f in files:
    inspect_page_structure(f)
