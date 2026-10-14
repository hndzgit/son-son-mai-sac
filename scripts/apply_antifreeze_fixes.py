# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# 1. Update _next/static/css/3d939b8161363d36.css and ma_nguon_css_js/css/3d939b8161363d36.css
css_files = [
    os.path.join(PROJECT_DIR, '_next/static/css/3d939b8161363d36.css'),
    os.path.join(PROJECT_DIR, 'ma_nguon_css_js/css/3d939b8161363d36.css')
]

for cf in css_files:
    if os.path.exists(cf):
        with open(cf, 'r', encoding='utf-8') as f:
            content = f.read()
        target = '.coreIntroduction_journey__bHzBt [data-reveal]:not([data-visible=true]){opacity:.01;transform:translateY(12px)}'
        replacement = '.coreIntroduction_journey__bHzBt [data-reveal]:not([data-visible=true]){opacity:1;transform:none}'
        if target in content:
            content = content.replace(target, replacement)
            with open(cf, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {cf}: replaced opacity:.01 with opacity:1")
        else:
            print(f"Target rule not found in {cf}")

# 2. Update _next/static/css/58e70d5489b56972.css
global_css = os.path.join(PROJECT_DIR, '_next/static/css/58e70d5489b56972.css')
if os.path.exists(global_css):
    with open(global_css, 'r', encoding='utf-8') as f:
        content = f.read()
    
    override_css = (
        "\n/* Anti-freeze reveal & preloader fix */\n"
        ".coreIntroduction_journey__bHzBt [data-reveal],"
        ".coreIntroduction_journey__bHzBt [data-reveal]:not([data-visible=\"true\"]),"
        "[data-reveal],"
        "[data-reveal]:not([data-visible=\"true\"]){opacity:1!important;transform:none!important;visibility:visible!important}\n"
        ".entry-screen,.core-v4-preloader{display:none!important;opacity:0!important;pointer-events:none!important;visibility:hidden!important}\n"
    )
    if "/* Anti-freeze reveal & preloader fix */" not in content:
        content += override_css
        with open(global_css, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Appended anti-freeze override to {global_css}")
    else:
        print("Override already present in global css")

# 3. Update _next/static/chunks/369-2063549c42145b16.js
chunk_file = os.path.join(PROJECT_DIR, '_next/static/chunks/369-2063549c42145b16.js')
if os.path.exists(chunk_file):
    with open(chunk_file, 'r', encoding='utf-8') as f:
        js = f.read()
    
    # Target:
    # if(window.matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver"in window)){t.forEach(e=>{e.dataset.visible="true"});return}
    old_code = 'if(window.matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver"in window)){t.forEach(e=>{e.dataset.visible="true"});return}'
    new_code = 't.forEach(e=>{e.dataset.visible="true"});if(window.matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver"in window)){return}'
    if old_code in js:
        js = js.replace(old_code, new_code)
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(js)
        print("Updated 369 chunk: immediately sets data-visible=true on mount")
    else:
        print("Target code not found in 369 chunk")

# 4. Update index.html and trai-nghiem/index.html to add data-visible="true"
html_files = [
    os.path.join(PROJECT_DIR, 'index.html'),
    os.path.join(PROJECT_DIR, 'trai-nghiem/index.html')
]

for hf in html_files:
    if os.path.exists(hf):
        with open(hf, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Replace data-reveal="true" with data-reveal="true" data-visible="true" (if not already having data-visible)
        # Be careful not to duplicate data-visible="true"
        def repl(match):
            tag = match.group(0)
            if 'data-visible=' not in tag:
                return tag.replace('data-reveal="true"', 'data-reveal="true" data-visible="true"')
            return tag

        new_html = re.sub(r'<[^>]*data-reveal="true"[^>]*>', repl, html)
        if new_html != html:
            with open(hf, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"Updated {hf}: added data-visible=\"true\" to static HTML")
        else:
            print(f"No changes needed for {hf}")

print("All reveal anti-freeze fixes applied successfully!")
