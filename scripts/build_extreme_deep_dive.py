import json
import os

# ==============================================================================
# 08. GIẢI MÃ KỸ THUẬT VÀ KIẾN TRÚC CÔNG NGHỆ
# ==============================================================================
tech_deep_dive = {
    "tieu_de": "Báo Cáo Kỹ Thuật Chuyên Sâu: Kiến Trúc Ứng Dụng, Đồ Họa WebGL & Động Cơ Mô Phỏng Sơn Mài",
    "stack_cong_nghe": {
        "framework": "Next.js 14+ (App Router)",
        "runtime": "React 18 / Node.js Vercel Edge Runtime",
        "hosting": "Vercel Deployment (dpl_6jQJ65uT65LPuzwTmJiqFs1xmLmA)",
        "ten_mien_chinh": "https://son-son-mai-sac-orpin.vercel.app/",
        "ten_mien_phu": "https://son-son-mai-sac-storytelling.vercel.app/",
        "thu_vien_do_hoa": ["Three.js (r128+)", "HTML5 Canvas 2D Dual-Buffer", "SVG Vector Filtering", "CSS Sub-pixel Animation"],
        "quan_ly_trang_thai": ["React Hooks (useState, useEffect, useRef, useMemo)", "HTML5 LocalStorage API", "HTML5 Custom Event Dispatcher"],
        "nguon_du_lieu": "Google News RSS Live Proxy (/api/news), Static JSON Data Bundles"
    },
    "dong_co_do_hoa_mo_phong_son_mai": {
        "kien_truc_dual_buffer": {
            "do_phan_giai": "900 x 620 pixels",
            "buffer_mau_rgb": "HTML5 Canvas (context 'a'): Chịu trách nhiệm hiển thị màu sắc, hoa văn, texture hạt vàng/vỏ trứng và các lớp sơn nền.",
            "buffer_do_sau_grayscale": "HTML5 Canvas (context 'r'): Chịu trách nhiệm lưu trữ độ sâu vật lý (Depthmap) dưới dạng giá trị xám [0..255] tương ứng với độ mài mòn của nước."
        },
        "thuat_toan_ve_vector_procedural": {
            "hoa_sen": "12 cánh hoa tạo hình bằng đường cong Bézier bậc 3 đối xứng [moveTo(0,14), bezierCurveTo(-53,-38,-47,-110,0,-164), bezierCurveTo(47,-110,53,-38,0,14)] xoay quanh tâm (PI/12 góc lệch) và nhụy hoa hình tròn arc(0,0,23).",
            "song_nuoc": "7 dải sóng thủy ba song song (e = -3..3, bước nhảy 48px) uốn lượn liên tục qua các điểm điều khiển Bézier [-280, a], [-120, a-54], [100, a+45], [280, a-10].",
            "may_cuon": "Cụm 4 tầng mây cuộn cổ truyền với các điểm cong liên hoàn [(-235, a+18) -> (-135, a+9) -> (-20, a+8) -> (90, a+12) -> (192, a+22)].",
            "rong_luon": "Hình thể rồng uốn khúc phức tạp kết hợp thân rồng Bézier, đầu rồng đa giác (Polygon head), râu rồng bậc 2 (Quadratic curve) và 6 vảy rồng hàm sin điều hòa [y = 62 * sin(0.9 * e)]."
        },
        "ky_thuat_composite_hoa_tron": {
            "source_in": "Cắt mặt nạ hoa văn (Stencil Masking) và phủ chất liệu lặp (createPattern texture) vào đúng biên dạng hoa văn.",
            "destination_in": "Áp dụng mặt nạ hình elip đa điểm [ellipse(690,190), ellipse(245,425)] để mô phỏng các vùng mài khuyết tự nhiên của bàn tay nghệ nhân."
        },
        "co_che_mai_nuoc_water_abrasion": {
            "depth_scale": "Thang đo độ mài phân tầng: 'Mài chưa tới' -> 'Độ sâu phù hợp' (coverage > 12%) -> 'Có nguy cơ mài quá sâu' (overSanded > 0%) -> 'Quá sâu'.",
            "tinh_toan_xuyen_lop": "Khi người dùng kéo dụng cụ mài, lớp phủ trong suốt bị mòn dần theo hệ số ma sát, so sánh độ sâu hiện tại với Depthmap của từng chất liệu để quyết định phần vỏ trứng hoặc vàng lá nào sẽ lộ ra."
        }
    },
    "trinh_khac_mat_hop_face_engraving_editor": {
        "mo_hinh_du_lieu": "Lưu trữ 6 mặt hộp [top, bottom, left, right, front, back] độc lập trong LocalStorage key 'ssms-applied-faces-v1'.",
        "cong_cu_ve": "Cọ vẽ đa chất liệu (Vàng quỳ, Vỏ trứng, Xà cừ) với tùy biến độ dày nét cọ (brush size), độ bóng bề mặt (surface gloss) và khắc văn bản cá nhân hóa (tối đa 18 ký tự)."
    },
    "bo_xoay_360_do_quang_hoc": {
        "so_khung_hinh": 16,
        "co_che_anh_xa": "Bắt sự kiện pointerdown/pointermove (dragX), chuẩn hóa góc quay [0..2*PI] và ánh xạ vào mảng 16 ảnh quang học thực tế [box-1.jpg .. box-23.jpg]."
    }
}

