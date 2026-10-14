#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. Remove redundant 'XƯỞNG SƠN MÀI SẮC' (#simulator) from /trai-nghiem
2. Update all references pointing to /trai-nghiem#simulator to /kham-pha#process-workshop-panel
3. Optimize water grinding / sanding simulation in chunk 648 and chunk 840
"""

import os
import subprocess

def optimize_chunk_648(filepath):
    print(f"Optimizing chunk 648 in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Enhance pass() and add sand() on controller.current
    old_pass = 'pass:()=>{en();let e=.15+S++%7*.1;for(let t=0;t<4;t++)el(new l.FM8(.12,e),new l.FM8(.88,e));eo()}'
    new_pass = (
        'pass:()=>{'
        'en();'
        'let row=.18+S++%5*.14;'
        'for(let t=0;t<3;t++){'
        'el(new l.FM8(.15,row),new l.FM8(.85,row));'
        'el(new l.FM8(row,.15),new l.FM8(row,.85));'
        '}'
        'for(let a=0;a<6.28;a+=1.25){'
        'el(new l.FM8(.5+Math.cos(a)*.26,.5+Math.sin(a)*.26),new l.FM8(.5+Math.cos(a+1.25)*.26,.5+Math.sin(a+1.25)*.26));'
        '}'
        'eo();'
        'if(ee&&ee.startSanding){'
        'ee.startSanding(1.2);'
        'setTimeout(()=>{if(ee&&ee.stopSanding)ee.stopSanding();},450);'
        '}'
        '},'
        'sand:function(){return this.pass()}'
    )

    if old_pass not in code:
        raise ValueError(f"old_pass not found in {filepath}")
    code = code.replace(old_pass, new_pass, 1)

    # 2. Enhance water sheen on abraded surface in sand mode
    old_water = 'O.uniforms.uWaterDroplets.value="sand"===f.mode&&w?.6:0;'
    new_water = 'O.uniforms.uWaterDroplets.value="sand"===f.mode?(w?.85:.42):0;'
    if old_water not in code:
        raise ValueError(f"old_water not found in {filepath}")
    code = code.replace(old_water, new_water, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Successfully optimized {filepath}")

def optimize_chunk_840(filepath):
    print(f"Optimizing chunk 840 in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    old_sand_click = (
        'null===(e=es.current)||void 0===e||e.sand&&e.sand(),'
        'B("Đang dùng mài nước. Kéo trên vùng đã phủ để mài phẳng và lộ lớp màu.")}'
    )
    new_sand_click = (
        'var sRef=es.current;if(sRef){if(sRef.pass)sRef.pass();else if(sRef.sand)sRef.sand()}'
        'let msgs=["Đang mài nước: Lớp sơn trong mờ dần, các mảng vỏ trứng và bụi vàng quỳ bắt đầu ánh lên.",'
        '"Đang mài nước: Bề mặt phẳng mịn, các đường nét hoa văn và sắc nền hiện rõ độ sâu.",'
        '"Nước mài hoàn thiện: Bề mặt đã lộ đều các lớp họa tiết và sắc nền, sẵn sàng đánh bóng."];'
        'B(msgs[Math.min(msgs.length-1,Math.floor(et/2))])}'
    )

    if old_sand_click not in code:
        raise ValueError(f"old_sand_click not found in {filepath}")
    code = code.replace(old_sand_click, new_sand_click, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Successfully optimized {filepath}")

def remove_simulator_from_trai_nghiem():
    # 1. Update trai-nghiem/index.html
    html_path = 'trai-nghiem/index.html'
    print(f"Removing simulator section from {html_path}...")
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    start_tag = '<section id="simulator"'
    end_tag = '</section></div></main>'
    idx_start = html.find(start_tag)
    if idx_start != -1:
        idx_end = html.find(end_tag, idx_start)
        if idx_end != -1:
            # Cut from idx_start up to idx_end + len('</section>')
            html = html[:idx_start] + html[idx_end + len('</section>'):]
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print("Successfully removed simulator section from trai-nghiem/index.html")
        else:
            print("WARNING: end_tag not found in trai-nghiem/index.html")
    else:
        print("simulator section already removed from trai-nghiem/index.html")

    # 2. Update trai-nghiem page bundle
    for p in ['_next/static/chunks/app/trai-nghiem/page-4cfd64a621149b8e.js', 'ma_nguon_css_js/js/app_trai-nghiem_page-4cfd64a621149b8e.js']:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
            old_mod = '1184:function(e,t,i){"use strict";i.d(t,{default:function(){return s}});var n=i(3890),a=i(5840);function s(){return(0,n.jsx)(a.Zp,{})}}'
            new_mod = '1184:function(e,t,i){"use strict";i.d(t,{default:function(){return s}});function s(){return null}}'
            if old_mod in content:
                content = content.replace(old_mod, new_mod, 1)
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Successfully updated module 1184 in {p}")

def update_simulator_links():
    print("Updating all /trai-nghiem#simulator links to /kham-pha#process-workshop-panel...")
    updated_files = 0
    for root, dirs, files in os.walk('.'):
        if 'kiem_tra' in root or 'trang_html_goc' in root or '.git' in root:
            continue
        for f in files:
            if f.endswith(('.html', '.js')) and not f.startswith('.'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8') as fl:
                        cnt = fl.read()
                    if '/trai-nghiem#simulator' in cnt:
                        cnt = cnt.replace('/trai-nghiem#simulator', '/kham-pha#process-workshop-panel')
                        with open(path, 'w', encoding='utf-8') as fl:
                            fl.write(cnt)
                        updated_files += 1
                except Exception as e:
                    pass
    print(f"Updated links in {updated_files} files.")

if __name__ == '__main__':
    optimize_chunk_648('_next/static/chunks/648.013156edff3e7a3c.js')
    optimize_chunk_648('ma_nguon_css_js/js/648.013156edff3e7a3c.js')

    optimize_chunk_840('_next/static/chunks/840-f19fdd306966b2e5.js')
    optimize_chunk_840('ma_nguon_css_js/js/840-f19fdd306966b2e5.js')

    remove_simulator_from_trai_nghiem()
    update_simulator_links()

    print("Verifying JS syntax with node -c...")
    subprocess.run(['node', '-c', '_next/static/chunks/648.013156edff3e7a3c.js'], check=True)
    subprocess.run(['node', '-c', '_next/static/chunks/840-f19fdd306966b2e5.js'], check=True)
    subprocess.run(['node', '-c', '_next/static/chunks/app/trai-nghiem/page-4cfd64a621149b8e.js'], check=True)
    print("ALL OPTIMIZATIONS COMPLETED AND SYNTAX VERIFIED!")
