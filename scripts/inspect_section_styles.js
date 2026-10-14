const cp = require('child_process');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9244',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9244/json/list').then(r => r.json());
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

    const res = await send('Runtime.evaluate', {
      expression: `(() => {
        const sec1 = document.getElementById('son-mai-la-gi');
        if (!sec1) return { error: 'sec1 not found' };
        const h2 = sec1.querySelector('h2');
        const p = sec1.querySelector('p');
        return {
          sec1Tag: sec1.tagName,
          sec1Class: sec1.className,
          sec1Style: sec1.getAttribute('style'),
          h2Color: h2 ? window.getComputedStyle(h2).color : 'no h2',
          h2Opacity: h2 ? window.getComputedStyle(h2).opacity : 'no h2',
          pColor: p ? window.getComputedStyle(p).color : 'no p',
          pOpacity: p ? window.getComputedStyle(p).opacity : 'no p',
          parentOpacity: window.getComputedStyle(sec1).opacity,
          parentFilter: window.getComputedStyle(sec1).filter
        };
      })()`,
      returnByValue: true
    });

    console.log('Result:', JSON.stringify(res, null, 2));
  } finally {
    chrome.kill();
  }
}

test().catch(console.error);
