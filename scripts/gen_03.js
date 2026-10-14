const fs = require('fs');

const code = fs.readFileSync('ma_nguon_css_js/js/app_cau-chuyen-son-mai_page-18999a17f9a00aec.js', 'utf8');
const regex = /JSON\.parse\('(.*?)'\)/g;
let match = regex.exec(code);

if (!match) {
  console.error("Could not find JSON.parse");
  process.exit(1);
}

const unescaped = match[1].replace(/\\x([0-9A-Fa-f]{2})/g, (m, p1) => String.fromCharCode(parseInt(p1, 16)))
                          .replace(/\\'/g, "'");
const rawStories = JSON.parse(unescaped);

const milestones = [
  {
    "id": "moc-01",
    "thoi_ky": "TRƯỚC HỘI HỌA",
    "chu_de": "Đời sống & tín ngưỡng",
    "tom_tat": "Từ vật dụng sinh hoạt hàng ngày đến không gian linh thiêng của đình chùa, sơn phủ bảo vệ và tôn nghiêm đồ vật thờ cúng.",
    "hinh_anh": "/story-assets/flow-11.jpg"
  },
  {
    "id": "moc-02",
    "thoi_ky": "TRI THỨC QUA THẾ HỆ",
    "chu_de": "Nghề thủ công & Làng nghề",
    "tom_tat": "Các thế hệ nghệ nhân đúc kết kinh nghiệm xử lý nhựa sơn ta, kỹ thuật hom vóc, đánh bóng bằng tro trấu và lòng bàn tay.",
    "hinh_anh": "/story-assets/flow-13.jpg"
  },
  {
    "id": "moc-03",
    "thoi_ky": "1925",
    "chu_de": "Mỹ thuật Đông Dương",
    "tom_tat": "Sự giao thoa lịch sử giữa chất liệu cổ truyền phương Đông và tư duy tạo hình hội họa phương Tây tại Trường Mỹ thuật Đông Dương.",
    "hinh_anh": "/story-assets/flow-21.jpg"
  },
  {
    "id": "moc-04",
    "thoi_ky": "THẾ KỶ XX",
    "chu_de": "Nghệ thuật hiện đại",
    "tom_tat": "Sơn mài chính thức trở thành một loại hình hội họa độc lập với kỹ thuật mài lộ lớp tiên phong của danh họa Nguyễn Gia Trí và các bậc thầy.",
    "hinh_anh": "/story-assets/flow-24.jpg"
  },
  {
    "id": "moc-05",
    "thoi_ky": "TRUYỀN NGHỀ",
    "chu_de": "Làng nghề Hạ Thái & Nghệ nhân",
    "tom_tat": "Nơi nuôi dưỡng và bảo tồn kỹ nghệ thủ công, nơi người thợ giữ vững cái tâm và tri thức cha truyền con nối.",
    "hinh_anh": "/story-assets/flow-32.jpg"
  },
  {
    "id": "moc-06",
    "thoi_ky": "ĐƯƠNG ĐẠI",
    "chu_de": "Vươn ra thế giới",
    "tom_tat": "Sơn mài hòa nhịp cùng thực hành nghệ thuật đương đại, vượt khỏi khung tranh phẳng để đối thoại với không gian và triển lãm quốc tế.",
    "hinh_anh": "/story-assets/flow-37.jpg"
  }
];

const cauChuyenData = {
  "tieu_de": "Câu chuyện sơn mài | Mỗi thời kỳ lại thêm một lớp",
  "khau_hieu": "Từ vật dụng đời sống đến thực hành đương đại, một chất liệu đi qua nhiều bàn tay và cách nhìn.",
  "sau_moc_thoi_gian": milestones,
  "cac_bai_viet_chuyen_sau": rawStories.map(s => ({
    "so_thu_tu": s.number,
    "tieu_de": s.title,
    "hinh_anh": `/story-assets/${s.image}.jpg`,
    "cac_doan_van": s.content
  }))
};

fs.writeFileSync('du_lieu_noi_dung/03_cau_chuyen_son_mai.json', JSON.stringify(cauChuyenData, null, 2), 'utf8');

// Write Markdown
let md = `# Câu Chuyện Sơn Mài: Mỗi Thời Kỳ Lại Thêm Một Lớp\n\n`;
md += `> *${cauChuyenData.khau_hieu}*\n\n`;
md += `## I. DÒNG THỜI GIAN: 6 MỐC LỊCH SỬ\n\n`;

milestones.forEach(m => {
  md += `### [${m.thoi_ky}] ${m.chu_de}\n`;
  md += `- **Tóm tắt:** ${m.tom_tat}\n`;
  md += `- **Hình ảnh minh họa:** \`${m.hinh_anh}\`\n\n`;
});

md += `## II. 12 BÀI VIẾT NỘI DUNG CHUYÊN SÂU\n\n`;

rawStories.forEach(s => {
  md += `### ${s.number}. ${s.title}\n`;
  md += `*Hình ảnh lưu trữ: \`/story-assets/${s.image}.jpg\`*\n\n`;
  s.content.forEach((p, idx) => {
    md += `${p}\n\n`;
  });
  md += `---\n\n`;
});

fs.writeFileSync('du_lieu_noi_dung/03_cau_chuyen_son_mai.md', md, 'utf8');
console.log("Saved 03_cau_chuyen_son_mai");
