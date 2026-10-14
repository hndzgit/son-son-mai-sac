# Dữ Liệu Toàn Diện & Chuyên Sâu Tối Thượng: Website Sơn Son Mài Sắc (https://sonsonmaisat.site/)

Dự án truyền thông văn hóa số & nghiên cứu di sản nghệ thuật sơn mài truyền thống Việt Nam: **"Sơn Son Mài Sắc" (SSMS)**.  
Khẩu hiệu: *"Đi qua từng đường mài, khám phá giá trị Việt"* — *"Từ thấy 'đẹp' đến hiểu vì sao 'đẹp'"*.  
Triết lý thẩm mỹ: **Sơn (Khởi nguồn) · Son (Lòng son & Sắc đỏ) · Mài (Nhẫn nại & Thử thách) · Sắc (Bản sắc & Tinh hoa)**.

---

## 🚀 Trải Nghiệm Trực Quan 3D Offline (Standalone 3D Workbench)

Bạn có thể mở trực tiếp ứng dụng 3D tương tác mà không cần kết nối mạng hay cài đặt máy chủ:
- **Tập tin chạy:** [`ung_dung_3d_offline/index.html`](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/ung_dung_3d_offline/index.html)
- **Tính năng nổi bật:**
  1. **Xoay 3D (Orbit):** Dựng hình Three.js r128 mô hình nhị phân gốc `vercel-lacquer-box.glb` (449 KB, 10 meshes, 4 vật liệu PBR).
  2. **Mài Nước 3D (Real-time Water Sanding):** Bắt tọa độ UV Raycasting, tính toán độ mài mòn theo Depthmap thời gian thực bằng Custom GLSL Shader.
  3. **Âm thanh ma sát nước DSP:** Tổng hợp tiếng nước và đá cọ xát bằng Web Audio API (Paul Kellet Pink Noise Filter) biến thiên 700Hz - 2200Hz theo tốc độ chuột.
  4. **Thanh trượt so sánh chia đôi (Split Polish Slider):** So sánh bề mặt mài thô và đánh bóng gương.
  5. **Bộ xoay quang học 360°:** Xem 16 khung ảnh thực tế với quán tính kéo vuốt.
  6. **Tùy biến xưởng:** Đổi nền sơn (Đỏ son, Cánh gián, Nâu đất, Đen then), họa tiết (Hoa sen, Kỷ hà, Hoa lá), chất liệu cẩn (Vỏ trứng, Vàng quỳ, Xà cừ), và xuất ảnh PNG thành phẩm.

---

## 📁 Cấu Trúc Toàn Diện Bộ Dữ Liệu Cào & Giải Mã Ngược

