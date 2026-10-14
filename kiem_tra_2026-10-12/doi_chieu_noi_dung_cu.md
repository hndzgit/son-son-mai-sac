# Đối chiếu 29 tài liệu nội dung cũ với nguồn website đã lưu

Kiểm tra lúc: 2026-10-12T14:13:17.935781+07:00. Các file gốc được giữ nguyên.

**Kết luận: 29 file cũ không phải bản lưu nguyên văn đầy đủ của website.** Có nội dung chép đúng nguồn, nội dung tóm tắt/đặt tên lại và nội dung nghiên cứu hoặc phân tích được bổ sung. Đặc biệt 08–13 cần phân biệt dữ kiện có chứng cứ trong CSS/JS/GLB với lời diễn giải của tài liệu.

- Phạm vi: 15 JSON và 14 Markdown.
- Tổng 1016 JSON leaf; 960 là chuỗi. Khớp nguyên văn: 628; chỉ khớp sau chuẩn hóa: 3; chưa có toàn chuỗi trong nguồn: 329.
- 578/981 chuỗi ứng viên lấy từ giao diện/JS không được giữ nguyên văn trong bất kỳ file cũ nào. Danh sách đầy đủ kèm vị trí nguồn nằm trong JSON báo cáo.

Các số trên đo khả năng truy nguồn của tài liệu cũ; **không phải phần trăm website đã cào**. Không khớp chữ không đồng nghĩa sai: có thể do tóm tắt, tiêu đề biên tập, tính toán, thay đổi dữ liệu trực tiếp hoặc phát biểu chưa có nguồn. Chuỗi ngắn trùng nhau cũng không xác nhận một phát biểu đúng ngữ cảnh.

## Kiểm tra từng file JSON

| File | Leaf | Chuỗi | Nguyên văn | Chuẩn hóa | Chưa có toàn chuỗi | % chuỗi khớp |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 00_tong_quan_du_an.json | 44 | 42 | 35 | 0 | 7 | 83.33% |
| 01_trang_chu.json | 90 | 90 | 88 | 0 | 2 | 97.78% |
| 02_kham_pha.json | 67 | 67 | 37 | 1 | 29 | 56.72% |
| 03_cau_chuyen_son_mai.json | 125 | 125 | 104 | 0 | 21 | 83.2% |
| 04_tin_tuc_su_kien.json | 130 | 130 | 101 | 1 | 28 | 78.46% |
| 05_ve_du_an.json | 40 | 40 | 33 | 0 | 7 | 82.5% |
| 06_san_pham.json | 86 | 86 | 65 | 0 | 21 | 75.58% |
| 07_trai_nghiem_mo_phong_3d.json | 77 | 72 | 41 | 0 | 31 | 56.94% |
| 08_giai_ma_ky_thuat_chuyen_sau.json | 32 | 31 | 1 | 0 | 30 | 3.23% |
| 09_he_thong_thiet_ke_design_system.json | 25 | 25 | 11 | 0 | 14 | 44.0% |
| 10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.json | 16 | 16 | 3 | 1 | 12 | 25.0% |
| 11_giai_ma_mo_hinh_3d_va_shader_webgl.json | 99 | 53 | 17 | 0 | 36 | 32.08% |
| 12_kien_truc_ma_nguon_va_reverse_engineering.json | 59 | 57 | 6 | 0 | 51 | 10.53% |
| 13_dai_bach_khoa_toan_thu_son_mai.json | 30 | 30 | 2 | 0 | 28 | 6.67% |
| api_tin_tuc_bao_chi.json | 96 | 96 | 84 | 0 | 12 | 87.5% |

Các số/boolean không được xác nhận bằng cách tìm một con số bất kỳ trong bundle. Riêng chương 11 có đối chiếu GLB theo đúng node/material; chi tiết và các phép rút gọn thập phân nằm tại `contextual_evidence` của từng leaf.

## Nguồn gốc và phát hiện cần lưu ý

### F01 — 00–07 JSON/MD

Các chương cũ được dựng bằng script tạo tài liệu, thường là dict và văn bản gán cứng. 03 lấy nguyên văn mảng bài viết qua JSON.parse rồi ghép các mốc thời gian viết riêng. Vì vậy có cả bản chép nguồn, tóm tắt/đặt tên lại và nội dung bổ sung. Không được gọi toàn bộ 29 file là nội dung nguyên văn đã cào.

