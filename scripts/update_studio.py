import json

# 1. Update 06_san_pham
san_pham_full = {
    "tieu_de": "Tìm một tác phẩm sơn mài | Sơn Son Mài Sắc",
    "loi_dan": "Mang câu chuyện di sản phù hợp với bạn.",
    "danh_sach_san_pham": [
        {
            "id": "box-lotus",
            "ten": "Hộp hoa sen",
            "phan_loai": "Hộp",
            "mau_nen": "Cánh gián",
            "hoa_van": "Hoa sen",
            "nghe_nhan": "Chưa có thông tin nghệ nhân",
            "chat_lieu": ["Vàng", "Vỏ trứng"],
            "cong_nang": "Lưu giữ",
            "hinh_anh": "/story-assets/finder-box-v5.webp",
            "ghi_chu": "Mẫu hình ảnh · hoa sen trên nền sơn tối",
            "bo_anh_xoay_360": [f"/story-assets/box-{i}.jpg" for i in [1, 5, 6, 7, 8, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]
        },
        {
            "id": "box-blank",
            "ten": "Hộp cốt · lớp sơn tối",
            "phan_loai": "Hộp",
            "mau_nen": "Đen then",
            "hoa_van": "Thêm",
            "nghe_nhan": "Chưa có thông tin nghệ nhân",
            "chat_lieu": ["Lớp nền"],
            "cong_nang": "Lưu giữ",
            "hinh_anh": "/story-assets/craft-blank-lacquer-generated.webp",
            "ghi_chu": "Mẫu hình ảnh · bề mặt sơn mài trơn"
        },
        {
            "id": "tray-lotus",
            "ten": "Khay hoa sen",
            "phan_loai": "Khay",
            "mau_nen": "Đỏ son",
            "hoa_van": "Hoa sen",
            "nghe_nhan": "Chưa có thông tin nghệ nhân",
            "chat_lieu": ["Vàng", "Vỏ trứng"],
            "cong_nang": "Bày vật phẩm",
            "hinh_anh": "/story-assets/hero-objects-generated.webp",
            "ghi_chu": "Mẫu minh họa · khay hoa sen"
        },
        {
            "id": "picture-lotus",
            "ten": "Tranh hoa sen",
            "phan_loai": "Tranh",
            "mau_nen": "Đỏ son",
            "hoa_van": "Hoa sen",
            "nghe_nhan": "Chưa có thông tin nghệ nhân",
            "chat_lieu": ["Vàng", "Vỏ trứng"],
            "cong_nang": "Trưng bày",
            "hinh_anh": "/story-assets/hero-objects-generated.webp",
            "ghi_chu": "Mẫu minh họa · tranh hoa sen"
        }
    ],
    "tuy_bien_ban_phoi_ca_nhan": {
        "mau_nen_chon": ["Đỏ son", "Cánh gián", "Đen then (#1a1010)"],
        "hoa_van_chon": ["Hoa sen", "Hoa lá", "Kỷ hà", "Thêm (vẽ tự do)"],
        "chat_lieu_can_chon": ["Vỏ trứng", "Vàng quỳ", "Xà cừ", "Lớp nền"],
        "kich_co": ["Nhỏ", "Trung", "Lớn"],
        "kieu_vien": ["Viền kép", "Viền kỷ hà", "Viền chấm", "Không viền"],
        "khac_ten_chu": {
            "gioi_han": "Tối đa 18 ký tự",
            "vi_tri": ["Mặt hộp (top)", "Trung tâm (center)"]
        },
        "xuat_ban_phoi": "Tải ảnh bản phối về thiết bị (lop-sac-cua-ban.png) và lưu trữ cục bộ (ssms-custom-design-v1)"
    }
}

with open('du_lieu_noi_dung/06_san_pham.json', 'w', encoding='utf-8') as f:
    json.dump(san_pham_full, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/06_san_pham.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Danh Mục Sản Phẩm: {san_pham_full['tieu_de']}

> *{san_pham_full['loi_dan']}*

---

## 1. Danh Sách 4 Mẫu Tác Phẩm Cốt
""")
    for sp in san_pham_full['danh_sach_san_pham']:
        f.write(f"""### {sp['ten']} (`{sp['id']}`)
- **Phân loại:** {sp['phan_loai']}
- **Màu nền:** {sp['mau_nen']}
- **Họa tiết:** {sp['hoa_van']}
- **Chất liệu:** {', '.join(sp['chat_lieu'])}
- **Công năng:** {sp['cong_nang']}
- **Ghi chú:** {sp['ghi_chu']}
- **Hình ảnh đại diện:** `{sp['hinh_anh']}`
""")
        if 'bo_anh_xoay_360' in sp:
            f.write(f"- **Bộ 16 ảnh xoay 360 độ:**\n")
            for img in sp['bo_anh_xoay_360']:
                f.write(f"  + `{img}`\n")
        f.write("\n---\n\n")

    f.write(f"""## 2. Hệ Thống Tùy Biến Bản Phối Cá Nhân (Studio)
Hệ thống cho phép người dùng tùy chọn phối màu và chất liệu theo ý muốn:
- **Màu nền:** {', '.join(san_pham_full['tuy_bien_ban_phoi_ca_nhan']['mau_nen_chon'])}
- **Hoa văn:** {', '.join(san_pham_full['tuy_bien_ban_phoi_ca_nhan']['hoa_van_chon'])}
- **Chất liệu khảm/cẩn:** {', '.join(san_pham_full['tuy_bien_ban_phoi_ca_nhan']['chat_lieu_can_chon'])}
- **Kích cỡ:** {', '.join(san_pham_full['tuy_bien_ban_phoi_ca_nhan']['kich_co'])}
- **Kiểu viền:** {', '.join(san_pham_full['tuy_bien_ban_phoi_ca_nhan']['kieu_vien'])}
- **Khắc tên/chữ cá nhân:** {san_pham_full['tuy_bien_ban_phoi_ca_nhan']['khac_ten_chu']['gioi_han']}
- **Xuất ảnh bản phối:** {san_pham_full['tuy_bien_ban_phoi_ca_nhan']['xuat_ban_phoi']}
""")

# 2. Update 07_trai_nghiem_mo_phong_3d
with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.json', 'r', encoding='utf-8') as f:
    trai_nghiem = json.load(f)

trai_nghiem['trinh_chinh_sua_mat_hop_face_engraving'] = {
    "ten": "Face Engraving Editor (Trình vẽ & khắc họa tiết mặt hộp)",
    "chuc_nang": [
        "Vẽ họa tiết thủ công lên từng mặt phẳng của hộp sơn mài",
        "Tùy chỉnh chất liệu cọ vẽ: vàng quỳ, vỏ trứng, bạc quỳ",
        "Điều chỉnh độ dày nét cọ và độ bóng (gloss) của bề mặt",
        "Áp dụng họa tiết lên các mặt hộp và lưu trạng thái (ssms-applied-faces-v1)",
        "Xem trước kết quả dưới dạng 3D đa góc xoay"
    ]
}

with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.json', 'w', encoding='utf-8') as f:
    json.dump(trai_nghiem, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.md', 'a', encoding='utf-8') as f:
    f.write(f"""
---

## Trình Chỉnh Sửa Mặt Hộp Chuyên Sâu (Face Engraving Editor)
Trang bị công cụ vẽ và khắc tương tác trực quan:
- **Tùy biến từng mặt:** Vẽ tự do lên từng bề mặt (nắp hộp, các cạnh bên).
- **Chất liệu tương tác:** Vẽ bằng bụi vàng lá, dán mảng vỏ trứng rạn nứt, cẩn vỏ trai óng ánh.
- **Hiệu ứng quang học:** Bề mặt phản chiếu độ bóng sơn ta (gloss) và độ sâu quang học.
- **Lưu trữ & chia sẻ:** Lưu bản phối vào bộ nhớ trình duyệt và tải ảnh thành phẩm độ nét cao (`lop-sac-cua-ban.png`).
""")

print("Updated 06_san_pham and 07_trai_nghiem_mo_phong_3d successfully!")
