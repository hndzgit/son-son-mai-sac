const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9240',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1100',
    '--user-data-dir=/tmp/chrome-test-doc-coords'
  ]);

  await new Promise(r => setTimeout(r, 1200));

  try {
    const targets = await fetch('http://127.0.0.1:9240/json/list').then(r => r.json());
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

    // Get document coordinates of controls or workshop
    const clipInfo = await send('Runtime.evaluate', {
      expression: `(() => {
        const controls = document.querySelector(".productExperience_galleryControls__WppUe") || document.getElementById("simulator");
        if (!controls) return null;
        const r = controls.getBoundingClientRect();
        return {
          x: Math.round(r.left + window.scrollX),
          y: Math.round(r.top + window.scrollY),
          width: Math.round(r.width),
          height: Math.round(r.height)
        };
      })()`,
      returnByValue: true
    });
    console.log('Document clip info:', clipInfo.result.value);

    const clip = clipInfo.result.value;
    const shot = await send('Page.captureScreenshot', {
      format: 'png',
      clip: {
        x: clip.x,
        y: clip.y,
        width: clip.width,
        height: clip.height,
        scale: 1
      },
      captureBeyondViewport: true
    });

    fs.writeFileSync('scripts/stage1_controls_verified.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved scripts/stage1_controls_verified.png successfully!');

  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
