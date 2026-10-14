css_rule = """
/* --- Core V4 Process Grid: Refined Slide Layout --- */
.core-v4-process-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0;list-style:none;margin:0;padding:0}
.core-v4-process-grid li{min-width:0;position:relative}
.core-v4-process-grid li:not(:last-child)::after{content:'';position:absolute;right:0;top:18px;bottom:22px;width:1px;background:linear-gradient(180deg,transparent,rgba(139,42,42,0.18) 15%,rgba(139,42,42,0.24) 50%,rgba(139,42,42,0.18) 85%,transparent);pointer-events:none}
.core-v4-process-grid li:not(:last-child)::before{content:'✦';position:absolute;right:-4px;top:50%;transform:translateY(-50%);font-size:8px;color:#b89358;z-index:2;pointer-events:none;line-height:1}
.core-v4-process-step{position:relative;display:flex;flex-direction:column;width:100%;height:100%;padding:0 16px 16px;border:0;border-bottom:2px solid transparent;background:transparent;color:#291b12;text-align:left;cursor:pointer;transition:background-color .25s,border-color .25s}
.core-v4-process-step:hover,.core-v4-process-step[aria-pressed=true]{background:rgba(132,32,34,0.035)}
.core-v4-process-step[aria-pressed=true]{border-bottom-color:#842022;box-shadow:0 2px 0 #842022}
.core-v4-step-number{order:1;display:flex;align-items:center;gap:12px;color:#842022;font-family:"Project Display","Playfair Display",Georgia,serif;font-weight:400;font-size:clamp(26px,2.3vw,34px);line-height:1;margin-bottom:6px}
.core-v4-step-number::after{content:'';display:inline-block;width:36px;height:1.5px;background:#842022;opacity:0.45}
.core-v4-step-title{order:2;display:flex;align-items:flex-start;min-height:42px;margin-bottom:12px;color:#842022;font-family:"Project Display","Playfair Display",Georgia,serif;font-weight:600;font-size:clamp(13.5px,1.15vw,16px);line-height:1.3;text-transform:uppercase;letter-spacing:0.025em}
.core-v4-process-photo{order:3;display:block;width:100%;aspect-ratio:1.15;background-image:url(/story-assets/process-five-stages-v4.webp);background-size:500% auto;background-position-y:65%;background-repeat:no-repeat;border-radius:2px;margin-bottom:14px;box-shadow:0 2px 8px rgba(45,25,10,0.08);filter:saturate(0.92);transition:filter .25s,transform .25s}
.core-v4-process-step:hover .core-v4-process-photo,.core-v4-process-step[aria-pressed=true] .core-v4-process-photo{filter:saturate(1.05);transform:translateY(-2px)}
.core-v4-step-short{order:4;display:block;margin-top:0;color:#493521;font-family:Inter,sans-serif;font-weight:400;font-size:clamp(11.5px,0.95vw,13px);line-height:1.65}
@media(max-width:900px){.core-v4-process-grid{grid-template-columns:repeat(5,220px);overflow-x:auto;scroll-snap-type:x mandatory;padding:0 0 16px;gap:12px}.core-v4-process-grid li{scroll-snap-align:start}.core-v4-process-grid li:not(:last-child)::after,.core-v4-process-grid li:not(:last-child)::before{display:none}.core-v4-process-step{padding:0 10px 14px;border-right:1px solid rgba(139,42,42,0.18)}}
"""

targets = [
    '_next/static/css/58e70d5489b56972.css',
    '_next/static/css/7d5ed180c1fe36fd.css',
    'ma_nguon_css_js/css/58e70d5489b56972.css'
]

for t in targets:
    try:
        with open(t, 'r', encoding='utf-8') as f:
            content = f.read()
        if '/* --- Core V4 Process Grid: Refined Slide Layout --- */' in content:
            # replace existing
            idx = content.find('/* --- Core V4 Process Grid: Refined Slide Layout --- */')
            content = content[:idx]
        content = content + "\n" + css_rule
        with open(t, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied CSS to {t}")
    except Exception as e:
        print(f"Error for {t}: {e}")