```text
Sơn son mài sắc/
├── ung_dung_3d_offline/        # Ứng dụng Web 3D offline độc lập hoàn chỉnh
│   ├── index.html              # Trang giao diện chính xưởng tương tác 3D
│   ├── lib/                    # Thư viện Three.js, GLTFLoader, OrbitControls cục bộ
│   └── assets/                 # Mô hình vercel-lacquer-box.glb (449 KB), 16 ảnh 360°, textures & stencils
├── du_lieu_noi_dung/           # Toàn bộ nội dung trích xuất sạch dạng JSON & Markdown (15 bộ chuyên khảo)
│   ├── 00_tong_quan_du_an.json / .md
│   ├── 01_trang_chu.json / .md
│   ├── 02_kham_pha.json / .md
│   ├── 03_cau_chuyen_son_mai.json / .md (6 mốc lịch sử, 12 bài viết & tri thức truyền nghề)
│   ├── 04_tin_tuc_su_kien.json / .md (Sự kiện FPT, triển lãm Văn Miếu, Toong, Biennale 2026 & 12 bài báo live)
│   ├── 05_ve_du_an.json / .md (Sứ mệnh, tầm nhìn, triết lý 4 chữ "Sơn - Son - Mài - Sắc" & 5 thành viên)
│   ├── 06_san_pham.json / .md (4 mẫu cốt tác phẩm & studio tùy biến phối màu)
│   ├── 07_trai_nghiem_mo_phong_3d.json / .md (Tiến trình xưởng 5 chặng, preset, Face Engraving & 3 bộ stencil)
│   ├── 08_giai_ma_ky_thuat_chuyen_sau.json / .md (Báo cáo kỹ thuật: Dual-Buffer Canvas 2D, Bézier procedural)
│   ├── 09_he_thong_thiet_ke_design_system.json / .md (Design tokens, bảng màu CSS, typography & hạt nhám noise)
│   ├── 10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.json / .md (Chuyên luận nhân học, hóa học cây sơn ta Phú Thọ)
│   ├── 11_giai_ma_mo_hinh_3d_va_shader_webgl.json / .md (Giải mã mô hình glTF 449KB, Shader GLSL & DSP Web Audio)
│   ├── 12_kien_truc_ma_nguon_va_reverse_engineering.json / .md (Bản đồ component React, Hydration & LocalStorage)
│   ├── 13_dai_bach_khoa_toan_thu_son_mai.json / .md (Đại bách khoa: Hóa học Laccol C23H36O2, Laccase, 5 loại sơn & bản đồ làng nghề)
│   ├── 14_tong_tap_hieu_ung_3d_va_shader_vat_ly.json / .md (Tổng tập 68 Shader GLSL, Ma trận PBR, Bào mòn & Phản xạ màng nước)
│   └── api_tin_tuc_bao_chi.json (Dữ liệu live từ endpoint /api/news)
├── hinh_anh_assets/            # 94 tệp tài nguyên hình ảnh, mô hình 3D, texture, font chữ (~28.5 MB)
│   ├── models/                 # Mô hình 3D nhị phân vercel-lacquer-box.glb (449 KB, 10 meshes, 4 vật liệu PBR)
│   ├── story-assets/           # Tranh nghệ thuật, chuỗi 16 ảnh xoay 360°, 18 ảnh flow, đủ 3 bộ stencil hoa văn
│   │   ├── team-members/       # Chân dung 5 thành viên (Đan Lê, Duy Nghĩa, Huyền Trang, Gia Đạt, Anh Vũ)
│   │   └── backgrounds/        # Hoa văn dát vàng, dải nền nghệ thuật
│   ├── textures/               # Texture SVG rạn nứt vỏ trứng, dát vàng lá
│   ├── brand-logo-white.png & brand-logo-red.png (Logo thương hiệu động đa chủ đề)
│   ├── favicon.svg & favicon.ico
│   ├── apple-touch-icon.png & opengraph-image.png (198 KB)
│   └── Inter, NotoSerif, PlayfairDisplay (.ttf)
├── trang_html_goc/             # 9 trang HTML gốc render từ Next.js App Router
├── ma_nguon_css_js/            # Bộ stylesheet CSS (9 tệp) và JS bundle (26 tệp Next.js/Three.js + Manifests)
├── kiem_tra_2026-10-12/        # Thư mục đối soát kiểm định vi mô: 67 tương tác trình duyệt, 68 Shader, AST analysis
└── scripts/                    # Toàn bộ mã nguồn script tự động cào, bóc tách và đối soát vi mô
```

---

## 📑 Bảng Mục Lục Chi Tiết Các Chuyên Khảo (`du_lieu_noi_dung/`)

