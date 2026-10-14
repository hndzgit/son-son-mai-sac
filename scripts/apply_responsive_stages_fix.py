# -*- coding: utf-8 -*-
"""
Script sửa triệt để và tối ưu hóa 5 chặng trong quá trình tạo tác trên:
- Điện thoại (Mobile 375px - 430px)
- Máy tính bảng (iPad / Tablet 768px - 1024px)
- Máy tính (Desktop 1200px+)
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PERFECT_STAGES_CSS = """
/* ==================== 5 CHẶNG TẠO TÁC: ĐỈNH CAO RESPONSIVE & SIÊU MƯỢT TRÊN MỌI THIẾT BỊ ==================== */

/* 1. Nền section đỏ nhạt dịu mắt */
.coreIntroduction_processSection__4gTz3 {
  position: relative !important;
  background: linear-gradient(180deg, rgba(139, 42, 42, 0.05) 0%, rgba(139, 42, 42, 0.09) 50%, rgba(139, 42, 42, 0.05) 100%) !important;
  border-top: 1px solid rgba(139, 42, 42, 0.22) !important;
  border-bottom: 1px solid rgba(139, 42, 42, 0.22) !important;
  padding: 56px clamp(16px, 3.5vw, 64px) 52px !important;
  margin-top: 50px !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
  width: 100% !important;
  max-width: 100% !important;
}

/* Tiêu đề mục: Căn giữa, co giãn tự nhiên không bao giờ bị cắt chữ */
.coreIntroduction_processIntro__xmAsV {
  display: block !important;
  text-align: center !important;
  margin: 0 auto 34px auto !important;
  max-width: 100% !important;
  padding: 0 10px !important;
}

.coreIntroduction_processIntro__xmAsV h3 {
  text-align: center !important;
  margin: 0 !important;
}

.coreIntroduction_processTitle__Y5ZSn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-wrap: wrap !important;
  white-space: normal !important;
  word-break: break-word !important;
  text-align: center !important;
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-size: clamp(21px, 3.2vw, 38px) !important;
  font-weight: 700 !important;
  color: #8b2a2a !important;
  letter-spacing: -0.01em !important;
  line-height: 1.3 !important;
  gap: 12px !important;
  max-width: 100% !important;
}

.coreIntroduction_titleOrnament__HAFqs {
  color: #8b2a2a !important;
  opacity: 0.85 !important;
  font-size: 20px !important;
  display: inline-flex !important;
  align-items: center !important;
  flex: 0 0 auto !important;
}
.coreIntroduction_titleOrnament__HAFqs:before {
  display: none !important;
}

/* 2. Grid & Flex: Tự động thích ứng trên mọi màn hình */
/* Màn hình lớn (Desktop >= 1024px): 5 cột song song hoàn hảo */
@media (min-width: 1024px) {
  .coreIntroduction_stageList__aTih3 {
    display: grid !important;
    grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
    gap: 16px !important;
    list-style: none !important;
    padding: 0 !important;
    margin: 0 auto !important;
    max-width: 1560px !important;
    overflow-x: visible !important;
  }
  .coreIntroduction_stageItem__C7_GF {
    width: 100% !important;
  }
}

/* Tablet & Mobile (< 1024px): Swipe Carousel trơn tru với scroll-snap */
@media (max-width: 1023px) {
  .coreIntroduction_processSection__4gTz3 {
    padding: 42px 14px 40px !important;
  }
  .coreIntroduction_stageList__aTih3 {
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    scroll-snap-type: x mandatory !important;
    -webkit-overflow-scrolling: touch !important;
    gap: 14px !important;
    padding: 6px 16px 12px 16px !important;
    margin: 0 -14px !important;
    list-style: none !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
  }
  .coreIntroduction_stageList__aTih3::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
  }
  .coreIntroduction_stageItem__C7_GF {
    flex: 0 0 255px !important;
    width: 255px !important;
    min-width: 255px !important;
    max-width: 82vw !important;
    scroll-snap-align: center !important;
  }
  .coreIntroduction_stageItem__C7_GF:not(:first-child):before {
    display: none !important;
  }
}

@media (max-width: 520px) {
  .coreIntroduction_processSection__4gTz3 {
    padding: 36px 12px 34px !important;
  }
  .coreIntroduction_processTitle__Y5ZSn {
    font-size: clamp(19px, 5.6vw, 24px) !important;
    letter-spacing: -0.015em !important;
  }
  .coreIntroduction_stageList__aTih3 {
    padding: 6px 12px 12px 12px !important;
    margin: 0 -12px !important;
    gap: 12px !important;
  }
  .coreIntroduction_stageItem__C7_GF {
    flex: 0 0 245px !important;
    width: 245px !important;
    min-width: 245px !important;
    max-width: 78vw !important;
  }
}

