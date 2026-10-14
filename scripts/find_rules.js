const fs = require('fs');
const cssPath = '_next/static/css/3d939b8161363d36.css';
const content = fs.readFileSync(cssPath, 'utf8');

const regex = /[^{}]*data-reveal[^{}]*\{[^{}]*\}/g;
let match;
while ((match = regex.exec(content)) !== null) {
  console.log('Match:', match[0]);
}

// Also check [data-visible
const regex2 = /[^{}]*data-visible[^{}]*\{[^{}]*\}/g;
while ((match = regex2.exec(content)) !== null) {
  console.log('Visible match:', match[0]);
}
