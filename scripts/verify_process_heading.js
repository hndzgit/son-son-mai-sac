const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9236',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);
  let targets = null;
  for (let i = 0; i < 20; i++) {
    try {
      targets = await fetch('http://localhost:9236/json/list').then(r => r.json());
      if (targets && targets.length) break;
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }
  try {
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const callbacks = new Map();
    const consoleLogs = [];
    let loadFired = null;
    const loadPromise = new Promise(r => { loadFired = r; });

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.method === 'Runtime.consoleAPICalled') {
        consoleLogs.push(msg.params.args.map(a => a.value || a.description).join(' '));
      }
      if (msg.method === 'Page.loadEventFired') {
        if (loadFired) loadFired();
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

    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await loadPromise;
    await new Promise(r => setTimeout(r, 2000));

    // Scroll to section 5-cong-doan
    const evalRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('5-cong-doan');
        if (!el) return { error: 'not found' };
        el.scrollIntoView();
        const heading = document.querySelector('.core-v4-process-heading');
        const rect = heading ? heading.getBoundingClientRect() : null;
        return {
          headingHtml: heading ? heading.outerHTML : null,
          headingText: heading ? heading.innerText : null,
          rect: rect ? { top: rect.top + window.scrollY, left: rect.left, width: rect.width, height: rect.height } : null
        };
      })()`,
      returnByValue: true
    });
    console.log('DOM Evaluation:', JSON.stringify(evalRes.result.value, null, 2));

    await new Promise(r => setTimeout(r, 600));

    // Capture screenshot of #5-cong-doan
    const secEval = await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('5-cong-doan');
        const rect = el.getBoundingClientRect();
        return { x: 0, y: Math.max(0, Math.floor(rect.top + window.scrollY)), width: 1440, height: 450 };
      })()`,
      returnByValue: true
    });

    const clip = secEval.result.value;
    const shot = await send('Page.captureScreenshot', {
      format: 'png',
      clip: { x: clip.x, y: clip.y, width: clip.width, height: clip.height, scale: 1 }
    });
    fs.writeFileSync('scripts/test_process_heading_no_text.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved scripts/test_process_heading_no_text.png');
    console.log('Console logs count:', consoleLogs.length);
    const errors = consoleLogs.filter(l => /error|hydration|mismatch/i.test(l));
    console.log('Hydration / Error logs:', errors);
  } finally {
    chrome.kill();
  }
}
test().catch(console.error);
