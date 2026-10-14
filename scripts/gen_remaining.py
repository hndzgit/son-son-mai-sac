import json
import os

# -------------------------------------------------------------
# 02. KHÁM PHÁ (5 CÔNG ĐOẠN & NGHỆ THUẬT SƠN MÀI)
# -------------------------------------------------------------
kham_pha = {
    "tieu_de": "Khám Phá Sơn Son Mài Sắc | Năm chặng. Một bề mặt nhiều lớp.",
    "loi_dan": "Khám phá cách một tác phẩm sơn mài được tạo nên qua những lớp sơn, vật liệu và bàn tay người thợ.",
    "ban_chat_son_mai": {
        "cau_hoi": "Vì sao lại là 'sơn mài'?",
        "giai_thich": [
            "Bởi có những thứ chỉ xuất hiện sau khi được mài đi. Trong quá trình tạo tác, màu sắc và vật liệu có thể được đặt ở những độ sâu khác nhau rồi tiếp tục được phủ bằng các lớp sơn phía trên.",
            "Khi bề mặt đã đạt điều kiện phù hợp, người thợ mài cùng nước, từng chút một. Mài quá ít, lớp bên dưới chưa xuất hiện; mài quá sâu, chi tiết đã tạo trước đó có thể bị ảnh hưởng.",
            "Qua mỗi lần mài, những lớp từng bị che khuất dần lộ ra: một mảng màu, một ánh vàng, một lớp vỏ trứng hay dấu vết của những công đoạn trước đó. Mài vì thế không chỉ làm phẳng bề mặt. Nó còn tham gia vào việc tạo nên hình ảnh cuối cùng."
        ]
    },
    "chat_lieu_son_ta": {
        "ten": "Sơn ta – Khởi nguồn từ nhựa cây tự nhiên",
        "nguon_goc": "Nhựa cây sơn được khai thác từ vùng trung du Bắc Bộ, trong đó tỉnh Phú Thọ là cái nôi nổi tiếng với nghề trồng và khai thác cây sơn.",
        "dac_tinh_va_ung_dung": "Sau khi thu hoạch và chế biến kỹ lưỡng, sơn ta được sử dụng trong suốt nhiều công đoạn: từ làm vóc, gắn kết chất liệu, phủ các lớp sơn bảo vệ đến hoàn thiện bề mặt. Sơn ta có đặc tính đóng rắn độc đáo trong môi trường ẩm, tạo nên độ bền hàng thế kỷ và chiều sâu quang học đặc biệt."
    },
    "nam_cong_doan_chuyen_sau": [
        {
            "cong_doan": "01",
            "ten": "Chuẩn bị cốt",
            "tom_tat": "Chọn và xử lý phần cốt nâng đỡ tác phẩm.",
            "chi_tiet": "Cốt là phần vật liệu tạo hình và nâng đỡ toàn bộ tác phẩm. Các chất liệu như gỗ tự nhiên, tre ép, gốm sứ, composite hay MDF cần được chọn lựa và xử lý kỹ lưỡng để chống cong vênh, mối mọt; đây là chặng mở đầu quyết định độ bền vững cho cấu trúc tác phẩm.",
            "vat_lieu_chinh": ["Gỗ", "Tre", "Gốm", "Composite", "MDF"],
            "hinh_anh": "/story-assets/craft-blank-lacquer-generated.webp",
            "alt": "Khối cốt gỗ hình hộp trước khi hoàn thiện, ảnh minh họa"
        },
        {
            "cong_doan": "02",
            "ten": "Làm vóc",
            "tom_tat": "Hom, bồi, ủ và mài để tạo mặt nền phẳng mịn.",
            "chi_tiet": "Cốt được hom bằng hỗn hợp phù sa/bột đá nhào sơn ta, bồi các lớp vải màn (cotton scrim) hoặc vải xô để gia cường chống nứt rạn. Sau đó ủ trong môi trường ẩm cho đạt trạng thái đóng rắn rồi mài phẳng bằng đá mài và nước. Các lượt xử lý này lặp lại nhiều lần cho đến khi đạt bề mặt vóc đanh chắc.",
            "vat_lieu_chinh": ["Nhựa sơn ta", "Bột phù sa/đá", "Vải màn (cotton scrim)", "Nước & đá mài"],
            "hinh_anh": "/story-assets/hero-objects-generated.webp",
            "alt": "Cận cảnh cốt gỗ đang được xử lý làm vóc, ảnh minh họa"
        },
        {
            "cong_doan": "03",
            "ten": "Sơn nền",
            "tom_tat": "Tạo sắc nền ban đầu cho bề mặt.",
            "chi_tiet": "Sau khi làm vóc, người thợ phủ lớp sơn nền để tạo sắc độ nâng đỡ hình ảnh (thường là sơn then đen láy hoặc sơn đỏ cánh gián). Với sơn ta, lớp sơn phải được ủ trong buồng ủ có độ ẩm cao (70-85%) và nhiệt độ phù hợp để khô tự nhiên; cách làm tùy vào yêu cầu của từng tác phẩm.",
            "vat_lieu_chinh": ["Sơn then (đen)", "Sơn cánh gián (nâu đỏ)", "Màu khoáng"],
            "hinh_anh": "/story-assets/team-workshop-generated.webp",
            "alt": "Mặt sơn mài đỏ đang được tạo lớp nền, ảnh minh họa"
        },
        {
            "cong_doan": "04",
            "ten": "Tạo hình và trang trí",
            "tom_tat": "Vẽ, cẩn trai, vỏ trứng hoặc thếp kim loại.",
            "chi_tiet": "Người nghệ sĩ thể hiện bố cục nghệ thuật bằng cách cẩn vỏ trứng (tạo sắc trắng rạn độc đáo), cẩn vỏ trai/xà cừ (tạo ánh ngũ sắc), thếp vàng quỳ, bạc quỳ hoặc vẽ màu thủ công. Các vật liệu này có thể được sắp đặt ở các độ sâu khác nhau, xen kẽ giữa các lớp sơn phủ.",
            "vat_lieu_chinh": ["Vỏ trứng vịt/gà", "Vỏ trai/xà cừ", "Vàng quỳ", "Bạc quỳ", "Bột màu"],
            "hinh_anh": "/story-assets/macro-hires-generated.webp",
            "alt": "Nghệ nhân đang thực hiện công đoạn tạo hình trang trí trên tác phẩm sơn mài"
        },
        {
            "cong_doan": "05",
            "ten": "Phủ, mài và hoàn thiện",
            "tom_tat": "Phủ lớp sơn bảo vệ, mài lộ hình rồi đánh bóng hoàn hảo.",
            "chi_tiet": "Tác phẩm tiếp tục được phủ lớp sơn cánh gián trong suốt để bảo vệ các chi tiết trang trí bên dưới. Khi sơn đã khô, nghệ nhân tiến hành mài nước với giấy nhám mịn hoặc lá chuối khô, bột than để lấy đi từng lớp sơn có kiểm soát, làm lộ ra các tầng màu và ánh kim bên dưới. Cuối cùng dùng bột than tinh và lòng bàn tay miết đều để đánh bóng bề mặt đạt độ sâu thẳm gương soi.",
            "vat_lieu_chinh": ["Sơn phủ trong suốt", "Nước", "Giấy ráp/đá mài", "Bột than mài", "Lòng bàn tay"],
            "hinh_anh": "/story-assets/process-five-stages-v4.webp",
            "alt": "Cận cảnh bề mặt sơn mài đã hoàn thiện, ảnh minh họa"
        }
    ]
}

