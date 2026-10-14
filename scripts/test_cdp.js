const cp = require('child_process');
const fs = require('fs');
const path = require('path');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9223',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);

  await new Promise(r => setTimeout(r, 1000));

  try {
    const targets = await fetch('http://localhost:9223/json/list').then(r => r.json());
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
    const failedRequests = [];

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
      if (msg.method === 'Network.loadingFailed') {
        failedRequests.push(`${msg.params.errorText}: requestId=${msg.params.requestId}`);
      }
    };

    await new Promise(r => ws.onopen = r);

    await send('Page.enable');
    await send('Runtime.enable');
    await send('Network.enable');

    console.log('Navigating to http://localhost:3000/ ...');
    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 3000));

    // Scroll down to trigger scroll reveal and viewer
    await send('Runtime.evaluate', { expression: 'window.scrollTo(0, 1000)' });
    await new Promise(r => setTimeout(r, 1000));
    await send('Runtime.evaluate', { expression: 'window.scrollTo(0, 2000)' });
    await new Promise(r => setTimeout(r, 2000));

    // Check canvas and reveal states
    const evalResult = await send('Runtime.evaluate', {
      expression: `({
        title: document.title,
        canvasCount: document.querySelectorAll('canvas').length,
        visibleReveals: document.querySelectorAll('[data-visible="true"]').length,
        totalReveals: document.querySelectorAll('[data-reveal]').length,
        buttons: Array.from(document.querySelectorAll('button')).map(b => b.textContent.trim()).filter(Boolean).slice(0, 10)
      })`,
      returnByValue: true
    });

    console.log('Page Evaluation Result:');
    console.log(JSON.stringify(evalResult.result.value, null, 2));

    console.log('\nConsole Logs count:', consoleLogs.length);
    consoleLogs.slice(0, 10).forEach(l => console.log('  ', l));

    console.log('\nRuntime Exceptions count:', errors.length);
    errors.forEach(e => console.log('  ERROR:', e));

    console.log('\nFailed Requests count:', failedRequests.length);

    // Capture screenshot
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(__dirname, 'screenshot_localhost_root.png'), Buffer.from(shot.data, 'base64'));
    console.log('Screenshot saved to screenshot_localhost_root.png');

    // Test clicking navigation link
    console.log('\nTesting navigation to /kham-pha by clicking link...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const link = document.querySelector('a[href="/kham-pha"]');
        if (link) { link.click(); return 'clicked'; }
        return 'link not found';
      })()`
    });
    await new Promise(r => setTimeout(r, 2000));

    const navResult = await send('Runtime.evaluate', {
      expression: `({
        url: window.location.href,
        title: document.title,
        h1: document.querySelector('h1')?.textContent
      })`,
      returnByValue: true
    });
    console.log('Navigation Result:', navResult.result.value);

    console.log('Console Logs after nav count:', consoleLogs.length);
    console.log('Runtime Exceptions after nav count:', errors.length);
    errors.forEach(e => console.log('  ERROR AFTER NAV:', e));

  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
