#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply accurate craft sequence for lacquer Stage 5:
"sau khi mài nước xong đến công đoạn đến phủ lớp sơn trong xong đến ủ khô xong rồi mới đánh bóng hoàn thiện"
Sequence:
1. Phủ lớp sơn đen (sơn then) & Ủ khô
2. Mài nước (làm lộ hoa văn)
3. Phủ lớp sơn trong & Ủ khô
4. Đánh bóng hoàn thiện
"""

import os
import subprocess
import re

FILES_840 = [
    "_next/static/chunks/840-f19fdd306966b2e5.js",
    "ma_nguon_css_js/js/840-f19fdd306966b2e5.js"
]

FILES_KHAM_PHA = [
    "_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js",
    "ma_nguon_css_js/js/app_kham-pha_page-b0c7a974225638c7.js"
]

def patch_840(filepath):
    print(f"\n--- Patching {filepath} ---")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found!")
        return False
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add state for u_clear_coat and u_clear_dry
    old_state = r'[u_reinf,set_reinf]=(0,r.useState)(!1),es=(0,r.useRef)(null);'
    new_state = r'[u_reinf,set_reinf]=(0,r.useState)(!1),[u_clear_coat,set_clear_coat]=(0,r.useState)(!1),[u_clear_dry,set_clear_dry]=(0,r.useState)(!1),es=(0,r.useRef)(null);'
    if old_state in content:
        content = content.replace(old_state, new_state, 1)
        print("Patched state: added u_clear_coat and u_clear_dry")
    else:
        print("Note: old_state not matched or already patched")

    # 2. Reset states in eh() and creation reset
    old_eh = r'eh=()=>{var e;null===(e=es.current)||void 0===e||e.clearCoat(),J(0),Y(!1),en(0),eo("Mờ"),z("orbit")}'
    new_eh = r'eh=()=>{var e;null===(e=es.current)||void 0===e||e.clearCoat(),J(0),Y(!1),en(0),eo("Mờ"),set_clear_coat(!1),set_clear_dry(!1),z("orbit")}'
    if old_eh in content:
        content = content.replace(old_eh, new_eh, 1)
        print("Patched eh() reset helper")

    # 3. Replace Section 3 (polish) with Section 3 (phủ lớp sơn trong & ủ khô) and Section 4 (đánh bóng hoàn thiện)
    old_polish_sec = r'(0,a.jsx)("span",{className:g().choiceLabel,style:{display:"block",margin:"14px 0 8px 0"},children:"3. Đ\xc1NH B\xd3NG & HO\xc0N THIỆN"}),(0,a.jsxs)("div",{className:g().finishActions,children:[(0,a.jsxs)("button",{type:"button",className:"studio_polish_btn",onClick:()=>{eo("Bóng"),z("orbit"),B("Đ\xe3 phủ lớp sơn trong v\xe0 đ\xe1nh b\xf3ng ho\xe0n thiện; \xe1nh phản xạ s\xe1ng b\xf3ng như gương.")},children:[(0,a.jsxs)("strong",{style:{display:"inline-flex",alignItems:"center",gap:"6px"},children:[(0,a.jsx)(w_sparkles,{size:14,style:{color:"#deb85a"}}),"Đ\xe1nh b\xf3ng"]}),(0,a.jsx)("small",{children:"Bóng"===ei?"Đ\xe3 phủ sơn trong & đ\xe1nh b\xf3ng s\xe1ng gương":"Lớp phủ trong (sơn c\xe1nh gi\xe1n) & đ\xe1nh b\xf3ng s\xe1ng gương"})]})]})'
    
    new_polish_sec = (
        r'(0,a.jsx)("span",{className:g().choiceLabel,style:{display:"block",margin:"14px 0 8px 0",color:"#842022",fontWeight:"800"},children:"3. PHỦ LỚP SƠN TRONG & Ủ KHÔ"}),'
        r'(0,a.jsxs)("div",{className:g().finishActions,children:['
        r'(0,a.jsxs)("button",{type:"button",className:"studio_coat_btn",onClick:()=>{var e;z("coat");null===(e=es.current)||void 0===e||e.applyCoat();set_clear_coat(!0);set_clear_dry(!1);B("Đ\xe3 phủ lớp sơn trong suốt (sơn c\xe1nh gi\xe1n/sơn quang) l\xean bề mặt; sẵn s\xe0ng đưa v\xe0o buồng ủ kh\xf4.")},children:[(0,a.jsx)("strong",{children:"Phủ lớp sơn trong"}),(0,a.jsx)("small",{children:u_clear_coat?"Đ\xe3 phủ lớp sơn trong (sơn c\xe1nh gi\xe1n)":"Phủ lớp sơn trong bảo vệ & tạo độ trong"})]}),'
        r'(0,a.jsxs)("button",{type:"button",className:"studio_dry_btn","aria-pressed":u_clear_dry,onClick:()=>{if(!u_clear_coat)set_clear_coat(!0);set_clear_dry(!0);z("orbit");B("Lớp sơn trong đ\xe3 được ủ kh\xf4 ho\xe0n to\xe0n trong buồng ẩm ti\xeau chuẩn. B\xe2y giờ sẵn s\xe0ng đ\xe1nh b\xf3ng ho\xe0n thiện.")},children:[(0,a.jsx)("strong",{children:"Ủ kh\xf4"}),(0,a.jsx)("small",{children:u_clear_dry?"Đ\xe3 ủ kh\xf4 · sẵn s\xe0ng đ\xe1nh b\xf3ng ho\xe0n thiện":"Ủ trong buồng ẩm đạt độ kh\xf4 ti\xeau chuẩn"})]})'
        r']}),'
        r'(0,a.jsx)("span",{className:g().choiceLabel,style:{display:"block",margin:"16px 0 8px 0",color:"#842022",fontWeight:"800"},children:"4. ĐÁNH BÓNG HOÀN THIỆN"}),'
        r'(0,a.jsxs)("div",{className:g().finishActions,children:['
        r'(0,a.jsxs)("button",{type:"button",className:"studio_polish_btn",onClick:()=>{set_clear_coat(!0);set_clear_dry(!0);eo("Bóng");z("orbit");B("Đ\xe3 ho\xe0n tất đ\xe1nh b\xf3ng ho\xe0n thiện! Bề mặt phẳng mịn, \xe1nh quang v\xe0 độ trong s\xe1ng b\xf3ng như gương.")},children:[(0,a.jsxs)("strong",{style:{display:"inline-flex",alignItems:"center",gap:"6px"},children:[(0,a.jsx)(w_sparkles,{size:14,style:{color:"#deb85a"}}),"Đ\xe1nh b\xf3ng ho\xe0n thiện"]}),(0,a.jsx)("small",{children:"Bóng"===ei?"Đ\xe3 đ\xe1nh b\xf3ng ho\xe0n thiện s\xe1ng gương":"Đ\xe1nh b\xf3ng bằng bột than mịn & l\xf2ng b\xe0n tay"})]})'
        r']})'
    )

    if old_polish_sec in content:
        content = content.replace(old_polish_sec, new_polish_sec, 1)
        print("Patched Stage 4 actions: split into Step 3 (Phủ lớp sơn trong & Ủ khô) + Step 4 (Đánh bóng hoàn thiện)")
    else:
        print("Warning: old_polish_sec not found!")

    # 4. Guide text above Step 1
    old_guide = r'"C\xf4ng đoạn phủ sơn trong (sơn c\xe1nh gi\xe1n/sơn quang) v\xe0 m\xe0i nước l\xe0 linh hồn của nghệ thuật sơn m\xe0i. C\xe0ng m\xe0i nước đều tay, từng lớp m\xe0u, vỏ trứng v\xe0 v\xe0ng quỳ c\xe0ng \xe1nh l\xean chiều s\xe2u huyền ảo."'
    new_guide = r'"Quy tr\xecnh m\xe0i nước v\xe0 ho\xe0n thiện: Sau khi m\xe0i nước l\xe0m lộ r\xf5 từng lớp họa tiết v\xe0 sắc nền, người thợ tiến h\xe0nh phủ lớp sơn trong, đem ủ kh\xf4 trong buồng ẩm đạt độ ti\xeau chuẩn, xong rồi mới tiến h\xe0nh đ\xe1nh b\xf3ng ho\xe0n thiện để tạo độ b\xf3ng gương v\xe0 chiều s\xe2u huyền ảo."'
    if old_guide in content:
        content = content.replace(old_guide, new_guide, 1)
        print("Patched guide text")

    # 5. Mài nước finish message
    old_msg = r'"Nước m\xe0i ho\xe0n thiện ("+nextQ+"%): Lớp sơn đen đ\xe3 được m\xe0i lộ đều, họa tiết hiện r\xf5 sắc n\xe9t, sẵn s\xe0ng đ\xe1nh b\xf3ng."'
    new_msg = r'"Nước m\xe0i ho\xe0n thiện ("+nextQ+"%): Lớp sơn đen đ\xe3 m\xe0i lộ r\xf5 họa tiết, sẵn s\xe0ng bước sang phủ lớp sơn trong v\xe0 ủ kh\xf4."'
    if old_msg in content:
        content = content.replace(old_msg, new_msg, 1)
        print("Patched mài nước finish message")

    # 6. Mài nước status badge
    old_badge = r'["M\xe0i lộ ho\xe0n tất (",q,"%) \xb7 T\xe1c phẩm lộ r\xf5 tr\xean nền sơn m\xe0i"]'
    new_badge = r'["M\xe0i lộ ho\xe0n tất (",q,"%) \xb7 Sẵn s\xe0ng phủ sơn trong & ủ kh\xf4"]'
    if old_badge in content:
        content = content.replace(old_badge, new_badge, 1)
        print("Patched mài nước status badge")

    # 7. eb[4] and e_[4]
    old_eb4 = r'["Phủ sơn & M\xe0i nước","Phủ lớp sơn đen (sơn then), ủ kh\xf4, m\xe0i nước l\xe0m lộ họa tiết v\xe0 đ\xe1nh b\xf3ng ho\xe0n thiện."]'
    new_eb4 = r'["Phủ, m\xe0i v\xe0 ho\xe0n thiện","M\xe0i nước l\xe0m lộ họa tiết, sau đ\xf3 phủ lớp sơn trong, ủ kh\xf4 rồi mới đ\xe1nh b\xf3ng ho\xe0n thiện."]'
    if old_eb4 in content:
        content = content.replace(old_eb4, new_eb4, 1)
        print("Patched eb[4]")

    old_e_4 = r'"Phủ lớp sơn đen (sơn then), tiến h\xe0nh m\xe0i nước để l\xe0m lộ họa tiết v\xe0 đ\xe1nh b\xf3ng ho\xe0n thiện."'
    new_e_4 = r'"M\xe0i nước l\xe0m lộ họa tiết; sau khi m\xe0i nước xong tiến h\xe0nh phủ lớp sơn trong, ủ kh\xf4 rồi mới đ\xe1nh b\xf3ng ho\xe0n thiện."'
    if old_e_4 in content:
        content = content.replace(old_e_4, new_e_4, 1)
        print("Patched e_[4]")

    # 8. Aside stage subtitle and title
    old_aside_sub = r'"Phủ lớp, m\xe0i nước, đ\xe1nh b\xf3ng"'
    new_aside_sub = r'"M\xe0i nước, phủ sơn trong, ủ kh\xf4, đ\xe1nh b\xf3ng"'
    if old_aside_sub in content:
        content = content.replace(old_aside_sub, new_aside_sub, 1)
        print("Patched aside stage 5 subtitle")

    old_aside_name = r'["CHUẨN BỊ CỐT","L\xc0M V\xd3C","SƠN NỀN","TẠO H\xccNH V\xc0 TRANG TR\xcd","PHỦ SƠN & M\xc0I NƯỚC"]'
    new_aside_name = r'["CHUẨN BỊ CỐT","L\xc0M V\xd3C","SƠN NỀN","TẠO H\xccNH V\xc0 TRANG TR\xcd","PHỦ, M\xc0I V\xc0 HO\xc0N THIỆN"]'
    if old_aside_name in content:
        content = content.replace(old_aside_name, new_aside_name, 1)
        print("Patched aside stage 5 title")

    old_sum_name = r'["Chọn cốt","L\xe0m v\xf3c","Sơn nền","Tạo h\xecnh v\xe0 trang tr\xed","Phủ sơn & M\xe0i nước"]'
    new_sum_name = r'["Chọn cốt","L\xe0m v\xf3c","Sơn nền","Tạo h\xecnh v\xe0 trang tr\xed","Phủ, m\xe0i v\xe0 ho\xe0n thiện"]'
    if old_sum_name in content:
        content = content.replace(old_sum_name, new_sum_name, 1)
        print("Patched stageSummary stage 5 title")

    old_eyebrow = r'4===n?"TẠO H\xccNH":"PHỦ SƠN & M\xc0I NƯỚC"'
    new_eyebrow = r'4===n?"TẠO H\xccNH":"PHỦ, M\xc0I V\xc0 HO\xc0N THIỆN"'
    if old_eyebrow in content:
        content = content.replace(old_eyebrow, new_eyebrow, 1)
        print("Patched galleryEyebrow")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    res = subprocess.run(["node", "-c", filepath], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error in {filepath}:\n{res.stderr}")
        return False
    print(f"OK: {filepath} syntax is valid!")
    return True

def patch_kham_pha(filepath):
    print(f"\n--- Patching {filepath} ---")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found!")
        return False
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # In array N[4]:
    old_n4 = r'{title:"PHỦ, MÀI VÀ HOÀN THIỆN",short:"Phủ lớp sơn cuối, mài nhẵn và đánh bóng để hoàn thiện bề mặt, làm nổi bật độ sâu và vẻ tinh xảo của tác phẩm.",detail:"Mài nước lấy đi có kiểm soát các lớp phía trên để sắc màu và vật liệu bên dưới hiện ra. Người làm có thể quay lại phủ và mài nhiều lượt; khi bố cục đạt yêu cầu mới đánh bóng hoàn thiện.",alt:"Cận cảnh bề mặt sơn mài đã hoàn thiện, ảnh minh họa"}'
    new_n4 = r'{title:"PHỦ, MÀI VÀ HOÀN THIỆN",short:"Mài nước làm lộ họa tiết, sau đó phủ lớp sơn trong, ủ khô rồi mới đánh bóng hoàn thiện để tạo độ sâu bóng cho tác phẩm.",detail:"Mài nước lấy đi có kiểm soát các lớp phía trên để sắc màu và vật liệu bên dưới hiện ra. Sau khi mài nước xong, người thợ tiến hành phủ lớp sơn trong, đưa vào buồng ủ khô đạt độ ẩm tiêu chuẩn rồi mới tiến hành đánh bóng hoàn thiện để tạo độ sâu và độ trong bóng tuyệt đối cho tác phẩm.",alt:"Cận cảnh bề mặt sơn mài đã hoàn thiện, ảnh minh họa"}'
    
    if old_n4 in content:
        content = content.replace(old_n4, new_n4, 1)
        print("Patched array N[4] short and detail copy")
    else:
        print("Warning: old_n4 not found!")

    # In g[4]:
    old_g4 = r'"K\xe9o trực tiếp tr\xean bề mặt 3D để m\xe0i nước: lớp tr\xean l\xf9i đi v\xe0 h\xecnh nằm dưới dần hiện ra. Người l\xe0m c\xf3 thể quay lại phủ, m\xe0i chỉnh rồi đ\xe1nh b\xf3ng ho\xe0n thiện."'
    new_g4 = r'"K\xe9o trực tiếp tr\xean bề mặt 3D để m\xe0i nước: lớp tr\xean l\xf9i đi v\xe0 h\xecnh nằm dưới dần hiện ra. Sau khi m\xe0i nước xong, tiếp tục phủ lớp sơn trong, ủ kh\xf4 rồi mới đ\xe1nh b\xf3ng ho\xe0n thiện."'
    if old_g4 in content:
        content = content.replace(old_g4, new_g4, 1)
        print("Patched g[4]")

    # In polish callout:
    old_polish_callout = r'children:"Đ\xe1nh b\xf3ng thay đổi bề mặt ho\xe0n thiện. Mức m\xe0i v\xe0 c\xe1c chi tiết đ\xe3 lộ được giữ nguy\xean."'
    new_polish_callout = r'children:"Ho\xe0n thiện \xe1nh v\xe0 độ nhẵn: Sau khi m\xe0i nước xong, bề mặt được phủ lớp sơn trong v\xe0 ủ kh\xf4 kỹ lưỡng trước khi đ\xe1nh b\xf3ng ho\xe0n thiện để tạo độ s\xe2u b\xf3ng tuyệt đối."'
    if old_polish_callout in content:
        content = content.replace(old_polish_callout, new_polish_callout, 1)
        print("Patched polish callout")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    res = subprocess.run(["node", "-c", filepath], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error in {filepath}:\n{res.stderr}")
        return False
    print(f"OK: {filepath} syntax is valid!")
    return True

def patch_html_files():
    print("\n--- Patching HTML files ---")
    
    # 1. kham-pha/index.html
    html_file = "kham-pha/index.html"
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            c = f.read()
        
        # Title and short in stage 5 item:
        c = re.sub(
            r'<li id="cong-doan-5"><button[^>]*>.*?<span class="core-v4-step-title">[^<]*</span><span class="core-v4-step-short">[^<]*</span></button></li>',
            r'<li id="cong-doan-5"><button type="button" class="core-v4-process-step" aria-pressed="false" aria-controls="core-v4-process-detail"><span class="core-v4-step-number">0<!-- -->5</span><span class="core-v4-process-photo" role="img" aria-label="Cận cảnh bề mặt sơn mài đã hoàn thiện, ảnh minh họa" style="background-position:100% center"></span><span class="core-v4-step-title">PHỦ, MÀI VÀ HOÀN THIỆN</span><span class="core-v4-step-short">Mài nước làm lộ họa tiết, sau đó phủ lớp sơn trong, ủ khô rồi mới đánh bóng hoàn thiện để tạo độ sâu bóng cho tác phẩm.</span></button></li>',
            c,
            flags=re.DOTALL
        )
        
        # In SSR studio stage list:
        c = c.replace(
            '<strong>PHỦ SƠN & MÀI NƯỚC</strong><small>Phủ lớp, mài, đánh bóng</small>',
            '<strong>PHỦ, MÀI VÀ HOÀN THIỆN</strong><small>Mài nước, phủ sơn trong, ủ khô, đánh bóng</small>'
        )
        c = c.replace(
            '<strong>PHỦ SƠN & MÀI NƯỚC</strong><small>Phủ lớp, mài nước, đánh bóng</small>',
            '<strong>PHỦ, MÀI VÀ HOÀN THIỆN</strong><small>Mài nước, phủ sơn trong, ủ khô, đánh bóng</small>'
        )
        c = c.replace(
            'aria-label="Mở công đoạn PHỦ SƠN & MÀI NƯỚC"',
            'aria-label="Mở công đoạn PHỦ, MÀI VÀ HOÀN THIỆN"'
        )
        
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(c)
        print("Updated kham-pha/index.html")

    # 2. index.html
    home_file = "index.html"
    if os.path.exists(home_file):
        with open(home_file, "r", encoding="utf-8") as f:
            c = f.read()
        c = c.replace(
            '<li id="cong-doan-5" class="coreIntroduction_stageItem__C7_GF" data-reveal="true" data-visible="true" style="--stage-position:100%"><span class="coreIntroduction_materialNumber__nbsF5">05</span><strong>PHỦ SƠN & MÀI NƯỚC</strong><span class="coreIntroduction_stagePhoto__e5sjm" role="img" aria-label="Công đoạn 5: phủ, mài và hoàn thiện"></span><a class="coreIntroduction_stageMore__uOSUQ" href="/kham-pha#cong-doan-5">Tìm hiểu thêm →</a></li>',
            '<li id="cong-doan-5" class="coreIntroduction_stageItem__C7_GF" data-reveal="true" data-visible="true" style="--stage-position:100%"><span class="coreIntroduction_materialNumber__nbsF5">05</span><strong>PHỦ, MÀI VÀ HOÀN THIỆN</strong><span class="coreIntroduction_stagePhoto__e5sjm" role="img" aria-label="Công đoạn 5: phủ, mài và hoàn thiện"></span><a class="coreIntroduction_stageMore__uOSUQ" href="/kham-pha#cong-doan-5">Tìm hiểu thêm →</a></li>'
        )
        with open(home_file, "w", encoding="utf-8") as f:
            f.write(c)
        print("Updated index.html")

    # 3. trai-nghiem/index.html
    tn_file = "trai-nghiem/index.html"
    if os.path.exists(tn_file):
        with open(tn_file, "r", encoding="utf-8") as f:
            c = f.read()
        c = c.replace(
            '<li id="cong-doan-5" class="coreIntroduction_stageItem__C7_GF" data-reveal="true" data-visible="true" style="--stage-position:100%"><span class="coreIntroduction_materialNumber__nbsF5">05</span><strong>PHỦ SƠN & MÀI NƯỚC</strong><span class="coreIntroduction_stagePhoto__e5sjm" role="img" aria-label="Công đoạn 5: phủ, mài và hoàn thiện"></span><a class="coreIntroduction_stageMore__uOSUQ" href="/kham-pha#cong-doan-5">Tìm hiểu thêm →</a></li>',
            '<li id="cong-doan-5" class="coreIntroduction_stageItem__C7_GF" data-reveal="true" data-visible="true" style="--stage-position:100%"><span class="coreIntroduction_materialNumber__nbsF5">05</span><strong>PHỦ, MÀI VÀ HOÀN THIỆN</strong><span class="coreIntroduction_stagePhoto__e5sjm" role="img" aria-label="Công đoạn 5: phủ, mài và hoàn thiện"></span><a class="coreIntroduction_stageMore__uOSUQ" href="/kham-pha#cong-doan-5">Tìm hiểu thêm →</a></li>'
        )
        with open(tn_file, "w", encoding="utf-8") as f:
            f.write(c)
        print("Updated trai-nghiem/index.html")

if __name__ == "__main__":
    ok = True
    for f in FILES_840:
        if not patch_840(f):
            ok = False
    for f in FILES_KHAM_PHA:
        if not patch_kham_pha(f):
            ok = False
    patch_html_files()
    print("\nResult:", "SUCCESS" if ok else "FAILED")
