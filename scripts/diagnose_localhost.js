const cp = require('child_process');
const fs = require('fs');
const path = require('path');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9225',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);

  await new Promise(r => setTimeout(r, 1000));

  try {
    const targets = await fetch('http://localhost:9225/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

    let id = 1;
    const pending = new Map();
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const msgId = id++;
      pending.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });

    const networkEvents = [];
    const failedRequests = [];
    const consoleLogs = [];
    const errors = [];

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
      if (msg.method === 'Network.responseReceived') {
        networkEvents.push({
          url: msg.params.response.url,
          status: msg.params.response.status,
          mime: msg.params.response.mimeType,
          headers: msg.params.response.headers
        });
      }
      if (msg.method === 'Network.loadingFailed') {
        failedRequests.push({
          requestId: msg.params.requestId,
          errorText: msg.params.errorText,
          canceled: msg.params.canceled
        });
      }
    };

    await new Promise(r => ws.onopen = r);

    await send('Page.enable');
    await send('Runtime.enable');
    await send('Network.enable');

    console.log('Navigating to http://localhost:3000/ ...');
    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 5000));

    await send('Runtime.evaluate', { expression: 'window.scrollTo(0, 1500)' });
    await new Promise(r => setTimeout(r, 3000));

    console.log('--- Network Responses (Total: ' + networkEvents.length + ') ---');
    networkEvents.forEach(n => {
      if (n.status >= 400 || n.url.includes('_rsc') || n.url.includes('chunk') || n.url.includes('api') || n.url.includes('model')) {
        console.log(`STATUS ${n.status} [${n.mime}] ${n.url}`);
      }
    });

    console.log('\n--- Failed Requests (Total: ' + failedRequests.length + ') ---');
    failedRequests.forEach(f => console.log('  Failed:', f));

    console.log('\n--- Console Logs (Total: ' + consoleLogs.length + ') ---');
    consoleLogs.forEach(c => console.log('  Log:', c));

    console.log('\n--- Exceptions (Total: ' + errors.length + ') ---');
    errors.forEach(e => console.log('  Error:', e));

    const domInfo = await send('Runtime.evaluate', {
      expression: `({
        viewerHtml: document.querySelector('[data-journey-phase]')?.innerHTML,
        loadingText: document.querySelector('.homeSurfaceExperience_loading__5p3s3')?.textContent || document.querySelector('[class*="loading"]')?.textContent,
        reveals: Array.from(document.querySelectorAll('[data-reveal]')).map(el => ({
          visible: el.getAttribute('data-visible'),
          class: el.className
        }))
      })`,
      returnByValue: true
    });

    console.log('\n--- DOM Info ---');
    console.log(JSON.stringify(domInfo.result.value, null, 2));

  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
