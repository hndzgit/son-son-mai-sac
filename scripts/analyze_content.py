import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0'}

def analyze_chunk(name, path):
    u = f'https://sonsonmaisat.site{path}'
    content = urllib.request.urlopen(urllib.request.Request(u, headers=headers)).read().decode('utf-8', errors='ignore')
    print(f"\n==================== {name} ({len(content)} bytes) ====================")
    # Search for vietnamese text or array definitions
    strings = re.findall(r'["\']([A-ZÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ][^"\'{}\\<>]{15,})["\']', content)
    print(f"Sample long strings ({len(strings)} found):")
    for s in strings[:15]:
        print(f" - {s}")

chunks = [
    ('Trang chủ', '/_next/static/chunks/app/page-1f5c1f7a3dcd2475.js'),
    ('Khám phá', '/_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js'),
    ('Câu chuyện', '/_next/static/chunks/app/cau-chuyen-son-mai/page-18999a17f9a00aec.js'),
    ('Tin tức sự kiện', '/_next/static/chunks/app/tin-tuc-su-kien/page-0044ed8affa87fe5.js'),
    ('Về dự án', '/_next/static/chunks/app/ve-du-an/page-4431fa17e862519b.js'),
    ('Sản phẩm', '/_next/static/chunks/app/san-pham/page-2a9f8a05b3d81499.js'),
    ('Trải nghiệm', '/_next/static/chunks/app/trai-nghiem/page-4cfd64a621149b8e.js'),
    ('Hành trình', '/_next/static/chunks/app/trai-nghiem/hanh-trinh/page-2c74554e92ef9036.js')
]

for name, path in chunks:
    analyze_chunk(name, path)
