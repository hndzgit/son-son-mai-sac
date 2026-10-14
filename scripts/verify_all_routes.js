const cp = require('child_process');

async function testAll() {
  const routes = [
    '/',
    '/kham-pha',
    '/cau-chuyen-son-mai',
    '/trai-nghiem',
    '/tu-chinh',
    '/san-pham',
    '/tin-tuc-su-kien',
    '/ve-du-an'
  ];

  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9226',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);

  await new Promise(r => setTimeout(r, 1000));

  try {
    const targets = await fetch('http://localhost:9226/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

    let id = 1;
    const pending = new Map();
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const msgId = id++;
      pending.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });

    const exceptions = [];
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id).resolve(msg.result);
        pending.delete(msg.id);
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        exceptions.push(msg.params.exceptionDetails.text);
      }
    };

    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');

    for (const r of routes) {
      const url = `http://localhost:3000${r}`;
      exceptions.length = 0;
      await send('Page.navigate', { url });
      await new Promise(res => setTimeout(res, 2000));
      const res = await send('Runtime.evaluate', {
        expression: `({
          title: document.title,
          h1: document.querySelector('h1')?.textContent || document.querySelector('h2')?.textContent,
          canvasCount: document.querySelectorAll('canvas').length
        })`,
        returnByValue: true
      });
      console.log(`Route ${r}:`, res.result.value, `Exceptions: ${exceptions.length}`);
    }

  } finally {
    chrome.kill();
  }
}

testAll().catch(console.error);