with open('du_lieu_noi_dung/02_kham_pha.json', 'w', encoding='utf-8') as f:
    json.dump(kham_pha, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/02_kham_pha.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Khám Phá Nghệ Thuật Sơn Mài: {kham_pha['tieu_de']}

> *{kham_pha['loi_dan']}*

---

## 1. Bản Chất Của Tên Gọi "Sơn Mài"
### {kham_pha['ban_chat_son_mai']['cau_hoi']}
""")
    for p in kham_pha['ban_chat_son_mai']['giai_thich']:
        f.write(f"{p}\n\n")

    f.write(f"""## 2. Chất Liệu Cội Nguồn: {kham_pha['chat_lieu_son_ta']['ten']}
- **Vùng xuất xứ:** {kham_pha['chat_lieu_son_ta']['nguon_goc']}
- **Đặc tính kỹ thuật:** {kham_pha['chat_lieu_son_ta']['dac_tinh_va_ung_dung']}

## 3. Quy Trình 5 Công Đoạn Tạo Nên Một Bề Mặt
""")
    for cd in kham_pha['nam_cong_doan_chuyen_sau']:
        f.write(f"""### Công đoạn {cd['cong_doan']}: {cd['ten']}
- **Tóm tắt:** {cd['tom_tat']}
- **Chi tiết kỹ thuật:** {cd['chi_tiet']}
- **Vật liệu chính:** {', '.join(cd['vat_lieu_chinh'])}
- **Hình ảnh tư liệu:** `{cd['hinh_anh']}` *(Alt: {cd['alt']})*

---
""")

# -------------------------------------------------------------
# 04. TIN TỨC & SỰ KIỆN
# -------------------------------------------------------------
tin_tuc = {
    "tieu_de": "Tin tức & Sự kiện | Sơn Son Mài Sắc",
    "loi_dan": "Những cuộc hẹn, dấu mốc và câu chuyện đang nối dài đời sống sơn mài Việt.",
    "su_kien_sap_dien_ra": {
        "ten_su_kien": "Booth truyền thông off 'Sơn Son Mài Sắc'",
        "phan_loai": "UPCOMING SSMS",
        "thoi_gian": "14–15/10/2026 (2 ngày)",
        "dia_diem": "Sảnh Delta - Beta Trường Đại Học FPT - Hòa Lạc (Hà Nội)",
        "don_vi_to_chuc": "Dự án Sơn Son Mài Sắc (SSMS)",
        "muc_dich": "Không gian trải nghiệm trực tiếp dành cho sinh viên và giới trẻ chạm vào các lớp chất liệu sơn mài thực tế, tương tác với mô hình 3D và giao lưu cùng đội ngũ thực hiện dự án."
    },
    "hoat_dong_noi_bat": [
        {
            "ten": "Sắc Tâm 2026",
            "thoi_gian": "03 — 18.10.2026",
            "trang_thai": "TRIỂN LÃM ĐANG DIỄN RA",
            "dia_diem": "Nhà Tiền Đường, Văn Miếu – Quốc Tử Giám · Hà Nội",
            "don_vi_dong_to_chuc": "Trung tâm Hoạt động Văn hóa Khoa học Văn Miếu – Quốc Tử Giám",
            "noi_dung": "Sơn mài đương đại và trầm hương cùng hiện diện tại Văn Miếu, nối chất liệu với ký ức của không gian di sản nghìn năm văn hiến.",
            "hinh_anh": "/story-assets/event-gallery-generated-v1.webp"
        },
        {
            "ten": "Dòng chảy sơn mài",
            "thoi_gian": "10.10 — 10.11.2026",
            "trang_thai": "TRIỂN LÃM ĐANG DIỄN RA",
            "dia_diem": "Không gian trưng bày nghệ thuật đương đại Hà Nội",
            "noi_dung": "Trưng bày 65 tác phẩm của 2 thế hệ nghệ nhân và họa sĩ sơn mài, thể hiện sự tiếp biến sáng tạo từ truyền thống đến hiện đại.",
            "hinh_anh": "/story-assets/event-lacquer-portrait-v7.webp"
        },
        {
            "ten": "Việt Nam tại Biennale Arte 2026",
            "thoi_gian": "Năm 2026",
            "trang_thai": "SỰ KIỆN QUỐC TẾ",
            "dia_diem": "Venice, Ý",
            "noi_dung": "Không gian nghệ thuật quốc tế vinh danh các sáng tác sơn mài đa chất liệu của nghệ sĩ Việt Nam trên diễn đàn mỹ thuật toàn cầu.",
            "hinh_anh": "/story-assets/project-ivory-vase-v5.webp"
        }
    ],
    "tin_tuc_son_mai_hom_nay": [
        "Những đổi mới trong kỹ thuật làm vóc nhẹ và vật liệu cốt thân thiện môi trường của các nghệ nhân làng nghề Hạ Thái.",
        "Sự giao thoa giữa sơn mài truyền thống và thiết kế sản phẩm ứng dụng hiện đại: hộp trang sức, bình hoa, phụ kiện cao cấp.",
        "Người trẻ và làn sóng tìm về di sản thủ công mỹ nghệ qua các workshop trải nghiệm thực hành."
    ]
}

with open('du_lieu_noi_dung/04_tin_tuc_su_kien.json', 'w', encoding='utf-8') as f:
    json.dump(tin_tuc, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/04_tin_tuc_su_kien.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Tin Tức & Sự Kiện: {tin_tuc['tieu_de']}

> *{tin_tuc['loi_dan']}*

---

## 1. Sự Kiện Trọng Điểm: {tin_tuc['su_kien_sap_dien_ra']['ten_su_kien']}
- **Thời gian:** {tin_tuc['su_kien_sap_dien_ra']['thoi_gian']}
- **Địa điểm:** {tin_tuc['su_kien_sap_dien_ra']['dia_diem']}
- **Đơn vị tổ chức:** {tin_tuc['su_kien_sap_dien_ra']['don_vi_to_chuc']}
- **Nội dung hoạt động:** {tin_tuc['su_kien_sap_dien_ra']['muc_dich']}

## 2. Các Hoạt Động & Triển Lãm Nổi Bật
""")
    for hd in tin_tuc['hoat_dong_noi_bat']:
        f.write(f"""### {hd['ten']} [{hd['trang_thai']}]
- **Thời gian:** {hd['thoi_gian']}
- **Địa điểm:** {hd['dia_diem']}
- **Nội dung:** {hd['noi_dung']}
- **Hình ảnh tư liệu:** `{hd['hinh_anh']}`

""")

    f.write(f"""## 3. Dòng Chảy Sơn Mài Hôm Nay
""")
    for tin in tin_tuc['tin_tuc_son_mai_hom_nay']:
        f.write(f"- {tin}\n")

