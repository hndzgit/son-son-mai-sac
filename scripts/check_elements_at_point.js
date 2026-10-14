const cp = require('child_process');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9245',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9245/json/list').then(r => r.json());
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

    // Scroll to 800
    await send('Runtime.evaluate', { expression: 'window.scrollTo({ top: 800, behavior: "instant" })' });
    await new Promise(r => setTimeout(r, 1000));

    const res = await send('Runtime.evaluate', {
      expression: `(() => {
        // Find elements at center of screen (720, 450)
        const els = document.elementsFromPoint(720, 450);
        return els.map(el => ({
          tag: el.tagName,
          id: el.id,
          class: el.className,
          zIndex: window.getComputedStyle(el).zIndex,
          opacity: window.getComputedStyle(el).opacity,
          background: window.getComputedStyle(el).backgroundColor,
          bgImage: window.getComputedStyle(el).backgroundImage.slice(0, 50),
          pointerEvents: window.getComputedStyle(el).pointerEvents,
          position: window.getComputedStyle(el).position
        }));
      })()`,
      returnByValue: true
    });

    console.log('Elements from point at (720, 450) when scroll=800:');
    console.log(JSON.stringify(res.result.value, null, 2));

  } finally {
    chrome.kill();
  }
}

test().catch(console.error);
