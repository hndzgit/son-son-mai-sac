import os
import subprocess
import sys

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update function K(e) to accept and pass stage
    old_k_decl = 'function K(e){let{configuration:t,className:n="",alt:i="Bề mặt sơn m\\xe0i xem trước",controllerRef:o,faceArtworks:l,mode:c="orbit",depth:s=45,zoom:d,onZoomChange:h,appearance:u="finished",coreMaterial:g="Gỗ",reinforced:k_reinf=!1,finish:p="B\\xf3ng",selectedFace:m,preparationStep:v=0,onStrokeComplete:f,onUndoComplete:x,coatLayers:b=0}=e'
    new_k_decl = 'function K(e){let{configuration:t,className:n="",alt:i="Bề mặt sơn m\\xe0i xem trước",controllerRef:o,faceArtworks:l,mode:c="orbit",depth:s=45,zoom:d,onZoomChange:h,appearance:u="finished",coreMaterial:g="Gỗ",reinforced:k_reinf=!1,finish:p="B\\xf3ng",selectedFace:m,preparationStep:v=0,onStrokeComplete:f,onUndoComplete:x,coatLayers:b=0,stage:k_stg=0}=e'

    if old_k_decl in content:
        content = content.replace(old_k_decl, new_k_decl, 1)
        print(f"[{filepath}] Updated function K(e) declaration with stage")
    else:
        print(f"[{filepath}] Warning: old_k_decl not found!")

    old_k_pass_e = 'selectedFace:m,coatLayers:b,onStrokeComplete:f,onUndoComplete:x,onChange:e=>{j.current=e}})'
    new_k_pass_e = 'selectedFace:m,coatLayers:b,stage:k_stg,onStrokeComplete:f,onUndoComplete:x,onChange:e=>{j.current=e}})'

    if old_k_pass_e in content:
        content = content.replace(old_k_pass_e, new_k_pass_e, 1)
        print(f"[{filepath}] Passed stage from K to E (LacquerStudio)")
    else:
        print(f"[{filepath}] Warning: old_k_pass_e not found!")

    # 2. Update line 41312 where K is called from studio: pass stage: n
    old_k_invoke = '(0,a.jsx)(K,{configuration:ey,controllerRef:es,mode:A,depth:q,zoom:D,'
    new_k_invoke = '(0,a.jsx)(K,{configuration:ey,stage:n,controllerRef:es,mode:A,depth:q,zoom:D,'

    if old_k_invoke in content:
        content = content.replace(old_k_invoke, new_k_invoke, 1)
        print(f"[{filepath}] Passed stage:n to K invocation")
    else:
        print(f"[{filepath}] Warning: old_k_invoke not found!")

    # 3. Update the Stage 3 advance button onClick to initialize q to 20 (coated state)
    old_advance_click = 'onClick:()=>{i(4);u(e=>Math.max(e,4));z("sand");B("Chuyển sang c\\xf4ng đoạn Phủ sơn & M\\xe0i nước. Bắt đầu phủ lớp sơn bảo vệ v\\xe0 m\\xe0i nước để lộ họa tiết.");'
    new_advance_click = 'onClick:()=>{i(4);u(e=>Math.max(e,4));z("sand");O(20);var sRef=es.current;if(sRef&&sRef.setCoverage)sRef.setCoverage(20);B("Chuyển sang c\\xf4ng đoạn Phủ sơn & M\\xe0i nước. Bắt đầu phủ lớp sơn bảo vệ v\\xe0 m\\xe0i nước để lộ họa tiết.");'

    if old_advance_click in content:
        content = content.replace(old_advance_click, new_advance_click, 1)
        print(f"[{filepath}] Updated Stage 3 advance onClick to initialize q=20")
    else:
        print(f"[{filepath}] Warning: old_advance_click not found!")

    # 4. Replace the entire studio_grind_card with the Live Surface Visualizer + Action Button + Slider
    # Find the bounds of studio_grind_card
    start_str = '(0,a.jsxs)("div",{className:"studio_grind_card",'
    end_str = '(0,a.jsx)("span",{className:g().choiceLabel,style:{display:"block",margin:"14px 0 8px 0"},children:"3. Đ\\xc1NH B\\xd3NG & HO\\xc0N THIỆN"})'

    start_pos = content.find(start_str)
    end_pos = content.find(end_str)

    if start_pos != -1 and end_pos != -1:
        current_grind_card = content[start_pos:end_pos]
        
        new_grind_card = (
            '(0,a.jsxs)("div",{className:"studio_grind_card",style:{padding:"14px",background:"linear-gradient(135deg, rgba(84,18,21,0.06) 0%, rgba(132,32,34,0.03) 100%)",border:"2px solid #842022",borderRadius:"10px",boxShadow:"0 4px 18px rgba(132,32,34,0.12)",marginBottom:"16px"},children:['
            # LIVE SURFACE PREVIEW COMPONENT
            '(0,a.jsxs)("div",{className:"studio_surface_preview_wrap",style:{marginBottom:"14px",padding:"10px",background:"#1c0c08",border:"1.5px solid #842022",borderRadius:"8px",boxShadow:"inset 0 2px 10px rgba(0,0,0,0.6)"},children:['
            '(0,a.jsxs)("div",{style:{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:"8px"},children:['
            '(0,a.jsxs)("span",{style:{fontSize:"11px",fontWeight:"700",color:"#deb85a",letterSpacing:"0.06em",textTransform:"uppercase"},children:["BỀ MẶT M\\xc0I NƯỚC THỜI GIAN THỰC \xb7 ",q,"%"]}),'
            '(0,a.jsx)("button",{type:"button",onClick:()=>{var el=document.getElementById("simulator")||document.querySelector("div[class*=\'viewer\']");if(el)el.scrollIntoView({behavior:"smooth",block:"center"})},style:{background:"rgba(222,184,90,0.15)",border:"1px solid rgba(222,184,90,0.4)",color:"#fcedc8",fontSize:"10.5px",padding:"2px 8px",borderRadius:"4px",cursor:"pointer"},children:"👁 Xem 3D"})'
            ']}),'
            '(0,a.jsxs)("div",{style:{position:"relative",width:"100%",height:"140px",borderRadius:"6px",overflow:"hidden",boxShadow:"0 4px 12px rgba(0,0,0,0.5)"},children:['
            '(0,a.jsx)("img",{src:(null==k?void 0:k.top)||G(ey),alt:"Mặt sơn m\\xe0i",style:{width:"100%",height:"100%",objectFit:"cover",display:"block"}}),'
            '(0,a.jsx)("div",{style:{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 50%, rgba(55,20,8,"+Math.max(0,.94-q/100*1.05)+") 0%, rgba(20,6,2,"+Math.max(0,.98-q/100*1.05)+") 100%)",transition:"background 0.12s ease",pointerEvents:"none"}}),'
            '(0,a.jsx)("div",{style:{position:"absolute",inset:0,background:"radial-gradient(circle at 50% 50%, transparent 35%, rgba(255,255,255,"+(q>8&&q<96?.14:.03)+") 65%, transparent 85%)",pointerEvents:"none"}}),'
            '(0,a.jsx)("div",{style:{position:"absolute",bottom:"8px",left:"8px",right:"8px",padding:"4px 10px",background:"rgba(0,0,0,0.75)",backdropFilter:"blur(4px)",borderRadius:"4px",fontSize:"11px",color:"#fcedc8",display:"flex",alignItems:"center",gap:"6px",fontWeight:"600"},children:['
            '(0,a.jsx)("span",{children:q<=15?"🔴 Lớp sơn phủ k\\xedn (Chưa m\\xe0i) \xb7 Họa tiết đang ẩn":q>=85?"✨ M\\xe0i ho\\xe0n tất \xb7 Hoa văn lộ r\\xf5 n\\xe9t & s\\xe1ng b\\xf3ng":"💧 Đang m\\xe0i nước: Lộ "+q+"% hoa văn \xb7 Vỏ trứng & V\\xe0ng quỳ đang dần hiện"})'
            ']})'
            ']})'
            ']}),'
            # MAIN GRIND ACTION BUTTON
            '(0,a.jsxs)("button",{type:"button",className:"studio_main_grind_btn",style:{width:"100%",padding:"14px 18px",background:"linear-gradient(135deg, #842022 0%, #5a1216 100%)",color:"#ffffff",border:"1.5px solid #deb85a",borderRadius:"8px",boxShadow:"0 6px 18px rgba(90,18,22,0.28)",cursor:"pointer",display:"flex",flexDirection:"column",alignItems:"center",gap:"4px"},'
            'onClick:()=>{'
            'var e;if(!Z){null===(e=es.current)||void 0===e||e.applyCoat();J(1);Y(!0)}else if(!Q){Y(!0)}'
            'z("sand");'
            'let nextQ=Math.min(100,Math.max(25,q<18?32:q+14));'
            'O(nextQ);'
            'en(e=>e+1);'
            'var sRef=es.current;'
            'if(sRef){if(sRef.setCoverage)sRef.setCoverage(nextQ);if(sRef.pass)sRef.pass();else if(sRef.sand)sRef.sand()}'
            'let msgs=["Đang m\\xe0i nước ("+nextQ+"%): Lớp sơn trong mờ dần, c\\xe1c mảng vỏ trứng v\\xe0 bụi v\\xe0ng quỳ bắt đầu \\xe1nh l\\xean.","Đang m\\xe0i nước ("+nextQ+"%): Bề mặt phẳng mịn, c\\xe1c đường n\\xe9t hoa văn v\\xe0 sắc nền hiện r\\xf5 độ s\\xe2u.","Nước m\\xe0i ho\\xe0n thiện ("+nextQ+"%): Bề mặt đ\\xe3 lộ đều c\\xe1c lớp họa tiết v\\xe0 sắc nền, sẵn s\\xe0ng đ\\xe1nh b\\xf3ng."];'
            'B(msgs[Math.min(msgs.length-1,Math.floor(nextQ/35))]);'
            '},children:['
            '(0,a.jsx)("span",{style:{fontSize:"15px",fontWeight:"800",letterSpacing:"0.04em",color:"#fff5e6"},children:"💧 M\\xc0I NƯỚC \xb7 NHẤN ĐỂ M\\xc0I LỘ HOA VĂN"}),'
            '(0,a.jsxs)("small",{style:{fontSize:"12px",color:"#fcedc8"},children:[et," lượt m\\xe0i ho\\xe0n tất \xb7 Đang lộ ",q,"% hoa văn (Nhấn để m\\xe0i tiếp)"]})'
            ']}),'
            '(0,a.jsx)("p",{style:{margin:"10px 0 12px 0",fontSize:"12.5px",lineHeight:"1.5",color:"#553a26"},children:"D\\xf9ng nước kết hợp giấy r\\xe1p/than củi m\\xe0i phẳng bề mặt. Mỗi lượt m\\xe0i l\\xe0m mỏng lớp sơn phủ, gi\\xfap họa tiết v\\xe0 sắc nền b\\xean dưới dần hiện r\\xf5 với chiều s\\xe2u sơn m\\xe0i."}),'
            # SLIDER WITH REALTIME SETCOVERAGE CALL
            '(0,a.jsxs)("label",{className:g().depthControl,style:{margin:"0",display:"flex",alignItems:"center",justifyContent:"space-between",gap:"10px"},children:['
            '(0,a.jsx)("span",{style:{fontSize:"12.5px",fontWeight:"700",color:"#331812"},children:"ĐỘ S\\xc2U M\\xc0I NƯỚC"}),'
            '(0,a.jsx)("input",{type:"range",min:"1",max:"100",value:q,onChange:e=>{let val=Number(e.target.value);O(val);var sRef=es.current;if(sRef&&sRef.setCoverage)sRef.setCoverage(val);},style:{flex:"1"}}),'
            '(0,a.jsxs)("output",{style:{fontWeight:"700",color:"#842022",minWidth:"36px",textAlign:"right"},children:[q,"%"]})'
            ']})'
            ']}),'
        )

        content = content[:start_pos] + new_grind_card + content[end_pos:]
        print(f"[{filepath}] Successfully replaced studio_grind_card with Live Surface Visualizer!")
    else:
        print(f"[{filepath}] Error: could not find studio_grind_card boundaries (start: {start_pos}, end: {end_pos})")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    res = subprocess.run(['node', '-c', filepath], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[{filepath}] Node syntax error:", res.stderr)
        return False
    else:
        print(f"[{filepath}] Node syntax PASSED!")

    return True

def run():
    files = [
        '_next/static/chunks/840-f19fdd306966b2e5.js',
        'ma_nguon_css_js/js/840-f19fdd306966b2e5.js'
    ]
    for f in files:
        if not patch_file(f):
            return False
    return True

if __name__ == '__main__':
    if not run():
        sys.exit(1)
    print("Done patching Stage 4 grind visualizer!")
