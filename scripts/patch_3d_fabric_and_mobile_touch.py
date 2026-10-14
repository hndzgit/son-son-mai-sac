import os
import subprocess
import sys

def patch_840():
    paths = [
        '_next/static/chunks/840-f19fdd306966b2e5.js',
        'ma_nguon_css_js/js/840-f19fdd306966b2e5.js'
    ]
    
    for path in paths:
        if not os.path.exists(path):
            print(f"Skipping {path} (not found)")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. In function K(e), extract reinforced:k_reinf=!1
        s1_old = 'coreMaterial:g="Gỗ",finish:p'
        s1_new = 'coreMaterial:g="Gỗ",reinforced:k_reinf=!1,finish:p'
        if s1_old in content:
            content = content.replace(s1_old, s1_new, 1)
            print(f"[{path}] Injected reinforced:k_reinf into K(e) props")
        elif 'reinforced:k_reinf' in content:
            print(f"[{path}] reinforced:k_reinf already in K(e) props")
        else:
            print(f"[{path}] ERROR: s1_old not found!")
            return False

        # 2. In K(e) JSX, pass reinforced:k_reinf to E
        s2_old = 'appearance:u,coreMaterial:g,preparationStep:v,'
        s2_new = 'appearance:u,coreMaterial:g,reinforced:k_reinf,preparationStep:v,'
        if s2_old in content:
            content = content.replace(s2_old, s2_new, 1)
            print(f"[{path}] Passed reinforced:k_reinf to <E />")
        elif 'reinforced:k_reinf' in content:
            print(f"[{path}] reinforced:k_reinf already passed to <E />")
        else:
            print(f"[{path}] ERROR: s2_old not found!")
            return False

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully patched {path}")

    # Syntax check
    res = subprocess.run(['node', '-c', '_next/static/chunks/840-f19fdd306966b2e5.js'])
    if res.returncode != 0:
        print("Syntax error in 840 chunk!")
        return False
    print("Chunk 840 syntax PASSED!")
    return True


