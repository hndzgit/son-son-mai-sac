#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch script to bring 'XƯỞNG SƠN MÀI SẮC' 3D studio widget into /kham-pha
under 'THAO TÁC TRỰC TIẾP · MÔ PHỎNG TƯƠNG TÁC' and unlock all features.
"""

import sys
import subprocess

def patch_840(filepath):
    print(f"Patching {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update function D signature and state initialization
    old_head = (
        'function D(){var e,t;'
        'let[n,i]=(0,r.useState)(0),'
        '[l,u]=(0,r.useState)(0),'
        '[p,m]=(0,r.useState)(""),'
        '[v,f]=(0,r.useState)(""),'
        '[x,b]=(0,r.useState)(!1),'
        '[_,y]=(0,r.useState)(!1),'
        '[j,C]=(0,r.useState)({...H,motif:"Th\\xeam",engraving:!1,ornament:"Kh\\xf4ng viền"}),'
        '[k,N]=(0,r.useState)({}),'
        '[E,P]=(0,r.useState)(!1),'
        '[L,F]=(0,r.useState)({}),'
        '[V,I]=(0,r.useState)("top"),'
        '[R,B]=(0,r.useState)(""),'
        '[A,z]=(0,r.useState)("orbit"),'
        '[q,O]=(0,r.useState)(48),'
        '[D,W]=(0,r.useState)(50),'
        '[X,U]=(0,r.useState)(0),'
        '[Z,J]=(0,r.useState)(0),'
        '[Q,Y]=(0,r.useState)(!1),'
        '[$,ee]=(0,r.useState)([!1,!1]),'
        '[et,en]=(0,r.useState)(0),'
        '[ea,er]=(0,r.useState)(0),'
        '[ei,eo]=(0,r.useState)("Mờ"),'
        '[el,ec]=(0,r.useState)([!1,!1,!1,!1]),'
        'es=(0,r.useRef)(null),'
    )

    new_head = (
        'function D(p_props){var e,t;'
        'let p_init=(p_props&&typeof p_props.stage==="number")?p_props.stage:0;'
        'let[n,i]=(0,r.useState)(p_init),'
        '[l,u]=(0,r.useState)(4),'
        '[p,m]=(0,r.useState)("Mặt hộp"),'
        '[v,f]=(0,r.useState)("Gỗ"),'
        '[x,b]=(0,r.useState)(!0),'
        '[_,y]=(0,r.useState)(!0),'
        '[j,C]=(0,r.useState)({...H,shape:"Mặt hộp",motif:"Th\\xeam",engraving:!1,ornament:"Kh\\xf4ng viền"}),'
        '[k,N]=(0,r.useState)({}),'
        '[E,P]=(0,r.useState)(!1),'
        '[L,F]=(0,r.useState)({}),'
        '[V,I]=(0,r.useState)("top"),'
        '[R,B]=(0,r.useState)(""),'
        '[A,z]=(0,r.useState)("orbit"),'
        '[q,O]=(0,r.useState)(48),'
        '[D,W]=(0,r.useState)(50),'
        '[X,U]=(0,r.useState)(0),'
        '[Z,J]=(0,r.useState)(1),'
        '[Q,Y]=(0,r.useState)(!0),'
        '[$,ee]=(0,r.useState)([!0,!0]),'
        '[et,en]=(0,r.useState)(1),'
        '[ea,er]=(0,r.useState)(0),'
        '[ei,eo]=(0,r.useState)("Mờ"),'
        '[el,ec]=(0,r.useState)([!0,!0,!0,!0]),'
        'es=(0,r.useRef)(null);'
        '(0,r.useEffect)(()=>{if(p_props&&typeof p_props.stage==="number"&&p_props.stage!==n){i(p_props.stage);z("orbit")}},[p_props&&p_props.stage]);'
        '(0,r.useEffect)(()=>{if(p_props&&p_props.onStageChange){p_props.onStageChange(n)}},[n]);'
        'let '
    )

    if old_head not in content:
        raise ValueError("Could not find old_head in 840 file")
    content = content.replace(old_head, new_head, 1)

    # 2. Unlock aside buttons
    old_aside = 'disabled:l<t,onClick:()=>{i(t),z("orbit")}'
    new_aside = 'onClick:()=>{i(t),z("orbit")}'
    if old_aside not in content:
        raise ValueError("Could not find old_aside in 840 file")
    content = content.replace(old_aside, new_aside, 1)

    # 3. Unlock Stage 1 vocTasks buttons & advance button
    old_voc_task = 'disabled:t>0&&!el[t-1]'
    new_voc_task = 'disabled:!1'
    if old_voc_task not in content:
        raise ValueError("Could not find old_voc_task in 840 file")
    content = content.replace(old_voc_task, new_voc_task, 1)

    old_stage1_adv = ',disabled:!el.every(Boolean)'
    if old_stage1_adv not in content:
        raise ValueError("Could not find old_stage1_adv in 840 file")
    content = content.replace(old_stage1_adv, '', 1)

    # 4. Stage 2 render condition: remove '&&x'
    old_stage2_cond = '2===n&&x&&'
    new_stage2_cond = '2===n&&'
    if old_stage2_cond not in content:
        raise ValueError("Could not find old_stage2_cond in 840 file")
    content = content.replace(old_stage2_cond, new_stage2_cond, 1)

    # 5. Unlock Stage 2 vocTasks buttons & advance button
    old_ground_task = 'disabled:t>0&&!$[t-1]'
    new_ground_task = 'disabled:!1'
    if old_ground_task not in content:
        raise ValueError("Could not find old_ground_task in 840 file")
    content = content.replace(old_ground_task, new_ground_task, 1)

    old_stage2_adv = ',disabled:!$.every(Boolean)'
    if old_stage2_adv not in content:
        raise ValueError("Could not find old_stage2_adv in 840 file")
    content = content.replace(old_stage2_adv, '', 1)

    # 6. Stage 3 render condition: remove '&&x&&_'
    old_stage3_cond = '3===n&&x&&_&&'
    new_stage3_cond = '3===n&&'
    if old_stage3_cond not in content:
        raise ValueError("Could not find old_stage3_cond in 840 file")
    content = content.replace(old_stage3_cond, new_stage3_cond, 1)

    # 7. Stage 4 buttons: unlock "Ủ khô", "Mài nước", "Đánh bóng"
    old_stage4_buttons = (
        '(0,a.jsxs)("button",{type:"button",disabled:!Z||Q,"aria-pressed":Q,'
        'onClick:()=>{Y(!0),z("orbit"),B("Lớp phủ đã được ủ khô trong mô phỏng. Bây giờ có thể mài nước.")},'
        'children:["Ủ khô ",(0,a.jsx)("small",{children:Q?"Đã ủ khô":"Ủ lớp phủ trước khi mài"})]}),'
        '(0,a.jsxs)("button",{type:"button",disabled:!Z||!Q,'
        'onClick:()=>{z("sand"),O(e=>Math.max(8,e-5)),U(e=>e+1),B("Đang d\\xf9ng m\\xe0i nước. K\\xe9o tr\\xean v\\xf9ng đ\\xe3 phủ để m\\xe0i lớp mặt.")},'
        'children:["M\\xe0i nước ",(0,a.jsxs)("small",{children:[et," lượt m\\xe0i ho\\xe0n tất"]})]}),'
        '(0,a.jsxs)("button",{type:"button",disabled:!Z||!Q||!et,'
        'onClick:()=>{eo("B\\xf3ng"),z("orbit"),B("Đ\\xe3 đ\\xe1nh b\\xf3ng lớp phủ đ\\xe3 qu\\xe9t; \\xe1nh phản xạ được l\\xe0m mịn.")},'
        'children:["Đ\\xe1nh b\\xf3ng ",(0,a.jsx)("small",{children:"B\\xf3ng"===ei?"Đ\\xe3 đ\\xe1nh b\\xf3ng":"Cần phủ v\\xe0 m\\xe0i thực tế trước"})]})'
    )

    new_stage4_buttons = (
        '(0,a.jsxs)("button",{type:"button","aria-pressed":Q,'
        'onClick:()=>{if(!Z)J(1);Y(!0),z("orbit"),B("Lớp phủ đã được ủ khô trong mô phỏng. Bây giờ có thể mài nước.")},'
        'children:["Ủ khô ",(0,a.jsx)("small",{children:Q?"Đã ủ khô":"Sẵn sàng ủ khô"})]}),'
        '(0,a.jsxs)("button",{type:"button",'
        'onClick:()=>{var e;if(!Z){null===(e=es.current)||void 0===e||e.applyCoat(),J(1),Y(!0)}else if(!Q){Y(!0)}'
        'z("sand"),O(e=>Math.max(8,e-5)),U(e=>e+1),en(e=>e+1),'
        'null===(e=es.current)||void 0===e||e.sand&&e.sand(),'
        'B("Đang dùng mài nước. Kéo trên vùng đã phủ để mài phẳng và lộ lớp màu.")},'
        'children:["Mài nước ",(0,a.jsxs)("small",{children:[et," lượt mài hoàn tất"]})]}),'
        '(0,a.jsxs)("button",{type:"button",'
        'onClick:()=>{eo("Bóng"),z("orbit"),B("Đã đánh bóng bề mặt; ánh phản xạ được làm mịn và sáng gương.")},'
        'children:["Đánh bóng ",(0,a.jsx)("small",{children:"Bóng"===ei?"Đã đánh bóng":"Làm mịn & sáng bóng bề mặt"})]})'
    )

    if old_stage4_buttons not in content:
        raise ValueError("Could not find old_stage4_buttons in 840 file")
    content = content.replace(old_stage4_buttons, new_stage4_buttons, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully patched {filepath}")

def patch_kham_pha(filepath):
    print(f"Patching {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add chunk 840 to Webpack loader footer
    old_loader = 'e.O(0,[824,498,649,945,744],'
    new_loader = 'e.O(0,[840,824,498,649,945,744],'
    if old_loader not in content:
        raise ValueError("Could not find old_loader in kham-pha page bundle")
    content = content.replace(old_loader, new_loader, 1)

    # 2. Add import for module 5840 in module 3562
    old_import = 'var s=n(3890),l=n(6788),o=n(8496),a=n(8491),i=n(7917),c=n.n(i);'
    new_import = 'var s=n(3890),l=n(6788),o=n(8496),a=n(8491),i=n(7917),c=n.n(i),u_studio=n(5840);'
    if old_import not in content:
        raise ValueError("Could not find old_import in kham-pha page bundle")
    content = content.replace(old_import, new_import, 1)

    # 3. Replace (0,s.jsx)(v,{stage:e}) in function w()
    old_v_render = '(0,s.jsx)(v,{stage:e})'
    new_studio_render = (
        '(0,s.jsxs)("section",{'
        'className:c().workshop,'
        '"aria-labelledby":"process-workshop-title",'
        'children:['
        '(0,s.jsx)("div",{'
        'className:c().entry,'
        'children:(0,s.jsxs)("div",{'
        'children:['
        '(0,s.jsx)("p",{className:c().kicker,children:"THAO T\\xc1C TRỰC TIẾP \\xb7 M\\xd4 PHỎNG TƯƠNG T\\xc1C"}),'
        '(0,s.jsxs)("h3",{id:"process-workshop-title",children:["Thực h\\xe0nh: ",m[e]]})'
        ']'
        '})'
        '}),'
        '(0,s.jsx)("div",{'
        'className:c().panel,'
        'id:"process-workshop-panel",'
        'style:{padding:0,border:"none",background:"transparent"},'
        'children:(0,s.jsx)(u_studio.Zp,{stage:e,onStageChange:t})'
        '})'
        ']'
        '})'
    )
    if old_v_render not in content:
        raise ValueError("Could not find old_v_render in kham-pha page bundle")
    content = content.replace(old_v_render, new_studio_render, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully patched {filepath}")

if __name__ == '__main__':
    # Patch chunk 840 files
    patch_840('_next/static/chunks/840-f19fdd306966b2e5.js')
    patch_840('ma_nguon_css_js/js/840-f19fdd306966b2e5.js')

    # Patch kham-pha page bundles
    patch_kham_pha('_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js')
    patch_kham_pha('ma_nguon_css_js/js/app_kham-pha_page-b0c7a974225638c7.js')

    print("Checking JS syntax with node -c...")
    subprocess.run(['node', '-c', '_next/static/chunks/840-f19fdd306966b2e5.js'], check=True)
    subprocess.run(['node', '-c', '_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js'], check=True)
    print("All patches applied and JS syntax verified successfully!")
