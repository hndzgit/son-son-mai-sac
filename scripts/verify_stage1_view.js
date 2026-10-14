const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9228',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1400,1200',
    '--user-data-dir=/tmp/chrome-test-stage1-3'
  ]);

  await new Promise(r => setTimeout(r, 1200));

  try {
    const targets = await fetch('http://127.0.0.1:9228/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension')) || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

    let id = 1;
    const pending = new Map();
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const msgId = id++;
      pending.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id).resolve(msg.result);
        pending.delete(msg.id);
      }
    };

    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');

    console.log('Navigating to http://localhost:3000/kham-pha ...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    // Wait for hydration and React state
    await new Promise(r => setTimeout(r, 4500));

    // Scroll callout into view
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('.studio_core_callout');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()`
    });
    await new Promise(r => setTimeout(r, 600));

    // Initial state
    const initRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const callout = document.querySelector('.studio_core_callout');
        return {
          calloutStrong: callout ? callout.querySelector('strong')?.textContent : null,
          calloutText: callout ? callout.querySelector('p')?.textContent : null
        };
      })()`,
      returnByValue: true
    });
    console.log('Initial callout:', initRes.result.value);

    // Click Tre button
    const clickTre = await send('Runtime.evaluate', {
      expression: `(() => {
        const btns = Array.from(document.querySelectorAll('.productExperience_materialChoices__hbtcl button'));
        const treBtn = btns.find(b => b.textContent.includes('Tre'));
        if (treBtn) {
          treBtn.click();
          return { clicked: true, text: treBtn.textContent.trim() };
        }
        return { clicked: false, count: btns.length };
      })()`,
      returnByValue: true
    });
    console.log('Click Tre:', clickTre.result.value);
    await new Promise(r => setTimeout(r, 600));

    // State after click
    const afterTre = await send('Runtime.evaluate', {
      expression: `(() => {
        const callout = document.querySelector('.studio_core_callout');
        return {
          calloutStrong: callout ? callout.querySelector('strong')?.textContent : null,
          calloutText: callout ? callout.querySelector('p')?.textContent : null
        };
      })()`,
      returnByValue: true
    });
    console.log('After Tre click:', afterTre.result.value);

    // Click cotton checkbox
    await send('Runtime.evaluate', {
      expression: `(() => {
        const cb = document.querySelector('.studio_reinforce_check input[type=\"checkbox\"]');
        if (cb) cb.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 600));

    const ss = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/stage1_enhanced_centered.png', Buffer.from(ss.data, 'base64'));
    console.log('Saved scripts/stage1_enhanced_centered.png');

  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
