const fs = require('fs');

const code = fs.readFileSync('ma_nguon_css_js/js/app_cau-chuyen-son-mai_page-18999a17f9a00aec.js', 'utf8');

// Find the definition of l and u
// In the code, look for pattern `l=[...],u=[...]`
const flowIdx = code.indexOf('flow-11');
console.log('Index of flow-11:', flowIdx);
console.log(code.slice(flowIdx - 200, flowIdx + 600));
