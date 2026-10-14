#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to update wording:
1. Re-word the section heading in kham-pha to: "5 chặng trong quá trình tạo tác"
2. Re-word navigation menu in layout chunk and all pages to: "5 chặng tạo tác"
3. Re-word related callouts consistently to "5 chặng tạo tác"
"""

import os
import glob
import subprocess

def update_file(path, old_sub, new_sub):
    if not os.path.exists(path):
        print(f"Skipping missing: {path}")
        return False
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_sub in content:
        content = content.replace(old_sub, new_sub)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {path}")
        return True
    else:
        print(f"Pattern not found in: {path}")
        return False

def main():
    print("--- 1. Updating kham-pha client page chunk ---")
    old_h2 = '(0,s.jsxs)("h2",{id:"core-v4-process-title",children:["05 C\\xd4NG ĐOẠN",(0,s.jsx)("br",{}),"TẠO N\\xcaN MỘT BỀ MẶT"]})'
    new_h2 = '(0,s.jsx)("h2",{id:"core-v4-process-title",children:"5 chặng trong quá trình tạo tác"})'
    
    update_file('_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js', old_h2, new_h2)
    update_file('ma_nguon_css_js/js/app_kham-pha_page-b0c7a974225638c7.js', old_h2, new_h2)

    print("\n--- 2. Updating layout navbar chunk ---")
    old_menu = '{title:"5 c\\xf4ng đoạn",href:"/kham-pha#5-cong-doan"'
    new_menu = '{title:"5 chặng tạo tác",href:"/kham-pha#5-cong-doan"'
    
    update_file('_next/static/chunks/app/layout-885788913b392875.js', old_menu, new_menu)
    update_file('ma_nguon_css_js/js/app_layout-885788913b392875.js', old_menu, new_menu)

    print("\n--- 3. Updating home chunk (369) ---")
    old_cta = 'children:"Tìm hiểu chi tiết 5 công đoạn tạo tác sơn mài"'
    new_cta = 'children:"Tìm hiểu chi tiết 5 chặng tạo tác"'
    update_file('_next/static/chunks/369-2063549c42145b16.js', old_cta, new_cta)
    update_file('ma_nguon_css_js/js/369-2063549c42145b16.js', old_cta, new_cta)

    print("\n--- 4. Updating ve-du-an/index.html ---")
    update_file('ve-du-an/index.html', 'Khám phá 5 công đoạn →', 'Khám phá 5 chặng tạo tác →')

    print("\n--- 5. Updating cau-chuyen-son-mai subpages ---")
    for f in glob.glob('cau-chuyen-son-mai/**/*.html', recursive=True):
        update_file(f, 'Khám phá 5 công đoạn sơn mài →', 'Khám phá 5 chặng tạo tác →')

    print("\n--- 6. Verifying JS syntax with node -c ---")
    for js_file in [
        '_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js',
        '_next/static/chunks/app/layout-885788913b392875.js',
        '_next/static/chunks/369-2063549c42145b16.js'
    ]:
        res = subprocess.run(['node', '-c', js_file], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Syntax OK: {js_file}")
        else:
            print(f"Syntax ERROR in {js_file}: {res.stderr}")

if __name__ == '__main__':
    main()
