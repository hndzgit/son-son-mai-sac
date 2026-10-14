# -*- coding: utf-8 -*-
"""
Script cập nhật Footer tối ưu thẩm mỹ:
1. Đặt Khẩu hiệu ("Đi Qua Từng Đường Mài / Khám Phá Giá Trị Việt") ngay DƯỚI chữ/logo Sơn Son Mài Sắc.
2. Tối ưu giao diện mạng xã hội thành các nút badge/pill hiện đại, thanh thoát, bỏ dấu ↗ thừa.
3. Đồng bộ vào CSS, Layout Chunk JS, RSC payloads và toàn bộ các trang HTML.
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

NEW_FOOTER_HTML = """<footer class="Footer_footer__eNA9m">
  <div class="Footer_mainGrid">
    <!-- Cột 1: Thương hiệu (Logo ở trên, Khẩu hiệu ngay dưới, Mạng xã hội dạng pill) -->
    <div class="Footer_brandBlock">
      <div class="Footer_brandHeader">
        <a aria-label="Sơn Son Mài Sắc — Trang chủ" class="Footer_logoLink" href="/">
          <span class="BrandMark_mark__I_sjn brand-mark" role="img" aria-label="Sơn Son Mài Sắc">
            <img src="/story-assets/brand-9782.png" alt="Logo Sơn Son Mài Sắc" width="880" height="560"/>
          </span>
        </a>
        <div class="Footer_identity__K9hsK">
          <p class="Footer_tagline__WuViG">Đi Qua Từng Đường Mài<br/>Khám Phá Giá Trị Việt</p>
        </div>
      </div>

      <!-- Mạng xã hội dạng pill sang trọng đặt ngay dưới -->
      <nav class="Footer_socials__SOcMQ" aria-label="Kết nối với Sơn Son Mài Sắc">
        <a href="https://www.facebook.com/Sonsonmaisac2026/" target="_blank" rel="noopener noreferrer">
          <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-facebook" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
          Facebook
        </a>
        <a href="https://www.tiktok.com/@sonsonmaisac.official" target="_blank" rel="noopener noreferrer">
          <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-music2" aria-hidden="true"><circle cx="8" cy="18" r="4"></circle><path d="M12 18V2l7 4"></path></svg>
          TikTok
        </a>
        <a href="https://www.threads.com/@Sonsonmaisac" target="_blank" rel="noopener noreferrer">
          Threads
        </a>
      </nav>
    </div>

    <!-- Cột 2: Khám phá -->
    <div class="Footer_navCol">
      <h3 class="Footer_colTitle">Khám phá</h3>
      <ul class="Footer_linkList">
        <li><a href="/son-mai-la-gi">Sơn mài là gì ?</a></li>
        <li><a href="/kham-pha#5-cong-doan">5 công đoạn</a></li>
        <li><a href="/trai-nghiem#simulator">Tự tạo 1 bề mặt sơn mài</a></li>
      </ul>
    </div>

    <!-- Cột 3: Câu chuyện sơn mài -->
    <div class="Footer_navCol">
      <h3 class="Footer_colTitle">Câu chuyện sơn mài</h3>
      <ul class="Footer_linkList">
        <li><a href="/cau-chuyen-son-mai#timeline-tab-0">Lịch sử</a></li>
        <li><a href="/cau-chuyen-son-mai#timeline-tab-1">Văn hoá</a></li>
        <li><a href="/cau-chuyen-son-mai#timeline-tab-3">Chất liệu</a></li>
        <li><a href="/cau-chuyen-son-mai#timeline-tab-4">Nghệ nhân</a></li>
        <li><a href="/cau-chuyen-son-mai#timeline-tab-5">Sơn mài hôm nay</a></li>
      </ul>
    </div>

    <!-- Cột 4: Tin tức sự kiện -->
    <div class="Footer_navCol">
      <h3 class="Footer_colTitle">Tin tức sự kiện</h3>
      <ul class="Footer_linkList">
        <li><a href="/tin-tuc-su-kien#upcoming-ssms">Up coming SSMS</a></li>
        <li><a href="/tin-tuc-su-kien#su-kien">Sự kiện nổi bật</a></li>
        <li><a href="/tin-tuc-su-kien#tin-son-mai">Tin sơn mài hôm nay</a></li>
      </ul>
    </div>

    <!-- Cột 5: Về Dự án -->
    <div class="Footer_navCol">
      <h3 class="Footer_colTitle">Về Dự án</h3>
      <ul class="Footer_linkList">
        <li><a href="/ve-du-an#son-son-mai-sac">Sơn Son Mài Sắc</a></li>
        <li><a href="/ve-du-an#doi-ngu">Đội ngũ</a></li>
        <li><a href="/ve-du-an#lien-he">Liên hệ</a></li>
      </ul>
    </div>

    <!-- Cột 6: Liên hệ + Đặt hình bản đồ địa chỉ Google Maps trực tiếp dưới địa chỉ -->
    <div class="Footer_navCol Footer_contactCol">
      <h3 class="Footer_colTitle">Liên hệ</h3>
      <ul class="Footer_contactList">
        <li><span>Đại diện dự án:</span> Đỗ Nguyễn Đan Lê</li>
        <li><span>Email:</span> <a href="mailto:sonsonmaisac.contact@gmail.com">sonsonmaisac.contact@gmail.com</a></li>
        <li><span>Số điện thoại:</span> <a href="tel:0963354111">0963354111</a></li>
        <li><span>Địa chỉ:</span> Trường Đại Học FPT</li>
      </ul>

      <!-- Hình bản đồ địa chỉ Google Maps đặt ngay dưới thông tin địa chỉ -->
      <a href="https://maps.app.goo.gl/YB2ycNHNqmumrPDd9" target="_blank" rel="noopener noreferrer" class="Footer_mapCard" aria-label="Xem bản đồ Trường Đại học FPT Hà Nội trên Google Maps">
        <div class="Footer_mapFrame">
          <img src="/story-assets/fpt-university-map.webp" alt="Bản đồ Trường Đại học FPT Hà Nội" width="280" height="130" loading="lazy"/>
          <div class="Footer_mapBadgeTop">
            <span>Maps</span>
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
          </div>
          <div class="Footer_mapPin">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="#d93025">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"></path>
            </svg>
            <span class="Footer_mapPinText">Trường Đại học FPT Hà Nội</span>
          </div>
          <div class="Footer_mapBadgeBottom">
            <span>Mở Google Maps ↗</span>
          </div>
        </div>
      </a>
    </div>
  </div>

  <!-- Đường kẻ phân cách -->
  <div class="Footer_divider"></div>

  <!-- Dòng dưới cùng: Bản quyền ©2026 Sơn Son Mài Sắc -->
  <div class="Footer_bottomBar">
    <p class="Footer_copyright">©2026 Sơn Son Mài Sắc</p>
  </div>
