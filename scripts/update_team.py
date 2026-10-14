import json

# Update 00_tong_quan_du_an
with open('du_lieu_noi_dung/00_tong_quan_du_an.json', 'r', encoding='utf-8') as f:
    tq = json.load(f)

members = [
    {
        "ho_ten": "Đỗ Nguyễn Đan Lê",
        "ky_hieu": "ĐL",
        "vai_tro": "Trưởng nhóm",
        "hinh_anh": "/story-assets/team-members/dan-le.jpg"
    },
    {
        "ho_ten": "Đỗ Duy Nghĩa",
        "ky_hieu": "DN",
        "vai_tro": "Phụ trách quay dựng",
        "hinh_anh": "/story-assets/team-members/duy-nghia.jpg"
    },
    {
        "ho_ten": "Chu Huyền Trang",
        "ky_hieu": "HT",
        "vai_tro": "Phụ trách đối ngoại",
        "hinh_anh": "/story-assets/team-members/huyen-trang.jpg"
    },
    {
        "ho_ten": "Dương Gia Đạt",
        "ky_hieu": "GĐ",
        "vai_tro": "Phụ trách tài chính",
        "hinh_anh": "/story-assets/team-members/gia-dat.jpg"
    },
    {
        "ho_ten": "Trần Anh Vũ",
        "ky_hieu": "AV",
        "vai_tro": "Phụ trách nội dung",
        "hinh_anh": "/story-assets/team-members/anh-vu.jpg"
    }
]

tq['doi_ngu_sang_lap'] = members
tq['thong_ke_thu_thap']['so_tep_hinh_anh_assets'] = 89  # with favicon.ico & opengraph-image.png

with open('du_lieu_noi_dung/00_tong_quan_du_an.json', 'w', encoding='utf-8') as f:
    json.dump(tq, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/00_tong_quan_du_an.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Tổng Quan Dự Án: {tq['ten_du_an']} ({tq['viet_tat']})

> **Thông điệp cốt lõi:** *"{tq['slogan']}"*  
> **Tôn chỉ hoạt động:** *"{tq['thong_diep_chinh']}"*

---

## 1. Thông Tin Chung
- **Tên dự án:** {tq['ten_du_an']}
- **Trang web chính thức:** [{tq['website']}]({tq['website']})
- **Hosting dự phòng:** [{tq['hosting_du_phong']}]({tq['hosting_du_phong']})
- **Địa điểm thực hiện:** {tq['dia_diem_hoat_dong']}
- **Email liên hệ:** [{tq['thong_tin_lien_he']['email']}](mailto:{tq['thong_tin_lien_he']['email']})

## 2. Kênh Truyền Thông Mạng Xã Hội
- **Facebook:** [{tq['thong_tin_lien_he']['facebook']}]({tq['thong_tin_lien_he']['facebook']})
- **TikTok:** [{tq['thong_tin_lien_he']['tiktok']}]({tq['thong_tin_lien_he']['tiktok']})
- **Threads:** [{tq['thong_tin_lien_he']['threads']}]({tq['thong_tin_lien_he']['threads']})

## 3. Sứ Mệnh & Tầm Nhìn
{tq['su_menh']}

## 4. Đội Ngũ Thực Hiện (Project Team - 5 Thành Viên Chính Thức)
""")
    for m in members:
        f.write(f"- **{m['ho_ten']}** (`{m['ky_hieu']}`): **{m['vai_tro']}**  \n  *(Ảnh đại diện: `{m['hinh_anh']}`)*\n")

    f.write(f"""
## 5. Dữ Liệu Thu Thập Được
- **Tổng số trang web:** {tq['thong_ke_thu_thap']['so_trang_web']} trang
- **Tổng số tệp tài nguyên hình ảnh & media:** {tq['thong_ke_thu_thap']['so_tep_hinh_anh_assets']} tệp (~26.5 MB)
- **Tệp mã nguồn & giao diện:** Đầy đủ HTML, CSS, JS runtime, Font chữ TTF (Inter, Noto Serif, Playfair Display), bộ ảnh 16 góc chụp xoay 360 độ sản phẩm, 18 ảnh tư liệu lịch sử dòng thời gian.
""")

# Update 05_ve_du_an
with open('du_lieu_noi_dung/05_ve_du_an.json', 'r', encoding='utf-8') as f:
    vda = json.load(f)

vda['doi_ngu_thuc_hien'] = [
    {
        "ho_ten": "Đỗ Nguyễn Đan Lê",
        "ky_hieu": "ĐL",
        "vai_tro": "Trưởng nhóm",
        "anh_chan_dung": "/story-assets/team-members/dan-le.jpg"
    },
    {
        "ho_ten": "Đỗ Duy Nghĩa",
        "ky_hieu": "DN",
        "vai_tro": "Phụ trách quay dựng",
        "anh_chan_dung": "/story-assets/team-members/duy-nghia.jpg"
    },
    {
        "ho_ten": "Chu Huyền Trang",
        "ky_hieu": "HT",
        "vai_tro": "Phụ trách đối ngoại",
        "anh_chan_dung": "/story-assets/team-members/huyen-trang.jpg"
    },
    {
        "ho_ten": "Dương Gia Đạt",
        "ky_hieu": "GĐ",
        "vai_tro": "Phụ trách tài chính",
        "anh_chan_dung": "/story-assets/team-members/gia-dat.jpg"
    },
    {
        "ho_ten": "Trần Anh Vũ",
        "ky_hieu": "AV",
        "vai_tro": "Phụ trách nội dung",
        "anh_chan_dung": "/story-assets/team-members/anh-vu.jpg"
    }
]

with open('du_lieu_noi_dung/05_ve_du_an.json', 'w', encoding='utf-8') as f:
    json.dump(vda, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/05_ve_du_an.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Về Dự Án: {vda['tieu_de']}

> **Định vị:** {vda['dinh_vi']}  
> **Slogan:** *"{vda['slogan']}"*

---

## 1. Giới Thiệu Chung
{vda['mo_ta_tong_quan']}

## 2. Câu Chuyện Dự Án: {vda['cau_chuyen_du_an']['tieu_de']}
{vda['cau_chuyen_du_an']['noi_dung']}

## 3. Sứ Mệnh Của Dự Án
> **"{vda['su_menh']['muc_tieu_chinh']}"**

{vda['su_menh']['chi_tiet']}

## 4. Những Người Thực Hiện (5 Thành Viên Ban Điều Hành)
""")
    for m in vda['doi_ngu_thuc_hien']:
        f.write(f"""### {m['ho_ten']} (`{m['ky_hieu']}`)
- **Vai trò chính thức:** **{m['vai_tro']}**
- **Ảnh chân dung:** `{m['anh_chan_dung']}`

""")

    f.write(f"""## 5. Lời Kêu Gọi
> *"{vda['thong_diep_ket']}"*
""")

print("Updated team member titles in 00 and 05!")
