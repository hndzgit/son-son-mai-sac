import os

files_to_update = [
    'index.html',
    'trai-nghiem/index.html',
    'kiem_tra_2026-10-12/ban_chup_goc/index.html',
    'kiem_tra_2026-10-12/ban_chup_goc/trai-nghiem/index.html'
]

old_block = (
    '<p class="coreIntroduction_definitionLead__EsPgn">Một tác phẩm được tạo nên bằng cả việc phủ lên và mài đi.</p>'
    '<p>Với sơn mài, hình ảnh không chỉ nằm trên bề mặt. Người nghệ sĩ tạo nên nhiều lớp sơn, màu sắc và vật liệu, có những lớp được phủ kín dưới lớp sơn tiếp theo. Qua quá trình mài với nước, các lớp nằm bên dưới dần xuất hiện và cùng tạo nên bề mặt cuối cùng.</p>'
    '<p class="coreIntroduction_definitionClose__6q2Dj">Càng đi qua nhiều lớp, hình ảnh càng được hé lộ.</p>'
)

new_block = (
    '<p class="coreIntroduction_definitionLead__EsPgn">Một tác phẩm sơn mài được tạo nên từ cả quá trình phủ lên và mài đi.</p>'
    '<p>Trong sơn mài, vẻ đẹp không chỉ nằm trên bề mặt mà được hình thành qua nhiều lớp sơn, màu sắc và vật liệu khác nhau. Các lớp ấy được phủ chồng lên nhau, sau đó người làm nghề dùng kỹ thuật mài để từng phần bên dưới dần hiện ra. Chính sự đan xen giữa phủ – mài – hé lộ tạo nên chiều sâu, sắc độ và vẻ đẹp đặc trưng của bề mặt sơn mài.</p>'
)

source_link = '<a class="coreIntroduction_source__x42B5" href="https://moit.gov.vn/tin-tuc/thi-truong-nuoc-ngoai/doc-dao-son-mai.html" target="_blank" rel="noopener noreferrer">Tư liệu về vóc và các công đoạn sơn mài · Bộ Công Thương <span aria-hidden="true">↗</span></a>'

for fp in files_to_update:
    if not os.path.exists(fp):
        print("Not found:", fp)
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    count = 0
    if old_block in content:
        content = content.replace(old_block, new_block)
        count += 1
        print(f"[{fp}] Replaced definition block successfully.")
    else:
        print(f"[{fp}] old_block NOT matched directly, checking partials...")

    if source_link in content:
        content = content.replace(source_link, '')
        count += 1
        print(f"[{fp}] Removed source link successfully.")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[{fp}] Done, changes: {count}\n")
