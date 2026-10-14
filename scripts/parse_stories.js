const fs = require('fs');

const content = fs.readFileSync('ma_nguon_css_js/js/app_cau-chuyen-son-mai_page-18999a17f9a00aec.js', 'utf8');

const regex = /JSON\.parse\('(.*?)'\)/g;
let match = regex.exec(content);
if (match) {
  const unescaped = match[1].replace(/\\x([0-9A-Fa-f]{2})/g, (m, p1) => String.fromCharCode(parseInt(p1, 16)))
                            .replace(/\\'/g, "'");
  const data = JSON.parse(unescaped);
  console.log(`Found ${data.length} story items!`);
  data.forEach((item, idx) => {
    console.log(`\n--- Item ${item.number}: ${item.title} (image: ${item.image}) ---`);
    console.log(`Paragraphs: ${item.content.length}`);
    item.content.forEach((p, pIdx) => {
      console.log(`  [P${pIdx+1}] ${p.slice(0, 100)}...`);
    });
  });
}
