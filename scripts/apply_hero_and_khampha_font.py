# -*- coding: utf-8 -*-
import re

def update_home_and_khampha():
    # 1. Update global CSS 58e70d5489b56972.css
    global_css_path = '_next/static/css/58e70d5489b56972.css'
    with open(global_css_path, 'r', encoding='utf-8') as f:
        global_css = f.read()

    home_rule = (
        '#core-v4-home-title,'
        '.homeHero_journeyTitle__c4_vR,'
        '.homeHero_hero__tom2X .homeHero_copy__DBESX h1{'
        'font-family:"Project Display","Playfair Display",Georgia,serif!important;'
        'font-weight:600!important;'
        'letter-spacing:0.01em!important;'
        'line-height:1.15!important'
        '}'
    )
    if '#core-v4-home-title' not in global_css:
        global_css += home_rule
        with open(global_css_path, 'w', encoding='utf-8') as f:
            f.write(global_css)
        print("Added home title rule to global CSS.")
    else:
        # Replace if existing
        global_css = re.sub(r'#core-v4-home-title[^}]*\}', home_rule, global_css)
        with open(global_css_path, 'w', encoding='utf-8') as f:
            f.write(global_css)
        print("Updated home title rule in global CSS.")

    # 2. Update 3d939b8161363d36.css
    for css_p in ['_next/static/css/3d939b8161363d36.css', 'ma_nguon_css_js/css/3d939b8161363d36.css']:
        try:
            with open(css_p, 'r', encoding='utf-8') as f:
                c = f.read()
            if home_rule not in c:
                c += home_rule
                with open(css_p, 'w', encoding='utf-8') as f:
                    f.write(c)
                print(f"Appended home_rule to {css_p}")
        except Exception as e:
            print(f"Error on {css_p}: {e}")

    # 3. Update kham-pha stylesheet 7d5ed180c1fe36fd.css
    kp_css_path = '_next/static/css/7d5ed180c1fe36fd.css'
    with open(kp_css_path, 'r', encoding='utf-8') as f:
        kp_css = f.read()

    # Look for .explore_intro__ycC8w h1 rule
    new_kp_h1 = (
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
    if '.explore_intro__ycC8w h1{' in kp_css:
        kp_css = re.sub(r'\.explore_intro__ycC8w h1\{[^}]*\}', new_kp_h1, kp_css)
        print("Replaced explore_intro h1 rule in kp_css.")
    else:
        kp_css += new_kp_h1
        print("Appended explore_intro h1 rule to kp_css.")

    with open(kp_css_path, 'w', encoding='utf-8') as f:
        f.write(kp_css)

    # 4. Update kham-pha/index.html HTML text to sentence case so diacritics don't clash
    kp_html_path = 'kham-pha/index.html'
    with open(kp_html_path, 'r', encoding='utf-8') as f:
        kp_html = f.read()

    # Replace uppercase with sentence case
    old_h1_markup = '<h1>QUA TỪNG LỚP,<br/>VẺ ĐẸP DẦN HIỆN RA.</h1>'
    new_h1_markup = '<h1>Qua từng lớp,<br/>vẻ đẹp dần hiện ra.</h1>'

    old_rsc_markup = '["QUA TỪNG LỚP,",["$","br",null,{}],"VẺ ĐẸP DẦN HIỆN RA."]'
    new_rsc_markup = '["Qua từng lớp,",["$","br",null,{}],"vẻ đẹp dần hiện ra."]'

    if old_h1_markup in kp_html:
        kp_html = kp_html.replace(old_h1_markup, new_h1_markup)
        print("Updated HTML markup in kham-pha/index.html.")
    if old_rsc_markup in kp_html:
        kp_html = kp_html.replace(old_rsc_markup, new_rsc_markup)
        print("Updated RSC markup in kham-pha/index.html.")

    with open(kp_html_path, 'w', encoding='utf-8') as f:
        f.write(kp_html)

    print("All updates applied successfully!")

if __name__ == '__main__':
    update_home_and_khampha()
