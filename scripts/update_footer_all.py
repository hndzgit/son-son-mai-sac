#!/usr/bin/env python3
import os
import re

NEW_FOOTER_HTML = '''<footer class="Footer_footer__eNA9m">
  <div class="Footer_mainGrid">
    <!-- Brand / Identity -->
    <div class="Footer_brandBlock">
      <a aria-label="Sơn Son Mài Sắc — Trang chủ" class="Footer_logoLink" href="/">
        <span class="BrandMark_mark__I_sjn brand-mark" role="img" aria-label="Sơn Son Mài Sắc">
          <img src="/story-assets/brand-9782.png" alt="Logo Sơn Son Mài Sắc" width="880" height="560"/>
        </span>
      </a>
      <div class="Footer_identity__K9hsK">
        <p class="Footer_tagline__WuViG">Đi Qua Từng Đường Mài<br/>Khám Phá Giá Trị Việt</p>
      </div>
    </div>

    <!-- Cột 1: Khám phá -->
    <div class="Footer_navCol">
      <h3 class="Footer_colTitle">Khám phá</h3>
      <ul class="Footer_linkList">
        <li><a href="/kham-pha#son-mai-la-gi">Sơn mài là gì ?</a></li>
        <li><a href="/kham-pha#5-cong-doan">5 công đoạn</a></li>
        <li><a href="/trai-nghiem#simulator">Tự tạo 1 bề mặt sơn mài</a></li>
      </ul>
    </div>

    <!-- Cột 2: Câu chuyện sơn mài -->
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

    <!-- Cột 3: Tin tức sự kiện -->
    <div class="Footer_navCol">
      <h3 class="Footer_colTitle">Tin tức sự kiện</h3>
      <ul class="Footer_linkList">
        <li><a href="/tin-tuc-su-kien#upcoming-ssms">Up coming SSMS</a></li>
        <li><a href="/tin-tuc-su-kien#su-kien">Sự kiện nổi bật</a></li>
        <li><a href="/tin-tuc-su-kien#tin-son-mai">Tin sơn mài hôm nay</a></li>
      </ul>
    </div>

    <!-- Cột 4: Về Dự án -->
    <div class="Footer_navCol">
      <h3 class="Footer_colTitle">Về Dự án</h3>
      <ul class="Footer_linkList">
        <li><a href="/ve-du-an#son-son-mai-sac">Sơn Son Mài Sắc</a></li>
        <li><a href="/ve-du-an#doi-ngu">Đội ngũ</a></li>
        <li><a href="/ve-du-an#lien-he">Liên hệ</a></li>
      </ul>
    </div>

    <!-- Cột 5: Liên hệ -->
    <div class="Footer_navCol Footer_contactCol">
      <h3 class="Footer_colTitle">Liên hệ</h3>
      <ul class="Footer_contactList">
        <li><span>Đại diện dự án:</span> Đỗ Nguyễn Đan Lê</li>
        <li><span>Email:</span> <a href="mailto:sonsonmaisac.contact@gmail.com">sonsonmaisac.contact@gmail.com</a></li>
        <li><span>Số điện thoại:</span> <a href="tel:0963354111">0963354111</a></li>
        <li><span>Địa chỉ:</span> Trường Đại Học FPT</li>
      </ul>
    </div>
  </div>

  <!-- Đường kẻ phân cách -->
  <div class="Footer_divider"></div>

  <!-- Bottom Bar: Socials + Copyright bên trái, Map bên phải -->
  <div class="Footer_bottomBar">
    <div class="Footer_bottomLeft">
      <nav class="Footer_socials__SOcMQ" aria-label="Kết nối với Sơn Son Mài Sắc">
        <a href="https://www.facebook.com/Sonsonmaisac2026/" target="_blank" rel="noopener noreferrer">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-facebook" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
          Facebook ↗
        </a>
        <a href="https://www.tiktok.com/@sonsonmaisac.official" target="_blank" rel="noopener noreferrer">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-music2" aria-hidden="true"><circle cx="8" cy="18" r="4"></circle><path d="M12 18V2l7 4"></path></svg>
          TikTok ↗
        </a>
        <a href="https://www.threads.com/@Sonsonmaisac" target="_blank" rel="noopener noreferrer">
          Threads ↗
        </a>
      </nav>
      <p class="Footer_copyright">©2026 Sơn Son Mài Sắc</p>
    </div>

    <!-- Hình bản đồ địa chỉ (Click mở Google Maps) -->
    <a href="https://maps.app.goo.gl/YB2ycNHNqmumrPDd9" target="_blank" rel="noopener noreferrer" class="Footer_mapCard" aria-label="Xem bản đồ Trường Đại học FPT Hà Nội trên Google Maps">
      <div class="Footer_mapFrame">
        <img src="/story-assets/fpt-university-map.webp" alt="Bản đồ Trường Đại học FPT Hà Nội" width="280" height="130" loading="lazy" />
        <div class="Footer_mapBadgeTop">
          <span>Maps</span>
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
        </div>
        <div class="Footer_mapPin">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="#d93025">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
          </svg>
          <span class="Footer_mapPinText">Trường Đại học FPT Hà Nội</span>
        </div>
        <div class="Footer_mapBadgeBottom">
          <span>Mở Google Maps ↗</span>
        </div>
      </div>
    </a>
  </div>
</footer>'''

