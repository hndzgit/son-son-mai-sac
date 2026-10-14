#!/usr/bin/env python3
import os
import re

def update_css():
    # 1. Update 58e70d5489b56972.css
    css_files_58 = [
        '_next/static/css/58e70d5489b56972.css',
        'ma_nguon_css_js/css/58e70d5489b56972.css'
    ]
    heading_font_rule = (
        '\n/* Global Heading Font: Project Display / Playfair Display 600 */\n'
        'h1, h2, h3, h4, h5, h6, .font-display, '
        '#lacquer-title, #process-heading, .coreIntroduction_processTitle__Y5ZSn, '
        '#layers-title, #core-v4-heritage-title, '
        '.coreIntroduction_introCopy__c7o__ h2, .coreIntroduction_processIntro__xmAsV h3, '
        '.coreIntroduction_layersLead__acYPE h2, .core-v4-heritage-copy h2, '
        '.craftJourney_entry__YVr2U h1, .events_heroTitle__Y1W2y h1, '
        '.events_upcoming__DAE0e h2, .events_sectionHead__N9mEK h2, '
        '.story_hero__754VY h1, .story_sectionTitle__ckkqZ h2, '
        '.story_inspiration__LM_OE h2, .story_continue__7Ttr_ h2, '
        '.productExperience_configIntro__aR2C6 h1, .productExperience_boardContext__7W1Go h2, '
        '.productExperience_galleryHeader__vgEuH h2, .productExperience_stageSummary__5L0I5 h1, '
        '.about_heroTitle__Yx78I, .projectIntro_title__oV5wW, .not-found_page__VFIr4 h1 {'
        'font-family: "Project Display", "Playfair Display", Georgia, serif !important;'
        'font-weight: 600 !important;'
        '}\n'
    )

    for p in css_files_58:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
            # Replace old Heritage rule if present
            content = content.replace(
                '.font-display,h1,h2,h3,h4{font-family:Heritage,Georgia,serif;font-weight:400;',
                '.font-display,h1,h2,h3,h4{font-family:"Project Display","Playfair Display",Georgia,serif!important;font-weight:600!important;'
            )
            if '/* Global Heading Font: Project Display' not in content:
                content += heading_font_rule
            with open(p, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {p}")

    # 2. Update 3d939b8161363d36.css
    css_files_3d = [
        '_next/static/css/3d939b8161363d36.css',
        'ma_nguon_css_js/css/3d939b8161363d36.css'
    ]
    font_face_3d = (
        '@font-face{font-family:"Project Display";src:url(/story-assets/PlayfairDisplay-Full.ttf) format("truetype");font-weight:400 900;font-style:normal;font-display:swap}\n'
        '@font-face{font-family:"Playfair Display";src:url(/story-assets/PlayfairDisplay-Full.ttf) format("truetype");font-weight:400 900;font-style:normal;font-display:swap}\n'
    )
    extra_3d_rules = (
        '\n/* Heading Font & Stage 5 Link Updates */\n'
        '#lacquer-title, #process-heading, .coreIntroduction_processTitle__Y5ZSn, '
        '#layers-title, #core-v4-heritage-title, '
        '.coreIntroduction_stageItem__C7_GF>strong, '
        '.coreIntroduction_introCopy__c7o__ h2, .coreIntroduction_processIntro__xmAsV h3, '
        '.coreIntroduction_layersLead__acYPE h2, .core-v4-heritage-copy h2 {'
        'font-family: "Project Display", "Playfair Display", Georgia, serif !important;'
        'font-weight: 600 !important;'
        '}\n'
        '.coreIntroduction_stageMore__uOSUQ{'
        'display:inline-flex !important;'
        'align-items:center;'
        'gap:5px;'
        'margin-top:10px !important;'
        'color:#8b2a2a !important;'
        'font-family:Inter,sans-serif !important;'
        'font-size:13.5px !important;'
        'font-weight:600 !important;'
        'text-decoration:none !important;'
        'line-height:1.4;'
        'cursor:pointer;'
        'transition:all .2s ease;'
        '}\n'
        '.coreIntroduction_stageMore__uOSUQ:hover{'
        'color:#5c1414 !important;'
        'text-decoration:underline !important;'
        'transform:translateX(3px);'
        '}\n'
        '.coreIntroduction_stagePhoto__e5sjm{'
        'cursor:pointer;'
        'transition:transform .2s ease;'
        '}\n'
        '.coreIntroduction_stagePhoto__e5sjm:hover{'
        'transform:scale(1.02);'
        '}\n'
    )

    for p in css_files_3d:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix grid-template-rows on stageItem so row 4 for stageMore fits cleanly
            content = content.replace(
                'grid-template-rows:auto 48px auto;',
                'grid-template-rows:auto 48px auto auto;'
            )
            content = content.replace(
                'grid-template-rows:auto 44px auto;',
                'grid-template-rows:auto 44px auto auto;'
            )
            # Center diamond ✥ with the photos
            content = content.replace(
                '.coreIntroduction_stageItem__C7_GF:not(:first-child):before{content:"✥";position:absolute;left:-7px;top:62%;color:#bd9666;font:18px/1 Georgia,serif}',
                '.coreIntroduction_stageItem__C7_GF:not(:first-child):before{content:"✥";position:absolute;left:-7px;top:55%;color:#bd9666;font:18px/1 Georgia,serif}'
            )

            if '@font-face{font-family:"Project Display"' not in content:
                content = font_face_3d + content

            if '/* Heading Font & Stage 5 Link Updates */' not in content:
                content += extra_3d_rules

            with open(p, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {p}")

def update_js():
    js_files = [
        '_next/static/chunks/369-2063549c42145b16.js',
        'ma_nguon_css_js/js/369-2063549c42145b16.js'
    ]

    target = '(0,r.jsx)("span",{className:s().stagePhoto,role:"img","aria-label":"Công đoạn ".concat(n+1,": ").concat(e.name.toLocaleLowerCase("vi-VN"))})]}'
    replacement = '(0,r.jsx)("span",{className:s().stagePhoto,role:"img","aria-label":"Công đoạn ".concat(n+1,": ").concat(e.name.toLocaleLowerCase("vi-VN"))}),(0,r.jsx)("a",{className:s().stageMore,href:"/kham-pha#cong-doan-".concat(n+1),children:"Tìm hiểu thêm →"})]}'

    for p in js_files:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
            if target in content:
                content = content.replace(target, replacement)
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated JS in {p}")
            else:
                if 'Tìm hiểu thêm →' in content:
                    print(f"Already updated in {p}")
                else:
                    print(f"Target pattern not found in {p}")

def update_html():
    html_files = [
        'index.html',
        'trai-nghiem/index.html'
    ]

    stages_data = [
        (1, "CHUẨN BỊ CỐT", "0%"),
        (2, "LÀM VÓC", "25%"),
        (3, "SƠN NỀN", "50%"),
        (4, "TẠO HÌNH VÀ TRANG TRÍ", "75%"),
        (5, "PHỦ, MÀI VÀ HOÀN THIỆN", "100%")
    ]

    new_list_items = "".join([
        f'<li id="cong-doan-{num}" class="coreIntroduction_stageItem__C7_GF" data-reveal="true" data-visible="true" style="--stage-position:{pos}">'
        f'<span class="coreIntroduction_materialNumber__nbsF5">{num:02d}</span>'
        f'<strong>{name}</strong>'
        f'<span class="coreIntroduction_stagePhoto__e5sjm" role="img" aria-label="Công đoạn {num}: {name.lower()}"></span>'
        f'<a class="coreIntroduction_stageMore__uOSUQ" href="/kham-pha#cong-doan-{num}">Tìm hiểu thêm →</a>'
        f'</li>'
        for num, name, pos in stages_data
    ])

    new_ol = f'<ol class="coreIntroduction_stageList__aTih3">{new_list_items}</ol>'

    delegated_script = (
        '<script>'
        'document.addEventListener("click",function(e){'
        'var p=e.target.closest(".coreIntroduction_stagePhoto__e5sjm");'
        'if(p){var li=p.closest("li");if(li&&li.id){window.location.href="/kham-pha#"+li.id;}}'
        '});'
        '</script>'
    )

    for p in html_files:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace ol in #5-cong-doan
            pat = r'<ol class="coreIntroduction_stageList__aTih3">.*?</ol>'
            content = re.sub(pat, new_ol, content, flags=re.DOTALL)

            # Bump cache buster to v=5
            content = re.sub(r'369-2063549c42145b16\.js(?:\?v=\d+)?', '369-2063549c42145b16.js?v=5', content)
            content = re.sub(r'3d939b8161363d36\.css(?:\?v=\d+)?', '3d939b8161363d36.css?v=5', content)
            content = re.sub(r'58e70d5489b56972\.css(?:\?v=\d+)?', '58e70d5489b56972.css?v=5', content)

            # Add delegated script if not present
            if 'coreIntroduction_stagePhoto__e5sjm' in content and 'var p=e.target.closest(".coreIntroduction_stagePhoto__e5sjm")' not in content:
                content = content.replace('</body>', delegated_script + '</body>')

            with open(p, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated HTML in {p}")

if __name__ == '__main__':
    update_css()
    update_js()
    update_html()
    print("All updates applied successfully!")
