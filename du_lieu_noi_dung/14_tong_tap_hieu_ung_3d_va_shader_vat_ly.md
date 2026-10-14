# Tổng Tập Kỹ Thuật 3D & Shader Vật Lý: Toàn Bộ 68 Mã Nguồn GLSL, Ma Trận PBR, Thuật Toán Bào Mòn & Mô Phỏng Đa Chiều

> **Hồ sơ chuyên khảo tối thượng về đồ họa không gian 3D (Master 3D Graphics Specification)**  
> **Dự án:** Sơn Son Mài Sắc · **Công nghệ:** Three.js r128+, Custom GLSL Shaders, glTF 2.0 Binary, DSP Web Audio API.

---

## I. MÔ HÌNH NHỊ PHÂN 3D `vercel-lacquer-box.glb` (449 KB)

Mô hình 3D nhị phân gốc của hộp sơn mài là kết tinh giữa tạo hình thủ công mỹ nghệ và tối ưu hóa thời gian thực WebGL:

```
+-----------------------------------------------------------------------------------------+
|                               LacquerBox_LOD0 (Root Node)                               |
+--------------------------------------------+--------------------------------------------+
                                             |
     +---------------------------------------+---------------------------------------+
     |                                       |                                       |
[Mesh_BaseBox]                          [Mesh_Lid]                             [Mesh_LidTrim]
- Thân hộp sơn then đen tuyền           - Nắp hộp 6 primitives                 - Viền bo chỉ vàng
- Roughness: 0.18, Metallic: 0.05       - Chứa lớp tranh mặt nắp               - Bo tròn mép nẹp
     |                                       |                                       |
     +---------------------------------------+---------------------------------------+
     |                                                                               |
[Group_Clasp] (Cụm khóa đồng hoàng gia)                         [4x Mesh_Foot_0..3] (4 Chân quỳ)
|-- Mesh_ClaspPlate: Mề đay hoa văn đồng đúc                     - Chân quỳ trước trái & phải
|-- Mesh_ClaspHasp: Móc khóa gài then chữ nhật                   - Chân quỳ sau trái & phải
\-- Mesh_ClaspRing: Khuyên tròn gài chốt                         - Roughness: 0.18, Metallic: 0.05
```

---

## II. HỆ THỐNG PHÂN LOẠI 68 SHADER GLSL CỐT LÕI

Dự án tích hợp tổng cộng 68 khối mã Shader GLSL (được trích xuất trọn vẹn tại `kiem_tra_2026-10-12/tai_nguyen_nhung/shader_glsl/`):

### 1. Shader Bóc Tách Sơn Mài Độc Quyền (`0cb9cc9e2e9c40f30189d48f.glsl` - 6,825 bytes)
Đây là trái tim của hệ thống mô phỏng tạo tác sơn mài:
- **Độ sâu bào mòn phi tuyến tính:**
  ```glsl
  float sandDepth = clamp(rawDepth / (0.6 + localMaterialDepth * 0.8), 0.0, 1.0);
  ```
- **Hòa trộn 3 tầng màu sơn:**
  - Tầng trên (Upper layer): Chuyển từ sơn then (`#0F0000`) sang nâu cánh gián (`#3D1200`).
  - Tầng giữa (Exposed ground): Chuyển từ cánh gián sang đỏ son (`#8C0E0E`).
  - Tầng cẩn (Inlay art): Hiển lộ vàng quỳ (`#FFBB10`) và vỏ trứng (`#EBEAE9`).
- **Tái tạo vi phân pháp tuyến (Normal Bump from Luminance):**
  Lấy đạo hàm độ chói qua 4 điểm texel lân cận `(1.0/1536.0, 1.0/1024.0)` để tạo hiệu ứng gồ ghề xúc giác cho mảnh vỏ trứng.
- **Vật lý phản xạ màng nước (Water Sheen Glint):**
  ```glsl
  float ripple = sin(vUv.x * 50.0 + uTime * 4.0) * cos(vUv.y * 50.0 + uTime * 3.0);
  float waterGlint = max(0.0, ripple) * 0.12 * uWaterDroplets * sandDepth;
  finalColor += vec3(waterGlint * 0.8, waterGlint * 0.9, waterGlint);
  ```

### 2. 30 Shader Chiếu Sáng Vật Lý PBR & Specular Blinn-Phong
- Tính toán góc nửa vector $H = 	ext{normalize}(L + V)$.
- Số mũ phản xạ gương thay đổi liên tục: Khi vóc còn thô ráp ($Roughness = 0.85 \implies Exponent = 12.0$), khi đã đánh bóng gương ($Roughness = 0.06 \implies Exponent = 180.0$).

### 3. 42 Shader Không Gian Pháp Tuyến & Tiếp Tuyến (Tangent Space)
- Xử lý các phép biến đổi pháp tuyến ma trận `normalMatrix`.
- Đảm bảo ánh sáng phản chiếu chính xác trên các đường cong vát của 4 chân quỳ và nắp hộp khi xoay 360 độ.

### 4. 10 Shader Bản Đồ Độ Sâu & Bóng Đổ Tiếp Xúc (Contact Shadow)
- Đóng gói độ sâu vào 4 kênh màu RGBA `DEPTH_PACKING == 3200`.
- Tạo bóng đổ mềm tự nhiên tiếp giáp mặt sàn triển lãm.

### 5. 4 Shader Phản Chiếu Môi Trường PMREM CubeUV
- Tạo ánh phản chiếu mờ của không gian triển lãm nghệ thuật lên men sơn ta hổ phách.

---

## III. BỘ TỔNG HỢP ÂM THANH MA SÁT NƯỚC THỜI GIAN THỰC (DSP WEB AUDIO)

- Không sử dụng file âm thanh ghi sẵn.
- **Thuật toán Pink Noise Paul Kellet:** Lọc 3 cực tạo dải âm thanh tự nhiên của tiếng nước và đá mài cọ xát vào mặt vóc.
- **Biquad Bandpass Filter:**
  - Tần số trung tâm: `1100 Hz` ($Q=2.2$).
  - Biến thiên động: `Math.min(2200, Math.max(700, 1000 + 1200 * speed))`.
  - Càng rê chuột nhanh, tần số càng cao, âm thanh chuyển từ tiếng xì xào êm dịu sang tiếng rào rào của nước chảy xiết!

---

## IV. BỘ XOAY QUANG HỌC 360° THỰC TẾ (16 KHUNG ẢNH THẬT)

- Gồm 16 khung ảnh độ phân giải cao (`box-1.jpg` đến `box-23.jpg`).
- Thuật toán bắt cử chỉ kéo vuốt với hệ số quán tính:
  ```javascript
  currentAngle += (targetAngle - currentAngle) * 0.08;
  let frameIndex = Math.floor((currentAngle / (2 * Math.PI)) * 16) % 16;
  ```
- Mang lại trải nghiệm phản quang chân thực 100% của tác phẩm sơn mài thật ngoài đời thực.
