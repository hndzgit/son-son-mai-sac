const cp = require('child_process');

async function testLive() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9255',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9255/json/list').then(r => r.json());
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

    await send('Page.navigate', { url: 'https://sonsonmaisac.site/tin-tuc-su-kien' });
    await new Promise(r => setTimeout(r, 3500));

    const evalResult = await send('Runtime.evaluate', {
      expression: `(() => {
        const h1 = document.getElementById('news-title');
        const p = h1 ? h1.parentElement.querySelector('p') : null;
        const disclaimerEl = document.querySelector('.eventProgramme_disclaimer__5a0ST');
        const textFound = document.body.innerText.includes('Ngày, địa điểm và trạng thái có thể thay đổi');
        return {
          h1TextAlign: h1 ? window.getComputedStyle(h1).textAlign : null,
          disclaimerElExists: !!disclaimerEl,
          textFound: textFound
        };
      })()`,
      returnByValue: true
    });

    console.log("Live Production Verification:", JSON.stringify(evalResult.result.value, null, 2));

    ws.close();
  } catch(e) {
    console.error(e);
  } finally {
    chrome.kill();
  }
}

testLive();
