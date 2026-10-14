#!/usr/bin/env python3
import os

def remove_disclaimer():
    # 1. Update tin-tuc-su-kien/index.html and trang_html_goc/07_tin_tuc_su_kien.html
    html_files = [
        'tin-tuc-su-kien/index.html',
        'trang_html_goc/07_tin_tuc_su_kien.html'
    ]
    target_p = '<p class="eventProgramme_disclaimer__5a0ST">Ngày, địa điểm và trạng thái có thể thay đổi; hãy kiểm tra nguồn của ban tổ chức trước khi tham gia. Ảnh có nhãn “Ảnh minh họa” không phải ảnh tư liệu của sự kiện.</p>'
    
    for p in html_files:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                c = f.read()
            if target_p in c:
                c = c.replace(target_p, '')
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(c)
                print(f"Removed disclaimer from {p}")
            else:
                print(f"Target not found in {p}")

    # 2. Update JS chunks
    js_files = [
        '_next/static/chunks/app/tin-tuc-su-kien/page-0044ed8affa87fe5.js',
        'ma_nguon_css_js/js/app_tin-tuc-su-kien_page-0044ed8affa87fe5.js'
    ]
    target_js = '(0,a.jsx)("p",{className:r().disclaimer,children:"Ng\\xe0y, địa điểm v\\xe0 trạng th\\xe1i c\\xf3 thể thay đổi; h\\xe3y kiểm tra nguồn của ban tổ chức trước khi tham gia. Ảnh c\\xf3 nh\\xe3n “Ảnh minh họa” kh\\xf4ng phải ảnh tư liệu của sự kiện."})'
    repl_js = 'null'

    for p in js_files:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                c = f.read()
            if target_js in c:
                c = c.replace(target_js, repl_js)
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(c)
                print(f"Removed disclaimer from {p}")
            else:
                print(f"Target not found in {p}")

    # 3. Add display:none to CSS files as safety net
    css_files = [
        '_next/static/css/033bcc6eb475b3ab.css',
        'ma_nguon_css_js/css/033bcc6eb475b3ab.css',
        '_next/static/css/58e70d5489b56972.css',
        'ma_nguon_css_js/css/58e70d5489b56972.css'
    ]
    css_rule = '\n.eventProgramme_disclaimer__5a0ST { display: none !important; }\n'
    for p in css_files:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                c = f.read()
            if '.eventProgramme_disclaimer__5a0ST { display: none !important; }' not in c:
                c += css_rule
            with open(p, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Updated CSS {p}")

if __name__ == '__main__':
    remove_disclaimer()
