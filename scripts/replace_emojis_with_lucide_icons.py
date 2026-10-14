import os
import subprocess
import sys

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Icons declaration
    old_c_decl = 'let c=(0,l.Z)("Rotate3d",[["path",{d:"M16.466 7.5C15.643 4.237 13.952 2 12 2 9.239 2 7 6.477 7 12s2.239 10 5 10c.342 0 .677-.069 1-.2",key:"10n0gc"}],["path",{d:"m15.194 13.707 3.814 1.86-1.86 3.814",key:"16shm9"}],["path",{d:"M19 15.57c-1.804.885-4.274 1.43-7 1.43-5.523 0-10-2.239-10-5s4.477-5 10-5c4.838 0 8.873 1.718 9.8 4",key:"1lxi77"}]]);'
    icons_decl = (
        'let w_droplets=(0,l.Z)("Droplets",[["path",{d:"M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z",key:"dr1"}],["path",{d:"M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97",key:"dr2"}]]);'
        'let w_sparkles=(0,l.Z)("Sparkles",[["path",{d:"m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z",key:"sp1"}],["path",{d:"M5 3v4",key:"sp2"}],["path",{d:"M19 17v4",key:"sp3"}],["path",{d:"M3 5h4",key:"sp4"}],["path",{d:"M17 19h4",key:"sp5"}]]);'
        'let w_check=(0,l.Z)("Check",[["polyline",{points:"20 6 9 17 4 12",key:"ck1"}]]);'
        'let w_eye=(0,l.Z)("Eye",[["path",{d:"M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z",key:"ey1"}],["circle",{cx:"12",cy:"12",r:"3",key:"ey2"}]]);'
    )

    if 'w_droplets' not in content:
        if old_c_decl in content:
            content = content.replace(old_c_decl, old_c_decl + icons_decl, 1)
            print(f"[{filepath}] Added icon definitions")
        else:
            print(f"[{filepath}] Error: old_c_decl not found")
            return False

    # 2. Eye button
    old_eye = '(0,a.jsx)("button",{type:"button",onClick:()=>{var el=document.getElementById("simulator")||document.querySelector("div[class*=\'viewer\']");if(el)el.scrollIntoView({behavior:"smooth",block:"center"})},style:{background:"rgba(222,184,90,0.15)",border:"1px solid rgba(222,184,90,0.4)",color:"#fcedc8",fontSize:"10.5px",padding:"2px 8px",borderRadius:"4px",cursor:"pointer"},children:"👁 Xem 3D"})'
    new_eye = '(0,a.jsxs)("button",{type:"button",onClick:()=>{var el=document.getElementById("simulator")||document.querySelector("div[class*=\'viewer\']");if(el)el.scrollIntoView({behavior:"smooth",block:"center"})},style:{display:"inline-flex",alignItems:"center",gap:"5px",background:"rgba(222,184,90,0.14)",border:"1px solid rgba(222,184,90,0.38)",color:"#fcedc8",fontSize:"11px",padding:"3px 9px",borderRadius:"4px",cursor:"pointer"},children:[(0,a.jsx)(w_eye,{size:13,style:{color:"#deb85a"}}),"Xem 3D"]})'
    if old_eye in content:
        content = content.replace(old_eye, new_eye, 1)
        print(f"[{filepath}] Replaced 👁 Xem 3D")
    else:
        print(f"[{filepath}] Warning: old_eye not found")

    # 3. Status pill
    old_status = '(0,a.jsx)("span",{children:q<=15?"🔴 Lớp sơn phủ k\\xedn (Chưa m\\xe0i) · Họa tiết đang ẩn":q>=85?"✨ M\\xe0i ho\\xe0n tất · Hoa văn lộ r\\xf5 n\\xe9t & s\\xe1ng b\\xf3ng":"💧 Đang m\\xe0i nước: Lộ "+q+"% hoa văn · Vỏ trứng & V\\xe0ng quỳ đang dần hiện"})'
    new_status = (
        'q<=15?(0,a.jsx)("span",{style:{width:"7px",height:"7px",borderRadius:"50%",background:"#d97706",display:"inline-block",flexShrink:0}}):'
        'q>=85?(0,a.jsx)(w_check,{size:13,style:{color:"#4ade80",flexShrink:0}}):'
        '(0,a.jsx)(w_droplets,{size:13,style:{color:"#38bdf8",flexShrink:0}}),'
        '(0,a.jsx)("span",{style:{whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"},children:'
        'q<=15?"Lớp sơn phủ k\\xedn (Chưa m\\xe0i) · Họa tiết đang ẩn":'
        'q>=85?["M\\xe0i ho\\xe0n tất (",q,"%) · Hoa văn lộ r\\xf5 n\\xe9t"]:'
        '["Đang m\\xe0i nước (",q,"%): Họa tiết & sắc nền dần hiện"]})'
    )
    if old_status in content:
        content = content.replace(old_status, new_status, 1)
        print(f"[{filepath}] Replaced status pill")
    else:
        print(f"[{filepath}] Warning: old_status not found")

    # 4. Grind button label
    old_grind = '(0,a.jsx)("span",{style:{fontSize:"15px",fontWeight:"800",letterSpacing:"0.04em",color:"#fff5e6"},children:"💧 M\\xc0I NƯỚC · NHẤN ĐỂ M\\xc0I LỘ HOA VĂN"})'
    new_grind = '(0,a.jsxs)("span",{style:{display:"inline-flex",alignItems:"center",gap:"8px",fontSize:"14.5px",fontWeight:"700",letterSpacing:"0.04em",color:"#fff5e6"},children:[(0,a.jsx)(w_droplets,{size:16,style:{color:"#deb85a"}}),"M\\xc0I NƯỚC · NHẤN ĐỂ M\\xc0I LỘ HOA VĂN"]})'
    if old_grind in content:
        content = content.replace(old_grind, new_grind, 1)
        print(f"[{filepath}] Replaced grind button label")
    else:
        print(f"[{filepath}] Warning: old_grind not found")

    # 5. Polish label in stage 5
    old_polish = '(0,a.jsx)("strong",{children:"✨ Đ\\xe1nh b\\xf3ng"})'
    new_polish = '(0,a.jsxs)("strong",{style:{display:"inline-flex",alignItems:"center",gap:"6px"},children:[(0,a.jsx)(w_sparkles,{size:14,style:{color:"#deb85a"}}),"Đ\\xe1nh b\\xf3ng"]})'
    if old_polish in content:
        content = content.replace(old_polish, new_polish, 1)
        print(f"[{filepath}] Replaced polish label")
    else:
        print(f"[{filepath}] Warning: old_polish not found")

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
    print("ALL SUCCESS!")
