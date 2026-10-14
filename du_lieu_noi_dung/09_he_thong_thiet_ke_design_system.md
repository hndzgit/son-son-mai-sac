# Hệ Thống Thiết Kế (Design System) & Design Tokens

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
