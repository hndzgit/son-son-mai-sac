import json

# 1. Update 07_trai_nghiem_mo_phong_3d
with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.json', 'r', encoding='utf-8') as f:
    tn = json.load(f)

tn['ban_mau_khoi_tao'] = [
    {"ten": "Hoa sen · cánh gián", "mo_ta": "Họa tiết hoa sen thanh tao trên nền sơn màu cánh gián truyền thống"},
    {"ten": "Sóng nước · đen then", "mo_ta": "Họa tiết sóng thủy ba uyển chuyển trên nền sơn then đen sâu thẳm"},
    {"ten": "Tự do · đỏ son", "mo_ta": "Sáng tạo tự do với sắc đỏ son rực rỡ và các chất liệu khảm"}
]

tn['tien_trinh_xuong_son_mai_5_chang'] = [
    {"so": "01", "ten": "CHUẨN BỊ CỐT", "mo_ta": "Dáng và vật liệu", "ghi_chu": "Chọn dáng hộp, khay hoặc tranh cùng vật liệu chịu lực trước khi tạo các lớp vóc."},
    {"so": "02", "ten": "LÀM VÓC", "mo_ta": "Gia cố, hom và làm phẳng", "ghi_chu": "Bó hom phù sa, bồi vải màn gia cường và mài phẳng mặt nền."},
    {"so": "03", "ten": "SƠN NỀN", "mo_ta": "Chọn sắc nền", "ghi_chu": "Phủ lớp sơn nền then đen, đỏ son hoặc cánh gián và ủ ẩm."},
    {"so": "04", "ten": "TẠO HÌNH VÀ TRANG TRÍ", "mo_ta": "Chọn mặt và đặt họa tiết", "ghi_chu": "Áp khuôn hoa văn, cẩn vỏ trứng, thếp vàng quỳ hoặc vẽ màu."},
    {"so": "05", "ten": "PHỦ, MÀI VÀ HOÀN THIỆN", "mo_ta": "Phủ lớp, mài, đánh bóng", "ghi_chu": "Phủ sơn bảo vệ, mài nước hé lộ các lớp ẩn và đánh bóng gương."}
]

with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.json', 'w', encoding='utf-8') as f:
    json.dump(tn, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Trải Nghiệm Tương Tác: {tn['tieu_de']}

> **Khuyến cáo:** *{tn['khuyen_cao_chung']}*  
> **Hành trình trải nghiệm:** *{tn['huong_dan_hanh_trinh']}*  
> **Tự chỉnh:** *{tn['huong_dan_tu_chinh']}*

---

## 1. Các Bản Mẫu Khởi Tạo Nhanh (Preset Templates)
Người dùng có thể bắt đầu tự do hoặc chọn nhanh 1 trong 3 bản mẫu nghệ thuật:
""")
    for bm in tn['ban_mau_khoi_tao']:
        f.write(f"- **{bm['ten']}**: {bm['mo_ta']}\n")

    f.write(f"""
---

## 2. Tiến Trình Xưởng Sơn Mài Sắc (01 / 05 Chặng)
""")
    for ch in tn['tien_trinh_xuong_son_mai_5_chang']:
        f.write(f"### {ch['so']}. {ch['ten']} ({ch['mo_ta']})\n{ch['ghi_chu']}\n\n")

    f.write(f"""---

## 3. Quy Trình 5 Bước Trải Nghiệm Chi Tiết
""")
    for step in tn['quy_trinh_mo_phong_hanh_trinh']:
        f.write(f"### Bước {step['buoc']}: {step['ten_buoc']}\n")
        if 'cac_lua_chon' in step:
            f.write("- **Các lựa chọn cốt:**\n")
            for c in step['cac_lua_chon']:
                f.write(f"  + {c['loai']} (Biểu tượng: `{c['bieu_tuong']}`)\n")
        if 'thao_tac' in step:
            f.write(f"- **Thao tác:** {step['thao_tac']}\n")
        if 'tai_nguyen' in step:
            if isinstance(step['tai_nguyen'], list):
                f.write("- **Tài nguyên hoa văn & texture sử dụng:**\n")
                for r in step['tai_nguyen']:
                    f.write(f"  + `{r}`\n")
            else:
                f.write(f"- **Tài nguyên sử dụng:** `{step['tai_nguyen']}`\n")
        f.write("\n")

    f.write(f"""---

## 4. Trình Chỉnh Sửa Mặt Hộp Chuyên Sâu (Face Engraving Editor)
Trang bị công cụ vẽ và khắc tương tác trực quan:
- **Tùy biến từng mặt:** Vẽ tự do lên từng bề mặt (nắp hộp, các cạnh bên).
- **Chất liệu tương tác:** Vẽ bằng bụi vàng lá, dán mảng vỏ trứng rạn nứt, cẩn vỏ trai óng ánh.
- **Hiệu ứng quang học:** Bề mặt phản chiếu độ bóng sơn ta (gloss) và độ sâu quang học.
- **Lưu trữ & chia sẻ:** Lưu bản phối vào bộ nhớ trình duyệt và tải ảnh thành phẩm độ nét cao (`lop-sac-cua-ban.png`).
""")

# 2. Update 03_cau_chuyen_son_mai
with open('du_lieu_noi_dung/03_cau_chuyen_son_mai.json', 'r', encoding='utf-8') as f:
    cc = json.load(f)

cc['nghe_nhan_truyen_nghe'] = {
    "tieu_de": "Những tri thức khó ghi hết thành công thức.",
    "noi_dung": "Tại những làng nghề như Hạ Thái, ta có thể nhìn thấy một dạng tri thức mà sách vở rất khó ghi lại đầy đủ. Một quy trình có thể được viết thành từng công đoạn. Người đọc có thể biết phải chuẩn bị cốt, làm vóc, phủ sơn, cẩn vật liệu, mài và hoàn thiện. Nhưng khi trực tiếp làm, mỗi bước lại mở ra rất nhiều quyết định. Lớp sơn này đã đạt độ khô để mài chưa? Mài đến đâu thì dừng lại để không phạm vào lớp vàng bạc bên dưới? Đó là sự nhạy cảm của đôi bàn tay và kinh nghiệm tích lũy qua năm tháng."
}

cc['tiep_noi_cau_chuyen'] = {
    "thong_diep": "Một lớp sắc đang chờ bạn.",
    "keu_goi": "Tìm hiểu vật liệu hoặc tự tạo một bề mặt sơn mài của riêng bạn.",
    "duong_dan": ["/kham-pha", "/trai-nghiem/hanh-trinh"]
}

with open('du_lieu_noi_dung/03_cau_chuyen_son_mai.json', 'w', encoding='utf-8') as f:
    json.dump(cc, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/03_cau_chuyen_son_mai.md', 'a', encoding='utf-8') as f:
    f.write(f"""
---

## III. NGHỆ NHÂN · TRUYỀN NGHỀ
> ### *"{cc['nghe_nhan_truyen_nghe']['tieu_de']}"*

{cc['nghe_nhan_truyen_nghe']['noi_dung']}

---

## IV. TIẾP NỐI CÂU CHUYỆN
> ### *"{cc['tiep_noi_cau_chuyen']['thong_diep']}"*

{cc['tiep_noi_cau_chuyen']['keu_goi']}  
- [Khám phá 5 công đoạn kỹ thuật →](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/02_kham_pha.md)
- [Tự tạo lớp sắc của riêng bạn →](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.md)
""")

print("Successfully enriched 07 and 03 with all exact nuances!")
