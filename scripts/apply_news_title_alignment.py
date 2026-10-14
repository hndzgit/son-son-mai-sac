#!/usr/bin/env python3
import os

def update_files():
    # 1. Update 033bcc6eb475b3ab.css files
    css_files_033 = [
        '_next/static/css/033bcc6eb475b3ab.css',
        'ma_nguon_css_js/css/033bcc6eb475b3ab.css'
    ]
    rule_news = (
        '\n/* Align news title flush left with content */\n'
        '#news-title, .events_hero__3INKQ h1, .events_heroTitle__Y1W2y h1 {\n'
        '  text-align: left !important;\n'
        '}\n'
    )
    for p in css_files_033:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                c = f.read()
            c = c.replace('.events_hero__3INKQ h1{margin:13px 0 12px;', '.events_hero__3INKQ h1{text-align:left!important;margin:13px 0 12px;')
            c = c.replace('.events_heroTitle__Y1W2y{max-width:650px}', '.events_heroTitle__Y1W2y{max-width:650px;text-align:left!important}')
            if '/* Align news title flush left with content */' not in c:
                c += rule_news
            with open(p, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Updated {p}")

    # 2. Update 58e70d5489b56972.css files
    css_files_58 = [
        '_next/static/css/58e70d5489b56972.css',
        'ma_nguon_css_js/css/58e70d5489b56972.css'
    ]
    for p in css_files_58:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                c = f.read()
            if '/* Align news title flush left with content */' not in c:
                c += rule_news
            with open(p, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Updated {p}")

    # 3. Update JS chunks
    js_files = [
        '_next/static/chunks/app/tin-tuc-su-kien/page-0044ed8affa87fe5.js',
        'ma_nguon_css_js/js/app_tin-tuc-su-kien_page-0044ed8affa87fe5.js'
    ]
    target_js = '(0,a.jsxs)("h1",{id:"news-title",children:"Sắc mài trong đời sống hôm nay"})'
    repl_js = '(0,a.jsxs)("h1",{id:"news-title",style:{textAlign:"left"},children:"Sắc mài trong đời sống hôm nay"})'
    for p in js_files:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                c = f.read()
            if target_js in c:
                c = c.replace(target_js, repl_js)
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(c)
                print(f"Updated {p}")

    # 4. Update HTML files
    html_files = [
        'tin-tuc-su-kien/index.html',
        'trang_html_goc/07_tin_tuc_su_kien.html'
    ]
    style_tag = '<style>#news-title, .events_hero__3INKQ h1, .events_heroTitle__Y1W2y h1 { text-align: left !important; }</style>'
    for p in html_files:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                c = f.read()
            c = c.replace('<h1 id="news-title">', '<h1 id="news-title" style="text-align:left!important;">')
            if style_tag not in c:
                c = c.replace('</head>', f'{style_tag}</head>')
            with open(p, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Updated {p}")

if __name__ == '__main__':
    update_files()