with open('du_lieu_noi_dung/08_giai_ma_ky_thuat_chuyen_sau.json', 'w', encoding='utf-8') as f:
    json.dump(tech_deep_dive, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/08_giai_ma_ky_thuat_chuyen_sau.md', 'w', encoding='utf-8') as f:
    f.write("""# Báo Cáo Kỹ Thuật Chuyên Sâu: Kiến Trúc Ứng Dụng, Đồ Họa WebGL & Động Cơ Mô Phỏng Sơn Mài

> **Tài liệu phân tích kỹ thuật giải mã ngược (Reverse-Engineering Technical Specification)**  
> **Dự án:** Sơn Son Mài Sắc (SSMS) · **Mã nguồn:** Next.js 14 / Three.js / Dual-Buffer Canvas 2D

---

## I. KIẾN TRÚC TỔNG THỂ HỆ THỐNG (SYSTEM ARCHITECTURE)

- **Framework cốt lõi:** Next.js 14+ App Router kết hợp kiến trúc React Server Components (RSC) và Client Hydration.
- **Môi trường vận hành:** Vercel Global Edge Network (Edge Runtime / Serverless Functions).
- **Phân tách mô-đun:**
  - *Server-side:* Đảm nhận pre-render toàn bộ 9 tuyến trang tĩnh, tối ưu hóa SEO meta, OpenGraph tags, và cung cấp endpoint `/api/news`.
  - *Client-side:* Đảm nhận 3 động cơ tương tác đồ họa chính:
    1. **Động cơ mô phỏng tạo tác sơn mài (Procedural Lacquer Engine - Canvas 2D Dual-Buffer)**
    2. **Bộ xoay 360 độ quang học (Interactive Photogrammetry Box Viewer)**
    3. **Trình khắc họa tiết mặt hộp đa chiều (Face Engraving Canvas Editor)**

---

## II. ĐỘNG CƠ ĐỒ HỌA MÔ PHỎNG SƠN MÀI (PROCEDURAL LACQUER ENGINE)

### 1. Kiến Trúc Dual-Buffer (2 Canvas Song Song 900x620)
Để tái hiện chân thực quá trình sơn mài (nơi các lớp vật liệu nằm ở các độ sâu khác nhau dưới lớp sơn then/sơn cánh gián và chỉ lộ ra khi mài nước), hệ thống sử dụng **2 Canvas 900x620 độc lập**:
1. **Color Buffer (Context 'a'):** Vẽ màu sắc, ánh kim, vân rạn vỏ trứng và độ phản quang quang học.
2. **Depthmap Buffer (Context 'r'):** Lưu trữ bản đồ độ sâu vật lý (Grayscale 0–255). Mỗi chất liệu khi đặt vào bố cục được gán một mức độ sâu:
   Grayscale Value = round((depth / 100) * 255)

### 2. Thuật Toán Tạo Hình Vector Độc Quyền (Bézier Procedural Geometry)
Động cơ hỗ trợ 5 chế độ họa tiết tạo hình hoàn toàn bằng giải thuật toán học:
- **Hoa Sen (12 Cánh Bézier):**
  - Sử dụng đường cong bậc 3 đối xứng qua trục:
    ```javascript
    a.moveTo(0, 14);
    a.bezierCurveTo(-53, -38, -47, -110, 0, -164);
    a.bezierCurveTo(47, -110, 53, -38, 0, 14);
    ```
  - Xoay đều 12 góc xung quanh nhụy hoa tròn `arc(0, 0, 23, 0, 2 * Math.PI)`.
- **Sóng Nước (7 Dải Thủy Ba):**
  - Chạy vòng lặp 7 dải (e = -3..3, khoảng cách 48px) với đường cong uốn lượn liên hoàn:
    ```javascript
    t.moveTo(-280, a);
    t.bezierCurveTo(-120, a - 54, 100, a + 45, 280, a - 10);
    ```
- **Mây Cuộn (4 Tầng Cổ Điển):**
  - Tổ hợp 4 điểm uốn nối tiếp tạo cụm mây cuộn truyền thống Việt Nam.
- **Rồng Lượn (Sinusoidal Dragon):**
  - Thân rồng uốn khúc kết hợp đường bao đầu rồng, râu rồng bậc 2 và 6 vảy rồng tính toán theo hàm điều hòa:
    y = 62 * sin(0.9 * e)

### 3. Kỹ Thuật Composite Hòa Trộn Lớp
- Sử dụng `globalCompositeOperation = "source-in"` để áp chất liệu hạt vàng quỳ, mảnh vỏ trứng và xà cừ vào đúng ranh giới của hoa văn vector.
- Sử dụng `globalCompositeOperation = "destination-in"` cùng các mặt nạ hình elip đa điểm `ellipse(690, 190, ...)` để mô phỏng các vệt mài nước không đồng đều của bàn tay con người.

---

## III. MÁY TRẠNG THÁI 8 BƯỚC TẠO TÁC (STATE MACHINE LIFECYCLE)

```mermaid
stateDiagram-v2
    [*] --> Step0_HinhThe: Chọn Cốt (Hộp / Khay / Tranh)
    Step0_HinhThe --> Step1_LamVoc: Hom bó & Bồi vải
    Step1_LamVoc --> Step2_SonNen: Phủ sơn then / Đỏ son / Cánh gián
    Step2_SonNen --> Step3_HoaVan: Chọn Hoa Sen / Sóng / Mây / Rồng / Tự do
    Step3_HoaVan --> Step4_ChatLieu: Cẩn Vàng / Bạc / Vỏ trứng / Xà cừ
    Step4_ChatLieu --> Step5_PhuSon: Phủ sơn trong (Clearcoat)
    Step5_PhuSon --> Step6_MaiNuoc: Mài lộ lớp (Depth Scale kiểm tra overSanded)
    Step6_MaiNuoc --> Step7_DanhBong: So sánh Mài vs Đánh bóng (Polish Slider)
    Step7_DanhBong --> Step8_HoanTat: Xuất ảnh thành phẩm (PNG 900x620)
    Step8_HoanTat --> [*]
```

### Tiêu Chuẩn Kiểm Soát Mài Nước (Step 6)
- **Mài chưa tới:** `coverage < 12%` → Các lớp bên dưới vẫn bị sơn che phủ.
- **Độ sâu phù hợp:** `coverage >= 12% && overSanded == 0%` → Lộ đúng mức màu và ánh kim.
- **Có nguy cơ mài quá sâu:** `overSanded > 0%` → Mài phạm vào các chi tiết cẩn bên dưới.

---

## IV. BỘ XOAY QUANG HỌC 360 ĐỘ (360° OPTICAL ROTATOR)

Thay vì dựng mô hình 3D thô sơ, nhóm tác giả sử dụng **16 góc chụp chất lượng cao của tác phẩm thật** (`box-1.jpg` đến `box-23.jpg`):
- Thuật toán bắt cử chỉ kéo vuốt:
  frameIndex = Math.floor((pointerAngle / (2 * Math.PI)) * 16) % 16
- Mang lại độ chân thực quang học 100% với ánh phản chiếu thực của vàng quỳ và men sơn ta.
""")

# ==============================================================================
# 09. HỆ THỐNG THIẾT KẾ (DESIGN SYSTEM)
# ==============================================================================
design_system = {
    "tieu_de": "Hệ Thống Thiết Kế (Design System) & Design Tokens Sơn Son Mài Sắc",
    "bang_mau_tokens": {
        "son_then_den": {"token": "--color-black-lacquer", "hex": "#0f0000", "y_nghia": "Sắc đen tuyền sâu thẳm của sơn then ủ lâu năm"},
        "do_son": {"token": "--color-vermilion", "hex": "#912723 / var(--red)", "y_nghia": "Sắc đỏ son cổ truyền trong mỹ thuật đình chùa"},
        "vang_quy": {"token": "--color-gold", "hex": "#deb85a / #ffbb10", "y_nghia": "Ánh kim ấm áp biến đổi theo góc nhìn của vàng quỳ thếp"},
        "vo_trung_ran": {"token": "--color-eggshell-white", "hex": "#ebeae9 / #f4e8c6", "y_nghia": "Sắc trắng ngà rạn nứt tự nhiên của vỏ trứng vịt/gà"},
        "xa_cu_ngu_sac": {"token": "--color-mother-of-pearl", "hex": "#ddbfab", "y_nghia": "Ánh xà cừ óng ánh chuyển sắc theo hướng sáng"},
        "canh_gian": {"token": "--color-lacquer-brown", "hex": "#6c3b20", "y_nghia": "Màu cánh gián nấu dầu trẩu hổ phách trong suốt"},
        "nen_the_card": {"token": "--color-surface-card", "hex": "#1a0a0a", "y_nghia": "Nền khối giao diện tối làm nổi bật các tác phẩm nghệ thuật"}
    },
    "typography": {
        "font_tieu_de": "Playfair Display / Noto Serif (Serif truyền thống, sang trọng, mang phong vị di sản mỹ thuật)",
        "font_noi_dung": "Inter (Sans-serif hiện đại, tối ưu khả năng đọc trên màn hình số độ phân giải cao)"
    },
    "hieu_ung_hat_nham_texture_noise": "Sử dụng bộ lọc SVG fractal noise (feTurbulence baseFrequency='.84' numOctaves='3') để tạo bề mặt hạt li ti mô phỏng cấu trúc chất liệu sơn ta truyền thống."
}

with open('du_lieu_noi_dung/09_he_thong_thiet_ke_design_system.json', 'w', encoding='utf-8') as f:
    json.dump(design_system, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/09_he_thong_thiet_ke_design_system.md', 'w', encoding='utf-8') as f:
    f.write("""# Hệ Thống Thiết Kế (Design System) & Design Tokens

> **Triết lý thẩm mỹ:** Sang trọng, tối giản, mang hơi thở di sản đương đại (Heritage Contemporary).

---

## 1. Bảng Màu Sắc Chuẩn (Color Tokens)

| Tên Chất Liệu | Token CSS | Giá trị HEX | Ý Nghĩa Văn Hóa & Thẩm Mỹ |
| :--- | :--- | :--- | :--- |
| **Sơn then** | `--color-black-lacquer` | `#0f0000` | Sắc đen tuyền huyền bí, sâu thẳm, tạo phông nền làm nổi bật mọi chất liệu đặt trên |
| **Đỏ son** | `--color-vermilion` | `#912723` | Sắc đỏ son rực rỡ, trang nghiêm, biểu trưng cho quyền quý và tâm linh Việt |
| **Vàng quỳ** | `--color-gold` | `#deb85a` / `#ffbb10` | Ánh kim ấm, biến thiên theo ánh sáng, biểu trưng cho sự vĩnh cửu |
| **Vỏ trứng** | `--color-eggshell-white` | `#ebeae9` / `#f4e8c6` | Màu trắng ngà với các đường rạn nứt tự nhiên độc bản |
| **Xà cừ** | `--color-mother-of-pearl` | `#ddbfab` | Ánh ngũ sắc xà cừ óng ả đổi màu theo góc nhìn |
| **Cánh gián** | `--color-lacquer-brown` | `#6c3b20` | Sắc nâu hổ phách trong veo của lớp sơn phủ bảo vệ |
| **Nền thẻ card** | `--color-surface-card` | `#1a0a0a` | Nền tối cao cấp nâng tầm thị giác |

---

## 2. Hệ Thống Kiểu Chữ (Typography Hierarchy)
- **Tiêu đề & Điểm nhấn:** `Noto Serif` & `Playfair Display` — Kiểu chữ có chân thanh thoát, tôn vinh nét hoài cổ và chiều sâu hàn lâm của nghệ thuật sơn mài.
- **Thân bài & Điều hướng:** `Inter` — Kiểu chữ không chân sắc nét, hiện đại, đảm bảo tính khả dụng và trải nghiệm đọc mượt mà trên mọi thiết bị.

---

## 3. Hiệu Ứng Hạt Nhám Vật Lý (Procedural Noise Texture)
Giao diện không dùng màu đơn sắc phẳng (flat color) mà phủ lớp noise vi mô tạo bởi thuật toán SVG Fractal Noise:
```xml
<filter id='lacquer-grain'>
  <feTurbulence type='fractalNoise' baseFrequency='.84' numOctaves='3' stitchTiles='stitch'/>
</filter>
```
Hiệu ứng này tái hiện chính xác cảm giác sần nhẹ và độ sâu quang học của một tấm vóc sơn mài thật.
""")

# ==============================================================================
# 10. NGHIÊN CỨU VĂN HÓA VÀ KHẾ ƯỚC NGHỆ THUẬT
# ==============================================================================
cultural_research = {
    "tieu_de": "Chuyên Luận Nghiên Cứu Văn Hóa: Lịch Sử, Kỹ Nghệ Và Triết Lý Thẩm Mỹ Sơn Mài Việt Nam",
    "cay_son_ta": {
        "ten_khoa_hoc": "Toxicodendron succedaneum (trước đây là Rhus succedanea)",
        "vung_trong": "Vùng gò đồi trung du tỉnh Phú Thọ (Tam Nông, Cẩm Khê, Thanh Ba)",
        "co_che_dong_ket_hoa_hoc": "Nhựa sơn ta không khô bằng cách bay hơi dung môi như sơn công nghiệp. Nó đóng rắn nhờ quá trình polyme hóa sinh hóa do enzyme laccase kích hoạt trong điều kiện độ ẩm cao (75–85% RH) và nhiệt độ 25–30°C. Đây là lý do người thợ phải 'ủ sơn' trong buồng kín ẩm."
    },
    "lang_nghe_ha_thai": {
        "vi_tri": "Xã Duyên Thái, huyện Thường Tín, TP. Hà Nội",
        "lich_su": "Làng nghề thủ công hơn 200 năm tuổi, ban đầu chuyên sơn son thếp vàng cho tượng phật, hoành phi câu đối đình chùa, sau trở thành cái nôi kỹ thuật cung cấp nghệ nhân và vóc cho các họa sĩ trường Mỹ thuật Đông Dương."
    },
    "buoc_ngoat_my_thuat_dong_duong_1925": {
        "su_kien": "Năm 1925, Trường Mỹ thuật Đông Dương được thành lập tại Hà Nội dưới sự dẫn dắt của Victor Tardieu và Joseph Inguimberty.",
        "dot_pha": "Họa sĩ Inguimberty khuyến khích sinh viên Việt Nam đưa chất liệu sơn ta vào hội họa giá vẽ. Các họa sĩ như Trần Văn Cẩn, Phạm Hậu, Nguyễn Khang và đặc biệt là Nguyễn Gia Trí đã phát minh ra kỹ thuật 'mài nước', biến chất liệu trang trí thủ công thành ngôn ngữ hội họa sơn mài độc nhất vô nhị trên thế giới."
    },
    "cac_tac_pham_kinh_dien": [
        {
            "tac_pham": "Phong cảnh chùa cổ ở Bắc Bộ (1934)",
            "tac_gia": "Nguyễn Gia Trí",
            "quy_mo": "Bộ 6 tấm vóc liên hoàn (104cm x 34cm mỗi tấm)",
            "gia_tri": "Tác phẩm đặt nền móng khẳng định sơn mài có thể diễn tả chiều sâu không gian, ánh sáng và tâm linh không thua kém sơn dầu phương Tây."
        },
        {
            "tac_pham": "Vườn xuân Trung Nam Bắc",
            "tac_gia": "Nguyễn Gia Trí",
            "gia_tri": "Bảo vật quốc gia Việt Nam, kết tinh hơn 20 năm lao động nghệ thuật với hàng trăm lớp màu, vàng quỳ, vỏ trứng được mài đan xen tinh diệu."
        }
    ],
    "triet_ly_mai": "Phủ lên để rồi mài đi. Trong hội họa phương Tây, họa sĩ vẽ thêm nét vào tranh. Trong sơn mài Việt Nam, người nghệ sĩ phủ kín rồi dùng nước mài đi từng chút một. Quá khứ của các lớp sơn bên dưới được hé lộ dần. Đó là vẻ đẹp của sự nhẫn nại, của thời gian và sự kỳ diệu không thể đoán trước hoàn toàn."
}

with open('du_lieu_noi_dung/10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.json', 'w', encoding='utf-8') as f:
    json.dump(cultural_research, f, ensure_ascii=False, indent=2)

with open('du_lieu_noi_dung/10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.md', 'w', encoding='utf-8') as f:
    f.write(f"""# Chuyên Luận Nghiên Cứu Văn Hóa: Lịch Sử, Kỹ Nghệ Và Triết Lý Thẩm Mỹ Sơn Mài Việt Nam

> **Tài liệu nghiên cứu học thuật & nhân học nghệ thuật trích xuất từ dự án Sơn Son Mài Sắc**

---

## I. CHẤT HỌC & HÓA HỌC TỰ NHIÊN CỦA SƠN TA

### 1. Loài Cây & Nguồn Gốc Địa Lý
- **Tên khoa học:** *{cultural_research['cay_son_ta']['ten_khoa_hoc']}*
- **Vùng sinh trưởng:** {cultural_research['cay_son_ta']['vung_trong']}.
- Khác với sơn công nghiệp khô bằng cách bay hơi dung môi, **sơn ta đóng rắn thông qua phản ứng trùng hợp sinh hóa (Biochemical Polymerization)**:
  - Enzyme *laccase* có trong nhựa cây xúc tác quá trình oxy hóa các hợp chất urushiol/laccol.
  - Phản ứng này bắt buộc phải diễn ra trong môi trường có **độ ẩm tương đối cao (75% - 85% RH)** và nhiệt độ ổn định (25°C - 30°C).
  - Do đó, người thợ sơn mài phải có **buồng ủ kín gió và ẩm**, biến việc làm sơn thành một cuộc đối thoại mật thiết với khí hậu nhiệt đới gió mùa của Việt Nam.

---

## II. LÀNG NGHỀ TRUYỀN THỐNG HẠ THÁI & TRI THỨC BẢN ĐỊA

- **Địa danh:** {cultural_research['lang_nghe_ha_thai']['vi_tri']}
- **Vai trò lịch sử:** {cultural_research['lang_nghe_ha_thai']['lich_su']}
- **Kỹ nghệ hom vóc gia truyền:**
  - Cốt gỗ (thường là gỗ dổi, vàng tâm nhẹ và không cong vênh) được quét sơn lót chống thấm.
  - Bó hom bằng hỗn hợp: phù sa sông Hồng mịn, bột đá nhào với sơn sống, miết chặt vào cốt.
  - Bồi vải màn (*cotton scrim*): dán lớp vải xô gia cường chống nứt xé khi thời tiết thay đổi.
  - Sau mỗi lượt hom bồi là quá trình mài phẳng với nước và đá mài. Một tấm vóc đạt chuẩn có thể tồn tại hàng trăm năm mà không biến dạng.

---

## III. BƯỚC NGOẶT LỊCH SỬ NĂM 1925 TẠI TRƯỜNG MỸ THUẬT ĐÔNG DƯƠNG

- {cultural_research['buoc_ngoat_my_thuat_dong_duong_1925']['su_kien']}
- {cultural_research['buoc_ngoat_my_thuat_dong_duong_1925']['dot_pha']}

### Các Kiệt Tác Tiêu Biểu:
""")
    for tp in cultural_research['cac_tac_pham_kinh_dien']:
        f.write(f"""### {tp['tac_pham']} — Họa sĩ {tp.get('tac_gia', 'Nguyễn Gia Trí')}
- **Đặc điểm & Quy mô:** {tp.get('quy_mo', 'Bảo vật quốc gia')}
- **Giá trị nghệ thuật:** {tp['gia_tri']}

""")

    f.write(f"""---

## IV. TRIẾT LÝ THẨM MỸ: "PHỦ LÊN ĐỂ RỒI MÀI ĐI"
> *"{cultural_research['triet_ly_mai']}"*

Sơn mài Việt Nam độc đáo ở chỗ nó là một nghệ thuật trừu xuất và khám phá:
1. **Thời gian là một chất liệu:** Mỗi lớp sơn cần nhiều ngày để ủ khô. Một tác phẩm lớn cần hàng tháng đến hàng năm trời.
2. **Sự bất ngờ có kiểm soát:** Khi mài nước, nghệ nhân vừa chủ động kiểm soát lực bàn tay, vừa đón nhận những bất ngờ mà các tầng chất liệu bên dưới hé lộ.
3. **Chiều sâu quang học (Optical Depth):** Nhờ lớp sơn cánh gián hổ phách trong suốt bao bọc, ánh sáng đi xuyên qua các lớp sơn, phản chiếu từ vàng quỳ, bạc quỳ và xà cừ rồi khúc xạ trở lại mắt người nhìn, tạo nên cảm giác huyền ảo, sâu thẳm không chất liệu nào khác có được.
""")

print("Successfully generated ultra-deep dive technical, design, and cultural monographs!")