FOOTER_CSS = '''
/* ==================== FOOTER REDESIGN ==================== */
.Footer_footer__eNA9m {
  display: flex !important;
  flex-direction: column !important;
  gap: 28px !important;
  padding: 44px clamp(20px, 4.5vw, 68px) 32px !important;
  background: var(--site-band-surface, #f8edcf) center/cover !important;
  color: #4a2f1b !important;
  border-top: 1px solid rgba(139, 42, 42, 0.28) !important;
  font-family: Inter, Arial, sans-serif !important;
  font-size: 13.5px !important;
  line-height: 1.6 !important;
}

.Footer_mainGrid {
  display: grid !important;
  grid-template-columns: minmax(210px, 1.35fr) repeat(4, minmax(120px, 1fr)) minmax(220px, 1.3fr) !important;
  gap: 28px 24px !important;
  align-items: start !important;
}

/* Brand Block */
.Footer_brandBlock {
  display: flex !important;
  flex-direction: column !important;
  gap: 14px !important;
}
.Footer_logoLink {
  display: inline-block !important;
}
.Footer_brandBlock .brand-mark {
  height: clamp(62px, 5.5vw, 84px) !important;
  width: auto !important;
}
.Footer_brandBlock .brand-mark img {
  height: 100% !important;
  width: auto !important;
  object-fit: contain !important;
}
.Footer_tagline__WuViG {
  font-family: "Project Display", "Playfair Display", Georgia, serif !important;
  font-weight: 600 !important;
  font-size: clamp(16px, 1.3vw, 19px) !important;
  line-height: 1.4 !important;
  color: #8b2a2a !important;
  margin: 0 !important;
  letter-spacing: -0.01em !important;
}

/* Nav Columns */
.Footer_navCol {
  display: flex !important;
  flex-direction: column !important;
}
.Footer_colTitle {
  font-family: "Project Display", "Playfair Display", Georgia, serif !important;
  font-weight: 700 !important;
  font-size: 15.5px !important;
  color: #3b1717 !important;
  margin: 0 0 14px 0 !important;
  letter-spacing: -0.01em !important;
}
.Footer_linkList, .Footer_contactList {
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 9px !important;
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

/* Contact List */
.Footer_contactList li {
  font-size: 13px !important;
  color: #5c3b28 !important;
  line-height: 1.55 !important;
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

/* Divider */
.Footer_divider {
  width: 100% !important;
  height: 1px !important;
  background: rgba(139, 42, 42, 0.18) !important;
}

/* Bottom Bar */
.Footer_bottomBar {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 20px !important;
  flex-wrap: wrap !important;
}
.Footer_bottomLeft {
  display: flex !important;
  flex-direction: column !important;
  gap: 10px !important;
}
.Footer_socials__SOcMQ {
  display: flex !important;
  align-items: center !important;
  gap: 18px !important;
  flex-wrap: wrap !important;
  border: 0 !important;
  padding: 0 !important;
}
.Footer_socials__SOcMQ a {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  color: #5c3b28 !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  text-decoration: none !important;
  transition: color 0.18s ease !important;
  min-height: unset !important;
}
.Footer_socials__SOcMQ a:hover {
  color: #8b2a2a !important;
  text-decoration: underline !important;
}
.Footer_copyright {
  color: #7a5c48 !important;
  font-size: 12.5px !important;
  margin: 0 !important;
}

/* Map Card */
.Footer_mapCard {
  display: block !important;
  text-decoration: none !important;
  color: inherit !important;
  width: 290px !important;
  max-width: 100% !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid rgba(139, 42, 42, 0.28) !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08) !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease !important;
  background: #fff !important;
}
.Footer_mapCard:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 18px rgba(139, 42, 42, 0.2) !important;
}
.Footer_mapFrame {
  position: relative !important;
  width: 100% !important;
  height: 128px !important;
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
  top: 8px !important;
  left: 8px !important;
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
  box-shadow: 0 2px 6px rgba(0,0,0,0.12) !important;
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
  background: rgba(255, 255, 255, 0.96) !important;
  color: #1a0f0a !important;
  font-size: 10.5px !important;
  font-weight: 600 !important;
  padding: 2px 6px !important;
  border-radius: 3px !important;
  white-space: nowrap !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.18) !important;
  margin-top: -3px !important;
  border: 1px solid rgba(0,0,0,0.06) !important;
}
.Footer_mapBadgeBottom {
  position: absolute !important;
  bottom: 8px !important;
  right: 8px !important;
  background: rgba(139, 42, 42, 0.92) !important;
  color: #fff8ec !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  padding: 3px 8px !important;
  border-radius: 4px !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
}

/* Responsive */
@media (max-width: 1080px) {
  .Footer_mainGrid {
    grid-template-columns: repeat(3, 1fr) !important;
  }
}
@media (max-width: 640px) {
  .Footer_mainGrid {
    grid-template-columns: 1fr !important;
  }
  .Footer_bottomBar {
    flex-direction: column !important;
    align-items: flex-start !important;
  }
  .Footer_mapCard {
    width: 100% !important;
  }
}
'''

