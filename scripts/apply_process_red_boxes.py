# -*- coding: utf-8 -*-
"""
Script cập nhật thiết kế 5 công đoạn trong quá trình tạo tác theo yêu cầu người dùng:
1. Tên công đoạn to hơn, căn giữa, đặt gần số thứ tự.
2. Các dòng "Tìm hiểu thêm" riêng lẻ được gộp lại thành 1 Ô BOX ĐẸP MẮT ở dưới cả 5 card.
3. Khung box của cả 5 card chuyển sang màu ĐỎ NHẠT NHẠT (đỏ son mờ sang trọng) đồng bộ với giao diện.
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

NEW_PROCESS_CSS = """
/* ==================== 5 CÔNG ĐOẠN: KHUNG ĐỎ NHẠT, TÊN TO CĂN GIỮA, GỘP NÚT TÌM HIỂU THÊM THÀNH 1 BOX ==================== */
/* 1. Nền section đỏ nhạt dịu mắt */
.coreIntroduction_processSection__4gTz3 {
  position: relative !important;
  background: linear-gradient(180deg, rgba(139, 42, 42, 0.05) 0%, rgba(139, 42, 42, 0.09) 50%, rgba(139, 42, 42, 0.05) 100%) !important;
  border-top: 1px solid rgba(139, 42, 42, 0.22) !important;
  border-bottom: 1px solid rgba(139, 42, 42, 0.22) !important;
  padding: 60px clamp(20px, 4vw, 64px) 56px !important;
  margin-top: 54px !important;
  box-sizing: border-box !important;
}

/* Tiêu đề mục */
.coreIntroduction_processIntro__xmAsV {
  margin-bottom: 36px !important;
}
.coreIntroduction_processTitle__Y5ZSn {
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-size: clamp(22px, 2.6vw, 38px) !important;
  font-weight: 700 !important;
  color: #8b2a2a !important;
  letter-spacing: -0.01em !important;
}
.coreIntroduction_titleOrnament__HAFqs {
  color: #8b2a2a !important;
  opacity: 0.85 !important;
}

/* 2. Grid 5 ô công đoạn */
.coreIntroduction_stageList__aTih3 {
  display: grid !important;
  grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
  gap: 16px !important;
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* 3. Từng ô: KHUNG BOX MÀU ĐỎ NHẠT NHẠT sang trọng */
.coreIntroduction_stageItem__C7_GF {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
  gap: 10px !important;
  padding: 22px 14px 22px !important;
  background: linear-gradient(180deg, rgba(139, 42, 42, 0.08) 0%, rgba(139, 42, 42, 0.13) 100%) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  border: 1px solid rgba(139, 42, 42, 0.26) !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 18px rgba(100, 25, 20, 0.07), inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease, background 0.25s ease !important;
  box-sizing: border-box !important;
  position: relative !important;
  cursor: pointer !important;
}
.coreIntroduction_stageItem__C7_GF:hover {
  transform: translateY(-5px) !important;
  background: linear-gradient(180deg, rgba(139, 42, 42, 0.14) 0%, rgba(139, 42, 42, 0.20) 100%) !important;
  box-shadow: 0 12px 28px rgba(139, 42, 42, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.7) !important;
  border-color: rgba(139, 42, 42, 0.45) !important;
}

/* Số thứ tự 01, 02... căn giữa */
.coreIntroduction_materialNumber__nbsF5 {
  font-family: "Noto Serif", Georgia, serif !important;
  font-size: 21px !important;
  font-weight: 700 !important;
  color: #8b2a2a !important;
  line-height: 1 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  margin: 0 0 2px 0 !important;
}
.coreIntroduction_materialNumber__nbsF5::after {
  content: "" !important;
  display: inline-block !important;
  width: 20px !important;
  height: 1.5px !important;
  background: rgba(139, 42, 42, 0.45) !important;
}

/* Tên công đoạn: TO, CĂN GIỮA, GẦN SỐ */
.coreIntroduction_stageItem__C7_GF > strong {
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-size: clamp(15.5px, 1.25vw, 19.5px) !important;
  font-weight: 700 !important;
  color: #431212 !important;
  line-height: 1.28 !important;
  min-height: 46px !important;
  margin: 0 0 10px 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  text-wrap: balance !important;
  letter-spacing: -0.015em !important;
}

/* Ảnh minh họa của từng box: viền đỏ nhẹ */
.coreIntroduction_stagePhoto__e5sjm {
  display: block !important;
  width: 100% !important;
  height: clamp(140px, 11vw, 175px) !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid rgba(139, 42, 42, 0.22) !important;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.12) !important;
  cursor: pointer !important;
  transition: transform 0.25s ease !important;
  aspect-ratio: auto !important;
}
.coreIntroduction_stageItem__C7_GF:hover .coreIntroduction_stagePhoto__e5sjm {
  transform: scale(1.025) !important;
}

