const cp = require('child_process');
const fs = require('fs');

async function capture() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9256',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9256/json/list').then(r => r.json());
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

    // 1. Check Trai-nghiem - son-mai-la-gi
    console.log('Navigating to http://localhost:3000/trai-nghiem...');
    await send('Page.navigate', { url: 'http://localhost:3000/trai-nghiem' });
    await new Promise(r => setTimeout(r, 2500));

    // Screenshot of son-mai-la-gi
    let clip = await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('#son-mai-la-gi');
        if (!el) return null;
        const rect = el.getBoundingClientRect();
        return { x: rect.left, y: rect.top, width: rect.width, height: rect.height };
      })()`,
      returnByValue: true
    });
    if (clip && clip.result && clip.result.value) {
      const shot = await send('Page.captureScreenshot', { clip: { ...clip.result.value, scale: 1 } });
      fs.writeFileSync('scripts/verify_son_mai_la_gi.png', Buffer.from(shot.data, 'base64'));
      console.log('Saved scripts/verify_son_mai_la_gi.png');
    }

    // Screenshot of core-v4-heritage ("Phủ lên để rồi mài đi")
    clip = await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('.core-v4-heritage');
        if (!el) return null;
        el.scrollIntoView();
        const rect = el.getBoundingClientRect();
        return { x: rect.left, y: rect.top + window.scrollY, width: rect.width, height: rect.height };
      })()`,
      returnByValue: true
    });
    await new Promise(r => setTimeout(r, 1000));
    const shotHeritage = await send('Page.captureScreenshot');
    fs.writeFileSync('scripts/verify_heritage_section.png', Buffer.from(shotHeritage.data, 'base64'));
    console.log('Saved scripts/verify_heritage_section.png');

    // 2. Check tin-tuc-su-kien
    console.log('Navigating to http://localhost:3000/tin-tuc-su-kien...');
    await send('Page.navigate', { url: 'http://localhost:3000/tin-tuc-su-kien' });
    await new Promise(r => setTimeout(r, 2000));

    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('#su-kien');
        if (el) el.scrollIntoView();
      })()`
    });
    await new Promise(r => setTimeout(r, 1000));
    const shotNews = await send('Page.captureScreenshot');
    fs.writeFileSync('scripts/verify_news_events.png', Buffer.from(shotNews.data, 'base64'));
    console.log('Saved scripts/verify_news_events.png');

    ws.close();
  } catch(e) {
    console.error('Error during capture:', e);
  } finally {
    chrome.kill();
  }
}

capture();
