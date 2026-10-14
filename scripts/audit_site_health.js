const cp = require('child_process');
const fs = require('fs');

const ROUTES = [
  '/ve-du-an',
  '/',
  '/kham-pha',
  '/cau-chuyen-son-mai',
  '/san-pham',
  '/tin-tuc-su-kien',
  '/trai-nghiem',
  '/son-mai-la-gi'
];

async function runAudit() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9255',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,1100'
  ]);

  for (let i = 0; i < 30; i++) {
    try {
      const targets = await fetch('http://localhost:9255/json/list').then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) break;
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  const targets = await fetch('http://localhost:9255/json/list').then(r => r.json());
  const validTarget = targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
  const ws = new WebSocket(validTarget.webSocketDebuggerUrl);

  let id = 1;
  const callbacks = new Map();
  const networkErrors = [];
  const consoleErrors = [];

  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.id && callbacks.has(msg.id)) {
      callbacks.get(msg.id)(msg.result);
      callbacks.delete(msg.id);
    }
    if (msg.method === 'Network.responseReceived') {
      const resp = msg.params.response;
      if (resp.status >= 400) {
        networkErrors.push({ url: resp.url, status: resp.status, statusText: resp.statusText });
      }
    }
    if (msg.method === 'Network.loadingFailed') {
      networkErrors.push({ url: msg.params.requestId, error: msg.params.errorText });
    }
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      consoleErrors.push(msg.params.args.map(a => a.value || a.description).join(' '));
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      consoleErrors.push(msg.params.exceptionDetails.text);
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
  await send('Network.enable');

  const results = {};

  for (const route of ROUTES) {
    networkErrors.length = 0;
    consoleErrors.length = 0;

    const url = `http://localhost:3000${route}`;
    await send('Page.navigate', { url });
    await new Promise(r => setTimeout(r, 2500));

    // Evaluate broken images and layout anomalies
    const pageCheck = await send('Runtime.evaluate', {
      expression: `(() => {
        const imgs = Array.from(document.querySelectorAll('img')).map(img => ({
          src: img.src || img.getAttribute('src'),
          alt: img.alt,
          complete: img.complete,
          naturalWidth: img.naturalWidth,
          naturalHeight: img.naturalHeight,
          isBroken: img.complete && img.naturalWidth === 0
        }));

        const brokenImgs = imgs.filter(i => i.isBroken);

        // Check horizontal overflow
        const docWidth = document.documentElement.offsetWidth;
        const scrollWidth = document.documentElement.scrollWidth;
        const hasHorizontalScroll = scrollWidth > docWidth + 5;

        return {
          totalImages: imgs.length,
          brokenImages: brokenImgs,
          hasHorizontalScroll,
          scrollWidth,
          docWidth
        };
      })()`,
      returnByValue: true
    });

    // Capture screenshot
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    const shotName = `scripts/audit_${route.replace(/\//g, '_') || '_root'}.png`;
    fs.writeFileSync(shotName, Buffer.from(shot.data, 'base64'));

    results[route] = {
      check: pageCheck.result.value,
      networkErrors: [...networkErrors],
      consoleErrors: [...consoleErrors],
      screenshot: shotName
    };
  }

  console.log(JSON.stringify(results, null, 2));
  chrome.kill();
}

runAudit().catch(console.error);
