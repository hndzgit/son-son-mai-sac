const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9225',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=390,844',
    '--user-data-dir=/tmp/chrome-test-sonmai-mobile'
  ]);

  await new Promise(r => setTimeout(r, 1200));

  try {
    const targets = await fetch('http://127.0.0.1:9225/json/list').then(r => r.json());
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

    console.log('Navigating to http://localhost:3000/kham-pha#son-mai-la-gi on Mobile ...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha#son-mai-la-gi' });
    await new Promise(r => setTimeout(r, 2500));

    // Capture screenshot at #son-mai-la-gi
    const ss1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_mobile_sonmai.png', Buffer.from(ss1.data, 'base64'));
    console.log('Saved scripts/khampha_mobile_sonmai.png');

    // Scroll down a bit to see the masterpiece and text
    await send('Runtime.evaluate', {
      expression: `window.scrollBy({ top: 400, behavior: 'instant' })`
    });
    await new Promise(r => setTimeout(r, 500));
    const ss2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_mobile_masterpiece.png', Buffer.from(ss2.data, 'base64'));
    console.log('Saved scripts/khampha_mobile_masterpiece.png');

    // Scroll down to 5 stages
    await send('Runtime.evaluate', {
      expression: `document.getElementById('5-cong-doan').scrollIntoView({ behavior: 'instant', block: 'start' })`
    });
    await new Promise(r => setTimeout(r, 500));
    const ss3 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_mobile_5stages.png', Buffer.from(ss3.data, 'base64'));
    console.log('Saved scripts/khampha_mobile_5stages.png');

  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