### F02 — 02_kham_pha.json, 02_kham_pha.md

Các đoạn chi tiết kỹ thuật có thêm vật liệu/công thức như độ ẩm 70–85%, phù sa/bột đá, vải màn, mài bằng lá chuối khô, trong khi nguồn giao diện nhấn mạnh năm chặng chỉ để giải thích và không phải công thức chế tác. Cần giữ bản nguyên văn riêng, không dùng bản diễn giải cũ làm bằng chứng web.

| Từ khóa kiểm tra | Kết quả trong snapshot |
| --- | --- |
| `Năm chặng để dễ hình dung, không phải công thức cứng` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js` |
| `70-85%` | Chưa tìm thấy chuỗi này |
| `lá chuối khô` | Chưa tìm thấy chuỗi này |

### F03 — 03_cau_chuyen_son_mai.json, 03_cau_chuyen_son_mai.md

scripts/gen_03.js:3–15 đọc/giải mã mảng bài viết trong JS; dòng 16–60 tự gán các mốc/tóm tắt. Những mốc này không mặc nhiên là câu chữ của tác giả website. Báo cáo từng leaf cho biết câu nào trùng nguồn.

### F04 — 08_giai_ma_ky_thuat_chuyen_sau.json, 08_giai_ma_ky_thuat_chuyen_sau.md

Script build_extreme_deep_dive.py tạo 08 từ dữ liệu gán cứng, sau đó generate_ultimate_deep_dive.py bổ sung mô tả WebGL. Có dấu vết triển khai thực về hai Canvas 900×620, shader, localStorage, GLB. Bundle còn ghi version Next.js 14.2.35 và React 18.3.0-canary-178c267a4e-20241218, chi tiết hơn nhãn 14+/18 của tài liệu. Các nhãn thuật toán, ý nghĩa vật lý, runtime Edge và cách kể kiến trúc là diễn giải; browser bundle không tự chứng minh môi trường chạy server.

| Từ khóa kiểm tra | Kết quả trong snapshot |
| --- | --- |
| `ssms-applied-faces-v1` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/840-f19fdd306966b2e5.js` |
| `localStorage` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/840-f19fdd306966b2e5.js` |
| `width=900` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js` |
| `height=620` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js` |
| `bezierCurveTo(-53,-38,-47,-110,0,-164)` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/trai-nghiem/hanh-trinh/page-2c74554e92ef9036.js` |
| `vercel-lacquer-box.glb` | Có: `kiem_tra_2026-10-12/ban_chup_goc/models/vercel-lacquer-box.glb` |
| `AudioContext` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/648.013156edff3e7a3c.js` |
| `14.2.35` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/945-9b486e563304ccbb.js` |
| `18.3.0-canary-178c267a4e-20241218` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/2200cc46-2612da093c775fbc.js` |

### F05 — 09_he_thong_thiet_ke_design_system.json, 09_he_thong_thiet_ke_design_system.md

Tên CSS token có thật nhưng bảng màu cũ chưa mô tả cascade/override. Trong 58e70d5489b56972.css, --color-vermilion ban đầu #8c0e0e rồi đổi sang var(--red); --red tiếp tục có các giá trị #8c0e0e, #8b2a2a, #8b2922. --color-eggshell-white cũng đổi từ #ebeae9 sang var(--cream). Noto Serif và Inter có khai báo font; chuỗi tên Playfair Display không xuất hiện trong CSS/JS/HTML được xét. Một file font tồn tại riêng không chứng minh nó đang được dùng. Ý nghĩa văn hóa, nhận định thẩm mỹ và lời khẳng định “tái hiện chính xác” là diễn giải tác giả tài liệu.

| Từ khóa kiểm tra | Kết quả trong snapshot |
| --- | --- |
| `--color-black-lacquer` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/css/58e70d5489b56972.css` |
| `--color-vermilion` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/css/58e70d5489b56972.css` |
| `--color-gold` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/css/58e70d5489b56972.css` |
| `--color-eggshell-white` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/css/58e70d5489b56972.css` |
| `--color-mother-of-pearl` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/css/58e70d5489b56972.css` |
| `--color-lacquer-brown` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/css/58e70d5489b56972.css` |
| `--color-surface-card` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/css/58e70d5489b56972.css` |
| `Playfair Display` | Chưa tìm thấy chuỗi này |
| `Noto Serif` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/840-f19fdd306966b2e5.js` |
| `Inter` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/2200cc46-2612da093c775fbc.js` |
| `feTurbulence` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/css/3d939b8161363d36.css` |

### F06 — 10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.json, 10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.md

Tên khoa học cây sơn, enzyme, độ ẩm/nhiệt độ, niên đại và quy mô tranh xuất hiện trong script tạo chuyên luận. Báo cáo tìm chứng cứ trong toàn bộ nguồn công khai đã lưu; không xác minh độc lập tính đúng sai học thuật. Nhãn “trích xuất từ dự án” không đủ chứng minh từng phát biểu.

| Từ khóa kiểm tra | Kết quả trong snapshot |
| --- | --- |
| `Toxicodendron` | Chưa tìm thấy chuỗi này |
| `Rhus succedanea` | Chưa tìm thấy chuỗi này |
| `laccase` | Chưa tìm thấy chuỗi này |
| `75–85%` | Chưa tìm thấy chuỗi này |
| `25–30` | Chưa tìm thấy chuỗi này |
| `104cm` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/cau-chuyen-son-mai/page-18999a17f9a00aec.js` |
| `Joseph Inguimberty` | Chưa tìm thấy chuỗi này |

