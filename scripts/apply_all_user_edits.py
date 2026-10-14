import os
import subprocess
import sys

def run():
    js_paths = [
        '_next/static/chunks/840-f19fdd306966b2e5.js',
        'ma_nguon_css_js/js/840-f19fdd306966b2e5.js'
    ]

    # --- 1. Update JS files ---
    for js_path in js_paths:
        if not os.path.exists(js_path):
            print(f"Skipping missing {js_path}")
            continue

        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix 1: Stage 1 checkbox text from "(chỉ phù hợp)" to "(khi phù hợp)"
        c1_old = '," Thêm lớp vải/xơ/dặm gia cố (chỉ phù hợp)"]})'
        c1_new = '," Thêm lớp vải/xơ/dặm gia cố (khi phù hợp)"]})'
        if c1_old in content:
            content = content.replace(c1_old, c1_new)
            print(f"[{js_path}] Replaced Stage 1 checkbox label with (khi phù hợp)")
        else:
            print(f"[{js_path}] Warning: c1_old not found!")

        # Fix 2: Add [u_decor_lock,set_decor_lock] state hook
        hook_old = '[u_reinf,set_reinf]=(0,r.useState)(!1)'
        hook_new = '[u_reinf,set_reinf]=(0,r.useState)(!1),[u_decor_lock,set_decor_lock]=(0,r.useState)(!1)'
        if hook_old in content and '[u_decor_lock,set_decor_lock]' not in content:
            content = content.replace(hook_old, hook_new, 1)
            print(f"[{js_path}] Added u_decor_lock hook")

        # Fix 3: Add u_decor_meta and u_motif_meta definitions
        decor_meta_def = (
            'var u_decor_meta={'
            '"Vỏ trứng":{name:"Vỏ trứng",note:"Vỏ trứng được ghép thành từng mảnh trên bề mặt, tạo nên sắc trắng cùng những đường nứt tự nhiên, mang lại hiệu ứng thị giác rất riêng cho tác phẩm.",color:"#f5eee6",border:"#d4c5b9"},'
            '"Vàng quỳ":{name:"Vàng quỳ",note:"Vàng được thếp hoặc sử dụng trong trang trí để tạo những điểm sáng ấm, bắt ánh sáng và làm tăng chiều sâu thị giác cho bề mặt sơn mài.",color:"#deb85a",border:"#b89535"},'
            '"Xà cừ":{name:"Xà cừ",note:"Vỏ trai, vỏ ốc được xử lý và khảm lên bề mặt, tạo hiệu ứng óng ánh với nhiều sắc độ thay đổi theo ánh sáng và góc nhìn.",color:"#8ec5d6",border:"#6ba5b6"},'
            '"Lớp nền":{name:"Lớp nền",note:"Sơn then mang sắc đen sâu hoặc sơn son mang gam đỏ ấm, thường được sử dụng để tạo nền tương phản và làm nổi bật những lớp chất liệu đặt trên bề mặt.",color:"#8c2020",border:"#641414"}'
            '};'
            'var u_motif_meta={'
            '"Hoa sen":"Họa tiết Hoa sen truyền thống — nét vẽ uyển chuyển hòa cùng chất liệu tạo nên vẻ thanh tịnh và trang nhã.",'
            '"Hoa lá":"Họa tiết Hoa lá tự nhiên — đường nét uốn lượn sinh động, mang nhịp điệu mềm mại cho bề mặt.",'
            '"Kỳ hà":"Họa tiết hình học Kỳ hà — kết cấu kỷ hà cổ điển tạo sự cân xứng, khúc chiết và sang trọng.",'
            '"Thêm":"Tự điều chỉnh — phác thảo nét vẽ tự do trực tiếp bằng cọ vẽ lên bề mặt 3D.",'
            '"Tự điều chỉnh":"Tự điều chỉnh — phác thảo nét vẽ tự do trực tiếp bằng cọ vẽ lên bề mặt 3D."'
            '};'
        )

        meta_marker = 'var u_core_meta={'
        if meta_marker in content and 'var u_decor_meta=' not in content:
            content = content.replace(meta_marker, decor_meta_def + meta_marker, 1)
            print(f"[{js_path}] Injected u_decor_meta and u_motif_meta")

        # Fix 4: Replace Stage 4 content block
        old_s4 = (
            '3===n&&(0,a.jsxs)("div",{className:g().stageContent,id:"studio-decoration",style:{scrollMarginTop:110},children:['
            '(0,a.jsx)("div",{className:g().choiceColumns,children:(0,a.jsxs)("div",{children:['
            '(0,a.jsx)("span",{className:g().choiceLabel,children:"CHẤT LIỆU TRANG TR\\xcd"}),'
            '(0,a.jsx)("div",{className:g().materialChoices,children:["Vỏ trứng","V\\xe0ng quỳ","X\\xe0 cừ","Lớp nền"].map(e=>(0,a.jsx)("button",{type:"button","aria-pressed":j.inlay===e,onClick:()=>eu("inlay",e),children:e},e))})'
            ']})}),'
            '(0,a.jsx)("span",{className:g().choiceLabel,children:"CHỌN MẶT ĐANG L\\xc0M"}),'
            '(0,a.jsx)("div",{className:g().faceChoices,role:"group","aria-label":"Chọn mặt để trang tr\\xed",children:ex.map(e=>(0,a.jsx)("button",{type:"button","aria-pressed":V===ev[e],onClick:()=>I(ev[e]),children:ef[e]},ev[e]))}),'
            '(0,a.jsxs)("span",{className:g().choiceLabel,children:["HỌA TIẾT \\xb7 \\xc1P DỤNG L\\xcaN ",ef[ev.indexOf(V)].toLocaleUpperCase("vi")]}),'
            '(0,a.jsx)("div",{className:g().motifChoices,children:M.map(e=>(0,a.jsx)("button",{type:"button","aria-pressed":L[V]===e,onClick:()=>ep(e),children:"Th\\xeam"===e?"Tự điều chỉnh":e},e))}),'
            'E&&(0,a.jsx)(w,{groundColor:(null===(e=S.find(e=>e.name===j.ground))||void 0===e?void 0:e.value)||S[0].value,materialColor:"V\\xe0ng quỳ"===j.inlay?"#deb85a":"X\\xe0 cừ"===j.inlay?"#dce5ef":"Lớp nền"===j.inlay?(null===(t=S.find(e=>e.name===j.ground))||void 0===t?void 0:t.value)||S[0].value:"#efe5cb",materialName:j.inlay,actionLabel:"\\xc1p dụng",onMaterialChange:e=>eu("inlay",e),initial:k,selectedFace:V,onSelectFace:e=>I(e),allowedFaces:ed,storageKey:"ssms-studio-".concat(p,"-draft-v1"),onApply:e=>{eh(),N(t=>({...t,...e})),P(!1),z("orbit"),B("Đ\\xe3 \\xe1p dụng n\\xe9t vẽ l\\xean m\\xf4 h\\xecnh. Bạn c\\xf3 thể tiếp tục trang tr\\xed hoặc chọn bước tiếp theo.")}}),'
            '!E&&(0,a.jsxs)("button",{type:"button",className:g().advanceButton,onClick:()=>{i(4),u(e=>Math.max(e,4)),z("coat"),B("Sang phủ m\\xe0i ho\\xe0n thiện. Lớp trang tr\\xed được giữ b\\xean dưới.")},children:["Bước tiếp theo ",(0,a.jsx)("span",{children:"→"})]})'
            ']})'
        )

        new_s4 = (
            '3===n&&(0,a.jsxs)("div",{className:g().stageContent,id:"studio-decoration",style:{scrollMarginTop:110},children:['
            '(0,a.jsx)("p",{className:"studio_core_guide",children:"Chọn chất liệu trang trí và họa tiết để áp dụng lên từng mặt của tác phẩm. Mỗi chất liệu mang lại hiệu ứng thị giác và chiều sâu đặc trưng cho bề mặt sơn mài."}),'
            '(0,a.jsx)("div",{className:g().choiceColumns,children:(0,a.jsxs)("div",{children:['
            '(0,a.jsx)("span",{className:g().choiceLabel,children:"CHẤT LIỆU TRANG TR\\xcd"}),'
            '(0,a.jsx)("div",{className:g().materialChoices,children:[{name:"Vỏ trứng",color:"#f5eee6",border:"#d4c5b9"},{name:"Vàng quỳ",color:"#deb85a",border:"#b89535"},{name:"Xà cừ",color:"#8ec5d6",border:"#6ba5b6"},{name:"Lớp nền",color:"#8c2020",border:"#641414"}].map(e=>(0,a.jsxs)("button",{type:"button","aria-pressed":j.inlay===e.name,onClick:()=>{eu("inlay",e.name);B("Đã chọn chất liệu trang trí "+e.name+". "+(u_decor_meta[e.name]?u_decor_meta[e.name].note:""))},children:[(0,a.jsx)("i",{className:"studio_material_dot",style:{background:e.color,borderColor:e.border||"rgba(0,0,0,0.2)"}}),e.name]},e.name))})'
            ']})}),'
            '(0,a.jsxs)("div",{className:"studio_core_callout",children:[(0,a.jsx)("strong",{children:(u_decor_meta[j.inlay]||u_decor_meta["Vỏ trứng"]).name}),(0,a.jsx)("p",{children:(u_decor_meta[j.inlay]||u_decor_meta["Vỏ trứng"]).note})]}),'
            '(0,a.jsx)("span",{className:g().choiceLabel,children:"CHỌN MẶT ĐANG L\\xc0M"}),'
            '(0,a.jsx)("div",{className:g().faceChoices,role:"group","aria-label":"Chọn mặt để trang tr\\xed",children:ex.map(e=>(0,a.jsx)("button",{type:"button","aria-pressed":V===ev[e],onClick:()=>I(ev[e]),children:ef[e]},ev[e]))}),'
            '(0,a.jsxs)("span",{className:g().choiceLabel,children:["HỌA TIẾT \\xb7 \\xc1P DỤNG L\\xcaN ",ef[ev.indexOf(V)].toLocaleUpperCase("vi")]}),'
            '(0,a.jsx)("div",{className:g().motifChoices,children:M.map(e=>(0,a.jsx)("button",{type:"button","aria-pressed":L[V]===e,onClick:()=>{ep(e);B("Đã chọn họa tiết "+("Thêm"===e?"Tự điều chỉnh":e)+" cho "+ef[ev.indexOf(V)].toLowerCase()+".")},children:"Th\\xeam"===e?"Tự điều chỉnh":e},e))}),'
            '(0,a.jsx)("p",{className:"studio_motif_subnote",style:{margin:"6px 0 14px 0",color:"#6d5436",fontSize:"12.5px",lineHeight:"1.55"},children:u_motif_meta[L[V]]||u_motif_meta["Hoa sen"]}),'
            '(0,a.jsxs)("label",{className:"studio_reinforce_check",children:[(0,a.jsx)("input",{type:"checkbox",checked:u_decor_lock,onChange:e=>{set_decor_lock(e.target.checked);if(e.target.checked)B("Đã bật xác nhận cố định lớp trang trí trước khi phủ sơn.")}})," Cố định và ủ lớp chất liệu trước khi phủ sơn (khi phù hợp)"]}),'
            '(0,a.jsx)("p",{className:"studio_reinforce_note",children:"Chất liệu cẩn hoặc thếp cần được cố định chắc vào nền sơn và để khô tự nhiên trước khi bước vào công đoạn phủ lớp và mài."}),'
            '(0,a.jsxs)("div",{className:"studio_stage_status",children:[(0,a.jsx)("span",{className:"studio_status_dot"}),(0,a.jsx)("span",{children:"Họa tiết và chất liệu trang trí đã được bố cục hài hòa trên bề mặt, sẵn sàng cho công đoạn tiếp theo."})]}),'
            'E&&(0,a.jsx)(w,{groundColor:(null===(e=S.find(e=>e.name===j.ground))||void 0===e?void 0:e.value)||S[0].value,materialColor:"V\\xe0ng quỳ"===j.inlay?"#deb85a":"X\\xe0 cừ"===j.inlay?"#dce5ef":"Lớp nền"===j.inlay?(null===(t=S.find(e=>e.name===j.ground))||void 0===t?void 0:t.value)||S[0].value:"#efe5cb",materialName:j.inlay,actionLabel:"\\xc1p dụng",onMaterialChange:e=>eu("inlay",e),initial:k,selectedFace:V,onSelectFace:e=>I(e),allowedFaces:ed,storageKey:"ssms-studio-".concat(p,"-draft-v1"),onApply:e=>{eh(),N(t=>({...t,...e})),P(!1),z("orbit"),B("Đ\\xe3 \\xe1p dụng n\\xe9t vẽ l\\xean m\\xf4 h\\xecnh. Bạn c\\xf3 thể tiếp tục trang tr\\xed hoặc chọn bước tiếp theo.")}}),'
            '!E&&(0,a.jsxs)("button",{type:"button",className:g().advanceButton,onClick:()=>{i(4),u(e=>Math.max(e,4)),z("coat"),B("Sang phủ m\\xe0i ho\\xe0n thiện. Lớp trang tr\\xed được giữ b\\xean dưới.")},children:["Bước tiếp theo ",(0,a.jsx)("span",{children:"→"})]})'
            ']})'
        )

        if old_s4 in content:
            content = content.replace(old_s4, new_s4)
            print(f"[{js_path}] Successfully replaced Stage 4 controls block!")
        else:
            print(f"[{js_path}] Warning: old_s4 not found!")

        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Node syntax check
        res = subprocess.run(['node', '-c', js_path], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Syntax error in {js_path}:", res.stderr)
            return False
        else:
            print(f"[{js_path}] Node syntax check PASSED!")

    # --- 2. Update HTML files ---
    html_paths = [
        'kham-pha/index.html'
    ]
    for hp in html_paths:
        if not os.path.exists(hp):
            continue
        with open(hp, 'r', encoding='utf-8') as f:
            c = f.read()

        old_html_check = 'Thêm lớp vải/xơ/dặm gia cố (chỉ phù hợp)'
        new_html_check = 'Thêm lớp vải/xơ/dặm gia cố (khi phù hợp)'
        if old_html_check in c:
            c = c.replace(old_html_check, new_html_check)
            print(f"[{hp}] Updated checkbox text to (khi phù hợp)")
        with open(hp, 'w', encoding='utf-8') as f:
            f.write(c)

    print("All updates completed successfully!")
    return True

if __name__ == '__main__':
    if not run():
        sys.exit(1)
