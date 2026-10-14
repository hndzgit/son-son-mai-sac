import sys
import subprocess

def patch_840():
    paths = ['_next/static/chunks/840-f19fdd306966b2e5.js', 'ma_nguon_css_js/js/840-f19fdd306966b2e5.js']
    
    for path in paths:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Add state [u_reinf, set_reinf]
        old_state_decl = '[el,ec]=(0,r.useState)([!0,!0,!0,!0]),es=(0,r.useRef)(null);'
        new_state_decl = '[el,ec]=(0,r.useState)([!0,!0,!0,!0]),[u_reinf,set_reinf]=(0,r.useState)(!1),es=(0,r.useRef)(null);var u_core_meta={"Gỗ":{name:"Gỗ",note:"Kiểm tra độ ổn định; thay đổi nhiệt độ và độ ẩm có thể ảnh hưởng cốt.",color:"#9a6843"},"Tre":{name:"Tre",note:"Cần cân nhắc độ ổn định và cách gia cố phù hợp với hình thể.",color:"#bb9854"},"Gốm":{name:"Gốm",note:"Bề mặt gốm có độ đặc và độ nhẵn riêng; cách chuẩn bị phụ thuộc cấu tạo tác phẩm.",color:"#a9654c"},"MDF / HDF":{name:"MDF / HDF",note:"Tấm ván công nghiệp có đặc điểm riêng; cách xử lý phụ thuộc cấu tạo.",color:"#a9865c"},"Composite":{name:"Composite",note:"Vật liệu tổng hợp có cấu tạo đa dạng; cách chuẩn bị tùy loại cốt.",color:"#856849"}};'
        
        if old_state_decl in content:
            content = content.replace(old_state_decl, new_state_decl, 1)
        elif '[u_reinf,set_reinf]' not in content:
            print("ERROR: old_state_decl not found in", path)
            return False

        # 2. Add reinforced:u_reinf to K viewer
        old_viewer = 'coreMaterial:v||"Gỗ",'
        new_viewer = 'coreMaterial:v||"Gỗ",reinforced:u_reinf,'
        if old_viewer in content and 'reinforced:u_reinf' not in content:
            content = content.replace(old_viewer, new_viewer, 1)

        # 3. Replace Stage 0 JSX
        old_stage0 = '0===n&&(0,a.jsxs)("div",{className:g().stageContent,children:[(0,a.jsxs)("div",{className:g().choiceColumns,children:[(0,a.jsxs)("div",{children:[(0,a.jsx)("span",{className:g().choiceLabel,children:"D\\xc1NG CỐT"}),(0,a.jsx)("div",{className:g().studioChoices,children:["Mặt hộp","Mặt khay","Mặt tranh"].map(e=>(0,a.jsxs)("button",{type:"button","aria-pressed":p===e,onClick:()=>eg(e,v||"Gỗ"),children:[e,(0,a.jsx)("small",{children:"Mặt hộp"===e?"S\\xe1u mặt":"Một mặt trang tr\\xed"})]},e))})]}),(0,a.jsxs)("div",{children:[(0,a.jsx)("span",{className:g().choiceLabel,children:"CHẤT LIỆU CỐT"}),(0,a.jsx)("div",{className:g().materialChoices,children:["Gỗ","Tre","Gốm","MDF / HDF","Composite"].map(e=>(0,a.jsx)("button",{type:"button","aria-pressed":v===e,onClick:()=>eg(p||"Mặt hộp",e),children:e},e))})]})]}),(0,a.jsxs)("button",{type:"button",className:g().advanceButton,disabled:!p||!v,onClick:()=>{i(1),u(e=>Math.max(e,1)),B("Cốt đ\\xe3 chọn. Tiếp theo l\\xe0 kiểm tra, chuẩn bị v\\xe0 l\\xe0m phẳng v\\xf3c theo vật liệu.")},children:["Bắt đầu l\\xe0m v\\xf3c ",(0,a.jsx)("span",{children:"→"})]})]}),'

        new_stage0 = '0===n&&(0,a.jsxs)("div",{className:g().stageContent,children:[(0,a.jsx)("p",{className:"studio_core_guide",children:"Chọn một loại cốt để xem vật liệu ảnh hưởng ra sao đến việc chuẩn bị. Gỗ, tre, gốm và vật liệu khác cần cách xử lý phù hợp với cấu tạo tác phẩm."}),(0,a.jsxs)("div",{className:g().choiceColumns,children:[(0,a.jsxs)("div",{children:[(0,a.jsx)("span",{className:g().choiceLabel,children:"D\\xc1NG CỐT"}),(0,a.jsx)("div",{className:g().studioChoices,children:["Mặt hộp","Mặt khay","Mặt tranh"].map(e=>(0,a.jsxs)("button",{type:"button","aria-pressed":p===e,onClick:()=>eg(e,v||"Gỗ"),children:[e,(0,a.jsx)("small",{children:"Mặt hộp"===e?"S\\xe1u mặt":"Một mặt trang tr\\xed"})]},e))})]}),(0,a.jsxs)("div",{children:[(0,a.jsx)("span",{className:g().choiceLabel,children:"CHẤT LIỆU CỐT"}),(0,a.jsx)("div",{className:g().materialChoices,children:[{name:"Gỗ",color:"#9a6843"},{name:"Tre",color:"#bb9854"},{name:"Gốm",color:"#a9654c"},{name:"MDF / HDF",color:"#a9865c"},{name:"Composite",color:"#856849"}].map(e=>(0,a.jsxs)("button",{type:"button","aria-pressed":v===e.name,onClick:()=>{eg(p||"Mặt hộp",e.name);B("Đã chọn cốt "+e.name+". "+(u_core_meta[e.name]?u_core_meta[e.name].note:""))},children:[(0,a.jsx)("i",{className:"studio_material_dot",style:{background:e.color}}),e.name]},e.name))})]})]}),(0,a.jsxs)("div",{className:"studio_core_callout",children:[(0,a.jsx)("strong",{children:(u_core_meta[v]||u_core_meta["Gỗ"]).name}),(0,a.jsx)("p",{children:(u_core_meta[v]||u_core_meta["Gỗ"]).note})]}),(0,a.jsxs)("label",{className:"studio_reinforce_check",children:[(0,a.jsx)("input",{type:"checkbox",checked:u_reinf,onChange:e=>{set_reinf(e.target.checked);if(e.target.checked)B("Đã bật xem lớp vải cotton gia cố bó cốt.")}})," Xem lớp vải cotton gia cố (khi phù hợp)"]}),(0,a.jsx)("p",{className:"studio_reinforce_note",children:u_reinf?("Gỗ"===v||"Tre"===v?"Có thể xem lớp vải gia cố trong mô phỏng; việc sử dụng còn tùy cốt và thực hành.":"Có thể bật để xem lớp vải trong mặt cắt; cốt này không mặc định cần gia cố bằng vải."):"Lớp vải chỉ là lựa chọn minh họa khi phù hợp với cấu tạo cốt; không phải bước bắt buộc cho mọi vật liệu."}),(0,a.jsxs)("button",{type:"button",className:g().advanceButton,disabled:!p||!v,onClick:()=>{i(1),u(e=>Math.max(e,1)),B("Cốt đ\\xe3 chọn. Tiếp theo l\\xe0 kiểm tra, chuẩn bị v\\xe0 l\\xe0m phẳng v\\xf3c theo vật liệu.")},children:["Bắt đầu l\\xe0m v\\xf3c ",(0,a.jsx)("span",{children:"→"})]})]}),'

        if old_stage0 in content:
            content = content.replace(old_stage0, new_stage0, 1)
        elif 'studio_core_guide' not in content:
            print("ERROR: old_stage0 not found in", path)
            return False

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated", path)

    return True

if __name__ == '__main__':
    if patch_840():
        res = subprocess.run(['node', '-c', '_next/static/chunks/840-f19fdd306966b2e5.js'])
        if res.returncode == 0:
            print("840 chunk syntax check PASSED!")
        else:
            print("840 chunk syntax check FAILED!")
            sys.exit(1)
