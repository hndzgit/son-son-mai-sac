const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9224',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1280,900',
    '--user-data-dir=/tmp/chrome-test-sonmai-2'
  ]);

  await new Promise(r => setTimeout(r, 1200));

  try {
    const targets = await fetch('http://127.0.0.1:9224/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension')) || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

    let id = 1;
    const pending = new Map();
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const msgId = id++;
      pending.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id).resolve(msg.result);
        pending.delete(msg.id);
      }
    };

    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');

    console.log('Navigating to http://localhost:3000/kham-pha ...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 2500));

    // Evaluate presence of elements
    const evalRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const sonmai = document.getElementById('son-mai-la-gi');
        const congdoan = document.getElementById('5-cong-doan');
        const workshop = document.getElementById('process-workshop-panel');
        return {
          hasSonMai: !!sonmai,
          sonMaiTitle: sonmai ? sonmai.querySelector('h2')?.textContent : null,
          sonMaiImg: sonmai ? !!sonmai.querySelector('.sonmai-masterpiece-frame img') : false,
          sonMaiRows: sonmai ? sonmai.querySelectorAll('.sonmai-row-grid').length : 0,
          hasCongDoan: !!congdoan,
          congDoanTitle: congdoan ? congdoan.querySelector('h2')?.textContent : null,
          hasWorkshop: !!workshop
        };
      })()`,
      returnByValue: true
    });

    console.log('Page elements verification:\n', JSON.stringify(evalRes.result.value, null, 2));

    // Capture screenshot 1: top of page
    const ss1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_top_verified.png', Buffer.from(ss1.data, 'base64'));
    console.log('Saved scripts/khampha_top_verified.png');

    // Scroll to #son-mai-la-gi
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('son-mai-la-gi');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
      })()`
    });
    await new Promise(r => setTimeout(r, 600));

    const ss2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_sonmai_section_verified.png', Buffer.from(ss2.data, 'base64'));
    console.log('Saved scripts/khampha_sonmai_section_verified.png');

    // Scroll down to #5-cong-doan
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('5-cong-doan');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
      })()`
    });
    await new Promise(r => setTimeout(r, 600));

    const ss3 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_5congdoan_verified.png', Buffer.from(ss3.data, 'base64'));
    console.log('Saved scripts/khampha_5congdoan_verified.png');

  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
