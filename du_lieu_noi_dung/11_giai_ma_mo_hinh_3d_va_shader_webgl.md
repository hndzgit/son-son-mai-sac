# Chuyên Luận Kỹ Thuật 3D: Giải Mã Mô Hình Nhị Phân glTF, Vật Liệu PBR & Bộ Shader GLSL Mô Phỏng Sơn Mài

> **Tài liệu kỹ thuật chuyên sâu tối thượng (Supreme Technical Specification)**  
> **Hồ sơ giải mã:** Mô hình nhị phân 3D `vercel-lacquer-box.glb`, Động cơ WebGL Three.js r128+, Bộ Shader GLSL phân tầng sơn mài, và Bộ tổng hợp âm thanh vật lý DSP Web Audio API.

---

## I. MÔ HÌNH NHỊ PHÂN 3D `vercel-lacquer-box.glb` (449 KB)

Trái với các giải pháp dựng hình web 3D đơn giản thông thường, dự án "Sơn Son Mài Sắc" tích hợp một mô hình nhị phân glTF 2.0 (GLB) độ chi tiết cao, mô phỏng hoàn chỉnh hộp sơn mài chân quỳ khóa khuyên đồng truyền thống Việt Nam.

```
+-----------------------------------------------------------------------+
|                         LacquerBox_LOD0 (Root)                        |
+-----------------------------------+-----------------------------------+
                                    |
     +------------------------------+------------------------------+
     |                              |                              |
[Mesh_BaseBox]                 [Mesh_Lid]                    [Mesh_LidTrim]
(Thân hộp sơn then)        (Nắp hộp 6 primitives)          (Viền bo nẹp nắp)
     |                              |                              |
     +------------------------------+------------------------------+
     |                              |
[Group_Clasp] (Khóa đồng)     [4x Mesh_Foot_0..3] (4 Chân quỳ chạm khắc)
     |-- Mesh_ClaspPlate (Bản lề mề đay)
     |-- Mesh_ClaspHasp (Móc cài khóa)
     \-- Mesh_ClaspRing (Khuyên tròn gài)
```

### 1. Tỷ Lệ Không Gian Vật Lý
- **Tỉ lệ vàng thủ công:** `3.2 (dài) : 2.24 (rộng) : 0.848 (cao)`.
- Kích thước này tương ứng tỉ lệ chuẩn của các hộp đựng sắc phong, tráp trầu hoặc hộp trang sức hoàng gia triều Nguyễn.

### 2. Bảng Phân Tích Vật Liệu Quang Học PBR (Physically Based Rendering)

| Tên Vật Liệu | Màu Cơ Bản (sRGB / Factor) | Mã HEX | Metallic | Roughness | Đặc Tính Quang Học |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Mat_BlackLacquer` | `[0.0030, 0.0027, 0.0024]` | `#0f0d0c` | `0.05` | `0.18` | Hấp thụ 99.7% ánh sáng, bóng sâu phản xạ mờ như men gốm cổ |
| `Mat_LidArt` | `[0.0060, 0.0051, 0.0043]` | `#191512` | `0.12` | `0.22` | Bề mặt nền mài chứa các lớp cẩn vỏ trứng và thếp vàng |
| `Mat_GoldFiligree` | `[0.7379, 0.4910, 0.0865]` | `#bc7d16` | `0.75` | `0.28` | Ánh kim vàng quỳ rực rỡ, phản xạ Fresnel kim loại ấm |
| `Mat_BrassHardware`| `[0.5394, 0.3277, 0.0395]` | `#8a540a` | `0.85` | `0.35` | Đồng thau đúc có độ nhám vi mô, mô phỏng kim loại nhuốm màu thời gian |

### 3. Bóng Đổ Tiếp Xúc Thích Ứng (Dynamic Contact Shadow)
Hệ thống sử dụng một Canvas 2D 256x256 tạo `RadialGradient(128, 128, 24 -> 122)` với 3 điểm dừng màu:
- Tâm (0%): `rgba(74, 43, 21, 0.20)`
- Giữa (65%): `rgba(74, 43, 21, 0.07)`
- Rìa (100%): `rgba(74, 43, 21, 0.0)`
Mặt phẳng PlaneGeometry (4.4 x 3.2) được đặt tại `y = -0.006` với `depthWrite = false`, tự động ẩn khi góc nhìn hộp bị lật đáy (`Math.cos(rotation.x) > 0.1`).

---

## II. BỘ SHADER GLSL TÙY BIẾN: MÔ PHỎNG VẬT LÝ BÀO MÒN SƠN MÀI

### 1. Vertex Shader (Tọa Độ Đỉnh)
```glsl
varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vViewPosition;
varying vec3 vWorldPosition;

void main() {
  vUv = uv;
  vec4 worldPosition = modelMatrix * vec4(position, 1.0);
  vWorldPosition = worldPosition.xyz;
  vec4 mvPosition = viewMatrix * worldPosition;
  vViewPosition = -mvPosition.xyz;
  vNormal = normalize(normalMatrix * normal);
  gl_Position = projectionMatrix * mvPosition;
}
```

### 2. Fragment Shader (Giải Thuật Bào Mòn Đa Tầng)

#### A. Công thức tính độ sâu mài thực tế (Depth Abrasion Function)
$$	ext{sandDepth} = 	ext{clamp}\left(rac{	ext{rawDepth}}{0.6 + 	ext{localMaterialDepth} 	imes 0.8}, 0.0, 1.0ight)$$
- `rawDepth`: Lấy từ kênh màu đỏ của Mask Canvas `texture2D(uMaskMap, vUv).r`.
- `localMaterialDepth`: Hòa trộn giữa giá trị độ sâu toàn cục và bản đồ Depthmap cục bộ.

