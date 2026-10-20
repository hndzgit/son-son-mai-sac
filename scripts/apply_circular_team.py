import re

NEW_TEAM_CSS = """
/* ==================== VỀ DỰ ÁN: BỐ CỤC Ô TRÒN ĐỘI NGŨ (TRƯỞNG NHÓM Ở GIỮA, 4 THÀNH VIÊN Ở DƯỚI) ==================== */
.project_team__Gn0Iu {
  max-width: 1220px !important;
  margin: 0 auto clamp(70px, 9vw, 130px) !important;
}

.project_teamHead___OCeu {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
  margin-bottom: clamp(38px, 5vw, 56px) !important;
}

.project_teamHead___OCeu > div {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
  max-width: 620px !important;
  margin: 0 auto !important;
}

.project_teamHead___OCeu .eyebrow {
  color: #9e3e1f !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  margin: 0 0 10px 0 !important;
}

.project_teamHead___OCeu h2 {
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-size: clamp(32px, 4vw, 48px) !important;
  color: #801C18 !important;
  font-weight: 600 !important;
  letter-spacing: -0.015em !important;
  margin: 0 0 12px 0 !important;
  line-height: 1.15 !important;
}

.project_teamHead___OCeu p:last-child {
  font-size: clamp(15px, 1.1vw, 17px) !important;
  line-height: 1.65 !important;
  color: #6d5843 !important;
  margin: 0 !important;
}

/* Lưới tổng thể: 4 cột trên Desktop */
.project_page__UA7p9 .team-portrait-v4-grid {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  grid-template-rows: auto auto !important;
  gap: clamp(32px, 4vw, 48px) clamp(16px, 2.5vw, 32px) !important;
  justify-items: center !important;
  align-items: start !important;
  max-width: 1040px !important;
  margin: 0 auto !important;
}

/* Base Card dạng thẻ không viền, căn giữa nội dung */
.project_page__UA7p9 .team-portrait-v4-card {
  border: none !important;
  background: transparent !important;
  box-shadow: none !important;
  border-radius: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
  min-width: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  max-width: 240px !important;
  overflow: visible !important;
  transition: transform 0.35s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
}

.project_page__UA7p9 .team-portrait-v4-card:hover {
  transform: translateY(-4px) !important;
}

/* Tắt mọi pseudo-element gây chắn ngang hoặc viền thừa */
.project_page__UA7p9 .team-portrait-v4-card::before,
.project_page__UA7p9 .team-portrait-v4-card::after,
.project_page__UA7p9 .team-portrait-v4-image-wrap::before,
.project_page__UA7p9 .team-portrait-v4-image-wrap::after,
.project_page__UA7p9 .team-portrait-v4-chibi {
  display: none !important;
  content: none !important;
}

/* Ẩn fallback layer để không bị chồng lấn hay lộ chữ/màu nền phía sau */
.project_page__UA7p9 .team-portrait-v4-fallback {
  display: none !important;
  opacity: 0 !important;
  visibility: hidden !important;
  pointer-events: none !important;
}

/* Base khung tròn chứa ảnh: Kích hoạt mask bo tròn chuẩn GPU WebKit/Blink tránh lỗi rách ảnh khi di chuột */
.project_page__UA7p9 .team-portrait-v4-image-wrap {
  border-radius: 50% !important;
  overflow: hidden !important;
  -webkit-mask-image: -webkit-radial-gradient(white, black) !important;
  mask-image: radial-gradient(white, black) !important;
  -webkit-mask-composite: source-over !important;
  mask-composite: add !important;
  isolation: isolate !important;
  -webkit-transform: translateZ(0) !important;
  transform: translateZ(0) !important;
  -webkit-backface-visibility: hidden !important;
  backface-visibility: hidden !important;
}

/* Ảnh chân dung: Khóa cố định tỉ lệ tròn, KHÔNG scale khi hover để tránh Blink clipping glitch */
.project_page__UA7p9 .team-portrait-v4-image {
  position: relative !important;
  z-index: 2 !important;
  display: block !important;
  width: 100% !important;
  height: 100% !important;
  border-radius: 50% !important;
  object-fit: cover !important;
  object-position: center 5% !important;
  filter: none !important;
  transform: none !important;
  -webkit-transform: none !important;
  transition: none !important;
}

/* Triệt tiêu triệt để mọi hành vi scale ảnh khi hover hoặc focus */
.project_page__UA7p9 .team-portrait-v4-card:hover .team-portrait-v4-image,
.project_page__UA7p9 .team-portrait-v4-card:focus-within .team-portrait-v4-image,
.project_page__UA7p9 .team-portrait-v4-card.is-featured:hover .team-portrait-v4-image,
.project_page__UA7p9 .team-portrait-v4-card:not(.is-featured):hover .team-portrait-v4-image,
.project_page__UA7p9 .team-portrait-v4-image-wrap:hover .team-portrait-v4-image {
  transform: none !important;
  -webkit-transform: none !important;
}

/* --- TRƯỞNG NHÓM (Ở GIỮA HÀNG ĐẦU, Ô TRÒN NỔI BẬT) --- */
.project_page__UA7p9 .team-portrait-v4-card.is-featured {
  grid-column: 1 / -1 !important;
  grid-row: 1 !important;
  justify-self: center !important;
  max-width: 320px !important;
  margin-bottom: clamp(8px, 1.5vw, 16px) !important;
}

.project_page__UA7p9 .team-portrait-v4-card.is-featured .team-portrait-v4-image-wrap {
  width: clamp(170px, 15vw, 198px) !important;
  height: clamp(170px, 15vw, 198px) !important;
  aspect-ratio: 1 / 1 !important;
  flex: none !important;
  border-radius: 50% !important;
  overflow: hidden !important;
  position: relative !important;
  border: 3.5px solid #d4af37 !important; /* Vành hoàng kim sơn mài */
  box-shadow: 0 0 0 5px rgba(212, 175, 55, 0.25), 0 14px 34px rgba(139, 42, 42, 0.22) !important;
  background: radial-gradient(circle at 50% 35%, #fffbf2, #ebdcc0) !important;
  transition: border-color 0.35s ease, box-shadow 0.35s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
}

.project_page__UA7p9 .team-portrait-v4-card.is-featured:hover .team-portrait-v4-image-wrap {
  border-color: #f3cf65 !important;
  box-shadow: 0 0 0 7px rgba(212, 175, 55, 0.42), 0 18px 40px rgba(139, 42, 42, 0.28) !important;
}

.project_page__UA7p9 .team-portrait-v4-card.is-featured h3 {
  background: transparent !important;
  color: #801C18 !important;
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-size: clamp(22px, 2.2vw, 27px) !important;
  font-weight: 600 !important;
  line-height: 1.25 !important;
  margin: 16px 0 8px 0 !important;
  padding: 0 !important;
  text-align: center !important;
  letter-spacing: -0.01em !important;
}

.project_page__UA7p9 .team-portrait-v4-card.is-featured p {
  background: linear-gradient(135deg, #801C18, #601410) !important;
  color: #fff9ed !important;
  border: 1px solid #d4af37 !important;
  border-radius: 999px !important;
  padding: 5px 22px 6px !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  letter-spacing: 0.03em !important;
  margin: 0 !important;
  box-shadow: 0 4px 12px rgba(128, 28, 24, 0.22) !important;
  display: inline-block !important;
  text-align: center !important;
}

/* --- 4 THÀNH VIÊN Ở DƯỚI (HÀNG 2 CÂN ĐỐI) --- */
.project_page__UA7p9 .team-portrait-v4-card:nth-child(2) {
  grid-column: 1 !important;
  grid-row: 2 !important;
}
.project_page__UA7p9 .team-portrait-v4-card:nth-child(3) {
  grid-column: 2 !important;
  grid-row: 2 !important;
}
.project_page__UA7p9 .team-portrait-v4-card:nth-child(4) {
  grid-column: 3 !important;
  grid-row: 2 !important;
}
.project_page__UA7p9 .team-portrait-v4-card:nth-child(5) {
  grid-column: 4 !important;
  grid-row: 2 !important;
}

.project_page__UA7p9 .team-portrait-v4-card:not(.is-featured) .team-portrait-v4-image-wrap {
  width: clamp(124px, 11vw, 148px) !important;
  height: clamp(124px, 11vw, 148px) !important;
  aspect-ratio: 1 / 1 !important;
  flex: none !important;
  border-radius: 50% !important;
  overflow: hidden !important;
  position: relative !important;
  border: 2.5px solid #c9a96e !important;
  box-shadow: 0 0 0 4px rgba(201, 169, 110, 0.22), 0 8px 22px rgba(60, 30, 15, 0.12) !important;
  background: radial-gradient(circle at 50% 35%, #fffbf2, #ebdcc0) !important;
  transition: border-color 0.35s ease, box-shadow 0.35s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
}

.project_page__UA7p9 .team-portrait-v4-card:not(.is-featured):hover .team-portrait-v4-image-wrap {
  border-color: #d4af37 !important;
  box-shadow: 0 0 0 6px rgba(212, 175, 55, 0.38), 0 14px 30px rgba(139, 42, 42, 0.2) !important;
}

.project_page__UA7p9 .team-portrait-v4-card:not(.is-featured) h3 {
  background: transparent !important;
  color: #801C18 !important;
  font-family: "Project Display", "Playfair Display", "Noto Serif", Georgia, serif !important;
  font-size: clamp(17px, 1.55vw, 20px) !important;
  font-weight: 600 !important;
  line-height: 1.25 !important;
  margin: 14px 0 6px 0 !important;
  padding: 0 !important;
  text-align: center !important;
  letter-spacing: -0.01em !important;
  white-space: nowrap !important;
}

.project_page__UA7p9 .team-portrait-v4-card:not(.is-featured) p {
  background: rgba(236, 221, 189, 0.72) !important;
  color: #59442e !important;
  border: 1px solid rgba(164, 135, 87, 0.45) !important;
  border-radius: 999px !important;
  padding: 3px 14px 4px !important;
  font-size: 12.5px !important;
  font-weight: 500 !important;
  letter-spacing: 0.01em !important;
  margin: 0 !important;
  display: inline-block !important;
  text-align: center !important;
  white-space: nowrap !important;
}

/* --- RESPONSIVE CHO TABLET & MOBILE --- */
@media (max-width: 880px) {
  .project_page__UA7p9 .team-portrait-v4-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    grid-template-rows: auto auto auto !important;
    gap: 30px 20px !important;
    max-width: 560px !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card.is-featured {
    grid-column: 1 / -1 !important;
    grid-row: 1 !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card:nth-child(2) {
    grid-column: 1 !important;
    grid-row: 2 !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card:nth-child(3) {
    grid-column: 2 !important;
    grid-row: 2 !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card:nth-child(4) {
    grid-column: 1 !important;
    grid-row: 3 !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card:nth-child(5) {
    grid-column: 2 !important;
    grid-row: 3 !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card:not(.is-featured) h3 {
    white-space: normal !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card:not(.is-featured) p {
    white-space: normal !important;
  }
}

@media (max-width: 480px) {
  .project_page__UA7p9 .team-portrait-v4-grid {
    gap: 24px 12px !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card.is-featured .team-portrait-v4-image-wrap {
    width: 148px !important;
    height: 148px !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card:not(.is-featured) .team-portrait-v4-image-wrap {
    width: 112px !important;
    height: 112px !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card.is-featured h3 {
    font-size: 20px !important;
    margin-top: 12px !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card:not(.is-featured) h3 {
    font-size: 15.5px !important;
    margin-top: 10px !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card.is-featured p {
    font-size: 12px !important;
    padding: 4px 16px !important;
  }
  .project_page__UA7p9 .team-portrait-v4-card:not(.is-featured) p {
    font-size: 11px !important;
    padding: 3px 10px !important;
  }
}
"""

def update_css():
    css_path = "_next/static/css/f7d6d17d52efcb3d.css"
    with open(css_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if section was already added
    marker = "/* ==================== VỀ DỰ ÁN: BỐ CỤC Ô TRÒN ĐỘI NGŨ"
    if marker in content:
        content = content[:content.find(marker)].rstrip()
    
    content = content.rstrip() + "\n\n" + NEW_TEAM_CSS.strip() + "\n"
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated CSS in", css_path)

def update_html_version():
    files = [
        "ve-du-an/index.html",
        "trang_html_goc/08_ve_du_an.html"
    ]
    for p in files:
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
        c_new = re.sub(r'f7d6d17d52efcb3d\.css\?v=\d+', 'f7d6d17d52efcb3d.css?v=29', c)
        if c_new != c:
            with open(p, "w", encoding="utf-8") as f:
                f.write(c_new)
            print("Updated CSS version to ?v=29 in", p)
        else:
            print("No version bump needed or pattern didn't match in", p)

if __name__ == "__main__":
    update_css()
    update_html_version()