| STT | Tập tin tài liệu | Nội dung trích xuất & Phân tích chuyên sâu |
| :---: | :--- | :--- |
| **00** | [00_tong_quan_du_an.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/00_tong_quan_du_an.md) | Tổng quan dự án, sứ mệnh, ban sáng lập, thông tin liên hệ, kênh mạng xã hội |
| **01** | [01_trang_chu.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/01_trang_chu.md) | Trang chủ: Định nghĩa sơn mài, 5 chặng tạo tác, 6 lớp vật liệu, mô phỏng tách lớp |
| **02** | [02_kham_pha.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/02_kham_pha.md) | Nhựa cây sơn ta Phú Thọ, chi tiết 5 công đoạn kỹ thuật, chú thích cốt gỗ/tre/gốm, sơ đồ mặt cắt |
| **03** | [03_cau_chuyen_son_mai.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/03_cau_chuyen_son_mai.md) | 6 mốc lịch sử (Trước hội họa -> Đương đại), 12 bài viết chi tiết & tri thức nghệ nhân truyền nghề |
| **04** | [04_tin_tuc_su_kien.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/04_tin_tuc_su_kien.md) | Booth ĐH FPT Hòa Lạc, Triển lãm Văn Miếu, Biennale 2026, địa điểm Toong & 12 bài báo live từ `/api/news` |
| **05** | [05_ve_du_an.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/05_ve_du_an.md) | Câu chuyện dự án, triết lý 4 chữ "Sơn - Son - Mài - Sắc", vai trò chính xác 5 thành viên sáng lập |
| **06** | [06_san_pham.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/06_san_pham.md) | 4 mẫu tác phẩm cốt (Hộp hoa sen, Hộp cốt tối, Khay hoa sen, Tranh hoa sen) & studio tùy biến |
| **07** | [07_trai_nghiem_mo_phong_3d.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/07_trai_nghiem_mo_phong_3d.md) | Tiến trình 5 chặng Xưởng, 3 preset bản mẫu khởi tạo, Face Engraving Editor & 3 bộ stencil hoa văn |
| **08** | [08_giai_ma_ky_thuat_chuyen_sau.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/08_giai_ma_ky_thuat_chuyen_sau.md) | Động cơ Canvas 2D Dual-Buffer (900x620), toán Bézier hoa sen/sóng/mây/rồng, máy trạng thái 8 bước |
| **09** | [09_he_thong_thiet_ke_design_system.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/09_he_thong_thiet_ke_design_system.md) | Design tokens (sơn then, son, vàng quỳ, cánh gián), typography Playfair/Inter, bộ lọc SVG fractal noise |
| **10** | [10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.md) | Chuyên luận nhân học: Polyme hóa sinh hóa sơn ta, làng nghề Hạ Thái, mốc 1925 Mỹ thuật Đông Dương |
| **11** | [11_giai_ma_mo_hinh_3d_va_shader_webgl.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/11_giai_ma_mo_hinh_3d_va_shader_webgl.md) | Khảo sát nhị phân `vercel-lacquer-box.glb` (449KB, 10 meshes, 4 PBR mats), Shader GLSL phân tầng sơn mài |
| **12** | [12_kien_truc_ma_nguon_va_reverse_engineering.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/12_kien_truc_ma_nguon_va_reverse_engineering.md) | Cây Component Next.js 14 App Router, Build ID `_w6excJGTCRbJVHnNuGcc`, phụ thuộc 26 gói JS, cơ chế Hydration |
| **13** | [13_dai_bach_khoa_toan_thu_son_mai.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/13_dai_bach_khoa_toan_thu_son_mai.md) | Đại Bách Khoa: Hóa học Laccol $C_{23}H_{36}O_2$ vs Urushiol $C_{21}H_{32}O_2$, cơ chế xúc tác Laccase, sổ tay 5 loại sơn |
| **14** | [14_tong_tap_hieu_ung_3d_va_shader_vat_ly.md](file:///Users/hoainam/Documents/S%C6%A1n%20son%20m%C3%A0i%20s%E1%BA%AFc/du_lieu_noi_dung/14_tong_tap_hieu_ung_3d_va_shader_vat_ly.md) | **Tổng Tập 3D:** Khảo cứu 68 Shader GLSL, công thức ma sát nước DSP 700-2200Hz, ma trận PBR Blinn-Phong, 16 khung ảnh quang học |
