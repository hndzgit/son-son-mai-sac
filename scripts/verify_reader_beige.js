const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9229',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=390,844',
    '--user-data-dir=/tmp/chrome-test-mobile-reader'
  ]);

  await new Promise(r => setTimeout(r, 1200));

  try {
    const targets = await fetch('http://127.0.0.1:9229/json/list').then(r => r.json());
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
    await send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true
    });

    console.log('Navigating to http://localhost:3000/cau-chuyen-son-mai/bai-viet/1 ...');
    await send('Page.navigate', { url: 'http://localhost:3000/cau-chuyen-son-mai/bai-viet/1' });
    await new Promise(r => setTimeout(r, 2000));

    // Evaluate colors
    const colors = await send('Runtime.evaluate', {
      expression: `(() => {
        const card = document.querySelector('.newspaper-card');
        const switcher = document.querySelector('.milestone-switcher');
        const topBar = document.querySelector('.reader-top-bar');
        const showcase = document.querySelector('.artifact-showcase');
        const badge = document.querySelector('.museum-badge');
        return {
          cardBg: card ? window.getComputedStyle(card).backgroundColor : null,
          switcherBg: switcher ? window.getComputedStyle(switcher).backgroundColor : null,
          topBarBg: topBar ? window.getComputedStyle(topBar).backgroundColor : null,
          showcaseBg: showcase ? window.getComputedStyle(showcase).backgroundColor : null,
          badgeBg: badge ? window.getComputedStyle(badge).backgroundColor : null
        };
      })()`,
      returnByValue: true
    });
    console.log('Computed styles:', JSON.stringify(colors.result.value, null, 2));

    const ss = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/reader_mobile_beige_verified.png', Buffer.from(ss.data, 'base64'));
    console.log('Saved scripts/reader_mobile_beige_verified.png');

    // Also desktop
    await send('Emulation.setDeviceMetricsOverride', {
      width: 1280,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });
    await new Promise(r => setTimeout(r, 500));
    const ssDesktop = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/reader_desktop_beige_verified.png', Buffer.from(ssDesktop.data, 'base64'));
    console.log('Saved scripts/reader_desktop_beige_verified.png');

  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
