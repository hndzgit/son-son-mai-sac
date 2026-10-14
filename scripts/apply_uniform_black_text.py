# -*- coding: utf-8 -*-
"""
Script xử lý:
1. Đồng bộ màu chữ đen 100% cho 2 đoạn văn dưới mục "NHỮNG ĐẶC TRƯNG LÀM NÊN SƠN MÀI"
   (loại bỏ tình trạng 1 đoạn đen đậm, 1 đoạn đen nhạt xám nâu #524432).
2. Chuẩn hóa 5 box công đoạn:
   - Xóa bỏ hoàn toàn gạch nối ::after bên cạnh số 01, 02..
   - Căn giữa 100% tiêu đề to (align-self: center, width: 100%) ngay sát dưới số.
   - Làm nổi bật màu đỏ nhạt nhạt (đỏ son mờ sang trọng) của khung box.
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

CUSTOM_FIX_CSS = """
/* ==================== FIX ĐỒNG BỘ CHỮ ĐEN VÀ CĂN GIỮA 5 CÔNG ĐOẠN ==================== */

/* 1. ĐỒNG BỘ MÀU CHỮ ĐEN TUYỆT ĐỐI CHO 2 ĐOẠN "NHỮNG ĐẶC TRƯNG LÀM NÊN SƠN MÀI" */
.coreIntroduction_layersLead__acYPE p,
.coreIntroduction_layersLead__acYPE > p,
.coreIntroduction_layersLead__acYPE > p:first-of-type,
.coreIntroduction_layersLead__acYPE > p:last-child {
  color: #201811 !important;
  font-size: 15px !important;
  line-height: 1.68 !important;
  font-weight: 400 !important;
  opacity: 1 !important;
  max-width: 440px !important;
  -webkit-font-smoothing: antialiased !important;
  margin: 0 !important;
}

.coreIntroduction_layersLead__acYPE > p:first-of-type {
  margin-bottom: 12px !important;
}

.coreIntroduction_layersLead__acYPE > p:last-child {
  margin-top: 0 !important;
  margin-bottom: 0 !important;
}

/* 2. CHUẨN HÓA 5 CÔNG ĐOẠN: KHUNG ĐỎ NHẠT, SỐ VÀ TIÊU ĐỀ TO CĂN GIỮA HOÀN TOÀN */
.coreIntroduction_stageList__aTih3 {
  display: grid !important;
  grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
  gap: 16px !important;
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

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

/* Số 01, 02... CĂN GIỮA, KHÔNG GẠCH NỐI */
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

/* Ảnh minh họa trong khung */
.coreIntroduction_stagePhoto__e5sjm {
  display: block !important;
  width: 100% !important;
  height: clamp(140px, 11vw, 175px) !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid rgba(160, 42, 42, 0.24) !important;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.12) !important;
  cursor: pointer !important;
  transition: transform 0.25s ease !important;
  aspect-ratio: auto !important;
  align-self: center !important;
}

.coreIntroduction_stageItem__C7_GF:hover .coreIntroduction_stagePhoto__e5sjm {
  transform: scale(1.025) !important;
}

/* Ẩn link Tìm hiểu thêm rải rác từng ô */
.coreIntroduction_stageItem__C7_GF .coreIntroduction_stageMore__uOSUQ {
  display: none !important;
}
"""

def append_to_css(rel_path):
    fpath = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Xóa khối cũ nếu có
        if "/* ==================== FIX ĐỒNG BỘ CHỮ ĐEN VÀ CĂN GIỮA 5 CÔNG ĐOẠN ==================== */" in content:
            idx = content.find("/* ==================== FIX ĐỒNG BỘ CHỮ ĐEN VÀ CĂN GIỮA 5 CÔNG ĐOẠN ==================== */")
            content = content[:idx]
        content = content.rstrip() + "\n\n" + CUSTOM_FIX_CSS + "\n"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {rel_path} ({len(content)} bytes)")

css_files = [
    '_next/static/css/58e70d5489b56972.css',
    '_next/static/css/3d939b8161363d36.css',
    'ma_nguon_css_js/css/58e70d5489b56972.css',
    'ma_nguon_css_js/css/3d939b8161363d36.css'
]

for cf in css_files:
    append_to_css(cf)

# Cập nhật cachebuster trên HTML files
html_files = ['index.html', 'trai-nghiem/index.html']
import re

for hf in html_files:
    fpath = os.path.join(BASE_DIR, hf)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()
        # bump version
        html = re.sub(r'58e70d5489b56972\.css(\?v=\d+)?', '58e70d5489b56972.css?v=15', html)
        html = re.sub(r'3d939b8161363d36\.css(\?v=\d+)?', '3d939b8161363d36.css?v=15', html)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Bumped cachebuster in {hf}")

print("DONE!")
