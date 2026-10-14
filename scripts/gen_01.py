import json
import os

# -------------------------------------------------------------
# 01. TRANG CHỦ
# -------------------------------------------------------------
trang_chu = {
    "tieu_de": "Sơn Son Mài Sắc | Chạm vào di sản",
    "mo_ta": "Khám phá nghệ thuật sơn mài Việt Nam qua từng lớp vật liệu, câu chuyện, sản phẩm và trải nghiệm tạo bề mặt 3D của riêng bạn.",
    "phan_mo_dau": {
        "slogan": "Đi qua từng lớp, khám phá sơn mài Việt Nam",
        "nut_keu_goi": "KHÁM PHÁ NGAY ⟶",
        "hinh_anh_chinh": {
            "duong_dan": "/story-assets/hero-lacquer-generated.webp",
            "chu_thich": "Bình sơn mài hoa sen trên nền vàng son và họa tiết truyền thống"
        },
        "the_chuyen_de": [
            {
                "nhan": "KHÁM PHÁ",
                "tieu_de": "Thế giới sơn mài Việt",
                "duong_dan": "/kham-pha",
                "hinh_anh": "/story-assets/key-visual.jpg",
                "alt": "Bề mặt tranh sơn mài khảm vàng và vỏ trứng"
            },
            {
                "nhan": "CHẤT LIỆU",
                "tieu_de": "Những gì làm nên sắc mài",
                "duong_dan": "/#gioi-thieu",
                "hinh_anh": "/story-assets/mat-gold.jpg",
                "alt": "Vàng quỳ và sắc màu trong nghệ thuật sơn mài"
            },
            {
                "nhan": "KỸ THUẬT",
                "tieu_de": "Bàn tay tạo tác vượt thời gian",
                "duong_dan": "/kham-pha#5-cong-doan",
                "hinh_anh": "/story-assets/team-workshop-generated.webp",
                "alt": "Bàn tay đang tạo tác trên bề mặt sơn mài, ảnh minh họa"
            },
            {
                "nhan": "CÂU CHUYỆN",
                "tieu_de": "Con người và di sản",
                "duong_dan": "/cau-chuyen-son-mai#dong-thoi-gian",
                "hinh_anh": "/story-assets/heritage-profiles-v5.webp",
                "alt": "Câu chuyện về con người và di sản sơn mài Việt Nam"
            }
        ]
    },
    "dinh_nghia_son_mai": {
        "tieu_de": "SƠN MÀI LÀ GÌ?",
        "khau_hieu": "Một tác phẩm được tạo nên bằng cả việc phủ lên và mài đi.",
        "noi_dung": [
            "Với sơn mài, hình ảnh không chỉ nằm trên bề mặt. Người nghệ sĩ tạo nên nhiều lớp sơn, màu sắc và vật liệu, có những lớp được phủ kín dưới lớp sơn tiếp theo.",
            "Qua quá trình mài với nước, các lớp nằm bên dưới dần xuất hiện và cùng tạo nên bề mặt cuối cùng.",
            "Càng đi qua nhiều lớp, hình ảnh càng được hé lộ."
        ],
        "nguon_tu_lieu": {
            "ten": "Tư liệu về vóc và các công đoạn sơn mài · Bộ Công Thương",
            "url": "https://moit.gov.vn/tin-tuc/thi-truong-nuoc-ngoai/doc-dao-son-mai.html"
        },
        "tac_pham_minh_hoa": {
            "hinh_anh": "/story-assets/macro-hires-generated.webp",
            "chu_thich": "Cận cảnh hoa sen, ánh vàng và nền sơn then trên tác phẩm sơn mài"
        }
    },
    "nam_chang_tao_tac": [
        {
            "so_thu_tu": "01",
            "ten": "CHUẨN BỊ CỐT",
            "mo_ta": "Tạo dáng và làm phẳng bề mặt cốt gỗ, xử lý kỹ để bảo đảm độ ổn định cho toàn bộ sản phẩm."
        },
        {
            "so_thu_tu": "02",
            "ten": "LÀM VÓC",
            "mo_ta": "Bó hom, phủ sơn lót và mài nhiều lớp để hình thành bề mặt nền mịn, chắc và đồng đều."
        },
        {
            "so_thu_tu": "03",
            "ten": "SƠN NỀN",
            "mo_ta": "Phủ các lớp sơn nền nhằm tạo chiều sâu màu sắc và chuẩn bị nền bám tốt cho các công đoạn trang trí tiếp theo."
        },
        {
            "so_thu_tu": "04",
            "ten": "TẠO HÌNH VÀ TRANG TRÍ",
            "mo_ta": "Đặt màu, gắn chất liệu như vỏ trứng, vàng quỳ hoặc họa tiết thủ công để xây dựng bố cục thẩm mỹ."
        },
        {
            "so_thu_tu": "05",
            "ten": "PHỦ, MÀI VÀ HOÀN THIỆN",
            "mo_ta": "Phủ lớp sơn cuối, mài nhẵn và đánh bóng để hoàn thiện bề mặt, làm nổi bật độ sâu và vẻ tinh xảo của tác phẩm."
        }
    ],
    "he_chat_lieu_ben_trong": {
        "tieu_de": "NHIỀU LỚP. MỘT BỀ MẶT.",
        "trinh_tu": "Làm vóc → Cẩn & tạo hình → Phủ & ủ → Mài nước → Đánh bóng",
        "cac_chat_lieu": [
            {
                "so_thu_tu": "01",
                "ten": "Sơn then",
                "mo_ta": "Nền sơn đen tạo chiều sâu, làm nổi màu và ánh kim của những vật liệu đặt trên bề mặt."
            },
            {
                "so_thu_tu": "02",
                "ten": "Sơn / màu",
                "mo_ta": "Màu được phối cùng sơn để xây dựng sắc độ, từ những mảng nền đến nét vẽ và chi tiết."
            },
            {
                "so_thu_tu": "03",
                "ten": "Vỏ trứng",
                "mo_ta": "Mảnh vỏ trứng tạo vùng sáng, đường rạn và một kết cấu rất riêng trên nền sơn."
            },
            {
                "so_thu_tu": "04",
                "ten": "Vàng",
                "mo_ta": "Vàng thếp tạo điểm sáng ấm; ánh kim biến đổi theo ánh sáng và góc nhìn."
            },
            {
                "so_thu_tu": "05",
                "ten": "Bạc",
                "mo_ta": "Bạc thếp mở ra những vùng ánh kim lạnh, cân bằng sắc son và nền tối."
            },
            {
                "so_thu_tu": "06",
                "ten": "Xà cừ",
                "mo_ta": "Vỏ trai, ốc mang ánh sắc óng, từ trắng ngà đến xanh và hồng khi đổi góc nhìn."
            }
        ]
    },
    "trai_nghiem_cham_vao_lop_sac": {
        "tieu_de": "Vẻ đẹp nằm sau từng đường mài",
        "cac_lop_vat_lieu": [
            {"tang": "01", "ten": "Cốt gỗ", "vai_tro": "Nền tảng của chiếc hộp"},
            {"tang": "02", "ten": "Sơn lót & Vóc", "vai_tro": "Tạo độ bền, liên kết"},
            {"tang": "03", "ten": "Sơn màu", "vai_tro": "Sơn đỏ truyền thống"},
            {"tang": "04", "ten": "Họa tiết khảm", "vai_tro": "Vàng lá, vỏ trứng…"},
            {"tang": "05", "ten": "Lớp phủ trong", "vai_tro": "Bảo vệ và tạo độ sâu"}
        ]
    }
}