#### B. Phân tầng quang học theo độ mài
1. **Lớp bề mặt (Upper Layer):** Chuyển từ màu sơn then đỉnh (`uTopColor` `#0F0000`) sang màu cánh gián hổ phách (`uAmberColor` `#3D1200`).
2. **Lớp nền lộ (Exposed Ground):** Lộ màu đỏ son trung gian (`uMidColor` `#8C0E0E`) và ánh vàng/trắng ngà (`uGoldColor` / `uEggshellColor`).
3. **Ngưỡng hiển lộ họa tiết (Reveal Threshold):**
   $$	ext{revealThreshold} = 0.33 + 	ext{localMaterialDepth} 	imes 0.28$$
   Chỉ khi độ mài vượt qua ngưỡng này, họa tiết vỏ trứng/vàng quỳ mới xuất hiện sắc nét thông qua hàm `smoothstep`.
4. **Phạm vào cốt gỗ (Over-sanded Wood Substrate):**
   Nếu người dùng mài vượt mức `rawDepth > 0.94`, hệ thống tính toán nhiễu hạt gỗ tự nhiên (Pseudo-random Wood Grain):
   ```glsl
   float worn = smoothstep(0.94, 1.0, rawDepth);
   float grain = fract(sin(dot(vUv, vec2(127.1, 311.7))) * 43758.5453);
   baseColor = mix(baseColor, vec3(0.17, 0.085, 0.035) + grain * 0.035, worn * 0.9);
   ```
   Màu sắc lập tức bị phá hủy và chuyển thành màu gỗ thô sần sùi!

#### C. Tái tạo pháp tuyến tiếp tuyến từ độ chói (Tangential Relief Normal Reconstruction)
Để các mảnh vỏ trứng và lá vàng không bị phẳng lì như hình dán (flat decals), Shader thực hiện quét vi phân 4 điểm (Sobel 4-tap stencil) trên độ phân giải 1536x1024:
```glsl
vec2 artTexel = vec2(1.0 / 1536.0, 1.0 / 1024.0);
float leftArt  = dot(texture2D(uArtMap, vUv - vec2(artTexel.x, 0.0)).rgb, vec3(0.299, 0.587, 0.114));
float rightArt = dot(texture2D(uArtMap, vUv + vec2(artTexel.x, 0.0)).rgb, vec3(0.299, 0.587, 0.114));
float lowArt   = dot(texture2D(uArtMap, vUv - vec2(0.0, artTexel.y)).rgb, vec3(0.299, 0.587, 0.114));
float highArt  = dot(texture2D(uArtMap, vUv + vec2(0.0, artTexel.y)).rgb, vec3(0.299, 0.587, 0.114));
N = normalize(N + vec3(leftArt - rightArt, lowArt - highArt, 0.0) * uDecorationRelief);
```

#### D. Hiệu ứng gợn sóng nước vi mô (Water Sheen Physics)
Khi đang mài nước, lớp nước mỏng phản chiếu ánh sáng tạo nên những tia lấp lánh (specular water glint):
```glsl
if (sandDepth > 0.03 && uWaterDroplets > 0.0) {
  float ripple = sin(vUv.x * 50.0 + uTime * 4.0) * cos(vUv.y * 50.0 + uTime * 3.0);
  float waterGlint = max(0.0, ripple) * 0.12 * uWaterDroplets * sandDepth;
  finalColor += vec3(waterGlint * 0.8, waterGlint * 0.9, waterGlint);
}
```

---

## III. BỘ TỔNG HỢP ÂM THANH VẬT LÝ DSP (WEB AUDIO SYNTHESIS)

Thay vì tải tệp MP3 tĩnh (gây trễ và lặp lại đơn điệu), hệ thống xây dựng một **bộ tổng hợp âm thanh thời gian thực (Procedural Audio Synthesizer - Class `v`)**:

### 1. Thuật toán tạo Pink Noise (Paul Kellet 3-pole IIR Filter)
Pink Noise ($1/f$) có mật độ năng lượng giảm 3dB mỗi octave, mô phỏng hoàn hảo tiếng cọ xát tự nhiên:
```javascript
for (let e = 0; e < bufferLength; e++) {
  let white = 2 * Math.random() - 1;
  b0 = 0.99886 * b0 + 0.0555179 * white;
  b1 = 0.99332 * b1 + 0.0750759 * white;
  b2 = 0.96900 * b2 + 0.1538520 * white;
  channelData[e] = (b0 + b1 + b2 + 0.5362 * white) * 0.25;
}
```

### 2. Chuỗi Xử Lý Âm Thanh (Audio Signal Chain)
```
[Pink Noise Buffer Source] (Loop 2.0s)
            |
            v
[BiquadFilter: Highpass 350 Hz] (Cắt tiếng ù rền âm trầm)
            |
            v
[BiquadFilter: Bandpass 1100 Hz, Q=2.2] (Tần số ma sát đá mài & than)
            | (Biến thiên động 700 Hz - 2200 Hz theo tốc độ chuột)
            v
[GainNode: Dynamic Volume] (Tự động tăng giảm độ lớn theo lực kéo)
            |
            v
[AudioContext.destination] (Loa thiết bị)
```

- Khi người dùng rê cọ nhanh: Tần số Bandpass được nâng lên tới `2200 Hz` mô phỏng tiếng nước chảy xiết và lực ma sát mạnh.
- Khi nhả chuột: Âm lượng hạ tuyến tính về 0 trong `120ms` (`linearRampToValueAtTime(1e-4, t + 0.12)`).