</footer>"""

INNER_FOOTER_HTML = re.search(r'<footer[^>]*>(.*?)</footer>', NEW_FOOTER_HTML, re.DOTALL).group(1).strip()

GUARDIAN_JS = r"""
(function() {
  var NEW_HTML = """ + repr(INNER_FOOTER_HTML) + r""";

  function restoreFooter() {
    var footers = document.querySelectorAll('footer');
    footers.forEach(function(f) {
      if (!f.querySelector('.Footer_mainGrid') || f.textContent.indexOf('Psharehub') !== -1 || !f.querySelector('.Footer_contactCol .Footer_mapCard')) {
        f.className = 'Footer_footer__eNA9m';
        f.innerHTML = NEW_HTML;
      }
    });
  }

  // Thực thi ngay
  restoreFooter();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', restoreFooter);
  }
  window.addEventListener('load', restoreFooter);

  // Quan sát đột biến DOM liên tục (chặn React hydration clobber)
  try {
    var obs = new MutationObserver(function() {
      var f = document.querySelector('footer');
      if (f && (!f.querySelector('.Footer_mainGrid') || f.textContent.indexOf('Psharehub') !== -1 || !f.querySelector('.Footer_contactCol .Footer_mapCard'))) {
        obs.disconnect();
        f.className = 'Footer_footer__eNA9m';
        f.innerHTML = NEW_HTML;
        if (document.body) {
          obs.observe(document.body, { childList: true, subtree: true });
        }
      }
    });

    if (document.body) {
      obs.observe(document.body, { childList: true, subtree: true });
    } else {
      document.addEventListener('DOMContentLoaded', function() {
        if (document.body) {
          obs.observe(document.body, { childList: true, subtree: true });
        }
      });
    }
  } catch(e) {}

  // Bắt router chuyển trang Next.js
  ['pushState', 'replaceState'].forEach(function(m) {
    var orig = history[m];
    if (typeof orig === 'function') {
      history[m] = function() {
        var r = orig.apply(this, arguments);
        setTimeout(restoreFooter, 0);
        setTimeout(restoreFooter, 60);
        setTimeout(restoreFooter, 200);
        return r;
      };
    }
  });
  window.addEventListener('popstate', function() {
    setTimeout(restoreFooter, 0);
    setTimeout(restoreFooter, 60);
  });
})();
"""

GUARDIAN_SCRIPT_TAG = f"<script id=\"footer-guardian\">{GUARDIAN_JS}</script>"

FOOTER_CSS = """
/* ==================== FOOTER REDESIGN (TỐI ƯU THƯƠNG HIỆU CĂN DƯỚI CHỮ SƠN SON MÀI SẮC) ==================== */
.Footer_footer__eNA9m {
  display: flex !important;
  flex-direction: column !important;
  gap: 24px !important;
  padding: 38px clamp(20px, 4vw, 56px) 26px !important;
  background: var(--site-band-surface, #f8edcf) center/cover !important;
  color: #4a2f1b !important;
  border-top: 1px solid rgba(139, 42, 42, 0.28) !important;
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  font-size: 13.5px !important;
  line-height: 1.6 !important;
  box-sizing: border-box !important;
  width: 100% !important;
}

.Footer_mainGrid {
  display: grid !important;
  grid-template-columns: minmax(210px, 1.25fr) repeat(4, minmax(110px, 0.9fr)) minmax(260px, 1.55fr) !important;
  gap: 28px 24px !important;
  align-items: start !important;
}

/* Cột 1: Thương hiệu (Khẩu hiệu và Mạng xã hội đặt gọn gàng ngay DƯỚI LOGO SƠN SON MÀI SẮC) */
.Footer_brandBlock {
  display: flex !important;
  flex-direction: column !important;
  gap: 16px !important;
}
.Footer_brandHeader {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  gap: 12px !important;
}
.Footer_logoLink {
  display: inline-block !important;
  flex-shrink: 0 !important;
  text-decoration: none !important;
}
.Footer_brandBlock .brand-mark {
  display: inline-block !important;
  height: 64px !important;
  width: auto !important;
}
.Footer_brandBlock .brand-mark img {
  height: 100% !important;
  max-height: 64px !important;
  width: auto !important;
  object-fit: contain !important;
  display: block !important;
}
.Footer_identity__K9hsK {
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
}
.Footer_tagline__WuViG {
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-weight: 600 !important;
  font-size: 16px !important;
  line-height: 1.45 !important;
  color: #7d1c1c !important;
  margin: 0 !important;
  letter-spacing: -0.01em !important;
}

/* Mạng xã hội dạng viên thuốc (pill) thanh thoát, tinh tế */
.Footer_socials__SOcMQ {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  flex-wrap: wrap !important;
  border: 0 !important;
  padding: 0 !important;
  margin-top: 4px !important;
}
.Footer_socials__SOcMQ a {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  padding: 6px 14px !important;
  border-radius: 999px !important;
  background: rgba(139, 42, 42, 0.08) !important;
  border: 1px solid rgba(139, 42, 42, 0.22) !important;
  color: #431212 !important;
  font-size: 12.5px !important;
  font-weight: 500 !important;
  text-decoration: none !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  min-height: unset !important;
}
.Footer_socials__SOcMQ a:hover {
  background: rgba(139, 42, 42, 0.16) !important;
  border-color: rgba(139, 42, 42, 0.45) !important;
  color: #8b2a2a !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 10px rgba(139, 42, 42, 0.15) !important;
}
.Footer_socials__SOcMQ a svg {
  opacity: 0.85 !important;
}

/* Các cột điều hướng */
.Footer_navCol {
  display: flex !important;
  flex-direction: column !important;
}
.Footer_colTitle {
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-weight: 700 !important;
  font-size: 15.5px !important;
  color: #3b1717 !important;
  margin: 0 0 12px 0 !important;
  letter-spacing: -0.01em !important;
}
.Footer_linkList, .Footer_contactList {
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 8.5px !important;
}
.Footer_linkList a {
  color: #5c3b28 !important;
  text-decoration: none !important;
  font-size: 13.5px !important;
  transition: color 0.18s ease, transform 0.18s ease !important;
  display: inline-block !important;
}
.Footer_linkList a:hover {
  color: #8b2a2a !important;
  text-decoration: underline !important;
  text-underline-offset: 3px !important;
  transform: translateX(2px) !important;
}

/* Cột 6: Liên hệ & Thẻ bản đồ địa chỉ Google Maps */
.Footer_contactCol {
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
}
.Footer_contactList li {
  font-size: 13px !important;
  color: #5c3b28 !important;
  line-height: 1.5 !important;
}
.Footer_contactList span {
  font-weight: 600 !important;
  color: #3b1717 !important;
}
.Footer_contactList a {
  color: #5c3b28 !important;
  text-decoration: none !important;
}
.Footer_contactList a:hover {
  color: #8b2a2a !important;
  text-decoration: underline !important;
}

/* Thẻ Bản đồ địa chỉ Google Maps đặt ngay dưới thông tin liên hệ */
.Footer_mapCard {
  display: block !important;
  text-decoration: none !important;
  color: inherit !important;
  width: 100% !important;
  max-width: 275px !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid rgba(139, 42, 42, 0.28) !important;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08) !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease !important;
  background: #fff !important;
  margin-top: 4px !important;
}
.Footer_mapCard:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 18px rgba(139, 42, 42, 0.2) !important;
}
.Footer_mapFrame {
  position: relative !important;
  width: 100% !important;
  height: 124px !important;
  overflow: hidden !important;
}
.Footer_mapFrame img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  display: block !important;
  transition: transform 0.3s ease !important;
}
.Footer_mapCard:hover .Footer_mapFrame img {
  transform: scale(1.04) !important;
}
.Footer_mapBadgeTop {
  position: absolute !important;
  top: 7px !important;
  left: 7px !important;
  background: rgba(255, 255, 255, 0.94) !important;
  backdrop-filter: blur(4px) !important;
  color: #2b1414 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  padding: 3px 8px !important;
  border-radius: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
}
.Footer_mapPin {
  position: absolute !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -60%) !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  pointer-events: none !important;
}
.Footer_mapPinText {
  font-size: 10.5px !important;
  font-weight: 700 !important;
  color: #1a1a1a !important;
  background: rgba(255, 255, 255, 0.92) !important;
  padding: 2px 6px !important;
  border-radius: 3px !important;
  margin-top: 2px !important;
  white-space: nowrap !important;
  box-shadow: 0 2px 4px rgba(0,0,0,0.12) !important;
}
.Footer_mapBadgeBottom {
  position: absolute !important;
  bottom: 7px !important;
  right: 7px !important;
  background: rgba(139, 42, 42, 0.92) !important;
  color: #fff !important;
  font-size: 10px !important;
  font-weight: 600 !important;
  padding: 3px 8px !important;
  border-radius: 4px !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
}

