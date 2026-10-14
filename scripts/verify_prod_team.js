const cp = require('child_process');
const fs = require('fs');

async function capture() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9254',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,1100'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9254/json/list').then(r => r.json());
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

    await send('Page.navigate', { url: 'https://son-son-mai-sac-orpin.vercel.app/ve-du-an' });
    await new Promise(r => setTimeout(r, 3000));

    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('doi-ngu');
        if (el) el.scrollIntoView({ block: 'start', behavior: 'instant' });
      })()`
    });
    await new Promise(r => setTimeout(r, 1200));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verified_live_circular_team.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved scripts/verified_live_circular_team.png');
  } finally {
    chrome.kill();
  }
}

capture().catch(console.error);