/* Ẩn link Tìm hiểu thêm rải rác trong từng card vì đã gộp thành 1 box ở dưới */
.coreIntroduction_stageItem__C7_GF .coreIntroduction_stageMore__uOSUQ {
  display: none !important;
}

/* 4. Ô BOX GỘP TÌM HIỂU THÊM Ở DƯỚI */
.coreIntroduction_processMoreWrap {
  margin-top: 36px !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  width: 100% !important;
}

.coreIntroduction_processMoreBox {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 12px !important;
  padding: 14px 34px !important;
  background: linear-gradient(135deg, rgba(139, 42, 42, 0.94) 0%, rgba(105, 25, 25, 0.98) 100%) !important;
  color: #fff6e0 !important;
  font-family: "Noto Serif", Georgia, serif !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  letter-spacing: 0.02em !important;
  text-decoration: none !important;
  border: 1px solid rgba(219, 184, 90, 0.65) !important;
  border-radius: 9999px !important;
  box-shadow: 0 8px 24px rgba(139, 42, 42, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease, color 0.2s ease !important;
  cursor: pointer !important;
}
.coreIntroduction_processMoreBox:hover {
  transform: translateY(-2px) !important;
  background: linear-gradient(135deg, #a83232 0%, #821f1f 100%) !important;
  box-shadow: 0 12px 28px rgba(139, 42, 42, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
  color: #ffffff !important;
}
.coreIntroduction_processMoreArrow {
  font-size: 19px !important;
  line-height: 1 !important;
  transition: transform 0.2s ease !important;
}
.coreIntroduction_processMoreBox:hover .coreIntroduction_processMoreArrow {
  transform: translateX(4px) !important;
}

/* Responsive cho tablet và mobile */
@media (max-width: 1100px) {
  .coreIntroduction_stageList__aTih3 {
    grid-template-columns: repeat(5, minmax(200px, 1fr)) !important;
    overflow-x: auto !important;
    scroll-snap-type: x mandatory !important;
    padding-bottom: 16px !important;
    gap: 14px !important;
  }
  .coreIntroduction_stageItem__C7_GF {
    scroll-snap-align: start !important;
  }
}
@media (max-width: 600px) {
  .coreIntroduction_processSection__4gTz3 {
    padding: 40px 16px 36px !important;
  }
  .coreIntroduction_stageList__aTih3 {
    grid-template-columns: repeat(5, minmax(225px, 1fr)) !important;
  }
  .coreIntroduction_processMoreBox {
    width: 100% !important;
    padding: 13px 20px !important;
    font-size: 14.5px !important;
    text-align: center !important;
  }
}
"""

def update_css():
    css_files = [
        os.path.join(BASE_DIR, '_next/static/css/58e70d5489b56972.css'),
        os.path.join(BASE_DIR, 'ma_nguon_css_js/css/58e70d5489b56972.css'),
        os.path.join(BASE_DIR, '_next/static/css/3d939b8161363d36.css'),
        os.path.join(BASE_DIR, 'ma_nguon_css_js/css/3d939b8161363d36.css')
    ]
    for cpath in css_files:
        if not os.path.exists(cpath):
            continue
        with open(cpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove previous section marker if exists
        marker1 = '/* ==================== NĂM CHẶNG TRONG QUÁ TRÌNH TẠO TÁC'
        marker2 = '/* ==================== 5 CÔNG ĐOẠN: KHUNG ĐỎ NHẠT'
        for m in [marker1, marker2]:
            pos = content.find(m)
            if pos != -1:
                content = content[:pos]

        content = content.rstrip() + "\n\n" + NEW_PROCESS_CSS
        with open(cpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CSS: {cpath}")

def update_html():
    more_box_html = (
        '<div class="coreIntroduction_processMoreWrap">'
        '<a class="coreIntroduction_processMoreBox" href="/kham-pha#5-cong-doan">'
        '<span>Tìm hiểu chi tiết 5 công đoạn tạo tác sơn mài</span>'
        '<span class="coreIntroduction_processMoreArrow" aria-hidden="true">⟶</span>'
        '</a>'
        '</div>'
    )

    card_click_script = (
        '<script>'
        'document.addEventListener("click",function(e){'
        'var li=e.target.closest(".coreIntroduction_stageItem__C7_GF");'
        'if(li&&li.id&&!e.target.closest("a")){'
        'window.location.href="/kham-pha#"+li.id;'
        '}'
        '});'
        '</script>'
    )

    pages = ['index.html', 'trai-nghiem/index.html']
    for p in pages:
        fpath = os.path.join(BASE_DIR, p)
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Insert more_box_html right after </ol> of stageList if not present
        if 'coreIntroduction_processMoreWrap' not in content:
            target = '</ol></section>'
            if target in content:
                content = content.replace(target, f'</ol>{more_box_html}</section>', 1)
                print(f"[{p}] Added coreIntroduction_processMoreWrap after </ol>")

        # Ensure card_click_script is present before </body>
        if 'coreIntroduction_stageItem__C7_GF' not in content or 'window.location.href="/kham-pha#"' not in content:
            if '</body>' in content:
                content = content.replace('</body>', f'{card_click_script}</body>', 1)
                print(f"[{p}] Added card click handler")

        # Cache buster bump
        content = re.sub(r'58e70d5489b56972\.css\?v=\d+', '58e70d5489b56972.css?v=13', content)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML: {fpath}")

def update_js_chunk():
    js_files = [
        os.path.join(BASE_DIR, '_next/static/chunks/369-2063549c42145b16.js'),
        os.path.join(BASE_DIR, 'ma_nguon_css_js/js/369-2063549c42145b16.js')
    ]
    for jpath in js_files:
        if not os.path.exists(jpath):
            continue
        with open(jpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if processMoreWrap is already in JS
        if 'coreIntroduction_processMoreWrap' not in content:
            # We want to replace the section children in JS
            # In JS: (0,r.jsxs)("section",{id:"5-cong-doan",className:s().processSection,"aria-labelledby":"process-heading",children:[(0,r.jsx)("div",{className:s().processIntro...}),(0,r.jsx)("ol",{className:s().stageList...})]})
            # We want to append the moreBox after ol!
            old_section_pat = r'(\(0,r\.jsx\)\("ol",\{className:s\(\)\.stageList,children:m\.map\([^)]*\)\}\))\]\}\)'
            new_append = (
                r'\1,(0,r.jsx)("div",{className:"coreIntroduction_processMoreWrap",children:(0,r.jsxs)("a",'
                r'{className:"coreIntroduction_processMoreBox",href:"/kham-pha#5-cong-doan",'
                r'children:[(0,r.jsx)("span",{children:"Tìm hiểu chi tiết 5 công đoạn tạo tác sơn mài"}),'
                r'(0,r.jsx)("span",{className:"coreIntroduction_processMoreArrow","aria-hidden":!0,children:"⟶"})]})})]})'
            )
            content, count = re.subn(old_section_pat, new_append, content)
            print(f"[{os.path.basename(jpath)}] Appended processMoreWrap in JS: {count} replacement(s)")

        with open(jpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved JS: {jpath}")

if __name__ == '__main__':
    update_css()
    update_html()
    update_js_chunk()
    print("FINISHED ALL UPDATES!")
