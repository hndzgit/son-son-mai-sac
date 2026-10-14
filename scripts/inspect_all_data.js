const fs = require('fs');

const files = [
  'ma_nguon_css_js/js/app_tin-tuc-su-kien_page-0044ed8affa87fe5.js',
  'ma_nguon_css_js/js/app_ve-du-an_page-4431fa17e862519b.js',
  'ma_nguon_css_js/js/app_san-pham_page-2a9f8a05b3d81499.js',
  'ma_nguon_css_js/js/app_trai-nghiem_page-4cfd64a621149b8e.js',
  'ma_nguon_css_js/js/app_trai-nghiem_hanh-trinh_page-2c74554e92ef9036.js',
  'ma_nguon_css_js/js/app_page-1f5c1f7a3dcd2475.js',
];

for (const file of files) {
  if (!fs.existsSync(file)) continue;
  const content = fs.readFileSync(file, 'utf8');
  console.log(`\n=== FILE: ${file} ===`);
  
  // Look for JSON.parse
  const regex = /JSON\.parse\('(.*?)'\)/g;
  let m;
  let jsonCount = 0;
  while ((m = regex.exec(content)) !== null) {
    jsonCount++;
    try {
      const unescaped = m[1].replace(/\\x([0-9A-Fa-f]{2})/g, (_, p1) => String.fromCharCode(parseInt(p1, 16)))
                            .replace(/\\'/g, "'");
      const d = JSON.parse(unescaped);
      console.log(`JSON.parse #${jsonCount}: keys/length =`, Array.isArray(d) ? `Array(${d.length})` : Object.keys(d));
      if (Array.isArray(d) && d.length > 0) {
        console.log('Sample item:', d[0]);
      }
    } catch (e) {
      console.log(`JSON error #${jsonCount}:`, e.message);
    }
  }
  if (jsonCount === 0) {
    console.log('No JSON.parse found in this file.');
  }
}
