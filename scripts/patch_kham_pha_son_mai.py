import sys
import subprocess

def patch_page_js():
    js_path = '_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js'
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sonmai_section_code = r'''function SonMaiSection(){return(0,s.jsxs)("section",{id:"son-mai-la-gi",className:"sonmai-page-wrapper","aria-labelledby":"sonmai-main-title",children:[(0,s.jsxs)("header",{className:"sonmai-header-block",children:[(0,s.jsx)("p",{className:"sonmai-eyebrow",children:"KH\xc1M PH\xc1 \xb7 S\u01a0N SON M\xc0I S\u1eaeC"}),(0,s.jsx)("h2",{id:"sonmai-main-title",className:"sonmai-main-title",children:"S\u01a1n m\xe0i l\xe0 g\xec?"}),(0,s.jsx)("p",{className:"sonmai-lead-quote",children:"M\u1ed9t t\xe1c ph\u1ea9m s\u01a1n m\xe0i \u0111\u01b0\u1ee3c t\u1ea1o n\xean t\u1eeb c\u1ea3 qu\xe1 tr\xecnh ph\u1ee7 l\xean v\xe0 m\xe0i \u0111i."}),(0,s.jsx)("p",{className:"sonmai-lead-body",children:"Trong s\u01a1n m\xe0i, v\u1ebb \u0111\u1eb9p kh\xf4ng ch\u1ec9 n\u1eb1m tr\xean b\u1ec1 m\u1eb7t m\xe0 \u0111\u01b0\u1ee3c h\xecnh th\xe0nh qua nhi\u1ec1u l\u1edbp s\u01a1n, m\xe0u s\u1eafc v\xe0 v\u1eadt li\u1ec7u kh\xe1c nhau. C\xe1c l\u1edbp \u1ea5y \u0111\u01b0\u1ee3c ph\u1ee7 ch\u1ed3ng l\xean nhau, sau \u0111\xf3 ng\u01b0\u1eddi l\xe0m ngh\u1ec1 d\xf9ng k\u1ef9 thu\u1eadt m\xe0i \u0111\u1ec3 t\u1eebng ph\u1ea7n b\xean d\u01b0\u1edbi d\u1ea7n hi\u1ec7n ra. Ch\xednh s\u1ef1 \u0111an xen gi\u1eefa ph\u1ee7 \u2013 m\xe0i \u2013 h\xe9 l\u1ed9 t\u1ea1o n\xean chi\u1ec1u s\xe2u, s\u1eafc \u0111\u1ed9 v\xe0 v\u1ebb \u0111\u1eb9p \u0111\u1eb7c tr\u01b0ng c\u1ee7a b\u1ec1 m\u1eb7t s\u01a1n m\xe0i."}) साइबर ]}),(0,s.jsx)("figure",{className:"sonmai-masterpiece-frame",children:(0,s.jsx)("img",{src:"/story-assets/son-mai-masterpiece.webp",alt:"Ki\u1ec7t t\xe1c tranh s\u01a1n m\xe0i truy\u1ec1n th\u1ed1ng Vi\u1ec7t Nam",width:"1279",height:"543",fetchPriority:"high"})}),(0,s.jsxs)("div",{className:"sonmai-content-rows",children:[(0,s.jsxs)("section",{className:"sonmai-row-grid","aria-labelledby":"vi-sao-title",children:[(0,s.jsxs)("div",{className:"sonmai-text-col",children:[(0,s.jsx)("h3",{id:"vi-sao-title",className:"sonmai-heading",children:"V\xec sao l\u1ea1i l\xe0 \u201cs\u01a1n m\xe0i\u201d?"}),(0,s.jsx)("p",{children:"B\u1edfi c\xf3 nh\u1eefng th\u1ee9 ch\u1ec9 xu\u1ea5t hi\u1ec7n sau khi \u0111\u01b0\u1ee3c m\xe0i \u0111i. Trong qu\xe1 tr\xecnh t\u1ea1o t\xe1c, m\xe0u s\u1eafc v\xe0 v\u1eadt li\u1ec7u c\xf3 th\u1ec3 \u0111\u01b0\u1ee3c \u0111\u1eb7t \u1edf nh\u1eefng \u0111\u1ed9 s\xe2u kh\xe1c nhau r\u1ed3i ti\u1ebfp t\u1ee5c \u0111\u01b0\u1ee3c ph\u1ee7 b\u1eb1ng c\xe1c l\u1edbp s\u01a1n ph\xeda tr\xean."}),(0,s.jsx)("p",{children:"Khi b\u1ec1 m\u1eb7t \u0111\xe3 \u0111\u1ea1t \u0111i\u1ec1u ki\u1ec7n ph\xf9 h\u1ee3p, ng\u01b0\u1eddi th\u1ee3 m\xe0i c\xf9ng n\u01b0\u1edbc, t\u1eebng ch\xfat m\u1ed9t. M\xe0i qu\xe1 \xedt, l\u1edbp b\xean d\u01b0\u1edbi ch\u01b0a xu\u1ea5t hi\u1ec7n; m\xe0i qu\xe1 s\xe2u, chi ti\u1ebft \u0111\xe3 t\u1ea1o tr\u01b0\u1edbc \u0111\xf3 c\xf3 th\u1ec3 b\u1ecb \u1ea3nh h\u01b0\u1edfng."}),(0,s.jsx)("p",{children:"Qua m\u1ed7i l\u1ea7n m\xe0i, nh\u1eefng l\u1edbp t\u1eebng b\u1ecb che khu\u1ea5t d\u1ea7n l\u1ed9 ra: m\u1ed9t m\u1ea3ng m\xe0u, m\u1ed9t \xe1nh v\xe0ng, m\u1ed9t l\u1edbp v\u1ecf tr\u1ee9ng hay d\u1ea5u v\u1ebft c\u1ee7a nh\u1eefng c\xf4ng \u0111o\u1ea1n tr\u01b0\u1edbc \u0111\xf3. M\xe0i v\xec th\u1ebf kh\xf4ng ch\u1ec9 l\xe0m ph\u1eb3ng b\u1ec1 m\u1eb7t. N\xf3 c\xf2n tham gia v\xe0o vi\u1ec7c t\u1ea1o n\xean h\xecnh \u1ea3nh cu\u1ed1i c\xf9ng."}) साइबर ]}),(0,s.jsxs)("div",{className:"sonmai-media-card",children:[(0,s.jsx)("div",{className:"sonmai-media-frame",children:(0,s.jsx)("img",{src:"/story-assets/son-mai-la-gi-mai-nuoc.webp",alt:"K\u1ef9 thu\u1eadt m\xe0i n\u01b0\u1edbc trong ngh\u1ec7 thu\u1eadt s\u01a1n m\xe0i",width:"1196",height:"656",loading:"lazy"})}),(0,s.jsx)("p",{className:"sonmai-caption align-right",children:"Ngu\u1ed3n: artnam"})]})]}),(0,s.jsxs)("section",{className:"sonmai-row-grid reverse-on-mobile","aria-labelledby":"giot-son-title",children:[(0,s.jsxs)("div",{className:"sonmai-media-card",children:[(0,s.jsx)("div",{className:"sonmai-media-frame",children:(0,s.jsx)("img",{src:"/story-assets/son-mai-la-gi-nhua-son.webp",alt:"Khai th\xe1c nh\u1ef1a s\u01a1n ta truy\u1ec1n th\u1ed1ng t\u1ea1i Ph\xfa Th\u1ecd",width:"1266",height:"588",loading:"lazy"})}),(0,s.jsx)("p",{className:"sonmai-caption align-center",children:"Ngu\u1ed3n: nongsandienbien"})]}),(0,s.jsxs)("div",{className:"sonmai-text-col",children:[(0,s.jsx)("h3",{id:"giot-son-title",className:"sonmai-heading",children:"T\u1eeb m\u1ed9t gi\u1ecdt s\u01a1n ta"}),(0,s.jsx)("p",{children:"Tr\u01b0\u1edbc khi tr\u1edf th\xe0nh m\u1ed9t l\u1edbp s\u01a1n, n\xf3 b\u1eaft \u0111\u1ea7u t\u1eeb nh\u1ef1a c\xe2y. M\u1ed9t trong nh\u1eefng ch\u1ea5t li\u1ec7u quan tr\u1ecdng c\u1ee7a s\u01a1n m\xe0i truy\u1ec1n th\u1ed1ng Vi\u1ec7t Nam l\xe0 s\u01a1n ta \u2013 nh\u1ef1a \u0111\u01b0\u1ee3c khai th\xe1c t\u1eeb c\xe2y s\u01a1n, m\u1ed9t lo\u1ea1i c\xe2y \u0111\u01b0\u1ee3c tr\u1ed3ng l\xe2u \u0111\u1eddi t\u1ea1i v\xf9ng trung du B\u1eafc B\u1ed9, trong \u0111\xf3 Ph\xfa Th\u1ecd l\xe0 v\xf9ng n\u1ed5i ti\u1ebfng v\u1edbi ngh\u1ec1 tr\u1ed3ng v\xe0 khai th\xe1c s\u01a1n."}),(0,s.jsx)("p",{children:"Sau khi \u0111\u01b0\u1ee3c khai th\xe1c v\xe0 ch\u1ebf bi\u1ebfn, s\u01a1n ta \u0111\u01b0\u1ee3c s\u1eed d\u1ee5ng trong nhi\u1ec1u c\xf4ng \u0111o\u1ea1n: l\xe0m v\xf3c, g\u1eafn k\u1ebft v\u1eadt li\u1ec7u, ph\u1ee7 c\xe1c l\u1edbp s\u01a1n v\xe0 ho\xe0n thi\u1ec7n b\u1ec1 m\u1eb7t. T\u1eeb m\u1ed9t ch\u1ea5t li\u1ec7u t\u1ef1 nhi\xean, ng\u01b0\u1eddi th\u1ee3 t\u1ea1o n\xean nh\u1eefng l\u1edbp s\u01a1n c\xf3 kh\u1ea3 n\u0103ng k\u1ebft n\u1ed1i v\u1edbi nhau qua c\u1ea3 m\u1ed9t qu\xe1 tr\xecnh d\xe0i."}) साइबर ]}) साइबर ]}) साइबर ]}) साइबर ]})}'''.replace(' साइबर ', '')

    # Find function w()
    old_w_start = 'function w(){let[e,t]=(0,o.useState)(0),n=N[e];return(0,o.useEffect)(()=>{let e=()=>{let e=window.location.hash.match(/^#cong-doan-(\\d)$/);if(e){let n=Number(e[1])-1;n>=0&&n<N.length&&t(n)}};return e(),window.addEventListener("hashchange",e),()=>window.removeEventListener("hashchange",e)},[]),(0,s.jsxs)("section",{id:"5-cong-doan",className:"core-v4-process",'
    
    new_w_start = sonmai_section_code + r'''function w(){let[e,t]=(0,o.useState)(0),n=N[e];return(0,o.useEffect)(()=>{let e=()=>{let e=window.location.hash.match(/^#cong-doan-(\d)$/);if(e){let n=Number(e[1])-1;n>=0&&n<N.length&&t(n)}};let s=()=>{let h=window.location.hash;if(h==="#son-mai-la-gi"||h==="#5-cong-doan"||h==="#process-workshop-panel"){let el=document.querySelector(h);if(el)setTimeout(()=>el.scrollIntoView({behavior:"smooth",block:"start"}),60)}};return e(),s(),window.addEventListener("hashchange",e),window.addEventListener("hashchange",s),()=>{window.removeEventListener("hashchange",e),window.removeEventListener("hashchange",s)}},[]),(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(SonMaiSection,{}),(0,s.jsxs)("section",{id:"5-cong-doan",className:"core-v4-process",'''

    if old_w_start not in content:
        print("ERROR: old_w_start not found!")
        return False

    content = content.replace(old_w_start, new_w_start, 1)

    # Now close Fragment at the end of w
    old_end_marker = 'core-v4-process-illustration",children:"Ảnh minh họa. Chọn một chặng để thao t\\xe1c ngay tr\\xean bề mặt 3D b\\xean dưới."})]})}}'
    new_end_marker = 'core-v4-process-illustration",children:"Ảnh minh họa. Chọn một chặng để thao t\\xe1c ngay tr\\xean bề mặt 3D b\\xean dưới."})]})]})}}'

    if old_end_marker not in content:
        print("ERROR: old_end_marker not found!")
        return False

    content = content.replace(old_end_marker, new_end_marker, 1)

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Patched", js_path)
    return True

if __name__ == '__main__':
    if patch_page_js():
        res = subprocess.run(['node', '-c', '_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js'])
        if res.returncode == 0:
            print("Syntax check PASSED!")
        else:
            print("Syntax check FAILED!")
            sys.exit(1)
