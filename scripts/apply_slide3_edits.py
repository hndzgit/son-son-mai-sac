#!/usr/bin/env python3
import re
import os

def update_html(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (not found)")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update heading
    old_heading = re.search(r'<div class="coreIntroduction_processIntro__xmAsV"[^>]*><h3 id="process-heading">.*?</h3></div>', content, re.DOTALL)
    if old_heading:
        new_heading = '<div class="coreIntroduction_processIntro__xmAsV" data-reveal="true"><h3 id="process-heading"><span class="coreIntroduction_processTitle__Y5ZSn">NĂM CHẶNG TRONG QUÁ TRÌNH TẠO TÁC<span class="coreIntroduction_titleOrnament__HAFqs" aria-hidden="true">✥</span></span></h3></div>'
        content = content[:old_heading.start()] + new_heading + content[old_heading.end():]
        print(f"Updated heading in {filepath}")
    else:
        print(f"Heading pattern not found in {filepath}")

    # 2. Update 5 cards (remove materialDescription and stageMore)
    # Match <li id="cong-doan-X" ...> ... </li>
    def clean_card(match):
        card_html = match.group(0)
        # remove materialDescription span
        card_html = re.sub(r'<span class="coreIntroduction_materialDescription__NCDzu">.*?</span>', '', card_html)
        # remove stageMore link
        card_html = re.sub(r'<a class="coreIntroduction_stageMore__uOSUQ"[^>]*>.*?</a>', '', card_html)
        return card_html

    content = re.sub(r'<li id="cong-doan-\d"[^>]*>.*?</li>', clean_card, content, flags=re.DOTALL)
    print(f"Cleaned cards in {filepath}")

    # 3. Update cache-busters: 369 chunk and 3d939b8161363d36.css
    content = re.sub(r'369-2063549c42145b16\.js(?:\?v=\d+)?', '369-2063549c42145b16.js?v=3', content)
    content = re.sub(r'3d939b8161363d36\.css(?:\?v=\d+)?', '3d939b8161363d36.css?v=3', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved {filepath}")

def update_js_chunk(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (not found)")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update heading render
    old_h3 = '(0,r.jsxs)("h3",{id:"process-heading",children:[(0,r.jsxs)("span",{className:s().processTitle,children:["NĂM CHẶNG",(0,r.jsx)("span",{className:s().titleOrnament,"aria-hidden":"true",children:"✥"})]}),(0,r.jsx)("span",{className:s().processSubtitle,children:"TRONG QUÁ TRÌNH TẠO TÁC"})]})'
    new_h3 = '(0,r.jsxs)("h3",{id:"process-heading",children:[(0,r.jsxs)("span",{className:s().processTitle,children:["NĂM CHẶNG TRONG QUÁ TRÌNH TẠO TÁC",(0,r.jsx)("span",{className:s().titleOrnament,"aria-hidden":"true",children:"✥"})]})]})'
    
    if old_h3 in content:
        content = content.replace(old_h3, new_h3)
        print(f"Updated JS heading in {filepath}")
    else:
        # Check if already updated or slight variation
        print(f"JS old_h3 exact string check in {filepath}: not found directly, checking regex")
        # Regex search for children of process-heading
        pat = r'\(0,r\.jsxs\)\("h3",\{id:"process-heading",children:\[.*?\]\}\)'
        m = re.search(pat, content)
        if m:
            print("Found heading match via regex:", m.group(0)[:80])
            content = content[:m.start()] + new_h3 + content[m.end():]
            print(f"Replaced JS heading via regex in {filepath}")

    # 2. Update cards render in m.map
    # We want children of li to NOT have materialDescription or stageMore
    old_card_children = 'children:[(0,r.jsx)("span",{className:s().materialNumber,children:String(n+1).padStart(2,"0")}),(0,r.jsx)("strong",{children:e.name}),(0,r.jsx)("span",{className:s().stagePhoto,role:"img","aria-label":"C\\xf4ng đoạn ".concat(n+1,": ").concat(e.name.toLocaleLowerCase("vi-VN"))}),(0,r.jsx)("span",{className:s().materialDescription,children:e.description}),(0,r.jsx)(i.default,{className:s().stageMore,href:"/kham-pha#cong-doan-".concat(n+1),children:"T\\xecm hiểu th\\xeam →"})]'
    new_card_children = 'children:[(0,r.jsx)("span",{className:s().materialNumber,children:String(n+1).padStart(2,"0")}),(0,r.jsx)("strong",{children:e.name}),(0,r.jsx)("span",{className:s().stagePhoto,role:"img","aria-label":"C\\xf4ng đoạn ".concat(n+1,": ").concat(e.name.toLocaleLowerCase("vi-VN"))})]'

    if old_card_children in content:
        content = content.replace(old_card_children, new_card_children)
        print(f"Updated JS cards children in {filepath}")
    else:
        print("Checking cards regex match...")
        card_pat = r'children:\[\(0,r\.jsx\)\("span",\{className:s\(\)\.materialNumber,children:String\(n\+1\)\.padStart\(2,"0"\)\}\),\(0,r\.jsx\)\("strong",\{children:e\.name\}\),\(0,r\.jsx\)\("span",\{className:s\(\)\.stagePhoto,[^]]*\}\),(0,r\.jsx)\("span",\{className:s\(\)\.materialDescription,[^]]*\}\),(0,r\.jsx)\(i\.default,\{className:s\(\)\.stageMore,[^]]*\}\)\]'
        m = re.search(card_pat, content)
        if m:
            print("Found card children match via regex!")
            content = content[:m.start()] + new_card_children + content[m.end():]
            print(f"Replaced JS card children via regex in {filepath}")
        else:
            print("Card children pattern not found in JS!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved {filepath}")

def update_css(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (not found)")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Base processTitle
    content = content.replace(
        '.coreIntroduction_processTitle__Y5ZSn{display:flex;align-items:center;gap:26px;font-size:clamp(66px,6.8vw,114px);line-height:1.05;white-space:nowrap}',
        '.coreIntroduction_processTitle__Y5ZSn{display:flex;align-items:center;gap:20px;font-size:clamp(22px,2.8vw,44px);line-height:1.2;white-space:nowrap;letter-spacing:-.03em}'
    )

    # 2. Responsive overrides for processTitle
    content = content.replace(
        '.coreIntroduction_processTitle__Y5ZSn{font-size:72px}',
        '.coreIntroduction_processTitle__Y5ZSn{font-size:38px}'
    )
    content = content.replace(
        '.coreIntroduction_processTitle__Y5ZSn{font-size:clamp(42px,8.5vw,66px);gap:12px}',
        '.coreIntroduction_processTitle__Y5ZSn{font-size:clamp(22px,4vw,34px);gap:12px}'
    )
    content = content.replace(
        '.coreIntroduction_processTitle__Y5ZSn{font-size:44px;letter-spacing:-.07em}',
        '.coreIntroduction_processTitle__Y5ZSn{font-size:26px;letter-spacing:-.04em}'
    )
    content = content.replace(
        '.coreIntroduction_processTitle__Y5ZSn{font-size:39px}',
        '.coreIntroduction_processTitle__Y5ZSn{font-size:22px}'
    )

    # 3. stageItem rows (remove row 4 for description)
    content = content.replace(
        'grid-template-rows:auto 48px auto 1fr',
        'grid-template-rows:auto 48px auto'
    )
    content = content.replace(
        'grid-template-rows:auto 44px auto 1fr',
        'grid-template-rows:auto 44px auto'
    )

    # 4. stageItem separator star position
    content = content.replace(
        '.coreIntroduction_stageItem__C7_GF:not(:first-child):before{content:"✥";position:absolute;left:-7px;top:44%;color:#bd9666;font:18px/1 Georgia,serif}',
        '.coreIntroduction_stageItem__C7_GF:not(:first-child):before{content:"✥";position:absolute;left:-7px;top:62%;color:#bd9666;font:18px/1 Georgia,serif}'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved {filepath}")

if __name__ == '__main__':
    html_files = [
        'index.html',
        'trai-nghiem/index.html',
        'kiem_tra_2026-10-12/ban_chup_goc/index.html',
        'kiem_tra_2026-10-12/ban_chup_goc/trai-nghiem/index.html'
    ]
    for hf in html_files:
        update_html(hf)

    js_files = [
        '_next/static/chunks/369-2063549c42145b16.js',
        'ma_nguon_css_js/js/369-2063549c42145b16.js',
        'kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/369-2063549c42145b16.js'
    ]
    for jf in js_files:
        update_js_chunk(jf)

    css_files = [
        '_next/static/css/3d939b8161363d36.css',
        'ma_nguon_css_js/css/3d939b8161363d36.css',
        'kiem_tra_2026-10-12/ban_chup_goc/_next/static/css/3d939b8161363d36.css'
    ]
    for cf in css_files:
        update_css(cf)
