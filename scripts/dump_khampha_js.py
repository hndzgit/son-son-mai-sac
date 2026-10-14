import re
import json

with open('ma_nguon_css_js/js/app_kham-pha_page-b0c7a974225638c7.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for objects with stage titles, descriptions, etc.
# Look for strings related to cong doan
matches = re.findall(r'(\{[^{}]*(?:Chuẩn bị cốt|Làm vóc|Sơn nền|Tạo hình và trang trí|Phủ, mài và hoàn thiện)[^{}]*\})', content)
print(f"Found {len(matches)} objects")
for m in matches[:5]:
    print(m)

# Find all vietnamese texts in this JS chunk
vietnamese_strings = set(re.findall(r'["\']([A-ZÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ][^"\'{}\\<>]{10,})["\']', content))
print(f"\nTotal Vietnamese strings: {len(vietnamese_strings)}")
for s in sorted(vietnamese_strings):
    print(f"- {s}")