/* Đường phân cách */
.Footer_divider {
  width: 100% !important;
  height: 1px !important;
  background: rgba(139, 42, 42, 0.18) !important;
  margin: 4px 0 0 0 !important;
}

/* Dòng dưới cùng: Bản quyền ©2026 Sơn Son Mài Sắc */
.Footer_bottomBar {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  padding-top: 4px !important;
}
.Footer_copyright {
  color: #7a5c48 !important;
  font-size: 13px !important;
  margin: 0 !important;
}

@media (max-width: 1180px) {
  .Footer_mainGrid {
    grid-template-columns: minmax(210px, 1.25fr) repeat(3, minmax(110px, 1fr)) minmax(230px, 1.4fr) !important;
    gap: 24px 18px !important;
  }
}
@media (max-width: 860px) {
  .Footer_mainGrid {
    grid-template-columns: 1fr 1fr !important;
    gap: 24px 18px !important;
  }
}
@media (max-width: 520px) {
  .Footer_mainGrid {
    grid-template-columns: 1fr !important;
    gap: 22px !important;
  }
  .Footer_brandHeader {
    flex-direction: column !important;
    align-items: flex-start !important;
  }
}
"""

def update_css():
    css_targets = [
        os.path.join(BASE_DIR, '_next/static/css/58e70d5489b56972.css'),
        os.path.join(BASE_DIR, '_next/static/css/3d939b8161363d36.css'),
        os.path.join(BASE_DIR, 'ma_nguon_css_js/css/58e70d5489b56972.css'),
        os.path.join(BASE_DIR, 'ma_nguon_css_js/css/3d939b8161363d36.css')
    ]
    for cpath in css_targets:
        if not os.path.exists(cpath):
            continue
        with open(cpath, 'r', encoding='utf-8') as f:
            content = f.read()

        pos = content.find('/* ==================== FOOTER REDESIGN')
        if pos != -1:
            content = content[:pos]

        content = content.rstrip() + "\n\n" + FOOTER_CSS
        with open(cpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated CSS: {cpath}")

def update_layout_chunk():
    chunk_path = os.path.join(BASE_DIR, '_next/static/chunks/app/layout-885788913b392875.js')
    if os.path.exists(chunk_path):
        with open(chunk_path, 'r', encoding='utf-8') as f:
            content = f.read()

        pos = content.find('// FOOTER GUARDIAN INJECTED')
        if pos != -1:
            content = content[:pos]

        injected = "\n\n// FOOTER GUARDIAN INJECTED\n" + GUARDIAN_JS
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(content.rstrip() + injected)
        print(f"Updated layout chunk: {chunk_path}")

def update_rsc_payloads():
    rsc_dir = os.path.join(BASE_DIR, 'rsc_payloads')
    for root, _, files in os.walk(rsc_dir):
        for file in files:
            if file.endswith('.rsc'):
                fpath = os.path.join(root, file)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if 'Psharehub' in content:
                    content = content.replace('Psharehub.com', 'Sơn Son Mài Sắc')
                    content = content.replace('©2026 Psharehub.com', '©2026 Sơn Son Mài Sắc')
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated RSC payload: {fpath}")

def update_html_files():
    pages = [
        'index.html',
        'kham-pha/index.html',
        'tin-tuc-su-kien/index.html',
        've-du-an/index.html',
        'san-pham/index.html',
        'cau-chuyen-son-mai/index.html',
        'trai-nghiem/index.html',
        'trai-nghiem/hanh-trinh/index.html',
        'tu-chinh/index.html'
    ]

    footer_regex = re.compile(r'<footer\s+class="Footer_footer__eNA9m"[^>]*>.*?</footer>', re.DOTALL)
    guardian_regex = re.compile(r'<script\s+id="footer-guardian"[^>]*>.*?</script>', re.DOTALL)

    for rel in pages:
        fpath = os.path.join(BASE_DIR, rel)
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Thay thế footer tĩnh
        if footer_regex.search(content):
            content = footer_regex.sub(NEW_FOOTER_HTML, content)
        else:
            content = re.sub(r'<footer[^>]*>.*?</footer>', NEW_FOOTER_HTML, content, flags=re.DOTALL)

        # 2. Xóa guardian script cũ nếu có
        content = guardian_regex.sub('', content)

        # 3. Chèn guardian script mới ngay trước </body>
        if '</body>' in content:
            content = content.replace('</body>', f'{GUARDIAN_SCRIPT_TAG}\n</body>')
        else:
            content += f'\n{GUARDIAN_SCRIPT_TAG}'

        # 4. Cập nhật version query string lên v=18
        content = re.sub(r'58e70d5489b56972\.css\?v=\d+', '58e70d5489b56972.css?v=18', content)
        content = re.sub(r'3d939b8161363d36\.css\?v=\d+', '3d939b8161363d36.css?v=18', content)
        if '58e70d5489b56972.css' in content and '58e70d5489b56972.css?v=' not in content:
            content = content.replace('58e70d5489b56972.css', '58e70d5489b56972.css?v=18')

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated HTML: {fpath}")

if __name__ == '__main__':
    update_css()
    update_layout_chunk()
    update_rsc_payloads()
    update_html_files()
    print("DONE! Footer brand optimized underneath Sơn Son Mài Sắc.")
