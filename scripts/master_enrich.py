import json
import os

# ==============================================================================
# 1. ENRICH 01_TRANG_CHU
# ==============================================================================
with open('du_lieu_noi_dung/01_trang_chu.json', 'r', encoding='utf-8') as f:
    tc = json.load(f)

tc['phan_mo_dau']['chu_thich_hinh_anh'] = "Hình ảnh minh họa nghệ thuật sơn mài"
tc['he_chat_lieu_ben_trong']['loi_dan'] = "Điều ta nhìn thấy ở một tác phẩm hoàn thiện chỉ là bề mặt cuối cùng của cả một quá trình. Mỗi công đoạn để lại một lớp, một dấu vết hoặc một thay đổi trên bề mặt. Và để hiểu sơn mài, cách trực quan nhất là đi qua chính những lớp ấy."
tc['trai_nghiem_cham_vao_lop_sac']['loi_dan'] = "Khám phá từng lớp vật liệu, ghép lại thành bề mặt sơn mài. Nền tảng tạo dáng, nâng đỡ toàn bộ các lớp sơn mài."
tc['trai_nghiem_cham_vao_lop_sac']['huong_dan_thao_tac'] = "Trải nghiệm minh họa cấu trúc và thao tác; quy trình thực tế tùy tác phẩm."