# -------------------------------------------------------------
# 05. VỀ DỰ ÁN
# -------------------------------------------------------------
ve_du_an = {
    "tieu_de": "Về Dự Án Sơn Son Mài Sắc | Chạm vào di sản",
    "dinh_vi": "DỰ ÁN TRUYỀN THÔNG VĂN HÓA VỀ NGHỆ THUẬT SƠN MÀI VIỆT NAM",
    "slogan": "Đi qua từng đường mài, khám phá giá trị Việt.",
    "mo_ta_tong_quan": "Sơn Son Mài Sắc là dự án truyền thông văn hóa hướng đến việc đưa những giá trị của sơn mài Việt Nam đến gần hơn với người trẻ, đặc biệt là những người đã từng nhìn thấy, từng biết đến sơn mài nhưng chưa có nhiều cơ hội để hiểu sâu về loại hình nghệ thuật và thủ công này.",
    "cau_chuyen_du_an": {
        "tieu_de": "Từ thấy 'đẹp' đến hiểu 'đẹp'",
        "noi_dung": "Đằng sau một bề mặt sơn mài hoàn thiện là nhiều lớp chất liệu, kỹ thuật, thời gian và công sức của người làm nghề. Chính khoảng cách giữa 'thấy đẹp' và 'hiểu vì sao đẹp' khiến nhiều giá trị nằm phía sau thành phẩm như quy trình tạo tác, kỹ nghệ, vai trò của nghệ nhân và chiều sâu văn hóa chưa được nhìn nhận đầy đủ. Dự án sinh ra để bắc cây cầu nối qua khoảng cách ấy."
    },
    "su_menh": {
        "muc_tieu_chinh": "Để sơn mài không chỉ được nhìn thấy, mà được hiểu và trân trọng.",
        "chi_tiet": "Đưa người trẻ đi từ 'thấy đẹp' đến 'hiểu vì sao đẹp'. Giúp người xem cảm nhận được linh hồn của từng lớp sơn, từng đường mài và sự kiên nhẫn vô tận của người nghệ nhân."
    },
    "doi_ngu_thuc_hien": [
        {
            "ho_ten": "Đỗ Nguyễn Đan Lê",
            "chuc_danh": "Trưởng nhóm dự án (Project Leader)",
            "vai_tro": "Điều phối chung, nghiên cứu nội dung và định hướng truyền thông văn hóa.",
            "anh_chan_dung": "/story-assets/team-members/dan-le.jpg"
        },
        {
            "ho_ten": "Đỗ Duy Nghĩa",
            "chuc_danh": "Thành viên cốt lõi (Core Member)",
            "vai_tro": "Phát triển công nghệ tương tác, trải nghiệm người dùng và lập trình web.",
            "anh_chan_dung": "/story-assets/team-members/duy-nghia.jpg"
        },
        {
            "ho_ten": "Chu Huyền Trang",
            "chuc_danh": "Thành viên cốt lõi (Core Member)",
            "vai_tro": "Quản lý truyền thông, quan hệ công chúng và tương tác cộng đồng.",
            "anh_chan_dung": "/story-assets/team-members/huyen-trang.jpg"
        },
        {
            "ho_ten": "Dương Gia Đạt",
            "chuc_danh": "Thành viên cốt lõi (Core Member)",
            "vai_tro": "Thiết kế đồ họa, hình ảnh trực quan và sản xuất nội dung media.",
            "anh_chan_dung": "/story-assets/team-members/gia-dat.jpg"
        },
        {
            "ho_ten": "Trần Anh Vũ",
            "chuc_danh": "Thành viên cốt lõi (Core Member)",
            "vai_tro": "Hỗ trợ sản xuất, vận hành sự kiện và tư liệu hóa triển lãm.",
            "anh_chan_dung": "/story-assets/team-members/anh-vu.jpg"
        }
    ],
    "thong_diep_ket": "Hãy cùng thêm một lớp. Mỗi sự quan tâm và sẻ chia của bạn là một lớp sắc giữ cho di sản sống mãi."
}

