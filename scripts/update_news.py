import json

with open('du_lieu_noi_dung/04_tin_tuc_su_kien.json', 'r', encoding='utf-8') as f:
    tin_tuc = json.load(f)

with open('du_lieu_noi_dung/api_tin_tuc_bao_chi.json', 'r', encoding='utf-8') as f:
    api_news = json.load(f)

tin_tuc['danh_sach_tin_tuc_bao_chi'] = api_news

with open('du_lieu_noi_dung/04_tin_tuc_su_kien.json', 'w', encoding='utf-8') as f:
    json.dump(tin_tuc, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/04_tin_tuc_su_kien.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Tin Tức & Sự Kiện: {tin_tuc['tieu_de']}

> *{tin_tuc['loi_dan']}*

---

## 1. Sự Kiện Trọng Điểm: {tin_tuc['su_kien_sap_dien_ra']['ten_su_kien']}
- **Phân loại:** {tin_tuc['su_kien_sap_dien_ra']['phan_loai']}
- **Thời gian:** {tin_tuc['su_kien_sap_dien_ra']['thoi_gian']}
- **Địa điểm:** {tin_tuc['su_kien_sap_dien_ra']['dia_diem']}
- **Đơn vị tổ chức:** {tin_tuc['su_kien_sap_dien_ra']['don_vi_to_chuc']}
- **Nội dung hoạt động:** {tin_tuc['su_kien_sap_dien_ra']['muc_dich']}

---

## 2. Các Hoạt Động & Triển Lãm Nổi Bật
""")
    for hd in tin_tuc['hoat_dong_noi_bat']:
        f.write(f"""### {hd['ten']} [{hd['trang_thai']}]
- **Thời gian:** {hd['thoi_gian']}
- **Địa điểm:** {hd['dia_diem']}
- **Nội dung:** {hd['noi_dung']}
- **Hình ảnh tư liệu:** `{hd['hinh_anh']}`

""")

    f.write(f"""---

## 3. Bản Tin Báo Chí & Truyền Thông (12 Bài Báo Cập Nhật)
""")
    for idx, item in enumerate(api_news, 1):
        f.write(f"""### {idx}. {item['title']}
- **Nguồn báo chí:** {item['source']} | **Ngày đăng:** {item['date'][:10]}
- **Ảnh thu nhỏ (Thumbnail):** `{item['thumbnail']}`
- **Tóm tắt:** {item['summary']}
- **Liên kết bài viết:** [{item['url']}]({item['url']})

""")

print("Updated 04_tin_tuc_su_kien with 12 API news articles!")
