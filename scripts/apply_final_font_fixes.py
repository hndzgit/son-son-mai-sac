# -*- coding: utf-8 -*-
import os
import re

def apply_final_fixes():
    print("Applying font and diacritic fixes...")

    # 1. Update kham-pha/index.html
    kp_html_path = 'kham-pha/index.html'
    with open(kp_html_path, 'r', encoding='utf-8') as f:
        kp_html = f.read()

    # Replace uppercase in self.__next_f
    # Target: [\"QUA TỪNG LỚP,\",[\"$\",\"br\",null,{}],\"VẺ ĐẸP DẦN HIỆN RA.\"]
    # With: [\"Qua từng lớp,\",[\"$\",\"br\",null,{}],\"vẻ đẹp dần hiện ra.\"]
    pattern_stream = r'\[\\"QUA TỪNG LỚP,\\",\[\\"\\$\\?,\\"br\\",null,\{\}\],\\"VẺ ĐẸP DẦN HIỆN RA\.\\"\]'
    # Or exact substring replacement:
    old_stream_exact = r'[\"QUA TỪNG LỚP,\",[\"$\",\"br\",null,{}],\"VẺ ĐẸP DẦN HIỆN RA.\"]'
    new_stream_exact = r'[\"Qua từng lớp,\",[\"$\",\"br\",null,{}],\"vẻ đẹp dần hiện ra.\"]'

    if old_stream_exact in kp_html:
        kp_html = kp_html.replace(old_stream_exact, new_stream_exact)
        print("Replaced exact stream in kham-pha/index.html")
    else:
        print("Exact stream not found by simple string, trying regex...")
        kp_html, count = re.subn(
            r'\[\\\"QUA TỪNG LỚP,\\\",\[\\\"\\$\\\",\\\"br\\\",null,\{\}\],\\\"VẺ ĐẸP DẦN HIỆN RA\.\\\"\]',
            r'[\\"Qua từng lớp,\\",[\"$\",\"br\",null,{}],\\"vẻ đẹp dần hiện ra.\\"]',
            kp_html
        )
        print(f"Regex replaced {count} occurrences in kham-pha/index.html")

    # Also ensure static HTML is sentence case
    old_static = '<h1>QUA TỪNG LỚP,<br/>VẺ ĐẸP DẦN HIỆN RA.</h1>'
    new_static = '<h1>Qua từng lớp,<br/>vẻ đẹp dần hiện ra.</h1>'
    if old_static in kp_html:
        kp_html = kp_html.replace(old_static, new_static)
        print("Replaced static HTML in kham-pha/index.html")

    with open(kp_html_path, 'w', encoding='utf-8') as f:
        f.write(kp_html)

    # 2. Update rsc_payloads/kham-pha.rsc
    rsc_path = 'rsc_payloads/kham-pha.rsc'
    if os.path.exists(rsc_path):
        with open(rsc_path, 'r', encoding='utf-8') as f:
            rsc = f.read()
        old_rsc = '["QUA TỪNG LỚP,",["$","br",null,{}],"VẺ ĐẸP DẦN HIỆN RA."]'
        new_rsc = '["Qua từng lớp,",["$","br",null,{}],"vẻ đẹp dần hiện ra."]'
        if old_rsc in rsc:
            rsc = rsc.replace(old_rsc, new_rsc)
            with open(rsc_path, 'w', encoding='utf-8') as f:
                f.write(rsc)
            print("Replaced in rsc_payloads/kham-pha.rsc")

    # 3. Update CSS files for Home and Khám phá
    home_css_rule = (
        '.homeHero_inner__pVJjI{'
        'grid-template-columns:minmax(340px,1.05fr) minmax(0,.95fr)!important'
        '}'
        '#core-v4-home-title,'
        '.homeHero_journeyTitle__c4_vR,'
        '.homeHero_hero__tom2X .homeHero_copy__DBESX h1{'
        'font-family:"Project Display","Playfair Display",Georgia,serif!important;'
        'font-weight:600!important;'
        'font-size:clamp(34px,3.4vw,46px)!important;'
        'line-height:1.2!important;'
        'max-width:660px!important;'
        'letter-spacing:-0.01em!important;'
        'text-transform:none!important'
        '}'
    )

    for css_p in ['_next/static/css/58e70d5489b56972.css', '_next/static/css/3d939b8161363d36.css', 'ma_nguon_css_js/css/3d939b8161363d36.css']:
        if os.path.exists(css_p):
            with open(css_p, 'r', encoding='utf-8') as f:
                c = f.read()
            # Remove any previous #core-v4-home-title rules
            c = re.sub(r'#core-v4-home-title[^{]*\{[^}]*\}', '', c)
            c = re.sub(r'\.homeHero_inner__pVJjI\{grid-template-columns:minmax\(340px,1\.05fr\)[^}]*\}', '', c)
            c += home_css_rule
            with open(css_p, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Updated Home hero styling in {css_p}")

    # 4. Update Khám phá CSS
    kp_css_path = '_next/static/css/7d5ed180c1fe36fd.css'
    if os.path.exists(kp_css_path):
        with open(kp_css_path, 'r', encoding='utf-8') as f:
            kp_css = f.read()

        new_kp_rule = (
            '.explore_intro__ycC8w h1{'
            'max-width:980px;'
            'margin:14px 0 18px;'
            'color:#842022;'
            'font-family:"Project Display","Playfair Display",Georgia,serif!important;'
            'font-weight:600!important;'
            'font-size:clamp(42px,5.8vw,76px)!important;'
            'line-height:1.15!important;'
            'letter-spacing:0.01em!important;'
            'text-transform:none!important;'
            'text-wrap:balance'
            '}'
        )
        kp_css = re.sub(r'\.explore_intro__ycC8w h1\{[^}]*\}', new_kp_rule, kp_css)
        with open(kp_css_path, 'w', encoding='utf-8') as f:
            f.write(kp_css)
        print("Updated Khám phá title styling in 7d5ed180c1fe36fd.css")

    print("All fixes applied successfully!")

if __name__ == '__main__':
    apply_final_fixes()
