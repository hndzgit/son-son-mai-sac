const cp = require('child_process');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9245',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1200,800'
  ]);
  let targets = null;
  for (let i = 0; i < 20; i++) {
    try {
      targets = await fetch('http://localhost:9245/json/list').then(r => r.json());
      if (targets && targets.length) break;
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
        callbacks.get(msg.id)(msg);
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

    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 2000));

    const res = await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('#core-v4-home-title');
        const rules = [];
        for (const sheet of document.styleSheets) {
          try {
            for (const r of sheet.cssRules) {
              if (r.selectorText && el.matches(r.selectorText)) {
                rules.push({ selector: r.selectorText, href: sheet.href, css: r.cssText });
              }
            }
          } catch(e){}
        }
        return rules;
      })()`,
      returnByValue: true
    });
    console.log(JSON.stringify(res.result.result.value, null, 2));
  } finally {
    chrome.kill();
  }
}
test().catch(console.error);
