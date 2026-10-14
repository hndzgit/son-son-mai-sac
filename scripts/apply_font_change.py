# -*- coding: utf-8 -*-
"""
Cập nhật font chữ cho các tiêu đề trang Khám phá (kham-pha)
sang font Playfair Display ('Project Display') giống như ở dòng
'Từ thấy “đẹp” đến hiểu “đẹp”' (ve-du-an).
"""

def update_fonts():
    font_face_rule = (
        '@font-face{'
        'font-family:"Project Display";'
        'src:url(/story-assets/PlayfairDisplay-Full.ttf) format("truetype");'
        'font-weight:400 900;'
        'font-style:normal;'
        'font-display:swap'
        '}'
        '@font-face{'
        'font-family:"Playfair Display";'
        'src:url(/story-assets/PlayfairDisplay-Full.ttf) format("truetype");'
        'font-weight:400 900;'
        'font-style:normal;'
        'font-display:swap'
        '}'
    )

    # 1. Update 58e70d5489b56972.css (global stylesheet)
    global_css_path = '_next/static/css/58e70d5489b56972.css'
    with open(global_css_path, 'r', encoding='utf-8') as f:
        global_css = f.read()
    if 'PlayfairDisplay-Full.ttf' not in global_css:
        global_css = font_face_rule + global_css
        with open(global_css_path, 'w', encoding='utf-8') as f:
            f.write(global_css)
        print("Added PlayfairDisplay font-face to global CSS.")
    else:
        print("PlayfairDisplay already in global CSS.")

    # 2. Update 7d5ed180c1fe36fd.css (kham-pha page stylesheet)
    kp_css_path = '_next/static/css/7d5ed180c1fe36fd.css'
    with open(kp_css_path, 'r', encoding='utf-8') as f:
        kp_css = f.read()

    # Prepend font-face if not present
    if 'PlayfairDisplay-Full.ttf' not in kp_css:
        kp_css = font_face_rule + kp_css

    # Update explore_intro h1
    old_h1_rule = '.explore_intro__ycC8w h1{max-width:820px;margin:14px 0 18px;color:#842022;font:400 clamp(46px,7vw,88px)/.98 Heritage,"Noto Serif",Georgia,serif;letter-spacing:-.035em;text-wrap:balance}'
    new_h1_rule = '.explore_intro__ycC8w h1{max-width:820px;margin:14px 0 18px;color:#842022;font:500 clamp(46px,7vw,88px)/1.02 "Project Display","Playfair Display",Georgia,serif;letter-spacing:-.015em;text-wrap:balance}'
    if old_h1_rule in kp_css:
        kp_css = kp_css.replace(old_h1_rule, new_h1_rule)
        print("Replaced explore_intro h1 rule.")
    else:
        print("Warning: old_h1_rule not found verbatim in kp_css.")

    # Update explore_definition h2 ("Sơn mài là gì?")
    old_h2_def = '.explore_definition__Nb9IJ h2{font:400 clamp(28px,4vw,46px)/1.25 "Noto Serif",Georgia,serif;color:#842022;margin:0 0 22px}'
    new_h2_def = '.explore_definition__Nb9IJ h2{font:500 clamp(28px,4vw,46px)/1.25 "Project Display","Playfair Display",Georgia,serif;color:#842022;margin:0 0 22px}'
    if old_h2_def in kp_css:
        kp_css = kp_css.replace(old_h2_def, new_h2_def)
        print("Replaced explore_definition h2 rule.")
    else:
        print("Warning: old_h2_def not found verbatim in kp_css.")

    # Update explore_definition summary ("Vì sao lại là sơn mài?", "Từ một giọt sơn ta")
    old_summary = '.explore_definition__Nb9IJ summary{cursor:pointer;color:#842022;font:500 clamp(17px,2vw,22px)/1.5 "Noto Serif",Georgia,serif;min-height:44px}'
    new_summary = '.explore_definition__Nb9IJ summary{cursor:pointer;color:#842022;font:500 clamp(17px,2vw,22px)/1.5 "Project Display","Playfair Display",Georgia,serif;min-height:44px}'
    if old_summary in kp_css:
        kp_css = kp_css.replace(old_summary, new_summary)
        print("Replaced explore_definition summary rule.")

    # Also add styles for process headings in kham-pha
    extra_rules = (
        '.core-v4-process-heading h2,'
        '.core-v4-process-detail h3,'
        '.processWorkshop_entry__6_wCN h3{'
        'font-family:"Project Display","Playfair Display",Georgia,serif!important;'
        'font-weight:500!important'
        '}'
    )
    if extra_rules not in kp_css:
        kp_css += extra_rules
        print("Added process heading rules.")

    with open(kp_css_path, 'w', encoding='utf-8') as f:
        f.write(kp_css)
    print("Updated kham-pha stylesheet successfully!")

if __name__ == '__main__':
    update_fonts()
