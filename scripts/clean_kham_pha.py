import os

with open('kham-pha/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

marker = 'explore_definition__Nb9IJ'
idx = text.find(marker)
if idx != -1:
    # Find the comma before this section
    start = text.rfind(',[\\"', 0, idx)
    # Find L7
    l7_pos = text.find('L7', idx)
    end_item = text.rfind(',[\\"', 0, l7_pos)
    print(f"Cutting from {start} ({repr(text[start:start+25])}) to {end_item} ({repr(text[end_item:end_item+25])})")
    text = text[:start] + text[end_item:]

with open('kham-pha/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Remaining occurrences of explore_definition__Nb9IJ:", text.count(marker))
