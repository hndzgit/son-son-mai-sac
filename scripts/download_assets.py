import urllib.request
import re
import os
import urllib.parse

BASE_URL = 'https://son-son-mai-sac-orpin.vercel.app'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def extract_asset_urls():
    urls = set()
    
    # 1. Look in all raw html files
    for fname in os.listdir('.'):
        if fname.endswith('.html'):
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
                # find /story-assets/..., /textures/..., etc.
                matches = re.findall(r'/(?:story-assets|textures|images)/[a-zA-Z0-9_\-\./]+', content)
                urls.update(matches)
                # find icons
                icons = re.findall(r'/(?:favicon\.svg|apple-touch-icon\.png|favicon\.ico)', content)
                urls.update(icons)

    # 2. Known assets from previous scan
    known = [
        '/story-assets/brand-9782.png',
        '/story-assets/hero-lacquer-generated.webp',
        '/story-assets/key-visual.jpg',
        '/story-assets/mat-gold.jpg',
        '/story-assets/team-workshop-generated.webp',
        '/story-assets/heritage-profiles-v5.webp',
        '/story-assets/macro-hires-generated.webp',
        '/story-assets/mat-egg.jpg',
        '/story-assets/materials-macro-atlas-v1.webp',
        '/story-assets/raw-wood-grain-v1.webp',
        '/story-assets/mat-pigment.jpg',
        '/story-assets/core-bamboo.svg',
        '/story-assets/core-ceramic.svg',
        '/story-assets/core-composite.svg',
        '/story-assets/core-mdf.svg',
        '/story-assets/cotton-scrim.svg',
        '/story-assets/craft-blank-lacquer-generated.webp',
        '/story-assets/event-gallery-generated-v1.webp',
        '/story-assets/event-lacquer-portrait-v7.webp',
        '/story-assets/finder-box-v5.webp',
        '/story-assets/flow-11.jpg',
        '/story-assets/flow-13.jpg',
        '/story-assets/flow-21.jpg',
        '/story-assets/flow-27.jpg',
        '/story-assets/flow-32.jpg',
        '/story-assets/flow-37.jpg',
        '/story-assets/hero-objects-generated.webp',
        '/story-assets/journey-lotus-stencil-v8.webp',
        '/story-assets/lacquer-five-strata-v6.webp',
        '/story-assets/latest-board-reference.webp',
        '/story-assets/lotus-inlay-stencil-v6.webp',
        '/story-assets/mat-pearl.jpg',
        '/story-assets/mat-shell.jpg',
        '/story-assets/mat-silver.jpg',
        '/story-assets/project-ivory-vase-v5.webp',
        '/story-assets/team-members/anh-vu.jpg',
        '/story-assets/team-members/dan-le.jpg',
        '/story-assets/team-members/duy-nghia.jpg',
        '/story-assets/team-members/gia-dat.jpg',
        '/story-assets/team-members/huyen-trang.jpg',
        '/textures/eggshell_crackle.svg',
        '/textures/gold_leaf_texture.svg',
        '/favicon.svg',
        '/apple-touch-icon.png',
        '/story-assets/Inter-Full.ttf',
        '/story-assets/NotoSerif-Full.ttf',
        '/story-assets/PlayfairDisplay-Full.ttf',
        '/story-assets/backgrounds/gold-band-v2.webp',
        '/story-assets/backgrounds/gold-foundation-v2.webp',
        '/story-assets/backgrounds/gold-story-v2.webp',
        '/story-assets/core-material-atlas-generated.webp',
        '/story-assets/kv-gold.jpg',
        '/story-assets/lacquer-gold-background-v1.webp',
        '/story-assets/lotus-linework-overlay-v1.png',
        '/story-assets/portal-mosaic-generated.webp',
        '/story-assets/process-five-stages-v4.webp',
        '/story-assets/team-portraits-generated.webp',
        '/story-assets/box-23.jpg'
    ]
    urls.update(known)
    return sorted(urls)

def download_all():
    urls = extract_asset_urls()
    print(f"Total assets to download: {len(urls)}")
    success = 0
    failed = []
    
    for u in urls:
        clean_path = u.lstrip('/')
        # local target path
        target_path = os.path.join('hinh_anh_assets', clean_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        full_url = BASE_URL + u
        try:
            req = urllib.request.Request(full_url, headers=HEADERS)
            data = urllib.request.urlopen(req).read()
            with open(target_path, 'wb') as f:
                f.write(data)
            print(f"Downloaded: {clean_path} ({len(data)} bytes)")
            success += 1
        except Exception as e:
            print(f"Failed {full_url}: {e}")
            failed.append((full_url, str(e)))
            
    print(f"\nFinished: {success} downloaded, {len(failed)} failed.")
    if failed:
        print("Failed details:", failed)

if __name__ == '__main__':
    download_all()