with open('du_lieu_noi_dung/01_trang_chu.json', 'w', encoding='utf-8') as f:
    json.dump(tc, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/01_trang_chu.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Trang Chủ: {tc['tieu_de']}

> *{tc['mo_ta']}*

---

## 1. Mở Đầu
- **Khẩu hiệu:** {tc['phan_mo_dau']['slogan']}
- **Nút hành động:** {tc['phan_mo_dau']['nut_keu_goi']}
- **Ảnh đại diện:** `{tc['phan_mo_dau']['hinh_anh_chinh']['duong_dan']}` ({tc['phan_mo_dau']['hinh_anh_chinh']['chu_thich']})
- **Ghi chú ảnh:** {tc['phan_mo_dau']['chu_thich_hinh_anh']}

### Các Thẻ Khám Phá Nổi Bật:
""")
    for card in tc['phan_mo_dau']['the_chuyen_de']:
        f.write(f"- **[{card['nhan']}] {card['tieu_de']}**: Liên kết `{card['duong_dan']}` | Ảnh: `{card['hinh_anh']}` *(Alt: {card['alt']})*\n")

    f.write(f"""
## 2. Sơn Mài Là Gì?
> **{tc['dinh_nghia_son_mai']['khau_hieu']}**

{chr(10).join(tc['dinh_nghia_son_mai']['noi_dung'])}

- **Nguồn tài liệu:** [{tc['dinh_nghia_son_mai']['nguon_tu_lieu']['ten']}]({tc['dinh_nghia_son_mai']['nguon_tu_lieu']['url']})
- **Minh họa chi tiết:** `{tc['dinh_nghia_son_mai']['tac_pham_minh_hoa']['hinh_anh']}` *(Chú thích: {tc['dinh_nghia_son_mai']['tac_pham_minh_hoa']['chu_thich']})*

## 3. 5 Chặng Trong Quá Trình Tạo Tác
""")
    for stg in tc['nam_chang_tao_tac']:
        f.write(f"### {stg['so_thu_tu']}. {stg['ten']}\n{stg['mo_ta']}\n\n")

    f.write(f"""## 4. Bên Trong Một Tác Phẩm: {tc['he_chat_lieu_ben_trong']['tieu_de']}
> *"{tc['he_chat_lieu_ben_trong']['loi_dan']}"*

*Trình tự thực hiện:* `{tc['he_chat_lieu_ben_trong']['trinh_tu']}`

""")
    for mat in tc['he_chat_lieu_ben_trong']['cac_chat_lieu']:
        f.write(f"- **{mat['so_thu_tu']}. {mat['ten']}**: {mat['mo_ta']}\n")

    f.write(f"""
## 5. Trải Nghiệm Tách Lớp Bề Mặt Sơn Mài
> *"{tc['trai_nghiem_cham_vao_lop_sac']['loi_dan']}"*

""")
    for layer in tc['trai_nghiem_cham_vao_lop_sac']['cac_lop_vat_lieu']:
        f.write(f"- **Lớp {layer['tang']} - {layer['ten']}**: {layer['vai_tro']}\n")

    f.write(f"\n*Lưu ý thao tác:* {tc['trai_nghiem_cham_vao_lop_sac']['huong_dan_thao_tac']}\n")


# ==============================================================================
# 2. ENRICH 02_KHAM_PHA
# ==============================================================================
with open('du_lieu_noi_dung/02_kham_pha.json', 'r', encoding='utf-8') as f:
    kp = json.load(f)

kp['loi_dan_quy_trinh'] = "Năm chặng để dễ hình dung, không phải công thức cứng: phủ, ủ, cẩn và mài thường đan xen, lặp lại theo từng tác phẩm."
kp['chat_lieu_son_ta']['giai_thich_sau'] = "Trước khi trở thành một lớp sơn, nó bắt đầu từ nhựa cây. Sau khi được khai thác và chế biến, sơn ta được sử dụng trong nhiều công đoạn: làm vóc, gắn kết vật liệu, phủ các lớp sơn và hoàn thiện bề mặt. Từ một chất liệu tự nhiên, người thợ tạo nên những lớp sơn có khả năng kết nối với nhau qua cả một quá trình dài."
kp['luu_y_thao_tac'] = {
    "chuan_bi_cot": "Chọn một loại cốt để xem vật liệu ảnh hưởng ra sao đến việc chuẩn bị. Gỗ, tre, gốm và vật liệu khác cần cách xử lý phù hợp với cấu tạo tác phẩm.",
    "lop_vai": "Lớp vải chỉ là lựa chọn minh họa khi phù hợp với cấu tạo cốt; không phải bước bắt buộc cho mọi vật liệu.",
    "mat_cat": "Mặt cắt là sơ đồ giải thích, không biểu diễn tỷ lệ hoặc thứ tự cố định cho mọi tác phẩm.",
    "mo_phong": "Mô phỏng tương tác để giải thích nguyên lý; lựa chọn và hình ảnh không phải công thức chế tác."
}

with open('du_lieu_noi_dung/02_kham_pha.json', 'w', encoding='utf-8') as f:
    json.dump(kp, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/02_kham_pha.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Khám Phá Nghệ Thuật Sơn Mài: {kp['tieu_de']}

> *{kp['loi_dan']}*

---

## 1. Bản Chất Của Tên Gọi "Sơn Mài"
### {kp['ban_chat_son_mai']['cau_hoi']}
""")
    for p in kp['ban_chat_son_mai']['giai_thich']:
        f.write(f"{p}\n\n")

    f.write(f"""## 2. Chất Liệu Cội Nguồn: {kp['chat_lieu_son_ta']['ten']}
- **Vùng xuất xứ:** {kp['chat_lieu_son_ta']['nguon_goc']}
- **Đặc tính kỹ thuật:** {kp['chat_lieu_son_ta']['dac_tinh_va_ung_dung']}
- **Quá trình hình thành:** {kp['chat_lieu_son_ta']['giai_thich_sau']}

## 3. Quy Trình 5 Công Đoạn Tạo Nên Một Bề Mặt
> *"{kp['loi_dan_quy_trinh']}"*

""")
    for cd in kp['nam_cong_doan_chuyen_sau']:
        f.write(f"""### Công đoạn {cd['cong_doan']}: {cd['ten']}
- **Tóm tắt:** {cd['tom_tat']}
- **Chi tiết kỹ thuật:** {cd['chi_tiet']}
- **Vật liệu chính:** {', '.join(cd['vat_lieu_chinh'])}
- **Hình ảnh tư liệu:** `{cd['hinh_anh']}` *(Alt: {cd['alt']})*

---
""")

    f.write(f"""## 4. Chú Thích Kỹ Thuật & Khuyến Cáo
- **Chuẩn bị cốt:** {kp['luu_y_thao_tac']['chuan_bi_cot']}
- **Lớp vải gia cường:** {kp['luu_y_thao_tac']['lop_vai']}
- **Sơ đồ mặt cắt:** {kp['luu_y_thao_tac']['mat_cat']}
- **Nguyên lý mô phỏng:** {kp['luu_y_thao_tac']['mo_phong']}
""")


# ==============================================================================
# 3. ENRICH 04_TIN_TUC_SU_KIEN
# ==============================================================================
with open('du_lieu_noi_dung/04_tin_tuc_su_kien.json', 'r', encoding='utf-8') as f:
    tt = json.load(f)

tt['khuyen_cao_su_kien'] = "Ngày, địa điểm và trạng thái có thể thay đổi; hãy kiểm tra nguồn của ban tổ chức trước khi tham gia. Ảnh có nhãn “Ảnh minh họa” không phải ảnh tư liệu của sự kiện."
tt['nguon_tu_lieu_su_kien'] = {
    "sac_tam": "Hanoi Grapevine · thông tin từ ban tổ chức",
    "dong_chay": "65 tác phẩm của 20 tác giả gặp nhau tại một điểm chung: tình yêu với nghệ thuật sơn mài Việt.",
    "biennale": "La Biennale di Venezia · trang quốc gia Việt Nam (Lần đầu Việt Nam tham gia chính thức; sơn mài là chất liệu trung tâm trong đối thoại nghệ thuật đương đại.)"
}

