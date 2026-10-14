# -*- coding: utf-8 -*-
"""
Trình tạo trang đọc bài viết chuyên biệt (Editorial Reader)
Chuẩn giao diện báo chí mỹ thuật Việt Nam theo yêu cầu người dùng (như Image 2)
"""
import os
import json
import html

BASE_DIR = "/Users/hoainam/Documents/Sơn son mài sắc"
MILESTONES_FILE = os.path.join(BASE_DIR, "scripts/milestones_data.json")

with open(MILESTONES_FILE, "r", encoding="utf-8") as f:
    milestones_raw = json.load(f)

# Bổ sung thông tin huy hiệu bảo tàng, trích dẫn nổi bật và chú thích tranh
METADATA = [
    {
        "id": 0,
        "kicker": "KỲ 01 / 06 · ĐỜI SỐNG & TÍN NGƯỠNG",
        "era": "TRƯỚC HỘI HỌA",
        "badge_org": "BẢO TÀNG LỊCH SỬ QUỐC GIA",
        "badge_sub": "Vietnam National Museum of History",
        "caption": "Hộp gỗ sơn khắc hoa văn & Ngai thờ thếp vàng thời Lê – Nguyễn lưu giữ tại Bảo tàng Lịch sử Quốc gia",
        "pull_quote": "Thưởng thức sơn mài vì thế không chỉ là nhìn một hình ảnh. Đó còn là nhìn cách thời gian, vật liệu và bàn tay con người được giữ lại trên bề mặt.",
        "read_time": "4 phút đọc"
    },
    {
        "id": 1,
        "kicker": "KỲ 02 / 06 · NGHỀ THỦ CÔNG",
        "era": "TRI THỨC QUA THẾ HỆ",
        "badge_org": "KỸ NGHỆ SƠN TA TRUYỀN THỐNG",
        "badge_sub": "Tri thức lưu truyền qua các thế hệ nghệ nhân",
        "caption": "Bức hoành phi cổ sơn son thếp vàng – Nơi hội tụ tinh hoa chạm khắc và kỹ nghệ phủ sơn truyền thống Việt Nam",
        "pull_quote": "Mỗi lớp là một thời điểm. Mỗi lần phủ là một lần hình ảnh thay đổi. Mỗi lần mài là một lần quá khứ của bề mặt được gọi trở lại.",
        "read_time": "4 phút đọc"
    },
    {
        "id": 2,
        "kicker": "KỲ 03 / 06 · MỸ THUẬT ĐÔNG DƯƠNG",
        "era": "BƯỚC NGOẶT 1925",
        "badge_org": "TRƯỜNG CAO ĐẲNG MỸ THUẬT ĐÔNG DƯƠNG",
        "badge_sub": "Tư liệu lưu trữ lịch sử thành lập năm 1925 tại Hà Nội",
        "caption": "Tòa nhà Trường Mỹ thuật Đông Dương tại Hà Nội – Cuộc gặp gỡ lịch sử giữa chất liệu sơn ta bản địa và ngôn ngữ tạo hình hiện đại",
        "pull_quote": "Nếu mài vốn là một bước xử lý bề mặt, liệu người nghệ sĩ có thể dùng chính việc mài để tạo nên hình ảnh? Những câu hỏi ấy mở ra một giai đoạn thử nghiệm đầy tính khám phá.",
        "read_time": "3 phút đọc"
    },
    {
        "id": 3,
        "kicker": "KỲ 04 / 06 · NGHỆ THUẬT HIỆN ĐẠI",
        "era": "THẾ KỶ XX",
        "badge_org": "HỘI HỌA SƠN MÀI TIÊN PHONG",
        "badge_sub": "Kiệt tác Les Fées (1936) · Bộ sưu tập Géraldine Galateau, Paris",
        "caption": "Nguyễn Gia Trí – Kiệt tác \"Les Fées\" (Các nàng tiên, c. 1936), Sơn mài trên vóc, 290 × 440 cm",
        "pull_quote": "Hình ảnh sơn mài từ đó được tạo nên bằng một cách rất đặc biệt: vừa thêm vào, vừa lấy đi. Bề mặt sơn mài từ đây không còn chỉ là một bề mặt. Nó trở thành một không gian được xây dựng theo chiều sâu.",
        "read_time": "7 phút đọc"
    },
    {
        "id": 4,
        "kicker": "KỲ 05 / 06 · LÀNG NGHỀ",
        "era": "TRUYỀN NGHỀ",
        "badge_org": "LÀNG NGHỀ SƠN MÀI HẠ THÁI",
        "badge_sub": "Thường Tín, Hà Nội · Đất tổ nghề sơn truyền thống",
        "caption": "Nghệ nhân làng nghề Hạ Thái miệt mài thực hiện từng nét vẽ và lớp sơn tỉ mỉ trên vóc truyền thống",
        "pull_quote": "Một người mang kinh nghiệm của nghề truyền thống bước vào môi trường mỹ thuật. Tại đó, kỹ thuật gặp những thử nghiệm mới. Những điều được học hỏi và phát triển lại quay trở về làng nghề.",
        "read_time": "3 phút đọc"
    },
    {
        "id": 5,
        "kicker": "KỲ 06 / 06 · VƯƠN RA THẾ GIỚI",
        "era": "ĐƯƠNG ĐẠI",
        "badge_org": "SƠN MÀI ĐƯƠNG ĐẠI & QUỐC TẾ",
        "badge_sub": "Không gian nghệ thuật & Đối thoại đương đại",
        "caption": "Không gian trưng bày tác phẩm sơn mài tại triển lãm đương đại – Mở rộng không gian ba chiều và đối thoại đa chất liệu",
        "pull_quote": "Câu chuyện của sơn mài Việt Nam chưa thật sự có một đoạn kết. Nó vẫn đang được viết bằng cách mỗi thế hệ tiếp tục thêm một lớp của mình lên những lớp đã có từ trước.",
        "read_time": "6 phút đọc"
    }
]

