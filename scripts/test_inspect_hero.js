const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9226',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);
  await new Promise(r => setTimeout(r, 1500));
  try {
    const targets = await fetch('http://localhost:9226/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
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

    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 2000));

    await send('Runtime.evaluate', {
      expression: '(() => { const p = document.querySelector(".core-v4-preloader, [data-preloader]"); if (p) p.remove(); })()'
    });
    await new Promise(r => setTimeout(r, 1000));

    const sections = await send('Runtime.evaluate', {
      expression: `(() => {
        return Array.from(document.querySelectorAll('section')).map(s => ({
          tag: s.tagName,
          className: s.className,
          id: s.id,
          width: s.getBoundingClientRect().width,
          maxWidth: window.getComputedStyle(s).maxWidth,
          margin: window.getComputedStyle(s).margin,
          padding: window.getComputedStyle(s).padding
        }));
      })()`,
      returnByValue: true
    });
    console.log('Home sections:', JSON.stringify(sections.result.value, null, 2));

    ws.close();
  } finally {
    chrome.kill();
  }
}
run();
