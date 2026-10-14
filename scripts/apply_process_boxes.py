# -*- coding: utf-8 -*-
"""
Script cập nhật giao diện section "NĂM CHẶNG TRONG QUÁ TRÌNH TẠO TÁC":
- Chuyển background 5 box từ trắng tinh (quá trắng) sang TRẮNG MỜ (frosted glass / translucent white).
- background: rgba(255, 252, 246, 0.46) với backdrop-filter: blur(10px) và viền trắng mờ tinh tế.
- Hover nhấc nhẹ và tăng độ sáng nhẹ nhàng.
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS_BOXES_CSS = """
/* ==================== NĂM CHẶNG TRONG QUÁ TRÌNH TẠO TÁC (RED BACK & FROSTED WHITE BOXES) ==================== */
/* 1. Background đỏ nhẹ nhẹ đằng sau cả section */
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

/* 3. Từng ô như 1 Chuẩn bị cốt... cho vào 1 box với background TRẮNG MỜ (frosted / translucent) */
.coreIntroduction_stageItem__C7_GF {
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
  padding: 20px 16px 20px !important;
  background: rgba(255, 252, 246, 0.46) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(255, 255, 255, 0.65) !important;
  border-radius: 12px !important;
  border-left: 1px solid rgba(255, 255, 255, 0.65) !important;
  box-shadow: 0 4px 16px rgba(100, 30, 25, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.75) !important;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease, background 0.22s ease !important;
  box-sizing: border-box !important;
  position: relative !important;
  min-height: 380px !important;
}
.coreIntroduction_stageItem__C7_GF:hover {
  transform: translateY(-5px) !important;
  background: rgba(255, 252, 246, 0.72) !important;
  box-shadow: 0 10px 24px rgba(139, 42, 42, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
  border-color: rgba(139, 42, 42, 0.3) !important;
}

/* Số thứ tự 01, 02... */
.coreIntroduction_materialNumber__nbsF5 {
  font-family: "Noto Serif", Georgia, serif !important;
  font-size: 20px !important;
  font-weight: 700 !important;
  color: #8b2a2a !important;
  line-height: 1 !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
}
.coreIntroduction_materialNumber__nbsF5::after {
  content: "" !important;
  display: inline-block !important;
  width: 22px !important;
  height: 1.5px !important;
  background: rgba(139, 42, 42, 0.35) !important;
}

/* Tên công đoạn */
.coreIntroduction_stageItem__C7_GF > strong {
  font-family: "Noto Serif", Georgia, serif !important;
  font-size: clamp(14px, 1.1vw, 16.5px) !important;
  font-weight: 700 !important;
  color: #3b1717 !important;
  line-height: 1.35 !important;
  min-height: 44px !important;
  margin: 0 !important;
  display: flex !important;
  align-items: flex-start !important;
  text-wrap: balance !important;
}

/* Ảnh minh họa của từng box */
.coreIntroduction_stagePhoto__e5sjm {
  display: block !important;
  width: 100% !important;
  height: clamp(140px, 11vw, 175px) !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid rgba(139, 42, 42, 0.12) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
  cursor: pointer !important;
  transition: transform 0.25s ease !important;
  aspect-ratio: auto !important;
}
.coreIntroduction_stageItem__C7_GF:hover .coreIntroduction_stagePhoto__e5sjm {
  transform: scale(1.025) !important;
}

/* Nút Tìm hiểu thêm */
.coreIntroduction_stageMore__uOSUQ {
  margin-top: auto !important;
  padding-top: 10px !important;
  color: #8b2a2a !important;
  font-family: Inter, Arial, sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  text-decoration: none !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  transition: gap 0.2s ease, color 0.2s ease !important;
}
.coreIntroduction_stageMore__uOSUQ:hover {
  color: #5b1717 !important;
  gap: 8px !important;
  text-decoration: underline !important;
}

/* Responsive cho tablet và mobile */
@media (max-width: 1100px) {
  .coreIntroduction_stageList__aTih3 {
    grid-template-columns: repeat(5, minmax(195px, 1fr)) !important;
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
    grid-template-columns: repeat(5, minmax(220px, 1fr)) !important;
  }
}
"""

def update_css():
    css_targets = [
        os.path.join(BASE_DIR, '_next/static/css/58e70d5489b56972.css'),
        os.path.join(BASE_DIR, 'ma_nguon_css_js/css/58e70d5489b56972.css'),
        os.path.join(BASE_DIR, '_next/static/css/3d939b8161363d36.css'),
        os.path.join(BASE_DIR, 'ma_nguon_css_js/css/3d939b8161363d36.css')
    ]
    for cpath in css_targets:
        if not os.path.exists(cpath):
            continue
        with open(cpath, 'r', encoding='utf-8') as f:
            content = f.read()

        pos = content.find('/* ==================== NĂM CHẶNG TRONG QUÁ TRÌNH TẠO TÁC')
        if pos != -1:
            content = content[:pos]

        content = content.rstrip() + "\n\n" + PROCESS_BOXES_CSS
        with open(cpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CSS: {cpath}")

def update_html_cache_buster():
    pages = [
        'index.html',
        'kham-pha/index.html',
        'tin-tuc-su-kien/index.html',
        've-du-an/index.html',
        'san-pham/index.html',
        'cau-chuyen-son-mai/index.html',
        'trai-nghiem/index.html',
        'trai-nghiem/hanh-trinh/index.html',
        'tu-chinh/index.html'
    ]

    for rel in pages:
        fpath = os.path.join(BASE_DIR, rel)
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        content = re.sub(r'58e70d5489b56972\.css\?v=\d+', '58e70d5489b56972.css?v=10', content)
        content = re.sub(r'3d939b8161363d36\.css\?v=\d+', '3d939b8161363d36.css?v=10', content)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML cache buster ?v=10: {fpath}")

if __name__ == '__main__':
    update_css()
    update_html_cache_buster()
    print("DONE! Box updated to frosted translucent white (trắng mờ).")