ARTICLES = []
for idx, m in enumerate(milestones_raw):
    meta = METADATA[idx]
    ARTICLES.append({
        "id": idx,
        "slug": m.get("slug", f"moc-{idx+1}"),
        "title": m.get("title", ""),
        "heading": m.get("heading", ""),
        "date": m.get("date", meta["era"]),
        "kicker": meta["kicker"],
        "badge_org": meta["badge_org"],
        "badge_sub": meta["badge_sub"],
        "image": f"/story-assets/{m.get('image', 'flow-11')}.jpg",
        "caption": meta["caption"],
        "pull_quote": meta["pull_quote"],
        "read_time": meta["read_time"],
        "paragraphs": m.get("fullContent", [])
    })

# Đọc Navbar và Footer từ cau-chuyen-son-mai/index.html
with open(os.path.join(BASE_DIR, "cau-chuyen-son-mai/index.html"), "r", encoding="utf-8") as f:
    orig_html = f.read()

h_start = orig_html.find('<header class="Navbar_header')
h_end = orig_html.find('</header>') + len('</header>')
NAVBAR_HTML = orig_html[h_start:h_end]

f_start = orig_html.find('<footer class="Footer_footer')
f_end = orig_html.find('</footer>') + len('</footer>')
FOOTER_HTML = orig_html[f_start:f_end]

