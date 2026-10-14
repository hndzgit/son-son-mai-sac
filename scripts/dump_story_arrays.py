import re
import json

with open('ma_nguon_css_js/js/app_cau-chuyen-son-mai_page-18999a17f9a00aec.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's find array l: headings
# Search for l=[{...}] or similar
match_l = re.search(r'([a-zA-Z0-9_]+)=\[\{title:\"([^\"]+)\"', c)
if match_l:
    print("Found array l starts with:", match_l.group(2).encode('utf-8').decode('unicode_escape'))

# Let's extract all headings in l
headings = re.findall(r'\{title:\"([^\"]+)\"\}', c)
print("\nHeadings found:")
for h in headings:
    print("-", h.encode('utf-8').decode('unicode_escape'))

# Let's extract array u (the text paragraphs)
# u is an array of arrays of strings: [[p1, p2, ...], [p1, p2, ...], ...]
match_u = re.findall(r'(\[\[\"(?:[^\"\\]|\\.)*\"(?:,\"(?:[^\"\\]|\\.)*\")*\](?:,\[\"(?:[^\"\\]|\\.)*\"(?:,\"(?:[^\"\\]|\\.)*\")*\])*\])', c)
print(f"\nArrays of arrays found: {len(match_u)}")
for idx, m in enumerate(match_u):
    print(f"Match {idx} length: {len(m)}")
