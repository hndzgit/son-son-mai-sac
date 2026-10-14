# -*- coding: utf-8 -*-
"""
Script đóng khung box và căn chỉnh tiêu đề ngang bằng nhau cho phần TẦM NHÌN & SỨ MỆNH:
- Đưa cả 2 cột vào 1 box sang trọng với nền giấy sơn mài sáng, viền vàng #c6a663, bo góc 16px, đổ bóng nhẹ
- Tiêu đề TẦM NHÌN và SỨ MỆNH đồng bộ cùng font-size, line-height, độ cao min-height 65px (chuẩn 2 dòng ngang bằng nhau)
- Các đoạn văn bên dưới bắt đầu ở cùng 1 đường chân ngang chuẩn xác
- Vạch ngăn cách dọc tinh tế ở giữa trên Desktop, chuyển thành ngăn cách ngang trên Mobile
- Cập nhật cachebuster CSS v=23 cho ve-du-an/index.html và trang_html_goc/08_ve_du_an.html
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

MISSION_BOX_CSS = """
/* ==================== VỀ DỰ ÁN: BOX TẦM NHÌN & SỨ MỆNH CÂN BẰNG TIÊU ĐỀ ==================== */
.project_mission__f2EwM {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: clamp(36px, 5vw, 64px) !important;
  padding: clamp(38px, 4.5vw, 56px) !important;
  border: 1px solid #c6a663 !important;
  border-radius: 16px !important;
  background: linear-gradient(145deg, rgba(255, 248, 235, 0.94), rgba(246, 234, 206, 0.78)) !important;
  box-shadow: 0 12px 32px rgba(76, 43, 20, 0.08) !important;
  max-width: 1220px !important;
  margin: 0 auto clamp(80px, 10vw, 142px) !important;
  box-sizing: border-box !important;
}

.project_mission__f2EwM > div {
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
}

.project_mission__f2EwM > div:first-child {
  border-right: 1px solid rgba(198, 166, 99, 0.45) !important;
  padding-right: clamp(24px, 3.5vw, 44px) !important;
}

.project_mission__f2EwM h2,
.project_mission__f2EwM h3 {
  font-family: "Project Display", "Playfair Display", Georgia, serif !important;
  font-size: clamp(21px, 1.75vw, 24px) !important;
  line-height: 1.35 !important;
  color: #8b2a2a !important;
  margin: 12px 0 20px !important;
  min-height: 65px !important;
  display: flex !important;
  align-items: flex-start !important;
  text-wrap: balance !important;
}

.project_mission__f2EwM > div p {
  line-height: 1.8 !important;
  color: #574937 !important;
  margin: 0 0 16px !important;
}

.project_mission__f2EwM > div p:last-of-type {
  margin-bottom: 0 !important;
}

.project_mission__f2EwM > div:last-child a {
  margin-top: auto !important;
  padding-top: 16px !important;
}

@media (max-width: 820px) {
  .project_mission__f2EwM {
    grid-template-columns: 1fr !important;
    gap: 32px !important;
    padding: 32px 22px !important;
  }
  .project_mission__f2EwM > div:first-child {
    border-right: none !important;
    border-bottom: 1px solid rgba(198, 166, 99, 0.45) !important;
    padding-right: 0 !important;
    padding-bottom: 32px !important;
  }
  .project_mission__f2EwM h2,
  .project_mission__f2EwM h3 {
    min-height: 0 !important;
    font-size: 22px !important;
  }
}
"""

def apply_css(rel_path):
    fpath = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove older version if present
        if "/* ==================== VỀ DỰ ÁN: BOX TẦM NHÌN & SỨ MỆNH CÂN BẰNG TIÊU ĐỀ ==================== */" in content:
            idx = content.find("/* ==================== VỀ DỰ ÁN: BOX TẦM NHÌN & SỨ MỆNH CÂN BẰNG TIÊU ĐỀ ==================== */")
            content = content[:idx]
            
        content = content.rstrip() + "\n\n" + MISSION_BOX_CSS.strip() + "\n"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CSS: {rel_path}")

css_targets = [
    '_next/static/css/f7d6d17d52efcb3d.css',
    'ma_nguon_css_js/css/f7d6d17d52efcb3d.css'
]

for ct in css_targets:
    apply_css(ct)

# Update cachebuster in HTML
html_targets = [
    've-du-an/index.html',
    'trang_html_goc/08_ve_du_an.html'
]

for ht in html_targets:
    fpath = os.path.join(BASE_DIR, ht)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'f7d6d17d52efcb3d.css?v=' in content:
            content = re.sub(r'f7d6d17d52efcb3d\.css\?v=\d+', 'f7d6d17d52efcb3d.css?v=23', content)
        else:
            content = re.sub(r'f7d6d17d52efcb3d\.css', 'f7d6d17d52efcb3d.css?v=23', content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML cachebuster (v=23): {ht}")

print("DONE APPLYING MISSION BOX AND BALANCED TITLES!")
