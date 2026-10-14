const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9242',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9242/json/list').then(r => r.json());
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
    await new Promise(r => setTimeout(r, 3000));

    // Scroll to 800px (around #son-mai-la-gi)
    await send('Runtime.evaluate', { expression: 'window.scrollTo({ top: 800, behavior: "instant" })' });
    await new Promise(r => setTimeout(r, 1000));

    const shot1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/screenshot_scroll_800.png', Buffer.from(shot1.data, 'base64'));

    // Scroll to 1500px
    await send('Runtime.evaluate', { expression: 'window.scrollTo({ top: 1500, behavior: "instant" })' });
    await new Promise(r => setTimeout(r, 1000));

    const shot2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/screenshot_scroll_1500.png', Buffer.from(shot2.data, 'base64'));

    const state = await send('Runtime.evaluate', {
      expression: `(() => {
        const reveals = Array.from(document.querySelectorAll('[data-reveal]')).map(el => ({
          tag: el.tagName,
          id: el.id,
          cls: el.className,
          visible: el.getAttribute('data-visible'),
          opacity: window.getComputedStyle(el).opacity,
          rect: el.getBoundingClientRect()
        }));
        return {
          scrollY: window.scrollY,
          reveals
        };
      })()`,
      returnByValue: true
    });

    console.log('State at 1500:', JSON.stringify(state.result.value, null, 2));

  } finally {
    chrome.kill();
  }
}

test().catch(console.error);
