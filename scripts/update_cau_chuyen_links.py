# -*- coding: utf-8 -*-
"""
Cập nhật nút đọc bài viết trong cau-chuyen-son-mai/index.html và chunk React
để chuyển hướng trực tiếp đến trang bài viết chuyên biệt (/cau-chuyen-son-mai/bai-viet?id=...)
"""
import os

BASE_DIR = "/Users/hoainam/Documents/Sơn son mài sắc"

# 1. Cập nhật React Chunk
chunk_path = os.path.join(BASE_DIR, "_next/static/chunks/app/cau-chuyen-son-mai/page-18999a17f9a00aec.js")
with open(chunk_path, "r", encoding="utf-8") as f:
    chunk_content = f.read()

old_chunk_target = '(0,i.jsx)("button",{className:o().readToggle,type:"button","aria-expanded":t,"aria-controls":"timeline-expanded-article",onClick:()=>m(n=>!n),children:t?"Thu gọn b\\xe0i viết ↑":"Đọc tiếp b\\xe0i viết →"})'
new_chunk_target = '(0,i.jsx)("a",{className:o().readToggle,href:"/cau-chuyen-son-mai/bai-viet?id="+n,onClick:(e)=>{e.preventDefault();window.location.href="/cau-chuyen-son-mai/bai-viet?id="+n},children:"Đọc b\\xe0i viết chi tiết →"})'

if old_chunk_target in chunk_content:
    chunk_content = chunk_content.replace(old_chunk_target, new_chunk_target)
    # Ẩn khối copy inline không cần thiết
    chunk_content = chunk_content.replace(
        'className:o().stopLongCopy,id:"timeline-expanded-article",hidden:!t,',
        'className:o().stopLongCopy,id:"timeline-expanded-article",hidden:!0,style:{display:"none"},'
    )
    with open(chunk_path, "w", encoding="utf-8") as f:
        f.write(chunk_content)
    print("Updated page-18999a17f9a00aec.js successfully!")
else:
    print("Warning: old_chunk_target not found in chunk (might be already modified).")

# 2. Cập nhật cau-chuyen-son-mai/index.html
html_path = os.path.join(BASE_DIR, "cau-chuyen-son-mai/index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

old_html_btn = '<button class="story_readToggle__Fczbq" type="button" aria-expanded="false" aria-controls="timeline-expanded-article">Đọc tiếp bài viết →</button>'
new_html_btn = '<a class="story_readToggle__Fczbq" id="timeline-read-article-link" href="/cau-chuyen-son-mai/bai-viet?id=0">Đọc bài viết chi tiết →</a>'

if old_html_btn in html_content:
    html_content = html_content.replace(old_html_btn, new_html_btn)
    print("Replaced button in cau-chuyen-son-mai/index.html!")

# Thêm script ủy quyền sự kiện (Event Delegation) để luôn đảm bảo chuyển hướng chính xác đến mốc đang chọn
delegation_script = """
<script>
  // Tự động đồng bộ link và chuyển hướng đến trang bài viết chuyên biệt
  (function() {
    function getActiveTabId() {
      var activeTab = document.querySelector('.story_timeline___fEgR button[aria-selected="true"]');
      if (activeTab && activeTab.id) {
        var match = activeTab.id.match(/timeline-tab-(\\d)/);
        if (match) return match[1];
      }
      return '0';
    }

    function syncArticleLink() {
      var id = getActiveTabId();
      var readBtn = document.querySelector('.story_readToggle__Fczbq');
      if (readBtn) {
        readBtn.href = '/cau-chuyen-son-mai/bai-viet?id=' + id;
        if (readBtn.tagName === 'BUTTON') {
          readBtn.textContent = 'Đọc bài viết chi tiết →';
        }
      }
    }

    document.addEventListener('click', function(e) {
      // Bắt click vào nút đọc bài viết
      var readBtn = e.target.closest('.story_readToggle__Fczbq');
      if (readBtn) {
        e.preventDefault();
        e.stopPropagation();
        var id = getActiveTabId();
        window.location.href = '/cau-chuyen-son-mai/bai-viet?id=' + id;
        return false;
      }
      // Khi bấm chuyển mốc thời gian
      var tabBtn = e.target.closest('.story_timeline___fEgR button, .story_detailNav__mfPwp button');
      if (tabBtn) {
        setTimeout(syncArticleLink, 60);
      }
    }, true);

    window.addEventListener('DOMContentLoaded', syncArticleLink);
    window.addEventListener('hashchange', function() {
      setTimeout(syncArticleLink, 60);
    });
    setInterval(syncArticleLink, 400);
  })();
</script>
"""

if "syncArticleLink" not in html_content:
    html_content = html_content.replace("</body>", delegation_script + "\n</body>")
    print("Added delegation script to cau-chuyen-son-mai/index.html!")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("cau-chuyen-son-mai/index.html updated successfully!")
