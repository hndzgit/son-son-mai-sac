# -*- coding: utf-8 -*-
"""
Apply updates for:
1. "đổi back trắng thành nền vàng đấy luôn để mỗi cái box đỏ đấy":
   - Remove white backgrounds from choice buttons, task tiles, and panels in simulator/workshop.
   - Use site golden paper surface so the only standout colored box is the red board (.productExperience_studioBoard__D_pEz).
2. "với bê backend này ra ngoài chỗ Thực hành: Chuẩn bị cốt ấy":
   - Apply the golden paper background to the outer wrapper of "Thực hành: Chuẩn bị cốt" (.processWorkshop_workshop__zFp89).
3. "với đổi ô nào đen chuyển sang đỏ nha":
   - Change dark/black elements (.productExperience_boardContext__7W1Go from #460f12 to red #842022, .processWorkshop_viewerFallback__0Crl6 from #17100d to #842022, etc.).
4. "và bỏ 2 ô này thay lại 1 ô là phủ lớp sơn trong ở bước 5 ấy cho tôi":
   - Replace the two buttons ("Phủ lớp sơn trong" + "Ủ khô") in Step 5 with a single button "Phủ lớp sơn trong".
"""

import os

# --- 1. UPDATE JS CHUNKS ---
js_files = [
    '_next/static/chunks/840-f19fdd306966b2e5.js',
    'ma_nguon_css_js/js/840-f19fdd306966b2e5.js'
]

# Old pattern: Two buttons (Phủ lớp sơn trong + Ủ khô)
# We search for the button with applyCoat followed by the button with Y(!0) (Ủ khô)
for js_path in js_files:
    if not os.path.exists(js_path):
        continue
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the target segment in finishActions
    target_start = 'finishActions,children:[(0,a.jsxs)("button",{type:"button",onClick:()=>{var e;z("coat"),null===(e=es.current)||void 0===e||e.applyCoat(),'
    target_end = '(0,a.jsxs)("button",{type:"button",disabled:!Z||!Q,onClick:()=>{z("sand"),'

    idx1 = content.find(target_start)
    if idx1 != -1:
        idx2 = content.find(target_end, idx1)
        if idx2 != -1:
            old_chunk = content[idx1:idx2]
            print(f"Found target chunk in {js_path}, length: {len(old_chunk)}")
            
            # New single button that applies coat AND sets Y(!0)
            new_chunk = (
                'finishActions,children:[(0,a.jsxs)("button",{'
                'type:"button",'
                'onClick:()=>{var e;z("coat"),null===(e=es.current)||void 0===e||e.applyCoat(),Y(!0),B("Đã phủ lớp sơn trong suốt trên bề mặt; sẵn sàng mài nước.")},'
                'children:["Phủ lớp sơn trong ",(0,a.jsx)("small",{children:"Phủ lớp sơn trong suốt để bảo vệ và chuẩn bị mài nước"})]'
                '}),'
            )
            content = content[:idx1] + new_chunk + content[idx2:]
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully updated step 5 buttons in {js_path}")
        else:
            print(f"Could not find target_end in {js_path}")
    else:
        print(f"Could not find target_start in {js_path}")


# --- 2. UPDATE CSS STYLES ---
css_files = [
    '_next/static/css/58e70d5489b56972.css',
    '_next/static/css/3d939b8161363d36.css',
    '_next/static/css/7d5ed180c1fe36fd.css',
    'ma_nguon_css_js/css/58e70d5489b56972.css',
    'ma_nguon_css_js/css/3d939b8161363d36.css',
    'ma_nguon_css_js/css/7d5ed180c1fe36fd.css'
]

