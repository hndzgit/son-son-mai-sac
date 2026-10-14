const cp = require('child_process');
const fs = require('fs');

async function capture() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9258',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9258/json/list').then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) {
        targets = [valid];
        break;
      }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets[0]) {
    console.error('Failed to get chrome target');
    chrome.kill();
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
    await send('DOM.enable');

    // 1. Check Homepage son-mai-la-gi
    console.log('Navigating to http://localhost:3000/#son-mai-la-gi...');
    await send('Page.navigate', { url: 'http://localhost:3000/#son-mai-la-gi' });
    await new Promise(r => setTimeout(r, 2000));

    // Scroll to #son-mai-la-gi
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('#son-mai-la-gi');
        if (el) el.scrollIntoView({ block: 'start' }); window.scrollBy(0, 50);
      })()`
    });
    await new Promise(r => setTimeout(r, 800));

    let shot = await send('Page.captureScreenshot');
    fs.writeFileSync('scripts/verified_homepage_son_mai.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved scripts/verified_homepage_son_mai.png');

    // Zoomed-in clip of the section
    let clip = await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('#son-mai-la-gi');
        if (!el) return null;
        const rect = el.getBoundingClientRect();
        return { x: Math.max(0, rect.left), y: Math.max(0, rect.top), width: rect.width, height: Math.min(rect.height, 750) };
      })()`,
      returnByValue: true
    });
    if (clip && clip.result && clip.result.value) {
      const clipShot = await send('Page.captureScreenshot', { clip: { ...clip.result.value, scale: 1 } });
      fs.writeFileSync('scripts/verified_son_mai_crop.png', Buffer.from(clipShot.data, 'base64'));
      console.log('Saved scripts/verified_son_mai_crop.png');
    }

    // 2. Check Trai-nghiem son-mai-la-gi
    console.log('Navigating to http://localhost:3000/trai-nghiem#son-mai-la-gi...');
    await send('Page.navigate', { url: 'http://localhost:3000/trai-nghiem#son-mai-la-gi' });
    await new Promise(r => setTimeout(r, 2000));
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('#son-mai-la-gi');
        if (el) el.scrollIntoView({ block: 'start' }); window.scrollBy(0, 50);
      })()`
    });
    await new Promise(r => setTimeout(r, 800));

    shot = await send('Page.captureScreenshot');
    fs.writeFileSync('scripts/verified_trainghiem_son_mai.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved scripts/verified_trainghiem_son_mai.png');

    ws.close();
  } catch(e) {
    console.error('Error during capture:', e);
  } finally {
    chrome.kill();
  }
}

capture();
