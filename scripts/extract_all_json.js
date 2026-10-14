const fs = require('fs');
const path = require('path');

const jsDir = 'ma_nguon_css_js/js';
const files = fs.readdirSync(jsDir);

for (const file of files) {
  if (!file.endsWith('.js')) continue;
  const content = fs.readFileSync(path.join(jsDir, file), 'utf8');
  
  // Find JSON.parse('...') or JSON.parse("...")
  const regex = /JSON\.parse\('(.*?)'\)/g;
  let match;
  let count = 0;
  while ((match = regex.exec(content)) !== null) {
    count++;
    try {
      const unescaped = match[1].replace(/\\x([0-9A-Fa-f]{2})/g, (m, p1) => String.fromCharCode(parseInt(p1, 16)))
                                .replace(/\\'/g, "'");
      const parsed = JSON.parse(unescaped);
      console.log(`\n[${file}] JSON.parse #${count}:`);
      console.log(JSON.stringify(parsed, null, 2).slice(0, 500) + '...');
    } catch (e) {
      console.log(`[${file}] Failed to parse JSON #${count}: ${e.message}`);
    }
  }
}
