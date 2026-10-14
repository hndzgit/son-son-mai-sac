const cp = require('child_process');
const fs = require('fs');
const path = require('path');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9224',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);

  await new Promise(r => setTimeout(r, 1000));

  try {
    const targets = await fetch('http://localhost:9224/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

    let id = 1;
    const pending = new Map();
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const msgId = id++;
      pending.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });

    const consoleLogs = [];
    const errors = [];
    const networkRequests = [];

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id).resolve(msg.result);
        pending.delete(msg.id);
      }
      if (msg.method === 'Runtime.consoleAPICalled') {
        const text = msg.params.args.map(a => a.value || JSON.stringify(a)).join(' ');
        consoleLogs.push(`[${msg.params.type}] ${text}`);
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        errors.push(msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text);
      }
      if (msg.method === 'Network.requestWillBeSent') {
        networkRequests.push(msg.params.request.url);
      }
    };

    await new Promise(r => ws.onopen = r);

    await send('Page.enable');
    await send('Runtime.enable');
    await send('Network.enable');

    console.log('Navigating to https://sonsonmaisat.site/ ...');
    await send('Page.navigate', { url: 'https://sonsonmaisat.site/' });
    await new Promise(r => setTimeout(r, 4000));

    await send('Runtime.evaluate', { expression: 'window.scrollTo(0, 1000)' });
    await new Promise(r => setTimeout(r, 1000));
    await send('Runtime.evaluate', { expression: 'window.scrollTo(0, 2000)' });
    await new Promise(r => setTimeout(r, 2000));

    const evalResult = await send('Runtime.evaluate', {
      expression: `({
        title: document.title,
        canvasCount: document.querySelectorAll('canvas').length,
        canvases: Array.from(document.querySelectorAll('canvas')).map(c => ({
          w: c.width, h: c.height, class: c.className, parent: c.parentElement?.className
        })),
        visibleReveals: document.querySelectorAll('[data-visible="true"]').length,
        totalReveals: document.querySelectorAll('[data-reveal]').length,
        viewerContent: document.querySelector('[data-journey-phase]')?.outerHTML?.slice(0, 200)
      })`,
      returnByValue: true
    });

    console.log('LIVE Page Evaluation Result:');
    console.log(JSON.stringify(evalResult.result.value, null, 2));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(__dirname, 'screenshot_live_root.png'), Buffer.from(shot.data, 'base64'));
    console.log('Screenshot saved to screenshot_live_root.png');

    console.log('\nNavigating to https://sonsonmaisat.site/trai-nghiem ...');
    await send('Page.navigate', { url: 'https://sonsonmaisat.site/trai-nghiem' });
    await new Promise(r => setTimeout(r, 4000));

    const tnResult = await send('Runtime.evaluate', {
      expression: `({
        title: document.title,
        canvasCount: document.querySelectorAll('canvas').length,
        canvases: Array.from(document.querySelectorAll('canvas')).map(c => ({
          w: c.width, h: c.height, class: c.className, parent: c.parentElement?.className
        }))
      })`,
      returnByValue: true
    });
    console.log('LIVE /trai-nghiem Result:', JSON.stringify(tnResult.result.value, null, 2));

    const shotTn = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(__dirname, 'screenshot_live_trainghiem.png'), Buffer.from(shotTn.data, 'base64'));

  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
