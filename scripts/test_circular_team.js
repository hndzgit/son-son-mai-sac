const cp = require('child_process');
const fs = require('fs');

async function capture() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9246',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,1100'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9246/json/list').then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) {
        targets = [valid];
        break;
      }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  try {
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const callbacks = new Map();
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg.result);
        callbacks.delete(msg.id);
      }
    };
    const send = (method, params = {}) => new Promise(res => {
      const msgId = id++;
      callbacks.set(msgId, res);
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');

    // 1. Desktop screenshot
    await send('Page.navigate', { url: 'http://localhost:3000/ve-du-an' });
    await new Promise(r => setTimeout(r, 2500));

    // Scroll to section #doi-ngu
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('doi-ngu');
        if (el) el.scrollIntoView({ block: 'start', behavior: 'instant' });
      })()`
    });
    await new Promise(r => setTimeout(r, 1200));

    const shotDesktop = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/circular_team_desktop.png', Buffer.from(shotDesktop.data, 'base64'));
    console.log('Saved scripts/circular_team_desktop.png');

    // 2. Mobile screenshot
    await send('Emulation.setDeviceMetricsOverride', {
      width: 414,
      height: 896,
      deviceScaleFactor: 2,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 1000));
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('doi-ngu');
        if (el) el.scrollIntoView({ block: 'start', behavior: 'instant' });
      })()`
    });
    await new Promise(r => setTimeout(r, 1000));
    const shotMobile = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/circular_team_mobile.png', Buffer.from(shotMobile.data, 'base64'));
    console.log('Saved scripts/circular_team_mobile.png');

  } finally {
    chrome.kill();
  }
}

capture().catch(console.error);
