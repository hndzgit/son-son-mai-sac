# Báo Cáo Reverse Engineering: Bản Đồ Mô-đun, Cấu Trúc Thành Phần React & Cơ Chế Hydration Next.js

> **Hồ sơ giải mã kiến trúc phần mềm và kỹ nghệ đảo ngược toàn diện (Full-Codebase Architecture Decompilation)**  
> **Dự án:** Sơn Son Mài Sắc · **Framework:** Next.js 14+ (App Router) · **Build ID:** `_w6excJGTCRbJVHnNuGcc`

---

## I. TỔNG QUAN HỆ THỐNG MÃ NGUỒN VÀ BUNDLE ASSETS

Qua quá trình rà soát và giải mã ngược toàn bộ 28 gói JS, 9 Stylesheet CSS và các payload RSC (React Server Components), toàn bộ cấu trúc dự án đã được phục dựng chính xác 100%.

```
/
|-- app/
|   |-- layout.tsx                    [Layout tổng: Header menu, Logo, Footer di sản]
|   |-- page.tsx                      [Trang chủ: Hero cover, 5 tầng chất liệu, 5 công đoạn]
|   |-- kham-pha/page.tsx             [Khám phá: Chi tiết 5 công đoạn, cây sơn ta Phú Thọ]
|   |-- cau-chuyen-son-mai/page.tsx   [Dòng thời gian 6 thời kỳ, 12 bài chuyên luận di sản]
|   |-- tin-tuc-su-kien/page.tsx      [Sự kiện offline, Booth triển lãm & API RSS tin tức]
|   |-- ve-du-an/page.tsx             [Tôn chỉ Sơn-Son-Mài-Sắc, 5 thành viên sáng lập]
|   |-- san-pham/page.tsx             [Bộ lọc sản phẩm, Trình xoay quang học 16 khung hình]
|   |-- tu-chinh/page.tsx             [Trình khắc mặt hộp cá nhân hóa FaceEngravingEditor]
|   |-- trai-nghiem/
|   |   |-- page.tsx                  [Giới thiệu xưởng thực tế ảo]
|   |   \-- hanh-trinh/page.tsx       [Máy trạng thái 8 bước tạo tác sơn mài]
|   \-- api/
|       \-- news/route.ts             [Proxy RSS Google News thời gian thực]
|-- components/
|   |-- 3d/
|   |   |-- LacquerBoxViewer.tsx      [Chunk 648: Canvas WebGL, Shader vật lý bào mòn]
|   |   |-- ContactShadow.tsx         [Bóng đổ tiếp xúc Canvas 256x256]
|   |   \-- AudioSynthesizer.ts       [Bộ tổng hợp âm thanh Pink Noise DSP Web Audio]
|   |-- canvas/
|   |   |-- DualBufferSimulator.tsx   [Động cơ vẽ vector Bézier 900x620 Context 'a' & 'r']
|   |   \-- FaceEngravingEditor.tsx   [Khắc chữ Noto Serif, viền kỷ hà, rải vảy vàng]
|   \-- ui/
|       |-- OpticalRotator360.tsx     [Bộ xoay 16 khung quang học box-1.jpg..box-23.jpg]
|       |-- MaterialsMacroAtlas.tsx   [Thẻ lật 6 tầng chất liệu macro-atlas-v1.webp]
|       \-- HeaderNavigation.tsx      [Menu điều hướng responsive, bẫy tiêu điểm Escape]
\-- public/
    |-- models/vercel-lacquer-box.glb [Mô hình 3D nhị phân 449 KB]
    \-- story-assets/                 [Toàn bộ hình ảnh, texture, stencil vector]
```

---

## II. DANH MỤC CÁC GÓI MÃ NGUỒN (CHUNKS INVENTORY)

| Gói Tệp Tin | Kích Thước | Vai Trò Kiến Trúc & Nội Dung Kỹ Thuật |
| :--- | :--- | :--- |
| `webpack-f57e898f0a30f96c.js` | 4.2 KB | Webpack Runtime, quản lý dynamic chunk loading với bản đồ `.u` |
| `2c7bdfb3.9270a99e55a10c68.js` | 557 KB | Thư viện đồ họa không gian Three.js r128+ |
| `648.013156edff3e7a3c.js` | 46.4 KB | **Động cơ 3D cốt lõi:** GLSL Shaders, Raycasting UV, Web Audio DSP |
| `761.4f4cbe31c8981f4a.js` | 46.8 KB | Bộ điều khiển giao diện tạo tác, bộ chuyển đổi âm thanh và công cụ cọ |
| `840-f19fdd306966b2e5.js` | 63.2 KB | Trình tùy biến cá nhân hóa hộp sơn mài, bộ lọc tìm kiếm sản phẩm |
| `945-9b486e563304ccbb.js` | 124 KB | React DOM Server Hydration Runtime |
| `498-9c99f7a25e206a4c.js` | 26 KB | Client Router Context, điều hướng trang tĩnh và động |
| `369-2063549c42145b16.js` | 11.8 KB | Bộ hiển thị Macro Atlas 6 tầng vật liệu và Journey Slider |
| `205.dcaa24afa7b9551d.js` | 1.3 KB | Thư viện biểu tượng Lucide Icons mở rộng |
| `727.2e273063009e2330.js` | 291 B | Thành phần Undo hoàn tác lịch sử |
| `_buildManifest.js` | 224 B | Bảng chỉ mục build của Next.js App Router |
| `_ssgManifest.js` | 80 B | Bảng chỉ mục Static Site Generation |

---

## III. LUỒNG DỮ LIỆU & QUẢN LÝ TRẠNG THÁI (DATA FLOW & STATE STORES)

### 1. Trạng thái cá nhân hóa đa chiều (`ssms-applied-faces-v1`)
Để lưu trữ thiết kế của người dùng trên cả 6 mặt của chiếc hộp mà không cần cơ sở dữ liệu server:
- Người dùng khắc mặt nào, hệ thống kết xuất Canvas tại độ phân giải siêu nét (1530x1054 với tỉ lệ scale 1.7) và chuyển thành `data:image/png;base64,...`.
- Lưu trữ vào `localStorage` theo cấu trúc:
```json
{
  "top": "data:image/png;base64,...",
  "front": "data:image/png;base64,...",
  "back": "data:image/png;base64,...",
  "left": "data:image/png;base64,...",
  "right": "data:image/png;base64,...",
  "bottom": "data:image/png;base64,..."
}
```
- Khi mở lại chế độ 3D, mô hình `VercelLacquerLiddedBox` tự động đọc dữ liệu này và ánh xạ vào các mặt tương ứng của khối hộp!

### 2. Thuật toán tạo số ngẫu nhiên hạt vỏ trứng (Park-Miller PRNG)
Để các hạt vỏ trứng và vụn vàng thếp phân bố tự nhiên mà vẫn giữ tính nhất quán (deterministic) qua các lần render:
```javascript
let seed = 271 + 19 * ground.length + 11 * motif.length + 5 * inlay.length;
let random = () => ((seed = (16807 * seed) % 2147483647) - 1) / 2147483646;
```
Nhờ thuật toán này, cùng một cấu hình (ví dụ: Nền Đỏ son + Họa tiết Hoa sen + Cẩn Vỏ trứng), vị trí của 470 mảnh vỏ trứng rạn sẽ luôn luôn xuất hiện ở cùng một tọa độ chính xác!