with open('du_lieu_noi_dung/05_ve_du_an.json', 'w', encoding='utf-8') as f:
    json.dump(ve_du_an, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/05_ve_du_an.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Về Dự Án: {ve_du_an['tieu_de']}

> **Định vị:** {ve_du_an['dinh_vi']}  
> **Slogan:** *"{ve_du_an['slogan']}"*

---

## 1. Giới Thiệu Chung
{ve_du_an['mo_ta_tong_quan']}

## 2. Câu Chuyện Dự Án: {ve_du_an['cau_chuyen_du_an']['tieu_de']}
{ve_du_an['cau_chuyen_du_an']['noi_dung']}

## 3. Sứ Mệnh Của Dự Án
> **"{ve_du_an['su_menh']['muc_tieu_chinh']}"**

{ve_du_an['su_menh']['chi_tiet']}

## 4. Những Người Thực Hiện (Team Members)
""")
    for m in ve_du_an['doi_ngu_thuc_hien']:
        f.write(f"""### {m['ho_ten']}
- **Chức danh:** {m['chuc_danh']}
- **Trách nhiệm:** {m['vai_tro']}
- **Ảnh chân dung:** `{m['anh_chan_dung']}`

""")

    f.write(f"""## 5. Lời Kêu Gọi: {ve_du_an['thong_diep_ket']}
""")

# -------------------------------------------------------------
# 06. SẢN PHẨM (MẪU HỘP CỐT SƠN MÀI)
# -------------------------------------------------------------
san_pham = {
    "tieu_de": "Tìm một tác phẩm sơn mài | Sơn Son Mài Sắc",
    "loi_dan": "Mang câu chuyện di sản phù hợp với bạn.",
    "tac_pham_tieu_bieu": {
        "ten": "Hộp hoa sen",
        "loai": "Mẫu hình ảnh minh họa · hoa sen trên nền sơn tối",
        "dac_diem": ["Hộp", "Màu cánh gián", "Hoa văn hoa sen"],
        "mo_ta": "Chiếc hộp cốt gỗ sơn mài truyền thống với họa tiết hoa sen cách điệu khảm vàng quỳ và vỏ trứng tinh xảo trên nền sơn then cánh gián.",
        "he_thong_anh_xoay_360": [f"/story-assets/box-{i}.jpg" for i in [1, 5, 6, 7, 8, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]],
        "huong_dan_tuong_tac": "Kéo trên mô hình hoặc dùng phím mũi tên để xem xoay 360 độ từ nhiều góc nhìn."
    },
    "bo_loc_phan_loai": {
        "mau_sac": ["Tất cả", "Cánh gián", "Đen then", "Đỏ son"],
        "hoa_van": ["Tất cả", "Hoa sen", "Họa tiết truyền thống"],
        "nghe_nhan": ["Tất cả", "Nghệ nhân Hạ Thái", "Nghệ nhân truyền thống"],
        "chat_lieu": ["Tất cả", "Vàng", "Vỏ trứng", "Lớp nền", "Xà cừ"],
        "cong_nang": ["Tất cả", "Lưu giữ", "Bày vật phẩm", "Trưng bày nghệ thuật"]
    }
}

with open('du_lieu_noi_dung/06_san_pham.json', 'w', encoding='utf-8') as f:
    json.dump(san_pham, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/06_san_pham.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Sản Phẩm: {san_pham['tieu_de']}

> *{san_pham['loi_dan']}*

---

## 1. Tác Phẩm Tiêu Biểu: {san_pham['tac_pham_tieu_bieu']['ten']}
- **Phân loại:** {san_pham['tac_pham_tieu_bieu']['loai']}
- **Đặc trưng:** {', '.join(san_pham['tac_pham_tieu_bieu']['dac_diem'])}
- **Mô tả:** {san_pham['tac_pham_tieu_bieu']['mo_ta']}
- **Hướng dẫn xem:** {san_pham['tac_pham_tieu_bieu']['huong_dan_tuong_tac']}

### Bộ ảnh đa góc xoay 360 độ (16 góc chụp chất lượng cao):
""")
    for img in san_pham['tac_pham_tieu_bieu']['he_thong_anh_xoay_360']:
        f.write(f"- `{img}`\n")

    f.write(f"""
## 2. Hệ Thống Bộ Lọc & Tiêu Chí Tùy Biến
- **Màu sắc:** {', '.join(san_pham['bo_loc_phan_loai']['mau_sac'])}
- **Hoa văn:** {', '.join(san_pham['bo_loc_phan_loai']['hoa_van'])}
- **Chất liệu:** {', '.join(san_pham['bo_loc_phan_loai']['chat_lieu'])}
- **Công năng:** {', '.join(san_pham['bo_loc_phan_loai']['cong_nang'])}
""")