CSS_STYLES = """
/* ===== EDITORIAL NEWSPAPER READER STYLES ===== */
:root {
  --reader-paper: #faf4e9;
  --reader-ink: #1e1711;
  --reader-secondary: #574637;
  --reader-accent: #8c0e0e;
  --reader-gold: #c59b48;
  --reader-border: rgba(160, 130, 80, 0.22);
}

/* Thanh tiến độ đọc */
#reading-progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  width: 0%;
  background: linear-gradient(90deg, #8c0e0e 0%, #d4a757 100%);
  z-index: 9999;
  transition: width 0.1s ease-out;
}

/* Bố cục trang bài viết */
.reader-page-wrapper {
  background: var(--site-paper-surface, linear-gradient(#fff3d4ad, #fff3d4ad), url(/story-assets/backgrounds/gold-foundation-v2.webp)) center / 600px 600px repeat !important;
  min-height: 100vh;
  padding: clamp(24px, 4vw, 56px) max(4vw, 20px) 90px;
  color: var(--reader-ink);
}

/* Thanh điều hướng nhanh phía trên */
.reader-top-bar {
  max-width: 900px;
  margin: 0 auto 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  padding: 12px 20px;
  background: rgba(250, 244, 233, 0.96);
  backdrop-filter: blur(8px);
  border: 1px solid var(--reader-border);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.03);
}

.reader-back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--reader-accent);
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  transition: transform 0.2s ease, color 0.2s ease;
}

.reader-back-btn:hover {
  transform: translateX(-3px);
  color: #630808;
}

.reader-tools {
  display: flex;
  align-items: center;
  gap: 12px;
}

.reader-tool-btn {
  background: transparent;
  border: 1px solid var(--reader-border);
  color: var(--reader-secondary);
  font-size: 12px;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reader-tool-btn:hover {
  background: #fdf5e2;
  border-color: var(--reader-gold);
  color: var(--reader-accent);
}

/* Ruy băng chuyển mốc 6 bài viết (Milestone Switcher Ribbon) */
.milestone-switcher {
  max-width: 900px;
  margin: 0 auto 32px;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
  background: rgba(250, 244, 233, 0.95);
  padding: 8px;
  border: 1px solid var(--reader-border);
  border-radius: 8px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.04);
}

.milestone-tab {
  background: transparent;
  border: 1px solid transparent;
  padding: 10px 6px;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  transition: all 0.22s ease;
  color: #554433;
}

.milestone-tab .m-num {
  display: block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #8c0e0e;
  margin-bottom: 2px;
}

.milestone-tab .m-name {
  display: block;
  font-size: 12px;
  line-height: 1.25;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.milestone-tab:hover {
  background: rgba(140, 14, 14, 0.06);
  border-color: rgba(140, 14, 14, 0.2);
}

.milestone-tab.active {
  background: #8c0e0e;
  color: #fff4d9;
  border-color: #8c0e0e;
  box-shadow: 0 4px 12px rgba(140, 14, 14, 0.25);
}

.milestone-tab.active .m-num {
  color: #ffde8a;
}

/* Khung bài viết dạng báo chí / Editorial Paper Card */
.newspaper-card {
  max-width: 860px;
  margin: 0 auto 48px;
  background: var(--reader-paper);
  border: 1px solid var(--reader-border);
  border-top: 5px solid var(--reader-accent);
  border-radius: 3px;
  padding: clamp(32px, 6vw, 68px) clamp(24px, 5.5vw, 64px);
  box-shadow: 0 16px 50px rgba(35, 20, 10, 0.08);
  transition: opacity 0.25s ease;
}

.newspaper-card.fading {
  opacity: 0.35;
}

/* Đầu trang báo chí */
.article-header {
  text-align: center;
  margin-bottom: 32px;
  border-bottom: 1px solid var(--reader-border);
  padding-bottom: 24px;
}

.article-kicker {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--reader-accent);
  background: #fbf0ec;
  padding: 4px 14px;
  border-radius: 999px;
  border: 1px solid rgba(140, 14, 14, 0.18);
  margin-bottom: 16px;
}

.article-title {
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-size: clamp(30px, 4.2vw, 46px) !important;
  line-height: 1.18 !important;
  font-weight: 700 !important;
  color: #170e08 !important;
  margin: 0 0 14px 0 !important;
  text-wrap: balance;
}

.article-subtitle {
  font-family: "Noto Serif", Georgia, serif;
  font-size: clamp(16px, 1.4vw, 19px);
  font-style: italic;
  line-height: 1.6;
  color: #63503e;
  margin: 0 0 18px 0;
  max-width: 720px;
  margin-inline: auto;
}

.article-meta-row {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 18px;
  font-size: 13px;
  color: #796653;
  margin-top: 14px;
}

.article-meta-row span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

/* Khung hiện vật tư liệu (Ảnh + Huy hiệu bảo tàng như Image 2) */
.artifact-showcase {
  text-align: center;
  margin: 0 auto 36px;
  background: #f4ecdc;
  border: 1px solid rgba(160, 130, 80, 0.28);
  border-radius: 4px;
  padding: 24px 20px 20px;
}

.artifact-image-frame {
  max-width: 100%;
  margin: 0 auto 16px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.artifact-image-frame img {
  max-height: 440px;
  width: auto;
  max-width: 100%;
  object-fit: contain;
  border-radius: 3px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.06);
}

/* Huy hiệu bảo tàng / Đơn vị tư liệu chuẩn Image 2 */
.museum-badge {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 8px 18px;
  background: #fffdf8;
  border: 1px solid rgba(160, 130, 80, 0.32);
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.museum-emblem {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.museum-info {
  text-align: left;
}

.museum-org {
  display: block;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #a87922;
  line-height: 1.25;
}

.museum-sub {
  display: block;
  font-size: 11px;
  color: #75624e;
  line-height: 1.25;
}

.museum-tick {
  width: 2px;
  height: 20px;
  background: #c59b48;
  margin: 16px auto 8px;
}

.artifact-caption {
  font-size: 13px;
  font-style: italic;
  color: #725f4b;
  margin: 6px 0 0 0;
  line-height: 1.5;
}

/* Thân bài viết đọc báo (Article Body) */
.article-body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 18px;
  line-height: 1.9;
  color: var(--reader-ink);
  letter-spacing: -0.01em;
}

.article-body p {
  margin: 0 0 24px 0;
  text-align: justify;
}

/* Drop-cap chữ cái đầu tiên phong cách tạp chí cổ điển */
.article-body p:first-of-type::first-letter {
  font-family: "Project Display", "Playfair Display", Georgia, serif;
  float: left;
  font-size: 56px;
  line-height: 48px;
  padding-top: 4px;
  padding-right: 12px;
  padding-bottom: 2px;
  color: var(--reader-accent);
  font-weight: 700;
}

/* Khối trích dẫn nổi bật (Pull Quote) */
.editorial-pullquote {
  position: relative;
  margin: 36px 0;
  padding: 22px 28px;
  background: #f1e4c9;
  border: 1px solid rgba(160, 130, 80, 0.25);
  border-left: 4px solid var(--reader-accent);
  border-radius: 0 6px 6px 0;
}

.editorial-pullquote p {
  font-family: "Noto Serif", Georgia, serif !important;
  font-size: clamp(18px, 1.6vw, 22px) !important;
  font-style: italic !important;
  line-height: 1.65 !important;
  color: #721619 !important;
  margin: 0 !important;
  text-align: left !important;
}

/* Hoa văn kết thúc bài viết */
.article-endmark {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin: 40px 0 28px;
  color: var(--reader-gold);
}

.article-endmark::before,
.article-endmark::after {
  content: "";
  height: 1px;
  width: 60px;
  background: var(--reader-border);
}

/* Điều hướng Mốc trước / Mốc sau */
.article-pager {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--reader-border);
}

.pager-btn {
  display: flex;
  flex-direction: column;
  padding: 16px 20px;
  background: #f5eedf;
  border: 1px solid var(--reader-border);
  border-radius: 6px;
  text-decoration: none;
  color: var(--reader-ink);
  transition: all 0.25s ease;
}

.pager-btn:hover {
  background: #eedebd;
  border-color: var(--reader-gold);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}

.pager-btn.prev {
  text-align: left;
}

.pager-btn.next {
  text-align: right;
}

.pager-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--reader-accent);
  margin-bottom: 4px;
}

.pager-title {
  font-family: "Project Display", "Playfair Display", Georgia, serif;
  font-size: 15px;
  font-weight: 600;
  line-height: 1.35;
}

.pager-btn:disabled,
.pager-btn.disabled {
  opacity: 0.35;
  pointer-events: none;
}

/* Khối hành động cuối trang */
.reader-bottom-actions {
  max-width: 860px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 14px;
}

.reader-bottom-actions .btn {
  font-size: 13px;
  padding: 12px 24px;
}

/* Toast sao chép */
#copy-toast {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%) translateY(100px);
  background: #1a0f07;
  color: #fff4d9;
  border: 1px solid var(--reader-gold);
  padding: 12px 24px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 500;
  z-index: 10000;
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

#copy-toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* Responsive cho thiết bị di động */
@media (max-width: 768px) {
  .milestone-switcher {
    grid-template-columns: repeat(3, 1fr);
  }
  .article-pager {
    grid-template-columns: 1fr;
  }
  .article-body {
    font-size: 16.5px;
    line-height: 1.85;
  }
  .article-body p {
    text-align: left;
  }
  .newspaper-card {
    padding: 28px 18px;
  }
}

@media (max-width: 480px) {
  .milestone-switcher {
    grid-template-columns: repeat(2, 1fr);
  }
  .reader-top-bar {
    flex-direction: column;
    align-items: flex-start;
  }
}
"""

