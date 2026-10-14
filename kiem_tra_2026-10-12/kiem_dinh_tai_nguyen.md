# Kiểm định tài nguyên — 12/10/2026

Tạo lúc 2026-10-12T14:10:58.663345+07:00. Đây là kiểm định trên file đã lưu; trạng thái HTTP lấy từ manifest của đợt cào mới.

## Kết quả chính

- Đã xét 268 file nguồn; 164 file ảnh (91 nội dung SHA-256 khác nhau), 6 font và 2 mô hình GLB.
- Ảnh lỗi giải mã/XML: 0. File manifest sai hash/kích thước: 0 / 163.
- 15 ảnh box-*.jpg cũ vẫn giải mã đầy đủ, không bị thay đổi so với kiểm kê đầu, dù URL hiện trả HTTP 404.
- Đã bóc 3 data URI có dữ liệu tĩnh, ghi lại 8 tiền tố data URI dùng kiểm tra dữ liệu tương tác; lỗi bóc: 0.
- Đã giữ riêng 313 chuỗi GLSL/shader khác nhau; có nguồn và vị trí ký tự.
- CSS: 26 nguồn gồm CSS ngoài và CSS inline; JSON chứa toàn bộ selector/declaration đã phân tích, custom properties, font-face, media/supports, keyframes, animation/transition.

## Ảnh box cũ và bằng chứng HTTP

| File | Kích thước | File cũ hợp lệ | SHA khớp kiểm kê đầu | HTTP mới |
|---|---:|---|---|---|
| box-1.jpg | 1045 × 612 | True | True | 404 |
| box-12.jpg | 526 × 269 | True | True | 404 |
| box-14.jpg | 803 × 574 | True | True | 404 |
| box-15.jpg | 861 × 508 | True | True | 404 |
| box-16.jpg | 861 × 508 | True | True | 404 |
| box-17.jpg | 861 × 508 | True | True | 404 |
| box-18.jpg | 861 × 508 | True | True | 404 |
| box-19.jpg | 861 × 508 | True | True | 404 |
| box-20.jpg | 861 × 508 | True | True | 404 |
| box-21.jpg | 861 × 508 | True | True | 404 |
| box-22.jpg | 861 × 461 | True | True | 404 |
| box-23.jpg | 1123 × 621 | True | True | 200 |
| box-5.jpg | 464 × 252 | True | True | 404 |
| box-6.jpg | 475 × 254 | True | True | 404 |
| box-7.jpg | 470 × 224 | True | True | 404 |
| box-8.jpg | 535 × 277 | True | True | 404 |

Không ghi đè ảnh cũ bằng HTML 404. File HTML lỗi mới được giữ riêng trong `http_loi/`; hash và đường dẫn có trong JSON.

## Favicon

- `favicon.ico`: giống nhau.
  - Cũ: 1150 byte, SHA-256 `c17f919ce7bb47bfb41ed377fcbdd80f4810a3dd3d0bec2f4cf173f6d34060f1`, ICO 16 × 16.
  - Mới: 1150 byte, SHA-256 `c17f919ce7bb47bfb41ed377fcbdd80f4810a3dd3d0bec2f4cf173f6d34060f1`, ICO 16 × 16.
- `favicon.svg`: khác nội dung.
  - Chỉ khác ký tự xuống dòng: 2 CRLF cũ thành LF. XML/nội dung đồ họa giữ nguyên.
  - Cũ: 3652 byte, SHA-256 `ac76206ab166c814130d30c3b51b80170e9036d0a3176290699240105fa4a316`, SVG None × None.
  - Mới: 3650 byte, SHA-256 `5aff18aea6e243f2983700cc4d3ef064157e97a7ebcead335933629a4562f6ee`, SVG None × None.

## Mô hình và font