# -------------------------------------------------------------
# 07. TRẢI NGHIỆM MÔ PHỎNG 3D
# -------------------------------------------------------------
trai_nghiem = {
    "tieu_de": "Trải Nghiệm Bề Mặt Sơn Mài & Mô Phỏng Tạo Tác 3D",
    "trang_lien_quan": ["/trai-nghiem", "/trai-nghiem/hanh-trinh", "/tu-chinh"],
    "quy_trinh_mo_phong_hanh_trinh": [
        {
            "buoc": 1,
            "ten_buoc": "Chọn cốt",
            "cac_lua_chon": [
                {"loai": "Gỗ tự nhiên", "bieu_tuong": "/story-assets/raw-wood-grain-v1.webp"},
                {"loai": "Tre ép", "bieu_tuong": "/story-assets/core-bamboo.svg"},
                {"loai": "Gốm sứ", "bieu_tuong": "/story-assets/core-ceramic.svg"},
                {"loai": "Composite", "bieu_tuong": "/story-assets/core-composite.svg"},
                {"loai": "MDF", "bieu_tuong": "/story-assets/core-mdf.svg"}
            ],
            "y_nghia": "Cốt là khung xương nền tảng tạo hình cho sản phẩm."
        },
        {
            "buoc": 2,
            "ten_buoc": "Làm vóc & Sơn lót",
            "thao_tac": "Dán bồi vải màn (cotton scrim), phủ các lớp sơn lót và ủ ẩm",
            "tai_nguyen": "/story-assets/cotton-scrim.svg"
        },
        {
            "buoc": 3,
            "ten_buoc": "Phủ sơn nền",
            "thao_tac": "Lựa chọn tông màu sơn then (đen huyền bí), sơn đỏ son hoặc cánh gián",
            "tai_nguyen": "/story-assets/mat-pigment.jpg"
        },
        {
            "buoc": 4,
            "ten_buoc": "Tạo hình và trang trí",
            "thao_tac": "Áp khuôn họa tiết sen, gắn mảnh vỏ trứng, dán vàng quỳ/bạc quỳ hoặc cẩn xà cừ",
            "tai_nguyen": [
                "/story-assets/journey-lotus-stencil-v8.webp",
                "/story-assets/lotus-inlay-stencil-v6.webp",
                "/textures/eggshell_crackle.svg",
                "/textures/gold_leaf_texture.svg",
                "/story-assets/mat-gold.jpg",
                "/story-assets/mat-silver.jpg",
                "/story-assets/mat-egg.jpg",
                "/story-assets/mat-pearl.jpg",
                "/story-assets/mat-shell.jpg"
            ]
        },
        {
            "buoc": 5,
            "ten_buoc": "Phủ sơn bảo vệ & Mài nước lộ lớp",
            "thao_tac": "Phủ sơn trong suốt bảo vệ, mài nước nhiều cấp độ để lộ các lớp trang trí ẩn giấu và đánh bóng gương"
        }
    ]
}

with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.json', 'w', encoding='utf-8') as f:
    json.dump(trai_nghiem, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Trải Nghiệm Tương Tác: {trai_nghiem['tieu_de']}

Dự án cung cấp một hệ thống mô phỏng 3D WebGL trực tiếp trên trình duyệt, cho phép người dùng tự tay trải nghiệm quy trình chế tác một bề mặt sơn mài:

## Quy Trình 5 Bước Trải Nghiệm:
""")
    for step in trai_nghiem['quy_trinh_mo_phong_hanh_trinh']:
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

print("All remaining sections saved successfully!")