def patch_648():
    paths = [
        '_next/static/chunks/648.013156edff3e7a3c.js',
        'ma_nguon_css_js/js/648.013156edff3e7a3c.js'
    ]

    for path in paths:
        if not os.path.exists(path):
            print(f"Skipping {path} (not found)")
            continue

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Update fabric texture in w() to an authentic, clearly visible cotton/linen weave
        t1_old = 'if(r&&n<2){s.fillStyle="rgba(226,214,187,.2)",s.fillRect(0,0,1536,1024);for(let e=0;e<1536;e+=9)s.strokeStyle=e%18?"rgba(88,68,48,.24)":"rgba(255,248,226,.42)",s.lineWidth=2.1,s.beginPath(),s.moveTo(e,0),s.lineTo(e,1024),s.stroke(),e<1024&&(s.beginPath(),s.moveTo(0,e),s.lineTo(1536,e),s.stroke());s.fillStyle="rgba(83,62,43,.18)";for(let e=4;e<1024;e+=18)for(let t=4+(e%2?4:0);t<1536;t+=18)s.fillRect(t,e,2,2)}'
        t1_new = 'if(r&&n<2){s.fillStyle="rgba(218,203,174,.85)",s.fillRect(0,0,1536,1024);for(let e=0;e<1536;e+=8)s.strokeStyle=e%16?"rgba(102,76,50,.35)":"rgba(255,248,228,.55)",s.lineWidth=2.2,s.beginPath(),s.moveTo(e,0),s.lineTo(e,1024),s.stroke();for(let e=0;e<1024;e+=8)s.strokeStyle=e%16?"rgba(102,76,50,.35)":"rgba(255,248,228,.55)",s.lineWidth=2.2,s.beginPath(),s.moveTo(0,e),s.lineTo(1536,e),s.stroke();s.fillStyle="rgba(88,62,38,.28)";for(let e=4;e<1024;e+=16)for(let t=4+(e%2?4:0);t<1536;t+=16)s.fillRect(t,e,3,3)}'
        if t1_old in content:
            content = content.replace(t1_old, t1_new, 1)
            print(f"[{path}] Updated fabric texture in w()")
        elif 'rgba(218,203,174,.85)' in content:
            print(f"[{path}] Fabric texture already updated in w()")
        else:
            print(f"[{path}] ERROR: t1_old not found!")
            return False

        # 2. Canvas touchAction: "none"
        t2_old = 'style:{touchAction:"orbit"===e.mode?"pan-y":"none"}'
        t2_new = 'style:{touchAction:"none"}'
        if t2_old in content:
            content = content.replace(t2_old, t2_new, 1)
            print(f"[{path}] Changed canvas touchAction to 'none'")
        elif 'touchAction:"none"' in content:
            print(f"[{path}] Canvas touchAction already 'none'")
        else:
            print(f"[{path}] WARNING: t2_old not found!")

        # 3. DevicePixelRatio optimization for mobile
        t3_old = 'o.setPixelRatio(Math.min(devicePixelRatio,2))'
        t3_new = 'o.setPixelRatio(Math.min(typeof window!=="undefined"&&window.innerWidth<768?1.5:2,window.devicePixelRatio||1))'
        if t3_old in content:
            content = content.replace(t3_old, t3_new, 1)
            print(f"[{path}] Optimized setPixelRatio for mobile")
        elif 'window.innerWidth<768?1.5:2' in content:
            print(f"[{path}] setPixelRatio already optimized")
        else:
            print(f"[{path}] WARNING: t3_old not found!")

        # 4. Mobile touch rotation responsiveness & prevent default
        t4_old = 'if("orbit"===k.current.mode)x=!0,s.dataset.orbitTouched="true",J.rotation.y+=(e.clientX-M.x)*.008,J.rotation.x=l.M8C.clamp(J.rotation.x+(e.clientY-M.y)*.005,-Math.PI,Math.PI);'
        t4_new = 'if("orbit"===k.current.mode){let isMob=typeof window!=="undefined"&&window.innerWidth<768;x=!0,s.dataset.orbitTouched="true",J.rotation.y+=(e.clientX-M.x)*(isMob?.013:.008),J.rotation.x=l.M8C.clamp(J.rotation.x+(e.clientY-M.y)*(isMob?.008:.005),-Math.PI/2.2,Math.PI/2.2);}'
        if t4_old in content:
            content = content.replace(t4_old, t4_new, 1)
            print(f"[{path}] Enhanced orbit rotation sensitivity for mobile")
        elif 'isMob?.013:.008' in content:
            print(f"[{path}] Orbit rotation sensitivity already enhanced")
        else:
            print(f"[{path}] WARNING: t4_old not found!")

        # 5. Safe pointer capture
        t5_old = '0===e.button&&(i.setPointerCapture(e.pointerId),'
        t5_new = '0===e.button&&(function(){try{i.setPointerCapture(e.pointerId)}catch(t){}}(),'
        if t5_old in content:
            content = content.replace(t5_old, t5_new, 1)
            print(f"[{path}] Made pointer capture safe")
        elif 'try{i.setPointerCapture' in content:
            print(f"[{path}] Pointer capture already safe")

        # 6. Prevent default during active pointer dragging
        t6_old = 'let eh=e=>{if(w){if(ed.has(e.pointerId)'
        t6_new = 'let eh=e=>{if(w){try{e.preventDefault()}catch(t){}if(ed.has(e.pointerId)'
        if t6_old in content:
            content = content.replace(t6_old, t6_new, 1)
            print(f"[{path}] Added preventDefault to eh during drag")
        elif 'try{e.preventDefault()}catch(t){}if(ed.has(e.pointerId)' in content:
            print(f"[{path}] preventDefault already added to eh")

        # 7. Add native touchmove preventDefault listener to canvas
        t7_old = 'i.addEventListener("pointerdown",ep),'
        t7_new = 'i.addEventListener("touchmove",function(e){e.preventDefault()},{passive:!1}),i.addEventListener("pointerdown",ep),'
        if t7_old in content:
            content = content.replace(t7_old, t7_new, 1)
            print(f"[{path}] Added passive:false touchmove listener")
        elif 'addEventListener("touchmove"' in content:
            print(f"[{path}] touchmove listener already present")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully patched {path}")

    # Syntax check
    res = subprocess.run(['node', '-c', '_next/static/chunks/648.013156edff3e7a3c.js'])
    if res.returncode != 0:
        print("Syntax error in 648 chunk!")
        return False
    print("Chunk 648 syntax PASSED!")
    return True


def patch_css():
    css_path = '_next/static/css/7d5ed180c1fe36fd.css'
    if not os.path.exists(css_path):
        print("CSS not found!")
        return False
        
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()

    css_rule = (
        '\n/* Mobile 3D Smooth Touch Orbit & Canvas Optimization */\n'
        '.productExperience_viewer__V3Heb canvas,\n'
        '.lacquer-surface-live canvas,\n'
        '.productExperience_viewer__V3Heb,\n'
        '.lacquer-surface-live {\n'
        '  touch-action: none !important;\n'
        '  -webkit-touch-callout: none !important;\n'
        '  -webkit-user-select: none !important;\n'
        '  user-select: none !important;\n'
        '}\n'
    )

    if '/* Mobile 3D Smooth Touch Orbit & Canvas Optimization */' not in css:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(css_rule)
        print(f"Appended touch-action rules to {css_path}")
    else:
        print("CSS touch-action rule already present")
    return True


if __name__ == '__main__':
    ok840 = patch_840()
    ok648 = patch_648()
    okcss = patch_css()
    if ok840 and ok648 and okcss:
        print("\nALL PATCHES SUCCESSFULLY APPLIED AND VALIDATED!")
    else:
        print("\nSOME PATCHES FAILED!")
        sys.exit(1)
