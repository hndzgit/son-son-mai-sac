import os, json, re
from bs4 import BeautifulSoup
import html

def extract_page_details(filename):
    with open(os.path.join('trang_html_goc', filename), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Remove scripts, styles
    for s in soup(['script', 'style', 'nav', 'header', 'footer']):
        s.decompose()
        
    main = soup.find('main')
    if not main:
        main = soup
        
    paragraphs = []
    for tag in main.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li', 'figcaption', 'blockquote', 'cite']):
        txt = html.unescape(tag.get_text(separator=' ', strip=True))
        txt = ' '.join(txt.split())
        if len(txt) > 3 and not txt.startswith('Bỏ qua'):
            paragraphs.append({
                'tag': tag.name,
                'text': txt
            })
    return paragraphs

files = [
    ('01_trang_chu.html', 'TrangChu'),
    ('02_kham_pha.html', 'KhamPha'),
    ('03_trai_nghiem.html', 'TraiNghiem'),
    ('04_trai_nghiem_hanh_trinh.html', 'TraiNghiemHanhTrinh'),
    ('05_tu_chinh.html', 'TuChinh'),
    ('06_cau_chuyen_son_mai.html', 'CauChuyenSonMai'),
    ('07_tin_tuc_su_kien.html', 'TinTucSuKien'),
    ('08_ve_du_an.html', 'VeDuAn'),
    ('09_san_pham.html', 'SanPham')
]

for f, name in files:
    res = extract_page_details(f)
    print(f"=== {f} ({name}): {len(res)} text elements ===")
    for item in res[:8]:
        print(f"  <{item['tag']}> {item['text'][:80]}...")
