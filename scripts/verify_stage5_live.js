const cp = require('child_process');

async function testLive() {
  console.log('--- Testing live https://sonsonmaisac.id.vn/kham-pha#cong-doan-5 ---');
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9293',
    '--no-sandbox',
    '--window-size=1280,1000'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9293/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  let id = 1;
  const callbacks = new Map();
  const errors = [];

  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      errors.push(msg.params.args.map(a => a.value || a.description || '').join(' '));
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      errors.push(msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || ''));
    }
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

  await send('Page.navigate', { url: 'https://sonsonmaisac.id.vn/kham-pha#cong-doan-5' });
  await new Promise(r => setTimeout(r, 4000));

  const info = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const item5 = document.querySelector('#cong-doan-5');
        const titleEl = item5 ? item5.querySelector('.core-v4-step-title') : null;
        const shortEl = item5 ? item5.querySelector('.core-v4-step-short') : null;
        const detailEl = document.querySelector('#core-v4-process-detail p');
        return {
          title: titleEl ? titleEl.textContent : '',
          short: shortEl ? shortEl.textContent : '',
          detail: detailEl ? detailEl.textContent : ''
        };
      })()
    `,
    returnByValue: true
  });

  console.log('Live Stage 5 Title :', info.result?.value?.title);
  console.log('Live Stage 5 Short :', info.result?.value?.short);
  console.log('Live Stage 5 Detail:', info.result?.value?.detail);
  console.log('Live Exceptions/Errors:', errors.length);

  ws.close();
  chrome.kill();
}

testLive().catch(console.error);
