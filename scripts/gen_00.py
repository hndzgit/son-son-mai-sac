import json
import os

os.makedirs('du_lieu_noi_dung', exist_ok=True)

# -------------------------------------------------------------
# 00. TỔNG QUAN DỰ ÁN
# -------------------------------------------------------------
tong_quan = {
    "ten_du_an": "Sơn Son Mài Sắc",
    "viet_tat": "SSMS",
    "slogan": "Chạm vào di sản · Đi qua từng đường mài, khám phá giá trị Việt",
    "thong_diep_chinh": "Từ thấy 'đẹp' đến hiểu vì sao 'đẹp'",
    "website": "https://son-son-mai-sac-orpin.vercel.app/",
    "hosting_du_phong": "https://son-son-mai-sac-storytelling.vercel.app/",
    "don_vi_to_chuc": "Dự án truyền thông văn hóa Sơn Son Mài Sắc (SSMS)",
    "dia_diem_hoat_dong": "Trường Đại học FPT - Phân hiệu Hà Nội (Khu CNC Hòa Lạc, Thạch Thất, Hà Nội)",
    "thong_tin_lien_he": {
        "email": "Sonsonmaisac.contact@gmail.com",
        "facebook": "https://www.facebook.com/Sonsonmaisac2026/",
        "tiktok": "https://www.tiktok.com/@sonsonmaisac.official",
        "threads": "https://www.threads.com/@Sonsonmaisac"
    },
    "su_menh": "Sơn Son Mài Sắc là dự án truyền thông văn hóa hướng đến việc đưa những giá trị của nghệ thuật sơn mài truyền thống Việt Nam đến gần hơn với thế hệ trẻ. Dự án thu hẹp khoảng cách giữa việc chỉ 'thấy đẹp' bên ngoài đến việc 'hiểu vì sao đẹp' qua việc đi sâu vào từng lớp vật liệu, công đoạn tạo tác công phu và bàn tay tài hoa của nghệ nhân.",
    "doi_ngu_sang_lap": [
        {
            "ho_ten": "Đỗ Nguyễn Đan Lê",
            "vai_tro": "Trưởng nhóm dự án / Nội dung & Nghiên cứu văn hóa",
            "hinh_anh": "/story-assets/team-members/dan-le.jpg"
        },
        {
            "ho_ten": "Đỗ Duy Nghĩa",
            "vai_tro": "Thành viên cốt lõi / Kỹ thuật & Thiết kế trải nghiệm",
            "hinh_anh": "/story-assets/team-members/duy-nghia.jpg"
        },
        {
            "ho_ten": "Chu Huyền Trang",
            "vai_tro": "Thành viên cốt lõi / Truyền thông & Quan hệ công chúng",
            "hinh_anh": "/story-assets/team-members/huyen-trang.jpg"
        },
        {
            "ho_ten": "Dương Gia Đạt",
            "vai_tro": "Thành viên cốt lõi / Sản xuất nội dung & Đồ họa",
            "hinh_anh": "/story-assets/team-members/gia-dat.jpg"
        },
        {
            "ho_ten": "Trần Anh Vũ",
            "vai_tro": "Thành viên cốt lõi / Hỗ trợ vận hành & Truyền thông",
            "hinh_anh": "/story-assets/team-members/anh-vu.jpg"
        }
    ],
    "thong_ke_thu_thap": {
        "so_trang_web": 9,
        "so_tep_hinh_anh_assets": 87,
        "dung_luong_assets": "26 MB",
        "dinh_dang_tep": ["webp", "jpg", "png", "svg", "ttf", "css", "js", "html"]
    }
}

with open('du_lieu_noi_dung/00_tong_quan_du_an.json', 'w', encoding='utf-8') as f:
    json.dump(tong_quan, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/00_tong_quan_du_an.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Tổng Quan Dự Án: {tong_quan['ten_du_an']} ({tong_quan['viet_tat']})

> **Thông điệp cốt lõi:** *"{tong_quan['slogan']}"*  
> **Tôn chỉ hoạt động:** *"{tong_quan['thong_diep_chinh']}"*

---

## 1. Thông Tin Chung
- **Tên dự án:** {tong_quan['ten_du_an']}
- **Trang web chính thức:** [{tong_quan['website']}]({tong_quan['website']})
- **Hosting dự phòng:** [{tong_quan['hosting_du_phong']}]({tong_quan['hosting_du_phong']})
- **Địa điểm thực hiện:** {tong_quan['dia_diem_hoat_dong']}
- **Email liên hệ:** [{tong_quan['thong_tin_lien_he']['email']}](mailto:{tong_quan['thong_tin_lien_he']['email']})

## 2. Kênh Truyền Thông Mạng Xã Hội
- **Facebook:** [{tong_quan['thong_tin_lien_he']['facebook']}]({tong_quan['thong_tin_lien_he']['facebook']})
- **TikTok:** [{tong_quan['thong_tin_lien_he']['tiktok']}]({tong_quan['thong_tin_lien_he']['tiktok']})
- **Threads:** [{tong_quan['thong_tin_lien_he']['threads']}]({tong_quan['thong_tin_lien_he']['threads']})

## 3. Sứ Mệnh & Tầm Nhìn
{tong_quan['su_menh']}

## 4. Đội Ngũ Thực Hiện (Project Team)
""")
    for m in tong_quan['doi_ngu_sang_lap']:
        f.write(f"- **{m['ho_ten']}**: {m['vai_tro']}  \n  *(Ảnh đại diện: `{m['hinh_anh']}`)*\n")

    f.write(f"""
## 5. Dữ Liệu Thu Thập Được
- **Tổng số trang web:** {tong_quan['thong_ke_thu_thap']['so_trang_web']} trang
- **Tổng số tệp tài nguyên đa phương tiện:** {tong_quan['thong_ke_thu_thap']['so_tep_hinh_anh_assets']} tệp (~{tong_quan['thong_ke_thu_thap']['dung_luong_assets']})
- **Tệp mã nguồn & giao diện:** Đầy đủ HTML, CSS, JS runtime, Font chữ TTF (Inter, Noto Serif, Playfair Display), hình ảnh xoay 360 độ sản phẩm.
""")

print("Saved 00_tong_quan_du_an")