def update_css():
    css_files = [
        '_next/static/css/58e70d5489b56972.css',
        'ma_nguon_css_js/css/58e70d5489b56972.css'
    ]
    for p in css_files:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
            if '/* ==================== FOOTER REDESIGN ==================== */' not in content:
                content += FOOTER_CSS
            else:
                # Update existing rule
                content = re.sub(r'/\* ==================== FOOTER REDESIGN ==================== \*/[\s\S]*$', FOOTER_CSS.strip(), content)
            with open(p, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated CSS in {p}")

def update_html():
    html_files = [
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

    for p in html_files:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace footer
            pat = r'<footer class="Footer_footer__eNA9m">.*?</footer>'
            if re.search(pat, content, flags=re.DOTALL):
                content = re.sub(pat, NEW_FOOTER_HTML, content, flags=re.DOTALL)
                # Bump version to v=6
                content = re.sub(r'58e70d5489b56972\.css(?:\?v=\d+)?', '58e70d5489b56972.css?v=6', content)
                content = re.sub(r'3d939b8161363d36\.css(?:\?v=\d+)?', '3d939b8161363d36.css?v=6', content)
                content = re.sub(r'369-2063549c42145b16\.js(?:\?v=\d+)?', '369-2063549c42145b16.js?v=6', content)

                with open(p, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated Footer in {p}")
            else:
                print(f"Footer pattern not found in {p}")

if __name__ == '__main__':
    update_css()
    update_html()
    print("All footer updates finished!")