with open('du_lieu_noi_dung/01_trang_chu.json', 'w', encoding='utf-8') as f:
    json.dump(trang_chu, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/01_trang_chu.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Trang Chủ: {trang_chu['tieu_de']}

> *{trang_chu['mo_ta']}*

## 1. Mở Đầu
- **Khẩu hiệu:** {trang_chu['phan_mo_dau']['slogan']}
- **Nút hành động:** {trang_chu['phan_mo_dau']['nut_keu_goi']}
- **Ảnh đại diện:** `{trang_chu['phan_mo_dau']['hinh_anh_chinh']['duong_dan']}` ({trang_chu['phan_mo_dau']['hinh_anh_chinh']['chu_thich']})

### Các Thẻ Khám Phá Nổi Bật:
""")
    for card in trang_chu['phan_mo_dau']['the_chuyen_de']:
        f.write(f"- **[{card['nhan']}] {card['tieu_de']}**: Liên kết `{card['duong_dan']}` | Ảnh: `{card['hinh_anh']}`\n")

    f.write(f"""
## 2. Sơn Mài Là Gì?
> **{trang_chu['dinh_nghia_son_mai']['khau_hieu']}**

{chr(10).join(trang_chu['dinh_nghia_son_mai']['noi_dung'])}

- **Nguồn tài liệu:** [{trang_chu['dinh_nghia_son_mai']['nguon_tu_lieu']['ten']}]({trang_chu['dinh_nghia_son_mai']['nguon_tu_lieu']['url']})
- **Minh họa chi tiết:** `{trang_chu['dinh_nghia_son_mai']['tac_pham_minh_hoa']['hinh_anh']}`

## 3. 5 Chặng Trong Quá Trình Tạo Tác
""")
    for stg in trang_chu['nam_chang_tao_tac']:
        f.write(f"### {stg['so_thu_tu']}. {stg['ten']}\n{stg['mo_ta']}\n\n")

    f.write(f"""## 4. Bên Trong Một Tác Phẩm: {trang_chu['he_chat_lieu_ben_trong']['tieu_de']}
*Trình tự thực hiện:* `{trang_chu['he_chat_lieu_ben_trong']['trinh_tu']}`

""")
    for mat in trang_chu['he_chat_lieu_ben_trong']['cac_chat_lieu']:
        f.write(f"- **{mat['so_thu_tu']}. {mat['ten']}**: {mat['mo_ta']}\n")

    f.write(f"""
## 5. Trải Nghiệm Tách Lớp Bề Mặt Sơn Mài
""")
    for layer in trang_chu['trai_nghiem_cham_vao_lop_sac']['cac_lop_vat_lieu']:
        f.write(f"- **Lớp {layer['tang']} - {layer['ten']}**: {layer['vai_tro']}\n")

print("Saved 01_trang_chu")
