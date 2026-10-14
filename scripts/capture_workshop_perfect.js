const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9232',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1100',
    '--user-data-dir=/tmp/chrome-test-perfect'
  ]);

  await new Promise(r => setTimeout(r, 1200));

  try {
    const targets = await fetch('http://127.0.0.1:9232/json/list').then(r => r.json());
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const pending = new Map();
    const send = (m, p = {}) => new Promise((res, rej) => {
      const i = id++;
      pending.set(i, { res, rej });
      ws.send(JSON.stringify({ id: i, method: m, params: p }));
    });
    ws.onmessage = e => {
      const msg = JSON.parse(e.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id).res(msg.result);
        pending.delete(msg.id);
      }
    };
    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');

    console.log('Navigating to http://localhost:3000/kham-pha ...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 4500));

    // Scroll to simulator panel
    const info = await send('Runtime.evaluate', {
      expression: `(() => {
        const sim = document.getElementById("simulator");
        if (sim) {
          const rect = sim.getBoundingClientRect();
          window.scrollTo(0, window.scrollY + rect.top - 80);
          return { top: rect.top, y: window.scrollY };
        }
        return null;
      })()`,
      returnByValue: true
    });
    console.log('Scroll info:', info.result.value);
    await new Promise(r => setTimeout(r, 1200));

    const ss = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/stage1_enhanced_verified.png', Buffer.from(ss.data, 'base64'));
    console.log('Saved scripts/stage1_enhanced_verified.png successfully!');
  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
