import os
import subprocess
import sys

def run():
    js_paths = [
        '_next/static/chunks/840-f19fdd306966b2e5.js',
        'ma_nguon_css_js/js/840-f19fdd306966b2e5.js'
    ]

    for js_path in js_paths:
        if not os.path.exists(js_path):
            print(f"Skipping {js_path} (not found)")
            continue

        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Update stageList labels: "PHỦ, MÀI VÀ HOÀN THIỆN" -> "PHỦ SƠN & MÀI NƯỚC"
        old_sl = '["CHUẨN BỊ CỐT","L\\xc0M V\\xd3C","SƠN NỀN","TẠO H\\xccNH V\\xc0 TRANG TR\\xcd","PHỦ, M\\xc0I V\\xc0 HO\\xc0N THIỆN"]'
        new_sl = '["CHUẨN BỊ CỐT","L\\xc0M V\\xd3C","SƠN NỀN","TẠO H\\xccNH V\\xc0 TRANG TR\\xcd","PHỦ SƠN & M\\xc0I NƯỚC"]'
        if old_sl in content:
            content = content.replace(old_sl, new_sl)
            print(f"[{js_path}] Updated stageList to PHỦ SƠN & MÀI NƯỚC")
        else:
            old_sl_raw = '["CHUẨN BỊ CỐT","LÀM VÓC","SƠN NỀN","TẠO HÌNH VÀ TRANG TRÍ","PHỦ, MÀI VÀ HOÀN THIỆN"]'
            new_sl_raw = '["CHUẨN BỊ CỐT","LÀM VÓC","SƠN NỀN","TẠO HÌNH VÀ TRANG TRÍ","PHỦ SƠN & MÀI NƯỚC"]'
            if old_sl_raw in content:
                content = content.replace(old_sl_raw, new_sl_raw)
                print(f"[{js_path}] Updated stageList (raw) to PHỦ SƠN & MÀI NƯỚC")

        # Update stageList subtext: "Phủ lớp, mài, đánh bóng" -> "Phủ lớp, mài nước, đánh bóng"
        old_sub = '["D\\xe1ng v\\xe0 vật liệu","Gia cố, hom v\\xe0 l\\xe0m phẳng","Chọn sắc nền","Chọn mặt v\\xe0 đặt họa tiết","Phủ lớp, m\\xe0i, đ\\xe1nh b\\xf3ng"]'
        new_sub = '["D\\xe1ng v\\xe0 vật liệu","Gia cố, hom v\\xe0 l\\xe0m phẳng","Chọn sắc nền","Chọn mặt v\\xe0 đặt họa tiết","Phủ lớp, m\\xe0i nước, đ\\xe1nh b\\xf3ng"]'
        if old_sub in content:
            content = content.replace(old_sub, new_sub)
            print(f"[{js_path}] Updated stageList subtext")
        else:
            old_sub_raw = '["Dáng và vật liệu","Gia cố, hom và làm phẳng","Chọn sắc nền","Chọn mặt và đặt họa tiết","Phủ lớp, mài, đánh bóng"]'
            new_sub_raw = '["Dáng và vật liệu","Gia cố, hom và làm phẳng","Chọn sắc nền","Chọn mặt và đặt họa tiết","Phủ lớp, mài nước, đánh bóng"]'
            if old_sub_raw in content:
                content = content.replace(old_sub_raw, new_sub_raw)
                print(f"[{js_path}] Updated stageList subtext (raw)")

        # 2. Update stageSummary array: "Phủ mài hoàn thiện" -> "Phủ sơn & Mài nước"
        old_ss = '["Chọn cốt","L\\xe0m v\\xf3c","SƠn nền","Tạo h\\xecnh v\\xe0 trang tr\\xed","Phủ m\\xe0i ho\\xe0n thiện"]'
        # let's find the exact summary array:
        pos_ss = content.find('.stageSummary')
        if pos_ss != -1:
            chunk = content[pos_ss:pos_ss+300]
            if '"Phủ m\\xe0i ho\\xe0n thiện"' in chunk:
                content = content[:pos_ss] + chunk.replace('"Phủ m\\xe0i ho\\xe0n thiện"', '"Phủ sơn & M\\xe0i nước"') + content[pos_ss+300:]
                print(f"[{js_path}] Updated stageSummary title to Phủ sơn & Mài nước")
            elif '"Phủ mài hoàn thiện"' in chunk:
                content = content[:pos_ss] + chunk.replace('"Phủ mài hoàn thiện"', '"Phủ sơn & Mài nước"') + content[pos_ss+300:]
                print(f"[{js_path}] Updated stageSummary title (raw) to Phủ sơn & Mài nước")

        # 3. Update eb[4]
        old_eb4 = '["Phủ, m\\xe0i v\\xe0 ho\\xe0n thiện","Tạo lớp phủ trong, m\\xe0i nước sau khi phủ rồi đ\\xe1nh b\\xf3ng bề mặt."]'
        new_eb4 = '["Phủ sơn & M\\xe0i nước","Phủ lớp sơn trong suốt, ủ kh\\xf4, m\\xe0i nước l\\xe0m lộ họa tiết v\\xe0 đ\\xe1nh b\\xf3ng ho\\xe0n thiện."]'
        if old_eb4 in content:
            content = content.replace(old_eb4, new_eb4)
            print(f"[{js_path}] Updated eb[4]")

        # 4. Update e_[4]
        old_e_4 = '"Phủ lớp sơn trong, m\\xe0i nước v\\xe0 đ\\xe1nh b\\xf3ng để ho\\xe0n thiện bề mặt."'
        new_e_4 = '"Phủ lớp sơn trong, tiến h\\xe0nh m\\xe0i nước để l\\xe0m lộ họa tiết v\\xe0 đ\\xe1nh b\\xf3ng ho\\xe0n thiện."'
        if old_e_4 in content:
            content = content.replace(old_e_4, new_e_4)
            print(f"[{js_path}] Updated e_[4]")

        # 5. Update galleryEyebrow for stage 4
        old_eyebrow = '3===n?"TẠO H\\xccNH":"HO\\xc0N THIỆN"'
        new_eyebrow = '3===n?"TẠO H\\xccNH":"PHỦ SƠN & M\\xc0I NƯỚC"'
        if old_eyebrow in content:
            content = content.replace(old_eyebrow, new_eyebrow)
            print(f"[{js_path}] Updated galleryEyebrow")

        # 6. REPLACE STAGE 3 ADVANCE BUTTON BLOCK WITH PROMINENT "PHỦ SƠN & MÀI NƯỚC" SECTION
        old_s3_advance = (
            '!E&&(0,a.jsxs)("button",{type:"button",className:g().advanceButton,onClick:()=>{i(4),u(e=>Math.max(e,4)),z("coat"),B("Sang phủ m\\xe0i ho\\xe0n thiện. Lớp trang tr\\xed được giữ b\\xean dưới.")},children:["Bước tiếp theo ",(0,a.jsx)("span",{children:"→"})]})'
        )

        new_s3_advance = (
            '(0,a.jsxs)("div",{className:"studio_next_step_card",style:{marginTop:"14px",padding:"14px 16px",background:"linear-gradient(135deg, rgba(84,18,21,0.07) 0%, rgba(132,32,34,0.03) 100%)",border:"1.5px solid rgba(132,32,34,0.22)",borderRadius:"8px"},children:['
            '(0,a.jsxs)("div",{style:{display:"flex",alignItems:"center",gap:"8px",marginBottom:"6px"},children:['
            '(0,a.jsx)("span",{style:{display:"inline-block",padding:"2px 8px",background:"#842022",color:"#fcedc8",fontSize:"11px",fontWeight:"700",borderRadius:"4px",letterSpacing:"0.06em"},children:"C\\xd4NG ĐOẠN TIẾP THEO"}),'
            '(0,a.jsx)("strong",{style:{color:"#22120c",fontSize:"13.5px",fontFamily:"\'Playfair Display\',serif"},children:"PHỦ SƠN & M\\xc0I NƯỚC"})'
            ']}),'
            '(0,a.jsx)("p",{style:{margin:"0 0 12px 0",fontSize:"12.5px",lineHeight:"1.5",color:"#553a26"},children:"Sau khi ho\\xe0n th\\xe0nh bố cục họa tiết, t\\xe1c phẩm được phủ c\\xe1c lớp sơn trong (sơn c\\xe1nh gi\\xe1n), ủ kh\\xf4 v\\xe0 tiến h\\xe0nh m\\xe0i nước tỉ mỉ để từng lớp họa tiết ẩn hiện với chiều s\\xe2u độc bản."}),'
            '!E&&(0,a.jsxs)("button",{type:"button",className:g().advanceButton,style:{width:"100%",padding:"13px 18px",display:"flex",alignItems:"center",justifyContent:"center",gap:"8px",fontSize:"14px",fontWeight:"700",background:"linear-gradient(135deg, #842022 0%, #5a1216 100%)",color:"#ffffff",boxShadow:"0 4px 14px rgba(90,18,22,0.25)",border:"1px solid rgba(229,210,169,0.4)",borderRadius:"8px",cursor:"pointer"},onClick:()=>{i(4);u(e=>Math.max(e,4));z("sand");B("Chuyển sang c\\xf4ng đoạn Phủ sơn & M\\xe0i nước. Bắt đầu phủ lớp sơn bảo vệ v\\xe0 m\\xe0i nước để lộ họa tiết.");setTimeout(()=>{var el=document.getElementById("studio-finish")||document.querySelector("div[class*=\'finishActions\']");if(el)el.scrollIntoView({behavior:"smooth",block:"start"})},80)},children:[(0,a.jsx)("span",{children:"Bước tiếp theo: Phủ sơn & M\\xe0i nước"}),(0,a.jsx)("span",{style:{fontSize:"16px"},children:"→"})]})'
            ']})'
        )

        if old_s3_advance in content:
            content = content.replace(old_s3_advance, new_s3_advance)
            print(f"[{js_path}] Successfully replaced Stage 3 advance button with PHỦ SƠN & MÀI NƯỚC card!")
        else:
            print(f"[{js_path}] Warning: old_s3_advance not found!")

        # 7. REPLACE STAGE 4 CONTENT BLOCK WITH STRUCTURED PHỦ SƠN & MÀI NƯỚC CONTROLS
        old_s4_block = (
            '4===n&&(0,a.jsxs)("div",{className:g().stageContent,children:['
            '(0,a.jsx)("p",{className:g().choiceLabel,children:"PHỦ LỚP SƠN TRONG"}),'
            '(0,a.jsxs)("div",{className:g().finishActions,children:['
            '(0,a.jsxs)("button",{type:"button",onClick:()=>{var e;z("coat"),null===(e=es.current)||void 0===e||e.applyCoat(),J(e=>e+1),Y(!1),B("Đã phủ thêm một lượt trong suốt trên bề mặt; sẵn sàng ủ khô.")},children:["Phủ lớp sơn trong ",(0,a.jsxs)("small",{children:[Z," lượt đã phủ · có thể phủ nhiều lượt"]})]}),'
            '(0,a.jsxs)("button",{type:"button","aria-pressed":Q,onClick:()=>{if(!Z)J(1);Y(!0),z("orbit"),B("Lớp phủ đã được ủ khô trong mô phỏng. Bây giờ có thể mài nước.")},children:["Ủ khô ",(0,a.jsx)("small",{children:Q?"Đã ủ khô":"Sẵn sàng ủ khô"})]}),'
            '(0,a.jsxs)("button",{type:"button",onClick:()=>{var e;if(!Z){null===(e=es.current)||void 0===e||e.applyCoat(),J(1),Y(!0)}else if(!Q){Y(!0)}z("sand"),O(e=>Math.max(8,e-5)),U(e=>e+1),en(e=>e+1);var sRef=es.current;if(sRef){if(sRef.pass)sRef.pass();else if(sRef.sand)sRef.sand()}let msgs=["Đang mài nước: Lớp sơn trong mờ dần, các mảng vỏ trứng và bụi vàng quỳ bắt đầu ánh lên.","Đang mài nước: Bề mặt phẳng mịn, các đường nét hoa văn và sắc nền hiện rõ độ sâu.","Nước mài hoàn thiện: Bề mặt đã lộ đều các lớp họa tiết và sắc nền, sẵn sàng đánh bóng."];B(msgs[Math.min(msgs.length-1,Math.floor(et/2))])},children:["Mài nước ",(0,a.jsxs)("small",{children:[et," lượt mài hoàn tất"]})]}),'
            '(0,a.jsxs)("button",{type:"button",onClick:()=>{eo("Bóng"),z("orbit"),B("Đã đánh bóng bề mặt; ánh phản xạ được làm mịn và sáng gương.")},children:["Đánh bóng ",(0,a.jsx)("small",{children:"Bóng"===ei?"Đã đánh bóng":"Làm mịn & sáng bóng bề mặt"})]})'
            ']}),'
            '(0,a.jsxs)("label",{className:g().depthControl,children:["ĐỘ S\\xc2U M\\xc0I",(0,a.jsx)("input",{type:"range",min:"1",max:"100",value:q,onChange:e=>O(Number(e.target.value))}),(0,a.jsxs)("output",{children:[q,"%"]})]}),'
            '(0,a.jsxs)("div",{className:g().stageActions,children:[(0,a.jsx)("button",{type:"button",onClick:()=>{i(3),z("orbit")},children:"← Trở lại trang tr\\xed"}),'
        )

        new_s4_block = (
            '4===n&&(0,a.jsxs)("div",{className:g().stageContent,id:"studio-finish",style:{scrollMarginTop:110},children:['
            '(0,a.jsx)("p",{className:"studio_core_guide",children:"C\\xf4ng đoạn phủ sơn trong (sơn c\\xe1nh gi\\xe1n/sơn quang) v\\xe0 m\\xe0i nước l\\xe0 linh hồn của nghệ thuật sơn m\\xe0i. C\\xe0ng m\\xe0i nước đều tay, từng lớp m\\xe0u, vỏ trứng v\\xe0 v\\xe0ng quỳ c\\xe0ng \\xe1nh l\\xean chiều s\\xe2u huyền ảo."}),'
            '(0,a.jsx)("span",{className:g().choiceLabel,style:{display:"block",margin:"12px 0 8px 0"},children:"1. PHỦ LỚP SƠN TRONG & Ủ KH\\xd4"}),'
            '(0,a.jsxs)("div",{className:g().finishActions,children:['
            '(0,a.jsxs)("button",{type:"button",className:"studio_coat_btn",onClick:()=>{var e;z("coat"),null===(e=es.current)||void 0===e||e.applyCoat(),J(e=>e+1),Y(!1),B("Đ\\xe3 phủ th\\xeam một lượt sơn trong suốt l\\xean bề mặt; sẵn s\\xe0ng ủ kh\\xf4.")},children:[(0,a.jsx)("strong",{children:"Phủ lớp sơn trong"}),(0,a.jsxs)("small",{children:[Z," lượt đ\\xe3 phủ \xb7 c\\xf3 thể phủ nhiều lượt"]})]}),'
            '(0,a.jsxs)("button",{type:"button",className:"studio_dry_btn","aria-pressed":Q,onClick:()=>{if(!Z)J(1);Y(!0),z("orbit"),B("Lớp phủ đ\\xe3 được ủ kh\\xf4 trong m\\xf4 phỏng. B\\xe2y giờ c\\xf3 thể m\\xe0i nước.")},children:[(0,a.jsx)("strong",{children:"Ủ kh\\xf4"}),(0,a.jsx)("small",{children:Q?"Đ\\xe3 ủ kh\\xf4 \xb7 sẵn s\\xe0ng m\\xe0i nước":"Sẵn s\\xe0ng ủ kh\\xf4"})]})'
            ']}),'
            '(0,a.jsx)("span",{className:g().choiceLabel,style:{display:"block",margin:"18px 0 8px 0",color:"#842022",fontWeight:"800"},children:"2. M\\xc0I NƯỚC (C\\xd4NG ĐOẠN CỐT L\\xd5I CỦA SƠN M\\xc0I)"}),'
            '(0,a.jsxs)("div",{className:"studio_grind_card",style:{padding:"14px",background:"linear-gradient(135deg, rgba(84,18,21,0.06) 0%, rgba(132,32,34,0.03) 100%)",border:"2px solid #842022",borderRadius:"10px",boxShadow:"0 4px 18px rgba(132,32,34,0.12)",marginBottom:"16px"},children:['
            '(0,a.jsxs)("button",{type:"button",className:"studio_main_grind_btn",style:{width:"100%",padding:"14px 18px",background:"linear-gradient(135deg, #842022 0%, #5a1216 100%)",color:"#ffffff",border:"1.5px solid #deb85a",borderRadius:"8px",boxShadow:"0 6px 18px rgba(90,18,22,0.28)",cursor:"pointer",display:"flex",flexDirection:"column",alignItems:"center",gap:"4px"},onClick:()=>{var e;if(!Z){null===(e=es.current)||void 0===e||e.applyCoat(),J(1),Y(!0)}else if(!Q){Y(!0)}z("sand"),O(e=>Math.max(8,e-5)),U(e=>e+1),en(e=>e+1);var sRef=es.current;if(sRef){if(sRef.pass)sRef.pass();else if(sRef.sand)sRef.sand()}let msgs=["Đang mài nước: Lớp sơn trong mờ dần, các mảng vỏ trứng và bụi vàng quỳ bắt đầu ánh lên.","Đang mài nước: Bề mặt phẳng mịn, các đường nét hoa văn và sắc nền hiện rõ độ sâu.","Nước mài hoàn thiện: Bề mặt đã lộ đều các lớp họa tiết và sắc nền, sẵn sàng đánh bóng."];B(msgs[Math.min(msgs.length-1,Math.floor(et/2))])},children:[(0,a.jsx)("span",{style:{fontSize:"15px",fontWeight:"800",letterSpacing:"0.04em",color:"#fff5e6"},children:"💧 M\\xc0I NƯỚC \xb7 NHẤN ĐỂ M\\xc0I LỘ HOA VĂN"}),(0,a.jsxs)("small",{style:{fontSize:"12px",color:"#fcedc8"},children:[et," lượt m\\xe0i ho\\xe0n tất \xb7 Nhấn để m\\xe0i tiếp"]})]}),'
            '(0,a.jsx)("p",{style:{margin:"10px 0 12px 0",fontSize:"12.5px",lineHeight:"1.5",color:"#553a26"},children:"D\\xf9ng nước kết hợp giấy r\\xe1p/than củi m\\xe0i phẳng bề mặt. Mỗi lượt m\\xe0i l\\xe0m mỏng lớp sơn phủ, gi\\xfap họa tiết v\\xe0 sắc nền b\\xean dưới dần hiện r\\xf5 với chiều s\\xe2u sơn m\\xe0i."}),'
            '(0,a.jsxs)("label",{className:g().depthControl,style:{margin:"0",display:"flex",alignItems:"center",justifyContent:"space-between",gap:"10px"},children:[(0,a.jsx)("span",{style:{fontSize:"12.5px",fontWeight:"700",color:"#331812"},children:"ĐỘ S\\xc2U M\\xc0I NƯỚC"}),(0,a.jsx)("input",{type:"range",min:"1",max:"100",value:q,onChange:e=>O(Number(e.target.value)),style:{flex:"1"}}),(0,a.jsxs)("output",{style:{fontWeight:"700",color:"#842022",minWidth:"36px",textAlign:"right"},children:[q,"%"]})]})'
            ']}),'
            '(0,a.jsx)("span",{className:g().choiceLabel,style:{display:"block",margin:"14px 0 8px 0"},children:"3. Đ\\xc1NH B\\xd3NG & HO\\xc0N THIỆN"}),'
            '(0,a.jsxs)("div",{className:g().finishActions,children:['
            '(0,a.jsxs)("button",{type:"button",className:"studio_polish_btn",onClick:()=>{eo("Bóng"),z("orbit"),B("Đ\\xe3 đ\\xe1nh b\\xf3ng bề mặt; \\xe1nh phản xạ được l\\xe0m mịn v\\xe0 s\\xe1ng gương.")},children:[(0,a.jsx)("strong",{children:"✨ Đ\\xe1nh b\\xf3ng"}),(0,a.jsx)("small",{children:"Bóng"===ei?"Đ\\xe3 đ\\xe1nh b\\xf3ng s\\xe1ng gương":"L\\xe0m mịn & s\\xe1ng b\\xf3ng bề mặt"})]})'
            ']}),'
            '(0,a.jsxs)("div",{className:g().stageActions,children:[(0,a.jsx)("button",{type:"button",onClick:()=>{i(3),z("orbit")},children:"← Trở lại bước trang tr\\xed"}),'
        )

        if old_s4_block in content:
            content = content.replace(old_s4_block, new_s4_block)
            print(f"[{js_path}] Successfully upgraded Stage 4 to HERO PHỦ SƠN & MÀI NƯỚC!")
        else:
            print(f"[{js_path}] Warning: old_s4_block not found!")

        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Run node syntax check
        res = subprocess.run(['node', '-c', js_path], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Syntax error in {js_path}:", res.stderr)
            return False
        else:
            print(f"[{js_path}] Node syntax check PASSED!")

    return True

if __name__ == '__main__':
    if not run():
        sys.exit(1)
    print("Done applying Phủ sơn & Mài nước updates!")
