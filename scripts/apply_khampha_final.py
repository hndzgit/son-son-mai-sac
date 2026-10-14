# -*- coding: utf-8 -*-
"""
Apply precise edits for /kham-pha:
1. Title:
   'QUA TỪNG LỚP,<br/>VẺ ĐẸP DẦN HIỆN RA.'
   (or Sentence Case if preferred, let's test both)
2. Lead copy:
   'Khám phá cách một tác phẩm sơn mài được tạo nên qua những lớp sơn, vật liệu và bàn tay người thợ.'
3. Action CTA Button:
   'Tạo nên sắc sơn mài của riêng bạn ⟶'
   plus note: 'Trải nghiệm khoảng 3–5 phút · Có tương tác'
4. Clearer background image:
   Restore authentic /story-assets/key-visual.jpg (with rooster, circle lotus, cat, vase)
   Set opacity: 0.72 - 0.75 in .explore_intro__ycC8w:after
   Smooth gradient mask so text remains clear while lacquer artwork is vivid
5. Update HTML static markup, Next.js hydration flight stream (__next_f), RSC payload, and guardian script synchronously to ensure 0 hydration error.
"""
import re
import os

HTML_PATH = 'kham-pha/index.html'
RSC_PATH = 'rsc_payloads/kham-pha.rsc'
CSS_PATHS = [
    '_next/static/css/7d5ed180c1fe36fd.css',
    'ma_nguon_css_js/css/7d5ed180c1fe36fd.css'
]