/* 3. Từng ô Card: KHUNG ĐỎ NHẠT SƠN MÀI SANG TRỌNG */
.coreIntroduction_stageItem__C7_GF {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-start !important;
  text-align: center !important;
  gap: 8px !important;
  padding: 22px 14px 20px !important;
  background: linear-gradient(180deg, rgba(160, 42, 42, 0.10) 0%, rgba(160, 42, 42, 0.16) 100%) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  border: 1px solid rgba(160, 42, 42, 0.30) !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 18px rgba(100, 25, 20, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease, background 0.25s ease !important;
  box-sizing: border-box !important;
  position: relative !important;
  cursor: pointer !important;
}

.coreIntroduction_stageItem__C7_GF:hover {
  transform: translateY(-5px) !important;
  background: linear-gradient(180deg, rgba(160, 42, 42, 0.16) 0%, rgba(160, 42, 42, 0.24) 100%) !important;
  box-shadow: 0 12px 28px rgba(139, 42, 42, 0.20), inset 0 1px 0 rgba(255, 255, 255, 0.7) !important;
  border-color: rgba(160, 42, 42, 0.48) !important;
}

/* Số 01, 02... CĂN GIỮA */
.coreIntroduction_materialNumber__nbsF5 {
  font-family: "Noto Serif", Georgia, serif !important;
  font-size: 22px !important;
  font-weight: 700 !important;
  color: #8b2a2a !important;
  line-height: 1 !important;
  display: block !important;
  width: 100% !important;
  text-align: center !important;
  margin: 0 auto 4px auto !important;
}

.coreIntroduction_materialNumber__nbsF5::after,
.coreIntroduction_materialNumber__nbsF5::before {
  content: none !important;
  display: none !important;
}

/* Tên công đoạn: TO, CĂN GIỮA HOÀN TOÀN, SÁT DƯỚI SỐ */
.coreIntroduction_stageItem__C7_GF > strong {
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-size: clamp(15.5px, 1.25vw, 19.5px) !important;
  font-weight: 700 !important;
  color: #431212 !important;
  line-height: 1.26 !important;
  min-height: 46px !important;
  margin: 0 0 10px 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  align-self: center !important;
  width: 100% !important;
  max-width: 100% !important;
  text-align: center !important;
  text-wrap: balance !important;
  letter-spacing: -0.015em !important;
}

/* 4. Ảnh minh họa từng công đoạn: CHUẨN ĐẸP TỶ LỆ, SẮC NÉT, KHÔNG BỊ CO ĐEN */
.coreIntroduction_stagePhoto__e5sjm {
  display: block !important;
  width: 100% !important;
  aspect-ratio: 16/11 !important;
  height: auto !important;
  min-height: 140px !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid rgba(160, 42, 42, 0.28) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  cursor: pointer !important;
  transition: transform 0.28s ease, box-shadow 0.28s ease !important;
  background-size: cover !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-color: #241612 !important;
  align-self: center !important;
}

.coreIntroduction_stageItem__C7_GF:hover .coreIntroduction_stagePhoto__e5sjm {
  transform: scale(1.03) !important;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.22) !important;
}

/* Ảnh riêng biệt cho từng công đoạn (sắc nét, không lệch vị trí, không vạch đen) */
#cong-doan-1 .coreIntroduction_stagePhoto__e5sjm {
  background-image: url(/story-assets/process-stage-1.webp) !important;
}
#cong-doan-2 .coreIntroduction_stagePhoto__e5sjm {
  background-image: url(/story-assets/process-stage-2.webp) !important;
}
#cong-doan-3 .coreIntroduction_stagePhoto__e5sjm {
  background-image: url(/story-assets/process-stage-3.webp) !important;
}
#cong-doan-4 .coreIntroduction_stagePhoto__e5sjm {
  background-image: url(/story-assets/process-stage-4.webp) !important;
}
#cong-doan-5 .coreIntroduction_stagePhoto__e5sjm {
  background-image: url(/story-assets/process-stage-5.webp) !important;
}

/* Ẩn link Tìm hiểu thêm rải rác từng ô */
.coreIntroduction_stageItem__C7_GF .coreIntroduction_stageMore__uOSUQ {
  display: none !important;
}

