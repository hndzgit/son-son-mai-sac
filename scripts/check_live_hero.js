const cp = require('child_process');
const fs = require('fs');

async function checkLiveHero() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9257',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,1100'
  ]);

  for (let i = 0; i < 30; i++) {
    try {
      const targets = await fetch('http://localhost:9257/json/list').then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) break;
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  const targets = await fetch('http://localhost:9257/json/list').then(r => r.json());
  const validTarget = targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
  const ws = new WebSocket(validTarget.webSocketDebuggerUrl);

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

  await send('Page.navigate', { url: 'https://son-son-mai-sac-orpin.vercel.app/ve-du-an#son-son-mai-sac' });
  await new Promise(r => setTimeout(r, 3000));

  const check = await send('Runtime.evaluate', {
    expression: `(() => {
      const imgs = Array.from(document.querySelectorAll('img')).map(img => ({
        src: img.src,
        complete: img.complete,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
        isBroken: img.complete && img.naturalWidth === 0
      }));
      return {
        broken: imgs.filter(i => i.isBroken),
        total: imgs.length
      };
    })()`,
    returnByValue: true
  });
  console.log('Live check results:', JSON.stringify(check.result.value, null, 2));

  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/live_prod_hero_fixed.png', Buffer.from(shot.data, 'base64'));
  console.log('Saved scripts/live_prod_hero_fixed.png');

  chrome.kill();
}

checkLiveHero().catch(console.error);
