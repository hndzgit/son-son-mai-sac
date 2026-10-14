# -*- coding: utf-8 -*-
"""
Cập nhật nhãn nút "Đọc bài viết →" và liên kết chuyên biệt cho từng mốc
Áp dụng đồng bộ cho:
1. cau-chuyen-son-mai/index.html
2. _next/static/chunks/app/cau-chuyen-son-mai/page-18999a17f9a00aec.js
3. ma_nguon_css_js/js/app_cau-chuyen-son-mai_page-18999a17f9a00aec.js
4. trang_html_goc/06_cau_chuyen_son_mai.html
"""
import os

BASE_DIR = "/Users/hoainam/Documents/Sơn son mài sắc"

# 1. Cập nhật JS chunks
js_files = [
    os.path.join(BASE_DIR, "_next/static/chunks/app/cau-chuyen-son-mai/page-18999a17f9a00aec.js"),
    os.path.join(BASE_DIR, "ma_nguon_css_js/js/app_cau-chuyen-son-mai_page-18999a17f9a00aec.js")
]

for js_path in js_files:
    if not os.path.exists(js_path):
        continue
    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Trường hợp 1: đã có href bai-viet?id=
    old_code_1 = '(0,i.jsx)("a",{className:o().readToggle,href:"/cau-chuyen-son-mai/bai-viet?id="+n,onClick:(e)=>{e.preventDefault();window.location.href="/cau-chuyen-son-mai/bai-viet?id="+n},children:"Đọc b\\xe0i viết chi tiết →"})'
    # Trường hợp 2: gốc button toggle
    old_code_2 = '(0,i.jsx)("button",{className:o().readToggle,type:"button","aria-expanded":t,"aria-controls":"timeline-expanded-article",onClick:()=>m(n=>!n),children:t?"Thu gọn b\\xe0i viết ↑":"Đọc tiếp b\\xe0i viết →"})'

    new_code = '(0,i.jsx)("a",{className:o().readToggle,href:"/cau-chuyen-son-mai/bai-viet/"+(n+1),onClick:(e)=>{e.preventDefault();window.location.href="/cau-chuyen-son-mai/bai-viet/"+(n+1)},children:"Đọc b\\xe0i viết →"})'

    if old_code_1 in content:
        content = content.replace(old_code_1, new_code)
        print(f"Updated JS (from old_code_1): {js_path}")
    elif old_code_2 in content:
        content = content.replace(old_code_2, new_code)
        content = content.replace(
            'className:o().stopLongCopy,id:"timeline-expanded-article",hidden:!t,',
            'className:o().stopLongCopy,id:"timeline-expanded-article",hidden:!0,style:{display:"none"},'
        )
        print(f"Updated JS (from old_code_2): {js_path}")
    else:
        # Thử tìm và thay chuỗi text trực tiếp
        if 'children:"Đọc b\\xe0i viết chi tiết →"' in content:
            content = content.replace('children:"Đọc b\\xe0i viết chi tiết →"', 'children:"Đọc b\\xe0i viết →"')
            content = content.replace('"/cau-chuyen-son-mai/bai-viet?id="+n', '"/cau-chuyen-son-mai/bai-viet/"+(n+1)')
            print(f"Patched text in JS: {js_path}")

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(content)

# 2. Cập nhật cau-chuyen-son-mai/index.html
html_path = os.path.join(BASE_DIR, "cau-chuyen-son-mai/index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Đổi nút ban đầu
html = html.replace(
    '<a class="story_readToggle__Fczbq" id="timeline-read-article-link" href="/cau-chuyen-son-mai/bai-viet?id=0">Đọc bài viết chi tiết →</a>',
    '<a class="story_readToggle__Fczbq" id="timeline-read-article-link" href="/cau-chuyen-son-mai/bai-viet/1">Đọc bài viết →</a>'
)
html = html.replace(
    '<a class="story_readToggle__Fczbq" id="timeline-read-article-link" href="/cau-chuyen-son-mai/bai-viet?id=0">Đọc tiếp bài viết →</a>',
    '<a class="story_readToggle__Fczbq" id="timeline-read-article-link" href="/cau-chuyen-son-mai/bai-viet/1">Đọc bài viết →</a>'
)
html = html.replace(
    '<button class="story_readToggle__Fczbq" type="button" aria-expanded="false" aria-controls="timeline-expanded-article">Đọc tiếp bài viết →</button>',
    '<a class="story_readToggle__Fczbq" id="timeline-read-article-link" href="/cau-chuyen-son-mai/bai-viet/1">Đọc bài viết →</a>'
)

# Cập nhật script đồng bộ
old_script_sync = """    function syncArticleLink() {
      var id = getActiveTabId();
      var readBtn = document.querySelector('.story_readToggle__Fczbq');
      if (readBtn) {
        readBtn.href = '/cau-chuyen-son-mai/bai-viet?id=' + id;
        if (readBtn.tagName === 'BUTTON') {
          readBtn.textContent = 'Đọc bài viết chi tiết →';
        }
      }
    }"""

new_script_sync = """    function syncArticleLink() {
      var id = getActiveTabId();
      var num = Number(id) + 1;
      var readBtn = document.querySelector('.story_readToggle__Fczbq');
      if (readBtn) {
        readBtn.href = '/cau-chuyen-son-mai/bai-viet/' + num;
        readBtn.textContent = 'Đọc bài viết →';
      }
    }"""

html = html.replace(old_script_sync, new_script_sync)

old_click = """        var id = getActiveTabId();
        window.location.href = '/cau-chuyen-son-mai/bai-viet?id=' + id;"""

new_click = """        var id = getActiveTabId();
        var num = Number(id) + 1;
        window.location.href = '/cau-chuyen-son-mai/bai-viet/' + num;"""

html = html.replace(old_click, new_click)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Updated HTML: {html_path}")

# 3. Cập nhật trang_html_goc/06_cau_chuyen_son_mai.html nếu có
goc_path = os.path.join(BASE_DIR, "trang_html_goc/06_cau_chuyen_son_mai.html")
if os.path.exists(goc_path):
    with open(goc_path, "r", encoding="utf-8") as f:
        goc = f.read()
    goc = goc.replace('Đọc tiếp bài viết →', 'Đọc bài viết →')
    with open(goc_path, "w", encoding="utf-8") as f:
        f.write(goc)
    print(f"Updated gốc: {goc_path}")

print("COMPLETED SYNCING BUTTON TEXT AND DEDICATED MILESTONE LINKS!")
