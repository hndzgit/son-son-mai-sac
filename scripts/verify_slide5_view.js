const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9234',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);
  let targets = null;
  for (let i = 0; i < 20; i++) {
    try {
      targets = await fetch('http://localhost:9234/json/list').then(r => r.json());
      if (targets && targets.length) break;
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

    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 2000));

    // Capture screenshot of top portion
    const shot = await send('Page.captureScreenshot', {
      format: 'png',
      clip: { x: 0, y: 0, width: 1440, height: 700, scale: 1 }
    });
    fs.writeFileSync('scripts/screenshot_khampha_banner.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved scripts/screenshot_khampha_banner.png');
  } finally {
    chrome.kill();
  }
}
test().catch(console.error);
