#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

FONT_FACE_BLOCK = """
@font-face {
  font-family: "Project Display";
  src: url("/story-assets/playfair-vietnamese-v40.woff2") format("woff2"),
       url("/story-assets/playfair-latin-v40.woff2") format("woff2"),
       url("/story-assets/PlayfairDisplay-Full.ttf") format("truetype");
  font-weight: 400 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "Playfair Display";
  src: url("/story-assets/playfair-vietnamese-v40.woff2") format("woff2"),
       url("/story-assets/playfair-latin-v40.woff2") format("woff2"),
       url("/story-assets/PlayfairDisplay-Full.ttf") format("truetype");
  font-weight: 400 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "Heritage";
  src: url("/story-assets/playfair-vietnamese-v40.woff2") format("woff2"),
       url("/story-assets/playfair-latin-v40.woff2") format("woff2"),
       url("/story-assets/PlayfairDisplay-Full.ttf") format("truetype");
  font-weight: 400 900;
  font-style: normal;
  font-display: swap;
}
"""

HEADING_RULES_BLOCK = """
/* ==================== VIETNAMESE TYPOGRAPHY & KERNING ENGINE FIX ==================== */
h1, h2, h3, h4, h5, h6, .font-display,
.story_hero__754VY h1,
.story_storyTitleWide__dDlnR,
.story_storyTitleNarrow__jseWg,
.coreIntroduction_processTitle__Y5ZSn,
#lacquer-title, #process-heading, #layers-title, #core-v4-heritage-title,
.craftJourney_entry__YVr2U h1, .events_heroTitle__Y1W2y h1,
.about_heroTitle__Yx78I, .projectIntro_title__oV5wW {
  font-family: "Project Display", "Playfair Display", "Heritage", "Noto Serif", "Times New Roman", Times, serif !important;
  font-weight: 600 !important;
  letter-spacing: normal !important;
  font-kerning: normal !important;
  font-optical-sizing: auto !important;
  font-feature-settings: "kern" 1, "liga" 1, "ccmp" 1 !important;
  text-rendering: optimizeLegibility !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
}

.story_hero__754VY h1 {
  font-size: clamp(30px, 4vw, 54px) !important;
  line-height: 1.16 !important;
  text-align: center !important;
  color: #8b2a2a !important;
}
"""

INLINE_HTML_STYLE = f"""<style id="vietnamese-typography-fix">
{FONT_FACE_BLOCK}
{HEADING_RULES_BLOCK}
</style>"""

PRELOAD_TAGS = (
    '<link rel="preload" href="/story-assets/playfair-vietnamese-v40.woff2" as="font" type="font/woff2" crossorigin="anonymous"/>\n'
    '<link rel="preload" href="/story-assets/playfair-latin-v40.woff2" as="font" type="font/woff2" crossorigin="anonymous"/>'
)

def fix_css_files():
    css_files = glob.glob(os.path.join(BASE_DIR, '_next/static/css/*.css')) + \
                glob.glob(os.path.join(BASE_DIR, 'ma_nguon_css_js/css/*.css'))
    
    for cpath in css_files:
        with open(cpath, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content
        
        # 1. Replace Georgia with safe Vietnamese serif stack
        content = re.sub(
            r'Heritage\s*,\s*Georgia\s*,\s*serif',
            '"Project Display","Playfair Display","Heritage","Noto Serif","Times New Roman",Times,serif',
            content
        )
        content = re.sub(
            r'"Project Display"\s*,\s*"Playfair Display"\s*,\s*Georgia\s*,\s*serif',
            '"Project Display","Playfair Display","Heritage","Noto Serif","Times New Roman",Times,serif',
            content
        )
        content = re.sub(
            r'"Noto Serif"\s*,\s*Georgia\s*,\s*serif',
            '"Noto Serif","Times New Roman",Times,serif',
            content
        )
        content = re.sub(
            r'Georgia\s*,\s*serif',
            '"Times New Roman",Times,"Noto Serif",serif',
            content
        )

        # 2. Add FONT_FACE_BLOCK if not present
        if 'font-family: "Heritage"' not in content and 'font-family:"Heritage"' not in content:
            content = FONT_FACE_BLOCK + '\n' + content

        # 3. Add HEADING_RULES_BLOCK at end of file if not present
        if '/* ==================== VIETNAMESE TYPOGRAPHY' not in content:
            content = content + '\n' + HEADING_RULES_BLOCK

        if content != orig:
            with open(cpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated CSS: {os.path.relpath(cpath, BASE_DIR)}")

def fix_html_files():
    html_files = [
        'index.html',
        'kham-pha/index.html',
        'cau-chuyen-son-mai/index.html',
        'trai-nghiem/index.html',
        'trai-nghiem/hanh-trinh/index.html',
        'san-pham/index.html',
        'tin-tuc-su-kien/index.html',
        've-du-an/index.html',
        'son-mai-la-gi/index.html',
        'tu-chinh/index.html'
    ]
    # Add article pages
    article_htmls = glob.glob(os.path.join(BASE_DIR, 'cau-chuyen-son-mai/**/*.html'), recursive=True)
    for ah in article_htmls:
        rel = os.path.relpath(ah, BASE_DIR)
        if rel not in html_files:
            html_files.append(rel)

    for hrel in html_files:
        hpath = os.path.join(BASE_DIR, hrel)
        if not os.path.exists(hpath):
            continue
        with open(hpath, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content

        # 1. Inject preloads before any stylesheet if not already present
        if 'playfair-vietnamese-v40.woff2' not in content:
            if '<link rel="stylesheet"' in content:
                content = content.replace(
                    '<link rel="stylesheet"',
                    PRELOAD_TAGS + '\n<link rel="stylesheet"',
                    1
                )
            elif '</head>' in content:
                content = content.replace('</head>', PRELOAD_TAGS + '\n</head>')

        # 2. Inject or replace inline style fix
        if 'id="vietnamese-typography-fix"' in content:
            content = re.sub(
                r'<style id="vietnamese-typography-fix">.*?</style>',
                INLINE_HTML_STYLE,
                content,
                flags=re.DOTALL
            )
        else:
            if '</head>' in content:
                content = content.replace('</head>', INLINE_HTML_STYLE + '\n</head>')

        # 3. Replace any lingering Georgia in inline styles
        content = content.replace('Georgia, serif', '"Times New Roman", Times, "Noto Serif", serif')
        content = content.replace('Georgia,serif', '"Times New Roman",Times,"Noto Serif",serif')

        if content != orig:
            with open(hpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated HTML: {hrel}")

if __name__ == '__main__':
    fix_css_files()
    fix_html_files()
    print("All Vietnamese typography fixes applied successfully!")
