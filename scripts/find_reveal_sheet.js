const cp = require('child_process');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9247',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9247/json/list').then(r => r.json());
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

    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 2000));

    const styles = await send('Runtime.evaluate', {
      expression: `(() => {
        const styles = Array.from(document.querySelectorAll('style'));
        return styles.map((s, idx) => ({
          idx,
          id: s.id,
          cls: s.className,
          snippet: s.textContent.slice(0, 300),
          length: s.textContent.length,
          containsReveal: s.textContent.includes('data-reveal')
        }));
      })()`,
      returnByValue: true
    });

    console.log('Style tags:', JSON.stringify(styles.result.value, null, 2));

    const sheetUrls = await send('Runtime.evaluate', {
      expression: `(() => {
        return Array.from(document.styleSheets).map((s, idx) => {
          let rulesCount = 0;
          let revealRule = false;
          try {
            rulesCount = s.cssRules.length;
            revealRule = Array.from(s.cssRules).some(r => r.cssText && r.cssText.includes('data-reveal'));
          } catch(e) {}
          return {
            idx,
            href: s.href,
            rulesCount,
            revealRule
          };
        });
      })()`,
      returnByValue: true
    });

    console.log('StyleSheets:', JSON.stringify(sheetUrls.result.value, null, 2));

  } finally {
    chrome.kill();
  }
}

test().catch(console.error);
