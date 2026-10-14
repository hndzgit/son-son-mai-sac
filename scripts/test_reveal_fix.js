const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9248',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9248/json/list').then(r => r.json());
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

    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 2000));

    // Inject CSS override: opacity 1 on all reveals
    await send('Runtime.evaluate', {
      expression: `(() => {
        const style = document.createElement('style');
        style.textContent = \`
          .coreIntroduction_journey__bHzBt [data-reveal],
          .coreIntroduction_journey__bHzBt [data-reveal]:not([data-visible="true"]),
          [data-reveal],
          [data-reveal]:not([data-visible="true"]) {
            opacity: 1 !important;
            transform: none !important;
            visibility: visible !important;
          }
        \`;
        document.head.appendChild(style);
        document.querySelectorAll('[data-reveal]').forEach(el => el.setAttribute('data-visible', 'true'));
      })()`
    });

    // Scroll to 800
    await send('Runtime.evaluate', { expression: 'window.scrollTo({ top: 800, behavior: "instant" })' });
    await new Promise(r => setTimeout(r, 500));
    const shot800 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_fixed_800.png', Buffer.from(shot800.data, 'base64'));

    // Scroll to 1500
    await send('Runtime.evaluate', { expression: 'window.scrollTo({ top: 1500, behavior: "instant" })' });
    await new Promise(r => setTimeout(r, 500));
    const shot1500 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_fixed_1500.png', Buffer.from(shot1500.data, 'base64'));

    console.log('Screenshots saved!');

  } finally {
    chrome.kill();
  }
}

test().catch(console.error);