with open('du_lieu_noi_dung/04_tin_tuc_su_kien.json', 'w', encoding='utf-8') as f:
    json.dump(tt, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/04_tin_tuc_su_kien.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Tin Tức & Sự Kiện: {tt['tieu_de']}

> *{tt['loi_dan']}*  
> **Lưu ý:** *{tt['khuyen_cao_su_kien']}*

---

## 1. Sự Kiện Trọng Điểm: {tt['su_kien_sap_dien_ra']['ten_su_kien']}
- **Phân loại:** {tt['su_kien_sap_dien_ra']['phan_loai']}
- **Thời gian:** {tt['su_kien_sap_dien_ra']['thoi_gian']}
- **Địa điểm:** {tt['su_kien_sap_dien_ra']['dia_diem']}
- **Đơn vị tổ chức:** {tt['su_kien_sap_dien_ra']['don_vi_to_chuc']}
- **Nội dung hoạt động:** {tt['su_kien_sap_dien_ra']['muc_dich']}

---

## 2. Các Hoạt Động & Triển Lãm Nổi Bật
""")
    for hd in tt['hoat_dong_noi_bat']:
        extra = ""
        if "Sắc Tâm" in hd['ten']:
            extra = f"- **Nguồn tư liệu:** {tt['nguon_tu_lieu_su_kien']['sac_tam']}\n"
        elif "Dòng chảy" in hd['ten']:
            extra = f"- **Quy mô:** {tt['nguon_tu_lieu_su_kien']['dong_chay']}\n"
        elif "Biennale" in hd['ten']:
            extra = f"- **Ý nghĩa lịch sử:** {tt['nguon_tu_lieu_su_kien']['biennale']}\n"

        f.write(f"""### {hd['ten']} [{hd['trang_thai']}]
- **Thời gian:** {hd['thoi_gian']}
- **Địa điểm:** {hd['dia_diem']}
- **Nội dung:** {hd['noi_dung']}
{extra}- **Hình ảnh tư liệu:** `{hd['hinh_anh']}`

""")

    f.write(f"""---

## 3. Bản Tin Báo Chí & Truyền Thông (12 Bài Báo Cập Nhật Từ /api/news)
""")
    for idx, item in enumerate(tt['danh_sach_tin_tuc_bao_chi'], 1):
        f.write(f"""### {idx}. {item['title']}
- **Nguồn báo chí:** {item['source']} | **Ngày đăng:** {item['date'][:10]}
- **Ảnh thu nhỏ (Thumbnail):** `{item['thumbnail']}`
- **Tóm tắt:** {item['summary']}
- **Liên kết bài viết:** [{item['url']}]({item['url']})

""")


# ==============================================================================
# 4. ENRICH 05_VE_DU_AN
# ==============================================================================
with open('du_lieu_noi_dung/05_ve_du_an.json', 'r', encoding='utf-8') as f:
    vda = json.load(f)

vda['cau_chuyen_du_an']['noi_dung_day_du'] = "Đằng sau một bề mặt sơn mài hoàn thiện là nhiều lớp chất liệu, kỹ thuật, thời gian và công sức của người làm nghề. Chính khoảng cách giữa “thấy đẹp” và “hiểu vì sao đẹp” khiến nhiều giá trị nằm phía sau thành phẩm như quy trình tạo tác, kỹ nghệ, vai trò của nghệ nhân và chiều sâu văn hóa chưa được nhận diện đầy đủ. Đây cũng là vấn đề mà dự án xác định cần được giải quyết bằng một cách tiếp cận trực quan và gần gũi hơn với người trẻ. Từ đó, Sơn Son Mài Sắc lựa chọn cách kể “đi từ bề mặt đến chiều sâu – từ thấy đẹp đến hiểu đẹp”, đưa công chúng lần lượt khám phá chất liệu, kỹ thuật, thời gian, con người và những giá trị văn hóa được gửi gắm trong sơn mài Việt Nam."

vda['y_nghia_ten_goi_bon_chu'] = {
    "tieu_de": "Ý NGHĨA TÊN GỌI · Sơn Son Mài Sắc",
    "loi_dan": "Tên gọi “Sơn Son Mài Sắc” cũng được hình thành từ những yếu tố gắn trực tiếp với nghề:",
    "cac_chu": {
        "Sơn": "gợi chất liệu và nghề sơn mài.",
        "Son": "gợi sắc son và sự bền bỉ.",
        "Mài": "là kỹ thuật đặc trưng của quá trình tạo tác.",
        "Sắc": "gợi vẻ đẹp thị giác và rộng hơn là bản sắc văn hóa."
    },
    "y_nghia_sau": "Qua bốn chữ ấy, dự án mở ra hành trình từ những gì có thể nhìn thấy trên bề mặt đến những giá trị sâu hơn được tạo nên bởi nghề và người làm nghề.",
    "ket_luan": "Từ thấy đẹp → đến hiểu đẹp → để thêm trân trọng giá trị Việt."
}

vda['tam_nhin_day_du'] = "Để sơn mài không chỉ được nhìn thấy, mà được hiểu và trân trọng. Sơn Son Mài Sắc hướng tới một cách nhìn gần gũi hơn về sơn mài Việt Nam, nơi những giá trị truyền thống không chỉ được nhắc đến như dấu vết của quá khứ mà tiếp tục được nhận diện, cảm nhận và thưởng thức trong đời sống hôm nay. Dự án mong muốn góp phần để người trẻ nhìn sơn mài như một giá trị văn hóa sống — được hình thành từ chất liệu, kỹ thuật, tư duy thẩm mỹ, tri thức nghề và những con người đang tiếp tục gìn giữ, thực hành và làm mới nghề qua từng thế hệ."

vda['su_menh_day_du'] = "Đưa người trẻ đi từ “thấy đẹp” đến “hiểu vì sao đẹp”. Sơn Son Mài Sắc sử dụng ngôn ngữ truyền thông trực quan, đương đại và dễ tiếp cận để mở ra những lớp giá trị phía sau một bề mặt sơn mài. Thông qua việc giải thích chất liệu, quy trình, kỹ thuật, thời gian tạo tác và câu chuyện của người làm nghề, dự án giúp người trẻ có một điểm bắt đầu dễ dàng hơn để khám phá sơn mài, từng bước hình thành hiểu biết, sự quan tâm và khả năng thưởng thức sâu hơn đối với giá trị văn hóa Việt Nam."

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
{vda['cau_chuyen_du_an']['noi_dung_day_du']}

## 3. Ý Nghĩa Tên Gọi 4 Chữ "SƠN SON MÀI SẮC"
> *"{vda['y_nghia_ten_goi_bon_chu']['loi_dan']}"*

- **Sơn:** {vda['y_nghia_ten_goi_bon_chu']['cac_chu']['Sơn']}
- **Son:** {vda['y_nghia_ten_goi_bon_chu']['cac_chu']['Son']}
- **Mài:** {vda['y_nghia_ten_goi_bon_chu']['cac_chu']['Mài']}
- **Sắc:** {vda['y_nghia_ten_goi_bon_chu']['cac_chu']['Sắc']}

> {vda['y_nghia_ten_goi_bon_chu']['y_nghia_sau']}  
> **{vda['y_nghia_ten_goi_bon_chu']['ket_luan']}**

## 4. Tầm Nhìn Dự Án
{vda['tam_nhin_day_du']}

## 5. Sứ Mệnh Dự Án
{vda['su_menh_day_du']}

## 6. Những Người Thực Hiện (5 Thành Viên Ban Điều Hành)
*Năm thành viên cùng đảm nhận các vai trò trong dự án:*

""")
    for m in vda['doi_ngu_thuc_hien']:
        f.write(f"""### {m['ho_ten']} (`{m['ky_hieu']}`)
- **Vai trò chính thức:** **{m['vai_tro']}**
- **Ảnh chân dung:** `{m['anh_chan_dung']}`

""")

    f.write(f"""## 7. Lời Kêu Gọi
> *"{vda['thong_diep_ket']}"*
""")