def render_article_html(article_idx):
    art = ARTICLES[article_idx]
    prev_idx = article_idx - 1 if article_idx > 0 else None
    next_idx = article_idx + 1 if article_idx < len(ARTICLES) - 1 else None

    # Tạo các thẻ paragraphs
    paras_html = ""
    for idx, p_text in enumerate(art["paragraphs"]):
        paras_html += f'<p>{html.escape(p_text)}</p>\n'
        # Chèn trích dẫn sau đoạn 2 hoặc đoạn 3
        if idx == 1 and art["pull_quote"]:
            paras_html += f'''
            <blockquote class="editorial-pullquote">
              <p>“{html.escape(art["pull_quote"])}”</p>
            </blockquote>
            '''

    # Các nút chuyển mốc ribbon
    tabs_html = ""
    for i, a in enumerate(ARTICLES):
        active_cls = "active" if i == article_idx else ""
        tabs_html += f'''
        <a href="/cau-chuyen-son-mai/bai-viet/{i+1}" class="milestone-tab {active_cls}" data-id="{i}" onclick="switchArticle({i}, true); return false;">
          <span class="m-num">0{i+1}</span>
          <span class="m-name">{html.escape(a["title"])}</span>
        </a>
        '''

    # Pager nút trước/sau
    if prev_idx is not None:
        prev_btn = f'''
        <a href="/cau-chuyen-son-mai/bai-viet/{prev_idx+1}" class="pager-btn prev" onclick="switchArticle({prev_idx}, true); return false;">
          <span class="pager-label">← Mốc trước (0{prev_idx+1})</span>
          <span class="pager-title">{html.escape(ARTICLES[prev_idx]["title"])}</span>
        </a>
        '''
    else:
        prev_btn = '<div class="pager-btn prev disabled"><span class="pager-label">Khởi đầu</span><span class="pager-title">Đầu dòng thời gian</span></div>'

    if next_idx is not None:
        next_btn = f'''
        <a href="/cau-chuyen-son-mai/bai-viet/{next_idx+1}" class="pager-btn next" onclick="switchArticle({next_idx}, true); return false;">
          <span class="pager-label">Mốc tiếp theo (0{next_idx+1}) →</span>
          <span class="pager-title">{html.escape(ARTICLES[next_idx]["title"])}</span>
        </a>
        '''
    else:
        next_btn = '<div class="pager-btn next disabled"><span class="pager-label">Tiếp nối</span><span class="pager-title">Hiện tại & Tương lai</span></div>'

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charSet="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{html.escape(art['title'])}: {html.escape(art['heading'])} | Câu chuyện sơn mài</title>
  <meta name="description" content="Đọc chuyên sâu tư liệu dòng thời gian sơn mài: {html.escape(art['heading'])}. Dự án Sơn Son Mài Sắc."/>
  
  <link rel="stylesheet" href="/_next/static/css/58e70d5489b56972.css?v=19"/>
  <link rel="stylesheet" href="/_next/static/css/3d939b8161363d36.css?v=19"/>
  <link rel="stylesheet" href="/_next/static/css/e133a03ebd4e8d3a.css"/>

  <link rel="shortcut icon" href="/favicon.svg" type="image/svg+xml"/>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" type="image/png" sizes="180x180"/>

  <style>
{CSS_STYLES}
  </style>