def apply_updates(title_uppercase=True, bg_opacity=0.75):
    if title_uppercase:
        h1_line1 = "QUA TỪNG LỚP,"
        h1_line2 = "VẺ ĐẸP DẦN HIỆN RA."
    else:
        h1_line1 = "Qua từng lớp,"
        h1_line2 = "vẻ đẹp dần hiện ra."

    lead_text = "Khám phá cách một tác phẩm sơn mài được tạo nên qua những lớp sơn, vật liệu và bàn tay người thợ."
    btn_text = "Tạo nên sắc sơn mài của riêng bạn "
    note_text = "Trải nghiệm khoảng 3–5 phút · Có tương tác"

    # --- 1. Update kham-pha/index.html ---
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Static HTML Header replacement
    new_header_html = (
        f'<header class="explore_intro__ycC8w">'
        f'<p class="eyebrow">KHÁM PHÁ · SƠN SON MÀI SẮC</p>'
        f'<h1>{h1_line1}<br/>{h1_line2}</h1>'
        f'<p class="explore_lead__PXqjY">{lead_text}</p>'
        f'<div class="explore_actions__K1B4A">'
        f'<a class="btn red" href="/trai-nghiem#simulator">{btn_text}<span aria-hidden="true">⟶</span></a>'
        f'<span>{note_text}</span>'
        f'</div>'
        f'</header>'
    )
    html = re.sub(r'<header class="explore_intro__ycC8w">.*?</header>', new_header_html, html, flags=re.DOTALL)

    # Guardian script in HTML
    guardian_pat = r'<script id="khampha-guardian">.*?</script>'
    new_guardian = f"""<script id="khampha-guardian">
(function(){{
  var obs = null;
  function fixHeader(){{
    var header = document.querySelector('header.explore_intro__ycC8w');
    if (!header) return;
    var h1 = header.querySelector('h1');
    var lead = header.querySelector('p.explore_lead__PXqjY');
    var btn = header.querySelector('a.btn');

    var needsUpdate = false;
    if (h1 && !h1.textContent.includes('QUA TỪNG LỚP') && !h1.textContent.includes('Qua từng lớp')) needsUpdate = true;
    if (lead && !lead.textContent.includes('Khám phá cách một tác phẩm')) needsUpdate = true;
    if (btn && !btn.textContent.includes('Tự tạo một bề mặt sơn mài')) needsUpdate = true;

    if (!needsUpdate) return;

    if (obs) obs.disconnect();

    if (h1 && !h1.textContent.includes('QUA TỪNG LỚP') && !h1.textContent.includes('Qua từng lớp')) {{
      h1.innerHTML = '{h1_line1}<br/>{h1_line2}';
    }}
    if (lead && !lead.textContent.includes('Khám phá cách một tác phẩm')) {{
      lead.textContent = '{lead_text}';
    }}
    if (btn && !btn.textContent.includes('Tự tạo một bề mặt sơn mài')) {{
      btn.innerHTML = 'Tự tạo một bề mặt sơn mài <span aria-hidden="true">⟶</span>';
    }}

    if (obs && header) {{
      obs.observe(header, {{ childList: true, subtree: true }});
    }}
  }}

  document.addEventListener('DOMContentLoaded', fixHeader);
  window.addEventListener('load', fixHeader);

  obs = new MutationObserver(fixHeader);
  var targetHeader = document.querySelector('header.explore_intro__ycC8w');
  if (targetHeader) {{
    obs.observe(targetHeader, {{ childList: true, subtree: true }});
  }}
  fixHeader();

  setTimeout(function() {{
    if (obs) obs.disconnect();
  }}, 3000);
}})();
</script>"""
    if re.search(guardian_pat, html, re.DOTALL):
        html = re.sub(guardian_pat, new_guardian, html, flags=re.DOTALL)

    # Flight stream (__next_f) in HTML
    # We need to replace the h1, lead, and action in the JSON flight data string
    # Current H1 in flight string is either:
    # [\"Năm chặng.\",[\"$\",\"br\",null,{}],\"Một bề mặt nhiều lớp.\"]
    # or [\"NĂM CHẶNG TẠO TÁC\",...
    # or [\"QUA TỪNG LỚP,\",...
    html = re.sub(
        r'\[\\\"(?:Năm chặng\.|NĂM CHẶNG TẠO TÁC|QUA TỪNG LỚP,|Qua từng lớp,)\\\",\[\\\"\$+\\\",\\\"br\\\",null,\{\}\],\\\"(?:Một bề mặt nhiều lớp\.|MỘT VẺ ĐẸP THÀNH HÌNH|VẺ ĐẸP DẦN HIỆN RA\.|vẻ đẹp dần hiện ra\.)\\\"\]',
        f'[\\"{h1_line1}\\",[\\"$\\",\\"br\\",null,{{}}],\\"{h1_line2}\\"]',
        html
    )

    # Lead text in flight string
    html = re.sub(
        r'\\\"explore_lead__PXqjY\\\",\\\"children\\\":\\\"(Từ chuẩn bị cốt[^"]*?|Khám phá cách một tác phẩm[^"]*?)\\\"',
        f'\\"explore_lead__PXqjY\\",\\"children\\":\\"{lead_text}\\"',
        html
    )

    # Action buttons in flight string
    # Should be an array with link and span
    new_actions_flight = (
        r'{\"className\":\"explore_actions__K1B4A\",\"children\":[['
        r'\"$\",\"$L6\",null,{\"className\":\"btn red\",\"href\":\"/trai-nghiem#simulator\",\"children\":['
        f'\\"{btn_text}\\",'
        r'[\"$\",\"span\",null,{\"aria-hidden\":\"true\",\"children\":\"⟶\"}]]}],'
        f'[\"$\",\"span\",null,{{\"children\":\"{note_text}\"}}]]}}'
    )

    # Replace any existing actions pattern in flight string
    html = re.sub(
        r'\{\\\"className\\\":\\\"explore_actions__K1B4A\\\",\\\"children\\\":(?:\[\\\"\$+\\\",\\\"\$+L6\\\",null,\{\\\"className\\\":\\\"btn red\\\"[^}]*\}\]\}|\[\[\\\"\$+\\\",\\\"\$+L6\\\"[^\]]*\],\[\\\"\$+\\\",\\\"span\\\"[^\]]*\]\]\})',
        new_actions_flight,
        html
    )

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated HTML and __next_f stream.")

    # --- 2. Update rsc_payloads/kham-pha.rsc ---
    if os.path.exists(RSC_PATH):
        with open(RSC_PATH, 'r', encoding='utf-8') as f:
            rsc = f.read()

        rsc = re.sub(
            r'\[\"(?:Năm chặng\.|NĂM CHẶNG TẠO TÁC|QUA TỪNG LỚP,|Qua từng lớp,)\",\[\"\$+\",\"br\",null,\{\}\],\"(?:Một bề mặt nhiều lớp\.|MỘT VẺ ĐẸP THÀNH HÌNH|VẺ ĐẸP DẦN HIỆN RA\.|vẻ đẹp dần hiện ra\.)\"\]',
            f'["{h1_line1}",["$","br",null,{{}}],"{h1_line2}"]',
            rsc
        )

        rsc = re.sub(
            r'\"explore_lead__PXqjY\",\"children\":\"(Từ chuẩn bị cốt[^"]*?|Khám phá cách một tác phẩm[^"]*?)\"',
            f'"explore_lead__PXqjY","children":"{lead_text}"',
            rsc
        )

        new_actions_rsc = (
            r'{"className":"explore_actions__K1B4A","children":[['
            r'"$","$L2",null,{"className":"btn red","href":"/trai-nghiem#simulator","children":['
            f'"{btn_text}",'
            r'["$","span",null,{"aria-hidden":"true","children":"⟶"}]]}],'
            f'["$","span",null,{{"children":"{note_text}"}}]]}}'
        )

        rsc = re.sub(
            r'\{"className":"explore_actions__K1B4A","children":(?:\[\"\$+\",\"\$+L2\",null,\{\"className\":\"btn red\"[^}]*\}\]\}|\[\[\"\$+\",\"\$+L2\"[^\]]*\],\[\"\$+\",\"span\"[^\]]*\]\]\})',
            new_actions_rsc,
            rsc
        )

        with open(RSC_PATH, 'w', encoding='utf-8') as f:
            f.write(rsc)
        print("Updated RSC payload.")

    # --- 3. Update CSS files ---
    for p in CSS_PATHS:
        if not os.path.exists(p):
            continue
        with open(p, 'r', encoding='utf-8') as f:
            css = f.read()

        # Update .explore_intro__ycC8w:after
        # Increase opacity to bg_opacity, refined gradient to reveal rooster, circle, cat, vase
        new_after = (
            f'.explore_intro__ycC8w:after{{position:absolute;z-index:-1;inset:0 0 0 38%;content:"";'
            f'background:linear-gradient(90deg,#f8edcf 0%,rgba(248,237,207,0.35) 18%,transparent 50%),url(/story-assets/key-visual.jpg) right center/cover no-repeat;'
            f'opacity:{bg_opacity};-webkit-mask-image:linear-gradient(90deg,transparent,#000 22%);mask-image:linear-gradient(90deg,transparent,#000 22%)}}'
        )
        css = re.sub(r'\.explore_intro__ycC8w:after\{[^}]*\}', new_after, css)

        # Update media query
        new_mobile_after = '.explore_intro__ycC8w:after{inset:8% 0 0 15%;opacity:.38}'
        css = re.sub(r'\.explore_intro__ycC8w:after\{inset:[^;]+;opacity:[^}]+}', new_mobile_after, css)

        with open(p, 'w', encoding='utf-8') as f:
            f.write(css)
        print(f"Updated CSS: {p}")

if __name__ == '__main__':
    apply_updates(title_uppercase=True, bg_opacity=0.75)
