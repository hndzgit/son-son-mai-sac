#!/usr/bin/env python3
import os
import subprocess

FILES = [
    "_next/static/chunks/840-f19fdd306966b2e5.js",
    "ma_nguon_css_js/js/840-f19fdd306966b2e5.js"
]

def clean_file(filepath):
    print(f"\n--- Processing {filepath} ---")
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist!")
        return False
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    replacements = [
        # 1. BỀ MẶT MÀI NƯỚC THỜI GIAN THỰC -> BỀ MẶT NƯỚC
        (
            'BỀ MẶT M\\xc0I NƯỚC THỜI GIAN THỰC',
            'BỀ MẶT NƯỚC'
        ),
        # 2. CÔNG ĐOẠN CỐT LÕI CỦA SƠN MÀI
        (
            '2. M\\xc0I NƯỚC (C\\xd4NG ĐOẠN CỐT L\\xd5I CỦA SƠN M\\xc0I)',
            '2. M\\xc0I NƯỚC'
        ),
        # 3. Main grind button
        (
            'M\\xc0I NƯỚC \xb7 NHẤN ĐỂ M\\xc0I LỘ HOA VĂN',
            'M\\xc0I NƯỚC'
        ),
        (
            'M\\xc0I NƯỚC · NHẤN ĐỂ M\\xc0I LỘ HOA VĂN',
            'M\\xc0I NƯỚC'
        ),
        (
            'M\\xc0I NƯỚC \\xb7 NHẤN ĐỂ M\\xc0I LỘ HOA VĂN',
            'M\\xc0I NƯỚC'
        ),
        # 4. Button subtitle "(Nhấn để mài tiếp)"
        (
            ' (Nhấn để m\\xe0i tiếp)',
            ''
        ),
        (
            ' lượt m\\xe0i ho\\xe0n tất',
            ' lượt m\\xe0i'
        ),
        # 5. Pill status under 15%
        (
            'Lớp sơn phủ k\\xedn (Chưa m\\xe0i) \xb7 Họa tiết đang ẩn',
            'Lớp sơn phủ k\\xedn \xb7 Họa tiết chìm b\\xean dưới'
        ),
        (
            'Lớp sơn phủ k\\xedn (Chưa m\\xe0i) · Họa tiết đang ẩn',
            'Lớp sơn phủ k\\xedn · Họa tiết chìm b\\xean dưới'
        ),
        (
            'Lớp sơn phủ k\\xedn (Chưa m\\xe0i) \\xb7 Họa tiết đang ẩn',
            'Lớp sơn phủ k\\xedn \\xb7 Họa tiết chìm b\\xean dưới'
        ),
        # 6. Slider label
        (
            'ĐỘ S\\xc2U M\\xc0I NƯỚC',
            'ĐỘ M\\xc0I NƯỚC'
        ),
        # 7. Sidebar footnote "Mô phỏng tương tác · Không thay thế hướng dẫn của nghệ nhân"
        (
            'M\\xf4 phỏng tương t\\xe1c \\xb7 Kh\\xf4ng thay thế hướng dẫn của nghệ nh\\xe2n',
            'Minh họa quy tr\\xecnh tạo t\\xe1c sơn m\\xe0i thủ c\\xf4ng'
        ),
        (
            'M\\xf4 phỏng tương t\\xe1c \xb7 Kh\\xf4ng thay thế hướng dẫn của nghệ nh\\xe2n',
            'Minh họa quy tr\\xecnh tạo t\\xe1c sơn m\\xe0i thủ c\\xf4ng'
        ),
        (
            'Mô phỏng tương tác · Không thay thế hướng dẫn của nghệ nhân',
            'Minh họa quy trình tạo tác sơn mài thủ công'
        ),
        # 8. "Lớp phủ đã được ủ khô trong mô phỏng. Bây giờ có thể mài nước."
        (
            'Lớp phủ đ\\xe3 được ủ kh\\xf4 trong m\\xf4 phỏng. B\\xe2y giờ c\\xf3 thể m\\xe0i nước.',
            'Lớp phủ đ\\xe3 ủ kh\\xf4 ho\\xe0n to\\xe0n. Sẵn s\\xe0ng tiến h\\xe0nh m\\xe0i nước.'
        ),
        # 9. "Ủ · lớp hom đạt trạng thái khô trong mô phỏng"
        (
            'Ủ \\xb7 lớp hom đạt trạng th\\xe1i kh\\xf4 trong m\\xf4 phỏng',
            'Ủ \\xb7 Lớp hom đạt độ kh\\xf4 ti\\xeau chuẩn'
        ),
        (
            'Ủ \xb7 lớp hom đạt trạng th\\xe1i kh\\xf4 trong m\\xf4 phỏng',
            'Ủ \xb7 Lớp hom đạt độ kh\\xf4 ti\\xeau chuẩn'
        ),
        # 10. "Ủ lớp hom đến trạng thái khô trong mô phỏng trước khi mài."
        (
            'Ủ lớp hom đến trạng th\\xe1i kh\\xf4 trong m\\xf4 phỏng trước khi m\\xe0i.',
            'Ủ lớp hom đạt độ kh\\xf4 ti\\xeau chuẩn trước khi m\\xe0i.'
        ),
        # 11. "Vóc đã sẵn sàng trong mô phỏng. Chọn sắc sơn nền."
        (
            'V\\xf3c đ\\xe3 sẵn s\\xe0ng trong m\\xf4 phỏng. Chọn sắc sơn nền.',
            'V\\xf3c đ\\xe3 ho\\xe0n thiện. Tiến h\\xe0nh chọn sắc sơn nền.'
        ),
        # 12. "Lớp nền đã được ủ trong mô phỏng. Tiếp theo mài phẳng và làm sạch."
        (
            'Lớp nền đ\\xe3 được ủ trong m\\xf4 phỏng. Tiếp theo m\\xe0i phẳng v\\xe0 l\\xe0m sạch.',
            'Lớp nền đ\\xe3 được ủ kh\\xf4. Tiếp theo m\\xe0i phẳng v\\xe0 l\\xe0m sạch.'
        ),
        # 13. "Đưa lớp sơn nền đến trạng thái khô trong mô phỏng."
        (
            'Đưa lớp sơn nền đến trạng th\\xe1i kh\\xf4 trong m\\xf4 phỏng.',
            'Ủ lớp sơn nền đến khi kh\\xf4 ho\\xe0n to\\xe0n.'
        ),
        # 14. "Có thể xem lớp vải gia cố trong mô phỏng; việc sử dụng còn tùy cốt và thực hành."
        (
            'Có thể xem lớp vải gia cố trong mô phỏng; việc sử dụng còn tùy cốt và thực hành.',
            'Lớp vải gia cố giúp tăng độ bền liên kết; việc sử dụng tùy thuộc cốt và kỹ thuật tạo tác.'
        ),
        (
            'C\\xf3 thể xem lớp vải gia cố trong m\\xf4 phỏng; việc sử dụng c\\xf2n t\\xf9y cốt v\\xe0 thực h\\xe0nh.',
            'Lớp vải gia cố gi\\xfap tăng độ bền li\\xean kết; việc sử dụng t\\xf9y thuộc cốt v\\xe0 kỹ thuật tạo t\\xe1c.'
        ),
        # 15. "Bản phối là hình mô phỏng theo lựa chọn, chưa phải đơn đặt hàng hay xác nhận chế tác."
        (
            'Bản phối l\\xe0 h\\xecnh m\\xf4 phỏng theo lựa chọn, chưa phải đơn đặt h\\xe0ng hay x\\xe1c nhận chế t\\xe1c.',
            'Bản phối l\\xe0 h\\xecnh minh họa theo lựa chọn, chưa phải đơn đặt h\\xe0ng hay x\\xe1c nhận chế t\\xe1c.'
        ),
    ]

    count_applied = 0
    for target, repl in replacements:
        if target in content:
            content = content.replace(target, repl)
            print(f"Applied replacement: {target[:40]}... -> {repl[:40]}...")
            count_applied += 1

    print(f"Total replacements applied: {count_applied}")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    res = subprocess.run(["node", "-c", filepath], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Node syntax ERROR in {filepath}:\n{res.stderr}")
        return False
    else:
        print(f"Node syntax OK for {filepath}")
        return True

if __name__ == "__main__":
    success = True
    for f in FILES:
        if not clean_file(f):
            success = False
    print("\nAll done, success:", success)