</head>
<body class="min-h-screen flex flex-col font-sans">
  <div id="reading-progress-bar"></div>
  <a href="#article-content" class="skip-link">Bỏ qua điều hướng</a>

  {NAVBAR_HTML}

  <main id="main-content" class="flex-1 main-content" style="padding-top: 88px;">
    <div class="reader-page-wrapper">
      
      <!-- Thanh điều hướng và tiện ích đọc -->
      <div class="reader-top-bar">
        <a id="btn-back-timeline" href="/cau-chuyen-son-mai#timeline-tab-{article_idx}" class="reader-back-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
          Quay lại Câu chuyện sơn mài
        </a>

        <div class="reader-tools">
          <button type="button" class="reader-tool-btn" onclick="adjustFontSize(-1)" title="Giảm cỡ chữ">A-</button>
          <button type="button" class="reader-tool-btn" onclick="adjustFontSize(1)" title="Tăng cỡ chữ">A+</button>
          <button type="button" class="reader-tool-btn" onclick="copyArticleLink()" title="Sao chép liên kết">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block; vertical-align:-2px; margin-right:4px;"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            Chia sẻ
          </button>
          <span id="art-readtime" style="font-size: 12px; color: #796653;">⏱ {art['read_time']}</span>
        </div>
      </div>

      <!-- Ruy băng chuyển đổi nhanh 6 mốc -->
      <nav class="milestone-switcher" aria-label="Chọn mốc thời gian">
        {tabs_html}
      </nav>

      <!-- Khung bài viết dạng báo chí mỹ thuật -->
      <article class="newspaper-card" id="article-content">
        <header class="article-header">
          <span class="article-kicker" id="art-kicker">{html.escape(art['kicker'])}</span>
          <h1 class="article-title" id="art-heading">{html.escape(art['heading'])}</h1>
          <p class="article-subtitle" id="art-subtitle">{html.escape(art['title'])} · Tư liệu theo mạch lịch sử và đời sống di sản</p>
          
          <div class="article-meta-row">
            <span>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              Sơn Son Mài Sắc Biên Soạn
            </span>
            <span>·</span>
            <span id="art-badge-name">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
              <span id="art-date-val">Giai đoạn: {html.escape(art['date'])}</span>
            </span>
            <span>·</span>
            <span>Tư liệu bảo tồn di sản</span>
          </div>
        </header>

        <!-- Khung ảnh hiện vật tư liệu & Huy hiệu bảo tàng -->
        <div class="artifact-showcase" id="art-showcase">
          <div class="artifact-image-frame">
            <img id="art-img" src="{art['image']}" alt="{html.escape(art['title'])}" loading="eager"/>
          </div>

          <div class="museum-badge" id="art-badge">
            <div class="museum-emblem">
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="11" fill="#8c0e0e"/>
                <path d="M12 4L6 8v2h12V8l-6-4zM7 11v6h2v-6H7zm4 0v6h2v-6h-2zm4 0v6h2v-6h-2zM5 18v2h14v-2H5z" fill="#f6d37a"/>
              </svg>
            </div>
            <div class="museum-info">
              <strong class="museum-org" id="art-badge-org">{html.escape(art['badge_org'])}</strong>
              <span class="museum-sub" id="art-badge-sub">{html.escape(art['badge_sub'])}</span>
            </div>
          </div>

          <div class="museum-tick"></div>

          <p class="artifact-caption" id="art-caption">{html.escape(art['caption'])}</p>
        </div>

        <!-- Thân bài viết đọc báo -->
        <div class="article-body" id="art-body">
          {paras_html}
        </div>

        <!-- Dấu kết thúc bài viết -->
        <div class="article-endmark">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z"/>
          </svg>
        </div>

        <!-- Phân trang mốc trước / mốc sau -->
        <footer class="article-pager" id="art-pager">
          {prev_btn}
          {next_btn}
        </footer>
      </article>

      <!-- Các liên kết chuyển tiếp cuối trang -->
      <div class="reader-bottom-actions">
        <a id="btn-bottom-back" class="btn outline" href="/cau-chuyen-son-mai#timeline-tab-{article_idx}">
          ← Quay lại Câu chuyện sơn mài
        </a>
        <a class="btn red" href="/kham-pha#5-cong-doan">
          Khám phá 5 công đoạn sơn mài →
        </a>
        <a class="btn outline" href="/trai-nghiem#simulator">
          Tự tạo một bề mặt sơn mài 3D →
        </a>
      </div>

    </div>
  </main>

  {FOOTER_HTML}

  <div id="copy-toast">Đã sao chép liên kết bài viết!</div>

  <!-- Dữ liệu bài viết để client chuyển mốc tức thì không cần tải lại trang -->
  <script id="articles-json" type="application/json">
{json.dumps(ARTICLES, ensure_ascii=False)}
  </script>

  <script>
    const articlesData = JSON.parse(document.getElementById('articles-json').textContent);
    let currentArticleId = {article_idx};
    let currentFontSize = 18;

    // Cập nhật thanh tiến độ đọc
    window.addEventListener('scroll', () => {{
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (winScroll / height) * 100;
      const bar = document.getElementById('reading-progress-bar');
      if (bar) bar.style.width = scrolled + '%';
    }});

    // Chuyển đổi cỡ chữ
    function adjustFontSize(delta) {{
      currentFontSize = Math.min(24, Math.max(15, currentFontSize + delta));
      const bodyEl = document.getElementById('art-body');
      if (bodyEl) bodyEl.style.fontSize = currentFontSize + 'px';
    }}

    // Sao chép liên kết
    function copyArticleLink() {{
      const url = window.location.origin + '/cau-chuyen-son-mai/bai-viet/' + (currentArticleId + 1);
      navigator.clipboard.writeText(url).then(() => {{
        const toast = document.getElementById('copy-toast');
        if (toast) {{
          toast.classList.add('show');
          setTimeout(() => toast.classList.remove('show'), 2400);
        }}
      }});
    }}

    // Chuyển đổi bài viết mượt mà
    function switchArticle(idx, isUserClick = false) {{
      if (idx < 0 || idx >= articlesData.length) return;
      currentArticleId = idx;
      const art = articlesData[idx];

      // Đổi URL trên trình duyệt
      const newUrl = '/cau-chuyen-son-mai/bai-viet/' + (idx + 1);
      window.history.pushState({{ id: idx }}, '', newUrl);

      // Cập nhật nút quay lại
      const btnBackTop = document.getElementById('btn-back-timeline');
      if (btnBackTop) btnBackTop.href = '/cau-chuyen-son-mai#timeline-tab-' + idx;
      const btnBackBottom = document.getElementById('btn-bottom-back');
      if (btnBackBottom) btnBackBottom.href = '/cau-chuyen-son-mai#timeline-tab-' + idx;

      // Cập nhật tab active
      document.querySelectorAll('.milestone-tab').forEach(tab => {{
        const tabId = Number(tab.getAttribute('data-id'));
        if (tabId === idx) tab.classList.add('active');
        else tab.classList.remove('active');
      }});

      // Cập nhật tiêu đề trang
      document.title = art.title + ': ' + art.heading + ' | Câu chuyện sơn mài';

      // Cập nhật nội dung đầu trang
      document.getElementById('art-kicker').textContent = art.kicker;
      document.getElementById('art-heading').textContent = art.heading;
      document.getElementById('art-subtitle').textContent = art.title + ' · Tư liệu theo mạch lịch sử và đời sống di sản';
      document.getElementById('art-date-val').textContent = 'Giai đoạn: ' + art.date;
      document.getElementById('art-readtime').textContent = '⏱ ' + art.read_time;

      // Cập nhật ảnh và huy hiệu
      const imgEl = document.getElementById('art-img');
      imgEl.src = art.image;
      imgEl.alt = art.title;
      document.getElementById('art-badge-org').textContent = art.badge_org;
      document.getElementById('art-badge-sub').textContent = art.badge_sub;
      document.getElementById('art-caption').textContent = art.caption;

      // Cập nhật các đoạn văn bản
      let bodyHtml = '';
      art.paragraphs.forEach((p, pIdx) => {{
        bodyHtml += '<p>' + p + '</p>';
        if (pIdx === 1 && art.pull_quote) {{
          bodyHtml += '<blockquote class="editorial-pullquote"><p>“' + art.pull_quote + '”</p></blockquote>';
        }}
      }});
      document.getElementById('art-body').innerHTML = bodyHtml;

      // Cập nhật nút phân trang dưới
      const pagerEl = document.getElementById('art-pager');
      let prevBtn = '', nextBtn = '';
      if (idx > 0) {{
        const prevArt = articlesData[idx - 1];
        prevBtn = '<a href="/cau-chuyen-son-mai/bai-viet/' + idx + '" class="pager-btn prev" onclick="switchArticle(' + (idx - 1) + ', true); return false;"><span class="pager-label">← Mốc trước (0' + idx + ')</span><span class="pager-title">' + prevArt.title + '</span></a>';
      }} else {{
        prevBtn = '<div class="pager-btn prev disabled"><span class="pager-label">Khởi đầu</span><span class="pager-title">Đầu dòng thời gian</span></div>';
      }}

      if (idx < articlesData.length - 1) {{
        const nextArt = articlesData[idx + 1];
        nextBtn = '<a href="/cau-chuyen-son-mai/bai-viet/' + (idx + 2) + '" class="pager-btn next" onclick="switchArticle(' + (idx + 1) + ', true); return false;"><span class="pager-label">Mốc tiếp theo (0' + (idx + 2) + ') →</span><span class="pager-title">' + nextArt.title + '</span></a>';
      }} else {{
        nextBtn = '<div class="pager-btn next disabled"><span class="pager-label">Tiếp nối</span><span class="pager-title">Hiện tại & Tương lai</span></div>';
      }}
      pagerEl.innerHTML = prevBtn + nextBtn;

      // Chỉ cuộn nếu người dùng click thủ công
      if (isUserClick) {{
        const contentEl = document.getElementById('article-content');
        if (contentEl) {{
          contentEl.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }}
      }}
    }}

    // Đọc tham số URL khi tải trang lần đầu
    window.addEventListener('DOMContentLoaded', () => {{
      const path = window.location.pathname;
      const numMatch = path.match(/\\/bai-viet\\/([1-6])(?:\\/|$)/);
      if (numMatch) {{
        const targetId = parseInt(numMatch[1], 10) - 1;
        if (targetId >= 0 && targetId < articlesData.length && targetId !== currentArticleId) {{
          switchArticle(targetId, false);
          return;
        }}
      }}
      articlesData.forEach((a, aIdx) => {{
        if (path.includes('/' + a.slug) && aIdx !== currentArticleId) {{
          switchArticle(aIdx, false);
          return;
        }}
      }});
      const params = new URLSearchParams(window.location.search);
      const qId = params.get('id');
      if (qId !== null && !isNaN(Number(qId))) {{
        let targetId = Number(qId);
        if (targetId >= 1 && targetId <= 6 && !params.get('zero')) targetId = targetId - 1;
        if (targetId >= 0 && targetId < articlesData.length && targetId !== currentArticleId) {{
          switchArticle(targetId, false);
        }}
      }}
    }});

    // Bắt sự kiện back/forward của trình duyệt
    window.addEventListener('popstate', (e) => {{
      const path = window.location.pathname;
      const numMatch = path.match(/\\/bai-viet\\/([1-6])(?:\\/|$)/);
      if (numMatch) {{
        const targetId = parseInt(numMatch[1], 10) - 1;
        if (targetId >= 0 && targetId < articlesData.length) {{
          switchArticle(targetId, false);
          return;
        }}
      }}
      if (e.state && typeof e.state.id === 'number') {{
        switchArticle(e.state.id, false);
      }}
    }});
  </script>
