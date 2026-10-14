# -*- coding: utf-8 -*-
"""
MÁY CHỦ PHỤC VỤ NGUYÊN BẢN 1:1 SƠN SON MÀI SẮC
Bản sao chuẩn xác 100% từ https://son-son-mai-sac-orpin.vercel.app/
Hỗ trợ đầy đủ:
- Tương tác 3D WebGL / Three.js Canvas
- Hiệu ứng hoạt ảnh cuộn trang (Scroll Reveal data-reveal)
- Lớp bóc tách vật liệu (Peeling layers & Material cards)
- Luồng React Server Components (Next.js _rsc flight stream với text/x-component)
- Định tuyến mượt mà Next.js client-side router không bị mất hiệu ứng
"""
import http.server
import socketserver
import mimetypes
import urllib.parse
import urllib.request
import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SITE_ROOT = BASE_DIR
RSC_DIR = os.path.join(BASE_DIR, 'rsc_payloads')
LIVE_FALLBACK_URL = "https://son-son-mai-sac-orpin.vercel.app"

# MIME types chuẩn
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('model/gltf+json', '.gltf')
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/avif', '.avif')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('image/png', '.png')
mimetypes.add_type('image/jpeg', '.jpg')
mimetypes.add_type('font/ttf', '.ttf')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/json', '.json')

RSC_MAP = {
    '': 'root.rsc',
    '/': 'root.rsc',
    '/kham-pha': 'kham-pha.rsc',
    '/cau-chuyen-son-mai': 'cau-chuyen-son-mai.rsc',
    '/cau-chuyen-son-mai/bai-viet': 'cau-chuyen-son-mai.rsc',
    '/tin-tuc-su-kien': 'tin-tuc-su-kien.rsc',
    '/ve-du-an': 've-du-an.rsc',
    '/san-pham': 'san-pham.rsc',
    '/trai-nghiem': 'trai-nghiem.rsc',
    '/trai-nghiem/hanh-trinh': os.path.join('trai-nghiem', 'hanh-trinh.rsc'),
    '/tu-chinh': 'tu-chinh.rsc',
}

class LacquerMirrorHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        clean_path = urllib.parse.unquote(parsed.path).rstrip('/')
        query_params = urllib.parse.parse_qs(parsed.query)

        is_rsc_request = (
            '_rsc' in query_params or
            self.headers.get('RSC') == '1' or
            self.headers.get('Next-Router-State-Tree') is not None
        )

        # 1. Xử lý RSC (React Server Component flight stream)
        if is_rsc_request:
            if clean_path == '/son-mai-la-gi':
                self.send_response(200)
                self.send_header('Content-Type', 'text/x-component; charset=utf-8')
                self.send_header('x-nextjs-redirect', '/son-mai-la-gi')
                self.end_headers()
                return
            rsc_rel = RSC_MAP.get(clean_path)
            if not rsc_rel and clean_path.startswith('/cau-chuyen-son-mai/bai-viet'):
                rsc_rel = 'cau-chuyen-son-mai.rsc'
            if rsc_rel:
                rsc_file = os.path.join(RSC_DIR, rsc_rel)
                if os.path.exists(rsc_file):
                    with open(rsc_file, 'rb') as fp:
                        data = fp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/x-component; charset=utf-8')
                    self.send_header('Content-Length', str(len(data)))
                    self.send_header('Vary', 'RSC, Next-Router-State-Tree, Next-Router-Prefetch')
                    self.send_header('x-matched-path', f'{clean_path}.rsc' if clean_path else '/root.rsc')
                    self.end_headers()
                    self.wfile.write(data)
                    return

            # Nếu không tìm thấy file RSC, fetch trực tiếp từ live để đảm bảo tương thích 100%
            try:
                live_url = f"{LIVE_FALLBACK_URL}{self.path}"
                req = urllib.request.Request(
                    live_url,
                    headers={
                        'User-Agent': self.headers.get('User-Agent', 'Mozilla/5.0'),
                        'RSC': '1',
                        'Next-Router-State-Tree': self.headers.get('Next-Router-State-Tree', '')
                    }
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/x-component; charset=utf-8')
                    self.send_header('Content-Length', str(len(data)))
                    self.send_header('Vary', 'RSC, Next-Router-State-Tree, Next-Router-Prefetch')
                    self.end_headers()
                    self.wfile.write(data)
                    return
            except Exception:
                # Nếu không thể fetch, trả về 404 để Next.js router kích hoạt fallback chuyển trang tự nhiên
                self.send_error(404, "RSC Payload Not Found")
                return

        # 2. Xử lý API JSON
        if clean_path.startswith('/api/'):
            api_file = os.path.join(SITE_ROOT, clean_path.lstrip('/'))
            if os.path.exists(api_file):
                with open(api_file, 'rb') as fp:
                    data = fp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return

        # 3. Xử lý biểu tượng apple touch icon precomposed
        if clean_path == '/apple-touch-icon-precomposed.png':
            target = os.path.join(SITE_ROOT, 'apple-touch-icon.png')
            if os.path.exists(target):
                with open(target, 'rb') as fp:
                    data = fp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return

        # 4. Phục vụ file tĩnh thông thường
        super().do_GET()

    def do_HEAD(self):
        parsed = urllib.parse.urlparse(self.path)
        clean_path = urllib.parse.unquote(parsed.path).rstrip('/')
        query_params = urllib.parse.parse_qs(parsed.query)

        is_rsc_request = (
            '_rsc' in query_params or
            self.headers.get('RSC') == '1' or
            self.headers.get('Next-Router-State-Tree') is not None
        )

        if is_rsc_request:
            rsc_rel = RSC_MAP.get(clean_path)
            if rsc_rel:
                rsc_file = os.path.join(RSC_DIR, rsc_rel)
                if os.path.exists(rsc_file):
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/x-component; charset=utf-8')
                    self.send_header('Content-Length', str(os.path.getsize(rsc_file)))
                    self.send_header('Vary', 'RSC, Next-Router-State-Tree, Next-Router-Prefetch')
                    self.send_header('x-matched-path', f'{clean_path}.rsc' if clean_path else '/root.rsc')
                    self.end_headers()
                    return

        super().do_HEAD()

    def translate_path(self, path):
        parsed = urllib.parse.urlparse(path)
        clean_path = urllib.parse.unquote(parsed.path)

        # Hỗ trợ /ung_dung_3d_offline nếu người dùng muốn xem thêm
        if clean_path.startswith('/ung_dung_3d_offline'):
            rel = clean_path[len('/ung_dung_3d_offline'):].lstrip('/')
            target = os.path.join(BASE_DIR, 'ung_dung_3d_offline', rel)
            if os.path.isdir(target):
                target = os.path.join(target, 'index.html')
            return target

        rel = clean_path.lstrip('/')
        target = os.path.join(SITE_ROOT, rel)

        # Xử lý clean URL Next.js: /kham-pha -> /kham-pha/index.html
        if os.path.isdir(target):
            index_file = os.path.join(target, 'index.html')
            if os.path.exists(index_file):
                return index_file

        if not os.path.exists(target):
            if os.path.exists(target + '.html'):
                return target + '.html'
            if os.path.exists(os.path.join(target, 'index.html')):
                return os.path.join(target, 'index.html')

        return target

    def guess_type(self, path):
        if path.endswith('/api/news') or path.endswith(os.sep + 'news'):
            return 'application/json'
        if path.endswith('/opengraph-image') or 'opengraph-image' in path:
            return 'image/png'
        if path.endswith('.glb'):
            return 'model/gltf-binary'
        if path.endswith('.webp'):
            return 'image/webp'
        if path.endswith('.ttf'):
            return 'font/ttf'
        return super().guess_type(path)

def run(port=3000):
    socketserver.TCPServer.allow_reuse_address = True
    for p in [port, 3001, 8080, 8000]:
        try:
            with socketserver.TCPServer(("", p), LacquerMirrorHandler) as httpd:
                print(f"================================================================")
                print(f"🌟 WEBSITE SƠN SON MÀI SẮC CHUẨN 100% NGUYÊN BẢN ĐANG CHẠY CỔNG {p}!")
                print(f"👉 Trang Chủ (Toàn bộ hiệu ứng 3D & cuộn): http://localhost:{p}/")
                print(f"👉 Khám Phá (5 công đoạn sơn mài):         http://localhost:{p}/kham-pha")
                print(f"👉 Câu Chuyện Sơn Mài (Lịch sử & nghệ nhân): http://localhost:{p}/cau-chuyen-son-mai")
                print(f"👉 Trải Nghiệm Xưởng 3D Sơn Mài:           http://localhost:{p}/trai-nghiem")
                print(f"👉 Tùy Chỉnh Khắc Mặt Hộp 3D:              http://localhost:{p}/tu-chinh")
                print(f"👉 Sản Phẩm Tác Phẩm Nghệ Thuật:           http://localhost:{p}/san-pham")
                print(f"👉 Tin Tức & Sự Kiện:                      http://localhost:{p}/tin-tuc-su-kien")
                print(f"👉 Về Dự Án:                               http://localhost:{p}/ve-du-an")
                print(f"================================================================")
                sys.stdout.flush()
                httpd.serve_forever()
                return
        except OSError:
            print(f"Cổng {p} bận, chuyển sang cổng tiếp theo...")
            continue
    print("Không thể mở cổng mạng!")

if __name__ == '__main__':
    p = 3000
    if len(sys.argv) > 1:
        try:
            p = int(sys.argv[1])
        except ValueError:
            pass
    run(p)
