const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9277',
    '--remote-allow-origins=*',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1100'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9277/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) {
        targets = [page];
        break;
      }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets.length) {
    chrome.kill();
    console.error('Failed to find Chrome target');
    return;
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

    console.log('Navigating to /kham-pha#process-workshop-panel...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha#process-workshop-panel' });
    await new Promise(r => setTimeout(r, 2500));

    // Scroll to simulator
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('simulator');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
      })()`
    });
    await new Promise(r => setTimeout(r, 1000));

    // Take screenshot of step 1 (red box + golden bg)
    let shot1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/shot_simulator_step1.png', Buffer.from(shot1.data, 'base64'));
    console.log('Saved scripts/shot_simulator_step1.png');

    // Click step 5 in the sidebar
    await send('Runtime.evaluate', {
      expression: `(() => {
        const items = document.querySelectorAll('.productExperience_stageList__k9Koe li');
        if (items && items[4]) {
          const btn = items[4].querySelector('button') || items[4];
          btn.removeAttribute('disabled');
          btn.click();
        }
      })()`
    });
    await new Promise(r => setTimeout(r, 1500));

    // Take screenshot of step 5 (single button check)
    let shot2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/shot_simulator_step5.png', Buffer.from(shot2.data, 'base64'));
    console.log('Saved scripts/shot_simulator_step5.png');

    // Also get the text of all buttons in finishActions
    const checkRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const finishActions = document.querySelector('.productExperience_finishActions___wK4h');
        if (!finishActions) return 'No finishActions found';
        const btns = Array.from(finishActions.querySelectorAll('button'));
        return btns.map(b => b.innerText.trim());
      })()`,
      returnByValue: true
    });
    console.log('FinishActions buttons:', checkRes.result ? checkRes.result.value : checkRes);

  } finally {
    chrome.kill();
  }
}

test().catch(console.error);
