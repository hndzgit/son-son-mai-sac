import os
import subprocess
import sys

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add uGrindDepth and uIsGrindStage uniforms in shader definition
    old_uniform_decl = 'uniform float uWaterDroplets;\\n  uniform float uCoatLayers;\\n\\n  varying vec2 vUv;'
    new_uniform_decl = 'uniform float uWaterDroplets;\\n  uniform float uCoatLayers;\\n  uniform float uGrindDepth;\\n  uniform float uIsGrindStage;\\n\\n  varying vec2 vUv;'

    if old_uniform_decl in content:
        content = content.replace(old_uniform_decl, new_uniform_decl, 1)
        print(f"[{filepath}] Added uniform declarations to fragment shader")
    else:
        print(f"[{filepath}] Warning: old_uniform_decl not found!")

    # 2. Update rawDepth calculation in fragment shader
    old_raw_depth = (
        'float rawDepth = texture2D(uMaskMap, vUv).r * (1.0 - uCompareBefore);\\n'
        '    if (uPreparation > 0.5) rawDepth = 180.0 / 255.0;\\n'
    )
    new_raw_depth = (
        'float rawDepth = texture2D(uMaskMap, vUv).r * (1.0 - uCompareBefore);\\n'
        '    if (uPreparation > 0.5) {\\n'
        '      rawDepth = 180.0 / 255.0;\\n'
        '    } else if (uIsGrindStage > 0.5) {\\n'
        '      float swirl = 0.5 + 0.5 * sin(vUv.x * 65.0 + sin(vUv.y * 55.0) * 3.5);\\n'
        '      float baseGrind = uGrindDepth * (0.85 + 0.15 * swirl);\\n'
        '      rawDepth = max(rawDepth, baseGrind);\\n'
        '    } else {\\n'
        '      rawDepth = 180.0 / 255.0;\\n'
        '    }\\n'
    )

    if old_raw_depth in content:
        content = content.replace(old_raw_depth, new_raw_depth, 1)
        print(f"[{filepath}] Updated rawDepth calculation in fragment shader")
    else:
        print(f"[{filepath}] Warning: old_raw_depth not found!")

    # 3. Add uGrindDepth and uIsGrindStage to uniforms map
    old_uniforms_map = 'uWaterDroplets:{value:1},uCoatLayers:{value:0}}'
    new_uniforms_map = 'uWaterDroplets:{value:1},uCoatLayers:{value:0},uGrindDepth:{value:.48},uIsGrindStage:{value:0}}'

    if old_uniforms_map in content:
        content = content.replace(old_uniforms_map, new_uniforms_map, 1)
        print(f"[{filepath}] Added uniforms to material uniform map")
    else:
        print(f"[{filepath}] Warning: old_uniforms_map not found!")

    # 4. Update eM loop to set uGrindDepth and uIsGrindStage
    old_em_coat = 'O.uniforms.uCoatLayers.value=null!==(r=f.coatLayers)&&void 0!==r?r:0,'
    new_em_coat = (
        'O.uniforms.uCoatLayers.value=null!==(r=f.coatLayers)&&void 0!==r?r:0,'
        'O.uniforms.uGrindDepth.value=(null!==f.depth&&void 0!==f.depth?f.depth:48)/100,'
        'O.uniforms.uIsGrindStage.value=("sand"===f.mode||4===f.stage||(f.coatLayers&&f.coatLayers>0))?1:0,'
    )

    if old_em_coat in content:
        content = content.replace(old_em_coat, new_em_coat, 1)
        print(f"[{filepath}] Updated eM animation loop to update uGrindDepth and uIsGrindStage")
    else:
        print(f"[{filepath}] Warning: old_em_coat not found!")

    # 5. Enhance setCoverage in controller.current to create authentic radial grind in mask
    old_set_cov = (
        'setCoverage:e=>{en(),h.fillStyle="#000",h.fillRect(0,0,512,512),h.fillStyle="#b4b4b4",'
        'h.fillRect(0,0,Math.max(0,Math.min(100,e))/100*512,512),N.needsUpdate=!0,eo()}'
    )
    new_set_cov = (
        'setCoverage:e=>{en();let dRatio=Math.max(0,Math.min(100,e))/100;'
        'h.fillStyle="#000";h.fillRect(0,0,512,512);'
        'let g=h.createRadialGradient(256,256,20,256,256,256);'
        'g.addColorStop(0,"rgba(230,230,230,"+Math.min(1,dRatio*1.2)+")");'
        'g.addColorStop(0.7,"rgba(180,180,180,"+dRatio+")");'
        'g.addColorStop(1,"rgba(100,100,100,"+(dRatio*0.7)+")");'
        'h.fillStyle=g;h.fillRect(0,0,512,512);'
        'N.needsUpdate=!0;eo()}'
    )

    if old_set_cov in content:
        content = content.replace(old_set_cov, new_set_cov, 1)
        print(f"[{filepath}] Updated controller.setCoverage to realistic radial abrasion")
    else:
        print(f"[{filepath}] Warning: old_set_cov not found!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Verify node syntax
    res = subprocess.run(['node', '-c', filepath], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[{filepath}] Node syntax error:", res.stderr)
        return False
    else:
        print(f"[{filepath}] Node syntax PASSED!")

    return True

def run():
    files = [
        '_next/static/chunks/648.013156edff3e7a3c.js',
        'ma_nguon_css_js/js/648.013156edff3e7a3c.js'
    ]
    for f in files:
        if not patch_file(f):
            return False
    return True

if __name__ == '__main__':
    if not run():
        sys.exit(1)
    print("Done patching 3D grinding reveal!")