- `hinh_anh_assets/models/vercel-lacquer-box.glb`: hợp lệ=True, {'scenes': 1, 'nodes': 12, 'meshes': 10, 'materials': 4, 'accessors': 44, 'bufferViews': 44, 'buffers': 1, 'textures': 0, 'images': 0, 'animations': 0, 'skins': 0, 'cameras': 0}; JSON chính xác: `kiem_tra_2026-10-12/tai_nguyen_nhung/glb/23c94939b49db25685c8.gltf.json`.
- `kiem_tra_2026-10-12/ban_chup_goc/models/vercel-lacquer-box.glb`: hợp lệ=True, {'scenes': 1, 'nodes': 12, 'meshes': 10, 'materials': 4, 'accessors': 44, 'bufferViews': 44, 'buffers': 1, 'textures': 0, 'images': 0, 'animations': 0, 'skins': 0, 'cameras': 0}; JSON chính xác: `kiem_tra_2026-10-12/tai_nguyen_nhung/glb/23c94939b49db25685c8.gltf.json`.
- `hinh_anh_assets/story-assets/Inter-Full.ttf`: hợp lệ=True; 2937 glyph, 2852 codepoint; Inter Variable, InterVariable, Regular.
- `hinh_anh_assets/story-assets/NotoSerif-Full.ttf`: hợp lệ=True; 3830 glyph, 2965 codepoint; Noto Serif, Regular, Noto Serif Regular, NotoSerif-Regular.
- `hinh_anh_assets/story-assets/PlayfairDisplay-Full.ttf`: hợp lệ=True; 1103 glyph, 659 codepoint; Playfair Display, Regular, Playfair Display Regular, PlayfairDisplay-Regular.
- `kiem_tra_2026-10-12/ban_chup_goc/story-assets/Inter-Full.ttf`: hợp lệ=True; 2937 glyph, 2852 codepoint; Inter Variable, InterVariable, Regular.
- `kiem_tra_2026-10-12/ban_chup_goc/story-assets/NotoSerif-Full.ttf`: hợp lệ=True; 3830 glyph, 2965 codepoint; Noto Serif, Regular, Noto Serif Regular, NotoSerif-Regular.
- `kiem_tra_2026-10-12/ban_chup_goc/story-assets/PlayfairDisplay-Full.ttf`: hợp lệ=True; 1103 glyph, 659 codepoint; Playfair Display, Regular, Playfair Display Regular, PlayfairDisplay-Regular.

## Tệp nhúng

- `kiem_tra_2026-10-12/tai_nguyen_nhung/data_uri/edf542ba39121c852852c582.svg`: image/svg+xml, 247 byte, hợp lệ=True, 2 vị trí nguồn.
- `kiem_tra_2026-10-12/tai_nguyen_nhung/data_uri/c90cff659645a312a2880496.webp`: image/webp, 42 byte, hợp lệ=True, 2 vị trí nguồn.
- `kiem_tra_2026-10-12/tai_nguyen_nhung/data_uri/44a885f39964f2a7a1af67d8.avif`: image/avif, 305 byte, hợp lệ=True, 2 vị trí nguồn.

Mục lục đầy đủ: `tai_nguyen_nhung/muc_luc.json`. Mỗi data URI có nguyên văn nguồn, offset và hash của dữ liệu giải mã; mỗi shader có nguồn và offset.

## Giới hạn kiểm định

- Kiểm tra tính toàn vẹn và cấu trúc file, không thay thế kiểm thử mọi thao tác UI.
- SVG chỉ được phân tích XML; shader chưa được biên dịch GPU; font chưa được render trực quan.
- Dữ liệu canvas sinh lúc chạy, ảnh người dùng tải lên, trạng thái lưu ở localStorage và kết quả tương tác không có một file cố định để bóc từ bundle.
- Tất cả dữ liệu gốc được giữ nguyên. Mọi kết luận HTTP chỉ tương ứng thời điểm lấy trong manifest.

Chi tiết máy đọc: `kiem_dinh_tai_nguyen.json`.
