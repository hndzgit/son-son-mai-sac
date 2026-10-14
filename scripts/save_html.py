import urllib.request
import re
from bs4 import BeautifulSoup
import html

# Let's check if bs4 is installed, if not we use regex/html.parser
try:
    from bs4 import BeautifulSoup
    has_bs4 = True
except ImportError:
    has_bs4 = False

headers = {'User-Agent': 'Mozilla/5.0'}

routes = [
    ('/', 'TrangChu'),
    ('/kham-pha', 'KhamPha'),
    ('/trai-nghiem', 'TraiNghiem'),
    ('/trai-nghiem/hanh-trinh', 'TraiNghiemHanhTrinh'),
    ('/tu-chinh', 'TuChinh'),
    ('/cau-chuyen-son-mai', 'CauChuyenSonMai'),
    ('/tin-tuc-su-kien', 'TinTucSuKien'),
    ('/ve-du-an', 'VeDuAn'),
    ('/san-pham', 'SanPham')
]

for r, name in routes:
    u = f'https://sonsonmaisat.site{r}'
    req = urllib.request.Request(u, headers=headers)
    html_content = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    
    # Save raw html
    with open(f'{name}_raw.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Saved {name}_raw.html ({len(html_content)} bytes)")