/* 5. Gợi ý vuốt ngang trên Mobile / Tablet bằng ::before của container nút (miễn nhiễm với React hydration) */
@media (max-width: 1023px) {
  .coreIntroduction_processMoreWrap {
    flex-direction: column !important;
    gap: 16px !important;
    margin-top: 18px !important;
  }
  .coreIntroduction_processMoreWrap::before {
    content: "← Vuốt ngang để khám phá 5 chặng →" !important;
    display: block !important;
    color: #8b2a2a !important;
    font-size: 13px !important;
    font-family: "Noto Serif", Georgia, serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    opacity: 0.85 !important;
    text-align: center !important;
  }
}
@media (min-width: 1024px) {
  .coreIntroduction_processMoreWrap::before {
    content: none !important;
    display: none !important;
  }
}

/* 6. Ô BOX GỘP TÌM HIỂU THÊM Ở DƯỚI */
.coreIntroduction_processMoreWrap {
  margin-top: 28px !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  width: 100% !important;
  box-sizing: border-box !important;
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
  max-width: 92% !important;
  box-sizing: border-box !important;
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

@media (max-width: 600px) {
  .coreIntroduction_processMoreWrap {
    margin-top: 20px !important;
  }
  .coreIntroduction_processMoreBox {
    width: auto !important;
    padding: 12px 22px !important;
    font-size: 14.5px !important;
    text-align: center !important;
    gap: 8px !important;
  }
}
"""

def clean_and_update_css_files():
    css_files = [
        os.path.join(BASE_DIR, '_next/static/css/3d939b8161363d36.css'),
        os.path.join(BASE_DIR, 'ma_nguon_css_js/css/3d939b8161363d36.css'),
        os.path.join(BASE_DIR, '_next/static/css/58e70d5489b56972.css'),
        os.path.join(BASE_DIR, 'ma_nguon_css_js/css/58e70d5489b56972.css')
    ]
    
    for cpath in css_files:
        if not os.path.exists(cpath):
            continue
        with open(cpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove previous sections if present
        p3 = '/* ==================== 5 CHẶNG TẠO TÁC: ĐỈNH CAO'
        if p3 in content:
            idx = content.find(p3)
            content = content[:idx]

        p2 = '/* 2. CHUẨN HÓA 5 CÔNG ĐOẠN: KHUNG ĐỎ NHẠT'
        if p2 in content:
            regex_p2 = r'/\* 2\. CHUẨN HÓA 5 CÔNG ĐOẠN.*?\.(?:coreIntroduction_stageItem__C7_GF\s*\.coreIntroduction_stageMore__uOSUQ|coreIntroduction_stageMore__uOSUQ)\s*\{[^}]*\}'
            content = re.sub(regex_p2, '', content, flags=re.DOTALL)

        p1 = '/* ==================== 5 CÔNG ĐOẠN: KHUNG ĐỎ NHẠT'
        if p1 in content:
            regex_p1 = r'/\* ==================== 5 CÔNG ĐOẠN: KHUNG ĐỎ NHẠT.*?(?:@media\s*\(max-width:\s*600px\)\s*\{[^}]*\}\s*\})'
            content = re.sub(regex_p1, '', content, flags=re.DOTALL)

        # Append PERFECT_STAGES_CSS at the end
        content = content.rstrip() + "\n\n" + PERFECT_STAGES_CSS + "\n"
        with open(cpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned and updated: {cpath}")

def update_html_hint():
    html_files = [
        os.path.join(BASE_DIR, 'index.html'),
        os.path.join(BASE_DIR, 'trang_html_goc/01_trang_chu.html'),
        os.path.join(BASE_DIR, 'kham-pha/index.html') if os.path.exists(os.path.join(BASE_DIR, 'kham-pha/index.html')) else None
    ]
    hint_html = '<div class="coreIntroduction_scrollHint" aria-hidden="true"><span>← Vuốt ngang để xem 5 chặng →</span></div>'

    for hpath in html_files:
        if not hpath or not os.path.exists(hpath):
            continue
        with open(hpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if hint already there
        if 'coreIntroduction_scrollHint' not in content:
            target = '</ol><div class="coreIntroduction_processMoreWrap">'
            replacement = f'</ol>{hint_html}<div class="coreIntroduction_processMoreWrap">'
            if target in content:
                content = content.replace(target, replacement)
                with open(hpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added scroll hint to: {hpath}")
            else:
                sec_idx = content.find('id="5-cong-doan"')
                if sec_idx != -1:
                    ol_end = content.find('</ol>', sec_idx)
                    if ol_end != -1:
                        content = content[:ol_end+5] + hint_html + content[ol_end+5:]
                        with open(hpath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Added scroll hint (alt) to: {hpath}")

if __name__ == '__main__':
    clean_and_update_css_files()
    update_html_hint()
    print("Done applying clean responsive 5 stages fix!")