</body>
</html>
"""

# 1. Tạo file chính cau-chuyen-son-mai/bai-viet/index.html (mặc định mốc 0)
main_reader_path = os.path.join(BASE_DIR, "cau-chuyen-son-mai/bai-viet/index.html")
with open(main_reader_path, "w", encoding="utf-8") as f:
    f.write(render_article_html(0))
print(f"Generated main reader: {main_reader_path}")

# 2. Tạo riêng từng trang cho tất cả 6 mốc
for i in range(len(ARTICLES)):
    art = ARTICLES[i]
    slug = art["slug"]
    rendered = render_article_html(i)

    # A. Đường dẫn dạng số: /cau-chuyen-son-mai/bai-viet/{1..6}/index.html
    sub_dir = os.path.join(BASE_DIR, f"cau-chuyen-son-mai/bai-viet/{i+1}")
    os.makedirs(sub_dir, exist_ok=True)
    with open(os.path.join(sub_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Generated milestone {i+1}: /cau-chuyen-son-mai/bai-viet/{i+1}")

    # B. Đường dẫn slug trong bai-viet: /cau-chuyen-son-mai/bai-viet/{slug}/index.html
    sub_slug_dir = os.path.join(BASE_DIR, f"cau-chuyen-son-mai/bai-viet/{slug}")
    os.makedirs(sub_slug_dir, exist_ok=True)
    with open(os.path.join(sub_slug_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(rendered)

    # C. Đường dẫn slug trực tiếp: /cau-chuyen-son-mai/{slug}/index.html
    top_slug_dir = os.path.join(BASE_DIR, f"cau-chuyen-son-mai/{slug}")
    os.makedirs(top_slug_dir, exist_ok=True)
    with open(os.path.join(top_slug_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Generated dedicated milestone route: /cau-chuyen-son-mai/{slug}")

# Hỗ trợ cả 0
sub_dir0 = os.path.join(BASE_DIR, "cau-chuyen-son-mai/bai-viet/0")
os.makedirs(sub_dir0, exist_ok=True)
with open(os.path.join(sub_dir0, "index.html"), "w", encoding="utf-8") as f:
    f.write(render_article_html(0))

print("ALL 6 MILESTONE DEDICATED PAGES GENERATED SUCCESSFULLY!")
