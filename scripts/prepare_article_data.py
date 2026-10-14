# -*- coding: utf-8 -*-
"""
Trình tạo trang đọc bài viết chuyên biệt (Editorial Reader)
Chuẩn giao diện báo chí mỹ thuật Việt Nam theo yêu cầu người dùng (như Image 2)
"""
import os
import json

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

# Kết hợp dữ liệu
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

print(f"Prepared {len(ARTICLES)} rich editorial articles.")
