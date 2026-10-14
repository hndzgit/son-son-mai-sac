import json

# Update 07_trai_nghiem_mo_phong_3d
with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.json', 'r', encoding='utf-8') as f:
    tn = json.load(f)

# Add all stencils to step 4
for step in tn['quy_trinh_mo_phong_hanh_trinh']:
    if step['buoc'] == 4:
        stencils = [
            "/story-assets/lotus-inlay-stencil-v6.webp",
            "/story-assets/journey-lotus-stencil-v8.webp",
            "/story-assets/geometric-inlay-stencil-v7.webp",
            "/story-assets/foliage-inlay-stencil-v7.webp",
            "/textures/eggshell_crackle.svg",
            "/textures/gold_leaf_texture.svg",
            "/story-assets/mat-gold.jpg",
            "/story-assets/mat-silver.jpg",
            "/story-assets/mat-egg.jpg",
            "/story-assets/mat-pearl.jpg",
            "/story-assets/mat-shell.jpg"
        ]
        step['tai_nguyen'] = stencils

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
                f.write("- **Tài nguyên hoa văn khuôn & texture sử dụng:**\n")
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
- **Khuôn mẫu hoa văn (Stencils):**
  + Hoa sen (`lotus-inlay-stencil-v6.webp`, `journey-lotus-stencil-v8.webp`)
  + Kỷ hà (`geometric-inlay-stencil-v7.webp`)
  + Hoa lá (`foliage-inlay-stencil-v7.webp`)
- **Hiệu ứng quang học:** Bề mặt phản chiếu độ bóng sơn ta (gloss) và độ sâu quang học.
- **Lưu trữ & chia sẻ:** Lưu bản phối vào bộ nhớ trình duyệt và tải ảnh thành phẩm độ nét cao (`lop-sac-cua-ban.png`).
""")

# Update README count
with open('du_lieu_noi_dung/00_tong_quan_du_an.json', 'r', encoding='utf-8') as f:
    tq = json.load(f)
tq['thong_ke_thu_thap']['so_tep_hinh_anh_assets'] = 91
tq['thong_ke_thu_thap']['dung_luong_assets'] = "28 MB"
with open('du_lieu_noi_dung/00_tong_quan_du_an.json', 'w', encoding='utf-8') as f:
    json.dump(tq, f, ensure_ascii=False, indent=2)

print("Updated 07 and 00 with the 2 new stencils!")