css_patch = """
/* ================================================================
   WORKSHOP & SIMULATOR UNIFIED GOLD PAPER THEME & RED LACQUER HIGHLIGHTS
   ================================================================ */

/* 1. Remove all white backgrounds and extend golden paper to 'Thực hành: Chuẩn bị cốt' */
.processWorkshop_workshop__zFp89 {
  background: var(--site-paper-surface) center / 900px 900px repeat !important;
  border-top: 1px solid rgba(139, 42, 42, 0.25) !important;
  border-bottom: 1px solid rgba(139, 42, 42, 0.25) !important;
}

.processWorkshop_entry__6_wCN,
.processWorkshop_panel__zVipm,
.productExperience_page__WKDXT,
.productExperience_studio__EDGqN,
.productExperience_coreStudio__V7jJJ,
.productExperience_studioWorkspace__is27_,
.productExperience_galleryPanel__LqR_e,
.productExperience_galleryView__p7LNe,
.productExperience_viewer__V3Heb,
.productExperience_galleryControls__WppUe {
  background: transparent !important;
}

/* 2. Change all white choice/task buttons into golden paper tiles, leaving only red box prominent */
.productExperience_studioChoices__jssx6 button,
.productExperience_materialChoices__hbtcl button,
.productExperience_colorChoices__sVGIt button,
.productExperience_faceChoices__y_olI button,
.productExperience_motifChoices__WNJtl button,
.productExperience_vocTasks__wd_6j button {
  background: rgba(254, 248, 233, 0.55) !important;
  border: 1px solid rgba(155, 116, 72, 0.45) !important;
  color: #432b20 !important;
  transition: all 0.2s ease !important;
}

.productExperience_studioChoices__jssx6 button:hover,
.productExperience_materialChoices__hbtcl button:hover,
.productExperience_colorChoices__sVGIt button:hover,
.productExperience_faceChoices__y_olI button:hover,
.productExperience_motifChoices__WNJtl button:hover,
.productExperience_vocTasks__wd_6j button:hover:not(:disabled) {
  background: rgba(254, 248, 233, 0.85) !important;
  border-color: #842022 !important;
  color: #842022 !important;
}

/* Active / pressed state */
.productExperience_studioChoices__jssx6 button[aria-pressed=true],
.productExperience_materialChoices__hbtcl button[aria-pressed=true],
.productExperience_colorChoices__sVGIt button[aria-pressed=true],
.productExperience_faceChoices__y_olI button[aria-pressed=true],
.productExperience_motifChoices__WNJtl button[aria-pressed=true],
.productExperience_vocTasks__wd_6j button[aria-pressed=true] {
  background: #842022 !important;
  border-color: #842022 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(132, 32, 34, 0.25) !important;
}

.productExperience_studioChoices__jssx6 button[aria-pressed=true] small,
.productExperience_vocTasks__wd_6j button[aria-pressed=true] small,
.productExperience_vocTasks__wd_6j button[aria-pressed=true] strong,
.productExperience_vocTasks__wd_6j button[aria-pressed=true] i {
  color: #fff4e2 !important;
}

/* 3. Turn any black/dark elements to red */
.productExperience_boardContext__7W1Go {
  background: #842022 !important;
  border: 1px solid rgba(240, 203, 123, 0.45) !important;
  border-radius: 6px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15) !important;
}
.productExperience_boardContext__7W1Go > span {
  color: #fce7b8 !important;
  letter-spacing: 0.12em !important;
}
.productExperience_boardContext__7W1Go h2 {
  color: #ffffff !important;
}
.productExperience_boardContext__7W1Go p {
  color: #fff1dc !important;
}

.processWorkshop_viewerFallback__0Crl6,
.processWorkshop_surface__hlVC7 .processWorkshop_viewerFallback__0Crl6 {
  background: #842022 !important;
  color: #fff1dc !important;
}

/* 4. Step 5 single action button "Phủ lớp sơn trong" styled red lacquer */
.productExperience_finishActions___wK4h button {
  background: rgba(254, 248, 233, 0.6) !important;
  border: 1px solid rgba(155, 116, 72, 0.5) !important;
  color: #432b20 !important;
}

.productExperience_finishActions___wK4h button:first-child {
  background: #842022 !important;
  border: 1px solid #842022 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(132, 32, 34, 0.25) !important;
}

.productExperience_finishActions___wK4h button:first-child small {
  color: #faeedb !important;
}

.productExperience_finishActions___wK4h button:first-child:hover {
  background: #9d2629 !important;
  border-color: #9d2629 !important;
}
"""

for css_p in css_files:
    if not os.path.exists(css_p):
        continue
    with open(css_p, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove previous patch if present
    marker = "WORKSHOP & SIMULATOR UNIFIED GOLD PAPER THEME"
    if marker in content:
        idx = content.find("/* ================================================================\n   " + marker)
        if idx != -1:
            content = content[:idx]

    # Append new patch
    content += "\n" + css_patch + "\n"
    with open(css_p, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully applied CSS patch to {css_p}")