# ==============================================================================
# 5. ENRICH 06_SAN_PHAM & 07_TRAI_NGHIEM
# ==============================================================================
with open('du_lieu_noi_dung/06_san_pham.json', 'r', encoding='utf-8') as f:
    sp = json.load(f)

sp['huong_dan_xem'] = "Kéo trên mô hình hoặc dùng phím mũi tên để xem nhiều góc. Đây là mẫu minh họa; thông tin nghệ nhân và chất liệu thực tế chưa được xác nhận."
sp['khuyen_cao_ban_phoi'] = "Bản phối là hình mô phỏng theo lựa chọn, chưa phải đơn đặt hàng hay xác nhận chế tác."
sp['huong_dan_tuong_tac'] = "Kéo để xoay · Dùng thanh trượt để thu phóng hoặc dùng phím mũi tên."

with open('du_lieu_noi_dung/06_san_pham.json', 'w', encoding='utf-8') as f:
    json.dump(sp, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/06_san_pham.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Danh Mục Sản Phẩm: {sp['tieu_de']}

> *{sp['loi_dan']}*  
> **Hướng dẫn xem:** *{sp['huong_dan_xem']}*  
> **Lưu ý bản phối:** *{sp['khuyen_cao_ban_phoi']}*

---

## 1. Danh Sách 4 Mẫu Tác Phẩm Cốt
""")
    for item in sp['danh_sach_san_pham']:
        f.write(f"""### {item['ten']} (`{item['id']}`)
- **Phân loại:** {item['phan_loai']}
- **Màu nền:** {item['mau_nen']}
- **Họa tiết:** {item['hoa_van']}
- **Chất liệu:** {', '.join(item['chat_lieu'])}
- **Công năng:** {item['cong_nang']}
- **Ghi chú:** {item['ghi_chu']}
- **Hình ảnh đại diện:** `{item['hinh_anh']}`
""")
        if 'bo_anh_xoay_360' in item:
            f.write(f"- **Bộ 16 ảnh xoay 360 độ:**\n")
            for img in item['bo_anh_xoay_360']:
                f.write(f"  + `{img}`\n")
        f.write("\n---\n\n")

    f.write(f"""## 2. Hệ Thống Tùy Biến Bản Phối Cá Nhân (Studio)
> *{sp['huong_dan_tuong_tac']}*

- **Màu nền:** {', '.join(sp['tuy_bien_ban_phoi_ca_nhan']['mau_nen_chon'])}
- **Hoa văn:** {', '.join(sp['tuy_bien_ban_phoi_ca_nhan']['hoa_van_chon'])}
- **Chất liệu khảm/cẩn:** {', '.join(sp['tuy_bien_ban_phoi_ca_nhan']['chat_lieu_can_chon'])}
- **Kích cỡ:** {', '.join(sp['tuy_bien_ban_phoi_ca_nhan']['kich_co'])}
- **Kiểu viền:** {', '.join(sp['tuy_bien_ban_phoi_ca_nhan']['kieu_vien'])}
- **Khắc tên/chữ cá nhân:** {sp['tuy_bien_ban_phoi_ca_nhan']['khac_ten_chu']['gioi_han']}
- **Xuất ảnh bản phối:** {sp['tuy_bien_ban_phoi_ca_nhan']['xuat_ban_phoi']}
""")


with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.json', 'r', encoding='utf-8') as f:
    tn = json.load(f)

tn['khuyen_cao_chung'] = "Mô phỏng tương tác để giải thích nguyên lý · Không thay thế hướng dẫn của nghệ nhân và không phải công thức sản xuất thực tế."
tn['huong_dan_hanh_trinh'] = "Chọn nền, chất liệu, bố cục, lớp phủ và mức độ mài để tạo một bề mặt sơn mài minh họa (khoảng 3–5 phút)."
tn['huong_dan_tu_chinh'] = "Chọn dáng hộp, khay hoặc tranh cùng vật liệu cốt để bắt đầu. Chọn màu nền, hoa văn và chất liệu. Xem mẫu thay đổi trực tiếp rồi lưu lựa chọn ngay trên thiết bị."

with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.json', 'w', encoding='utf-8') as f:
    json.dump(tn, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Trải Nghiệm Tương Tác: {tn['tieu_de']}

> **Khuyến cáo:** *{tn['khuyen_cao_chung']}*  
> **Hành trình trải nghiệm:** *{tn['huong_dan_hanh_trinh']}*  
> **Tự chỉnh:** *{tn['huong_dan_tu_chinh']}*

---

## 1. Quy Trình 5 Bước Trải Nghiệm:
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

## 2. Trình Chỉnh Sửa Mặt Hộp Chuyên Sâu (Face Engraving Editor)
Trang bị công cụ vẽ và khắc tương tác trực quan:
- **Tùy biến từng mặt:** Vẽ tự do lên từng bề mặt (nắp hộp, các cạnh bên).
- **Chất liệu tương tác:** Vẽ bằng bụi vàng lá, dán mảng vỏ trứng rạn nứt, cẩn vỏ trai óng ánh.
- **Hiệu ứng quang học:** Bề mặt phản chiếu độ bóng sơn ta (gloss) và độ sâu quang học.
- **Lưu trữ & chia sẻ:** Lưu bản phối vào bộ nhớ trình duyệt và tải ảnh thành phẩm độ nét cao (`lop-sac-cua-ban.png`).
""")

print("Master enrichment completed successfully!")
