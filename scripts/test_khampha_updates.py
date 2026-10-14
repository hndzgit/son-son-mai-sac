# -*- coding: utf-8 -*-
import re
import subprocess
import os

HTML_PATH = 'kham-pha/index.html'
CSS_PATHS = [
    '_next/static/css/7d5ed180c1fe36fd.css',
    'ma_nguon_css_js/css/7d5ed180c1fe36fd.css'
]

def update_html(title_case=True):
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Title
    if title_case:
        # Title case / Sentence case matching beautiful Playfair Display typography
        new_title = '<h1>Qua từng lớp,<br/>vẻ đẹp dần hiện ra.</h1>'
    else:
        new_title = '<h1>QUA TỪNG LỚP,<br/>VẺ ĐẸP DẦN HIỆN RA.</h1>'

    # Replace H1 in header
    html = re.sub(r'<h1>.*?</h1>', new_title, html, count=1)

    # Lead paragraph - match the exact text from screenshot
    new_lead = '<p class="explore_lead__PXqjY">Khám phá cách một tác phẩm sơn mài được tạo nên qua những lớp sơn, vật liệu và bàn tay người thợ.</p>'
    html = re.sub(r'<p class="explore_lead__PXqjY">.*?</p>', new_lead, html, count=1)

    # Action buttons
    new_action = '<div class="explore_actions__K1B4A"><a class="btn red" href="/trai-nghiem#simulator">Tạo nên sắc sơn mài của riêng bạn <span aria-hidden="true">⟶</span></a><span>Trải nghiệm khoảng 3–5 phút · Có tương tác</span></div>'
    html = re.sub(r'<div class="explore_actions__K1B4A">.*?</div>', new_action, html, count=1)

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated HTML")

def update_css(opacity=0.75):
    for p in CSS_PATHS:
        if not os.path.exists(p):
            continue
        with open(p, 'r', encoding='utf-8') as f:
            css = f.read()

        # Update .explore_intro__ycC8w:after
        # We make the background artwork much clearer:
        # inset: 0 0 0 40%;
        # opacity: 0.75;
        # smooth left-edge gradient fade so text is comfortable to read
        new_after = (
            f'.explore_intro__ycC8w:after{{position:absolute;z-index:-1;inset:0 0 0 40%;content:"";'
            f'background:linear-gradient(90deg,#f8edcf 0%,rgba(248,237,207,0.3) 22%,transparent 55%),url(/story-assets/key-visual.jpg) right center/cover no-repeat;'
            f'opacity:{opacity};-webkit-mask-image:linear-gradient(90deg,transparent,#000 25%);mask-image:linear-gradient(90deg,transparent,#000 25%)}}'
        )
        css = re.sub(r'\.explore_intro__ycC8w:after\{[^}]*\}', new_after, css)

        # Update media query max-width:600px
        # .explore_intro__ycC8w:after{inset:15% 0 0 25%;opacity:.14} -> opacity:.38
        new_mobile_after = '.explore_intro__ycC8w:after{inset:10% 0 0 15%;opacity:.35}'
        css = re.sub(r'\.explore_intro__ycC8w:after\{inset:15% 0 0 25%;opacity:\.14\}', new_mobile_after, css)

        with open(p, 'w', encoding='utf-8') as f:
            f.write(css)
        print(f"Updated CSS: {p}")

if __name__ == '__main__':
    update_html(title_case=True)
    update_css(opacity=0.72)