### F07 — 11_giai_ma_mo_hinh_3d_va_shader_webgl.json, 11_giai_ma_mo_hinh_3d_va_shader_webgl.md

GLB tải về thực sự dài 449344 byte, glTF 2.0, 12 nodes, 10 meshes, 4 materials. Các tên node, children, mesh index, metallicFactor và roughnessFactor có thể đối chiếu ngữ cảnh trực tiếp. baseColorFactor trong tài liệu đã rút gọn số thập phân, không bảo toàn nguyên giá trị. Bộ lọc âm thanh có hệ số .99886, .0555179, .0750759, .153852 trong mã minify; bản cũ rút gọn hệ số .0555/.075/.153. Không tìm thấy dạng có số 0 trước dấu chấm không có nghĩa thuật toán vắng mặt. Ý nghĩa văn hóa/kích thước “chuẩn mực”, tên “Sobel”, “Paul Kellet” cần tách khỏi bằng chứng mã.

| Từ khóa kiểm tra | Kết quả trong snapshot |
| --- | --- |
| `rawDepth = texture2D(uMaskMap, vUv).r` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/648.013156edff3e7a3c.js` |
| `revealThreshold` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/648.013156edff3e7a3c.js` |
| `.99886*n+.0555179*t` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/648.013156edff3e7a3c.js` |
| `.99332*i+.0750759*t` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/648.013156edff3e7a3c.js` |
| `.969*l+.153852*t` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/648.013156edff3e7a3c.js` |
| `Math.min(2200,Math.max(700,1e3+1200*e))` | Có: `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/648.013156edff3e7a3c.js` |
| `Paul Kellet` | Chưa tìm thấy chuỗi này |
| `Sobel` | Chưa tìm thấy chuỗi này |

### F08 — 12_kien_truc_ma_nguon_va_reverse_engineering.json, 12_kien_truc_ma_nguon_va_reverse_engineering.md

Tên component và đường dẫn .tsx trong phần “reconstructed” là bản tái dựng đặt tên; không phải bằng chứng đã tải được mã nguồn TSX. Tên hash webpack và số lượng bundle chỉ đúng với snapshot cụ thể. Không nên coi mô tả 28 JS/9 CSS là định mức để chứng minh website đã cào đủ.

| Từ khóa kiểm tra | Kết quả trong snapshot |
| --- | --- |
| `HeaderNavigation` | Chưa tìm thấy chuỗi này |
| `HeroCover` | Chưa tìm thấy chuỗi này |
| `EightStepJourneyStateMachine` | Chưa tìm thấy chuỗi này |
| `app/layout.tsx` | Chưa tìm thấy chuỗi này |
| `_w6excJGTCRbJVHnNuGcc` | Có: `kiem_tra_2026-10-12/trich_xuat_html/cau-chuyen-son-mai.json` |
| `dpl_6jQJ65uT65LPuzwTmJiqFs1xmLmA` | Chưa tìm thấy chuỗi này |
| `webpack-f57e898f0a30f96c.js` | Chưa tìm thấy chuỗi này |

### F09 — 13_dai_bach_khoa_toan_thu_son_mai.json, 13_dai_bach_khoa_toan_thu_son_mai.md

Các công thức phân tử, tỉ lệ 65–70%, 20–25%, 5–7%, 2–3%, thời gian 40–60 giờ, 3–5 ngày và diễn giải phản ứng hóa học được gán cứng trong generate_ultimate_deep_dive.py. Không tìm thấy cả chuỗi hoặc thuật ngữ đặc thù tương ứng là dấu hiệu chưa có chứng cứ web trong snapshot, không phải kết luận khoa học sai.

| Từ khóa kiểm tra | Kết quả trong snapshot |
| --- | --- |
| `C23H36O2` | Chưa tìm thấy chuỗi này |
| `C21H32O2` | Chưa tìm thấy chuỗi này |
| `laccol` | Chưa tìm thấy chuỗi này |
| `ortho-quinone` | Chưa tìm thấy chuỗi này |
| `40-60` | Chưa tìm thấy chuỗi này |
| `3-5 ngày` | Chưa tìm thấy chuỗi này |
| `Polyphenol oxidase` | Chưa tìm thấy chuỗi này |

### F10 — api_tin_tuc_bao_chi.json, 04_tin_tuc_su_kien.json, 04_tin_tuc_su_kien.md

API tin tức thay đổi id theo lần/snapshot dù URL bài, tiêu đề hoặc ngày có thể không đổi. Trong hai snapshot đang xét, cả 12 URL bài và các trường ngoài id trùng nhau. Phần api_snapshot_comparison đối chiếu theo URL, tránh gắn cờ id mới thành bài báo thiếu hoặc dữ liệu bịa.

## Kiểm tra từng file Markdown

Mỗi dòng có chữ được đánh giá trong JSON. “Có nội dung JSON” chỉ chỉ ra quan hệ giữa hai tài liệu, không tự xác nhận nguồn web. Dòng tiêu đề/bố cục được phân loại riêng. Các dòng mã/sơ đồ cần đọc đúng ngữ cảnh; không gắn nhãn sai chỉ vì khác tên biến hoặc định dạng.

| File | Dòng nội dung | Khớp nguồn trực tiếp | Có nội dung JSON cùng chương | Tiêu đề | Cần đối chiếu thêm |
| --- | ---: | ---: | ---: | ---: | ---: |
| 00_tong_quan_du_an.md | 30 | 6 | 15 | 6 | 3 |
| 01_trang_chu.md | 47 | 26 | 11 | 10 | 0 |
| 02_kham_pha.md | 43 | 16 | 21 | 6 | 0 |
| 03_cau_chuyen_son_mai.md | 105 | 68 | 13 | 22 | 2 |
| 04_tin_tuc_su_kien.md | 89 | 36 | 35 | 18 | 0 |
| 05_ve_du_an.md | 38 | 20 | 4 | 13 | 1 |
| 06_san_pham.md | 63 | 32 | 23 | 6 | 2 |
| 07_trai_nghiem_mo_phong_3d.md | 60 | 14 | 22 | 13 | 11 |
| 08_giai_ma_ky_thuat_chuyen_sau.md | 59 | 0 | 0 | 9 | 50 |
| 09_he_thong_thiet_ke_design_system.md | 20 | 1 | 7 | 4 | 8 |
| 10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.md | 34 | 0 | 10 | 9 | 15 |
| 11_giai_ma_mo_hinh_3d_va_shader_webgl.md | 104 | 25 | 12 | 15 | 52 |
| 12_kien_truc_ma_nguon_va_reverse_engineering.md | 68 | 0 | 5 | 6 | 57 |
| 13_dai_bach_khoa_toan_thu_son_mai.md | 89 | 0 | 3 | 13 | 73 |

## API tin tức

Bản cũ: 12 mục; snapshot mới: 12 mục; cùng URL bài: 12. URL chỉ có ở bản cũ: 0; URL chỉ có ở bản mới: 0. Xem thay đổi từng trường trong JSON để phân biệt id thay đổi với bài báo thay đổi.

## Ví dụ nguyên văn nguồn chưa có trong tài liệu cũ

Đây là mẫu từ danh sách đối chiếu ngược, không phải toàn bộ các phần thiếu. Tất cả chuỗi tìm thấy được lưu trong trường `source_candidate_strings_missing_from_old_files` của JSON.

- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/369-2063549c42145b16.js` — Cận cảnh hoa sen, ánh vàng và nền sơn then trên tác phẩm sơn mài, ảnh minh họa
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/369-2063549c42145b16.js` — Tác phẩm sơn mài hoàn chỉnh cùng các mẫu chất liệu được đặt chồng bên cạnh.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/648.013156edff3e7a3c.js` — Kéo để xoay tác phẩm 3D; hoặc dùng phím mũi tên, Home để đặt lại góc
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/648.013156edff3e7a3c.js` —  Bố cục của bạn vẫn được giữ để tiếp tục bằng các điều khiển thay thế.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/840-f19fdd306966b2e5.js` — Không lưu được bản nháp. Nét vẽ vẫn sẽ được áp dụng khi bạn tiếp tục.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/840-f19fdd306966b2e5.js` — Không thể tạo ảnh mặt hộp lúc này. Hãy thử lại.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/840-f19fdd306966b2e5.js` — Chọn mặt, đặt nét vẽ rồi dùng nút bên dưới để đưa bản phối lên mô hình.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/cau-chuyen-son-mai/page-18999a17f9a00aec.js` — Tìm hiểu vật liệu hoặc tự tạo một bề mặt sơn mài.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js` — Kiểm tra độ ổn định; thay đổi nhiệt độ và độ ẩm có thể ảnh hưởng cốt.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js` — Cần cân nhắc độ ổn định và cách gia cố phù hợp với hình thể.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js` — Bề mặt gốm có độ đặc và độ nhẵn riêng; cách chuẩn bị phụ thuộc cấu tạo tác phẩm.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/page-1f5c1f7a3dcd2475.js` —  hình ảnh chưa tải được. Bạn vẫn có thể tiếp tục.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/page-1f5c1f7a3dcd2475.js` — Lớp vóc và sơn lót tạo mặt nền phẳng, độ bền và sự liên kết.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/page-1f5c1f7a3dcd2475.js` — Sắc son xây dựng chiều sâu màu sắc bên dưới hình ảnh.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/tin-tuc-su-kien/page-0044ed8affa87fe5.js` — Sơn mài đương đại và trầm hương cùng hiện diện tại Văn Miếu, nối chất liệu với ký ức của không gian di sản.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/tin-tuc-su-kien/page-0044ed8affa87fe5.js` — Đã lưu bản đăng ký minh họa trên thiết bị này. Thông tin chưa được gửi đến ban tổ chức.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/tin-tuc-su-kien/page-0044ed8affa87fe5.js` — Thiết bị chưa cho phép lưu bản đăng ký minh họa. Hãy liên hệ ban tổ chức qua đường dẫn nguồn.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/trai-nghiem/hanh-trinh/page-2c74554e92ef9036.js` — Không thể đọc bản đang làm; bạn có thể bắt đầu một bản mới.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/trai-nghiem/hanh-trinh/page-2c74554e92ef9036.js` — Bản phối đang mở vẫn dùng được, nhưng thiết bị không thể lưu bản nháp sau khi đóng trang.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/trai-nghiem/hanh-trinh/page-2c74554e92ef9036.js` — Chọn nền, chất liệu, bố cục, lớp phủ và mức độ mài để tạo một bề mặt sơn mài minh họa.
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/trai-nghiem/page-4cfd64a621149b8e.js` — Cận cảnh khảm hoa trên nền sơn đỏ, ảnh minh họa
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/trai-nghiem/page-4cfd64a621149b8e.js` — Cận cảnh các lớp vật liệu bên dưới mặt sơn mài, ảnh minh họa
- **Nguồn:** `kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/app/trai-nghiem/page-4cfd64a621149b8e.js` — Sơn mài không chỉ là một vật liệu, mà còn là cách người Việt kể câu chuyện về bản sắc dân tộc.
- **Nguồn:** `kiem_tra_2026-10-12/trich_xuat_html/kham-pha.json` — Trước khi trở thành một lớp sơn, nó bắt đầu từ nhựa cây. Một trong những chất liệu quan trọng của sơn mài truyền thống Việt Nam là sơn ta – nhựa được khai thác từ cây sơn, một loại cây được trồng lâu đời tại vùng trung du Bắc Bộ, trong đó Phú Thọ là vùng nổi tiếng với nghề trồng và khai thác sơn.
- **Nguồn:** `kiem_tra_2026-10-12/trich_xuat_html/tin-tuc-su-kien.json` — Báo Nhân Dân điện tử · 29/3/2026 · ẢNH MINH HỌA
- **Nguồn:** `kiem_tra_2026-10-12/trich_xuat_html/ve-du-an.json` — Năm thành viên cùng đảm nhận các vai trò trong dự án.
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/02_cong_doan_5.json` — Có thể quan sát một phần lớp phía dưới. Kéo trực tiếp trên vật thể hoặc mài từng lượt. Nước cuốn phần bị mài đi; sơn không hòa tan hay chảy.
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/02_hoan_thien_Ho_n_t_t.json` — Nền Đỏ son · hoàn thiện Bóng · mức mài mô phỏng 0%. Đây không phải công thức hay đơn đặt hàng.
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/02_hoan_thien_M_i_n__c.json` — Chưa mài tới: lớp trên còn che nhiều chi tiết. Kéo trực tiếp trên vật thể hoặc mài từng lượt. Nước cuốn phần bị mài đi; sơn không hòa tan hay chảy.
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/03_xuong_lam_voc.json` — Kiểm tra độ ổn định của Gỗ, gia cố khi phù hợp, sau đó hom và làm phẳng trước khi sơn nền.
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/04_hanh_trinh_phu_lop_xong.json` — Đã phủ 1 lượt; sắc màu và vân trang trí vẫn được giữ nguyên.
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/05_tu_chinh_mac_dinh.json` — Xem trước: Đỏ son · Hoa sen · Vỏ trứng · khắc tên
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/06_cau_chuyen_moc_1_day_du.json` — TRI THỨC QUA THẾ HỆ · TƯ LIỆU THEO MẠCH THỜI GIAN
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/06_cau_chuyen_moc_3_day_du.json` — Nhiều thập niên sau, Vườn xuân Trung Nam Bắc đưa những nghiên cứu lâu dài về chất liệu, màu sắc và cấu trúc nhiều lớp của Nguyễn Gia Trí vào một tác phẩm có quy mô lớn hơn. Đặt những tác phẩm ấy cạnh nhau, người ta không chỉ nhìn thấy phong cách của từng họa sĩ. Người ta nhìn thấy sự trưởng thành của chính chất liệu.
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/06_cau_chuyen_moc_4_day_du.json` — Đến giai đoạn những thử nghiệm về sơn mài diễn ra trong môi trường Mỹ thuật Đông Dương, mối quan hệ giữa làng nghề và môi trường mỹ thuật trở nên đặc biệt đáng chú ý. Nghệ nhân Đinh Văn Thành, người xuất thân từ Hạ Thái và làm việc trong môi trường của Trường Cao đẳng Mỹ thuật Đông Dương, thường được nhắc đến như một nhân vật kết nối hai thế giới ấy.
- **Nguồn:** `kiem_tra_2026-10-12/trinh_duyet/06_cau_chuyen_moc_5_day_du.json` — Bề mặt có thể bóng hoặc lì. Có thể phẳng hoặc để lộ cấu trúc. Có thể được xử lý rất mịn hoặc chủ động giữ lại dấu vết của quá trình làm. Đề tài cũng tiếp tục đi xa hơn. Phong cảnh và con người vẫn còn đó, đồng thời xuất hiện thêm những câu chuyện về ký ức cá nhân, bản sắc, đô thị, môi trường, công nghệ và trải nghiệm trong đời sống hiện đại. Chất liệu cũ bắt đầu kể những câu chuyện mới.

## Cách tái kiểm tra

Chạy `python3 scripts/audit_old_content.py` tại thư mục dự án. Script chỉ đọc các file cũ và nguồn đã lưu; chỉ ghi hai file báo cáo của lần kiểm tra. Không gọi mạng, không sửa tài liệu gốc. SHA-256 của đầu vào được lưu để biết báo cáo ứng với snapshot nào.

Chuẩn hóa gồm HTML entity, Unicode NFKC, chữ hoa/thường, khoảng trắng và dấu ngoặc kép/gạch ngang kiểu chữ. Không bỏ dấu tiếng Việt, không đổi nghĩa câu. Phần xác minh kỹ thuật GLB là riêng biệt với phép đối chiếu chuỗi.
