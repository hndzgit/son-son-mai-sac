const cp = require('child_process');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9250',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions'
  ]);

  for (let i = 0; i < 30; i++) {
    try {
      const targets = await fetch('http://localhost:9250/json/list').then(r => r.json());
      if (targets && targets.length) break;
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  const targets = await fetch('http://localhost:9250/json/list').then(r => r.json());
  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  let id = 1;
  const callbacks = new Map();
  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.id && callbacks.has(msg.id)) {
      callbacks.get(msg.id)(msg.result);
      callbacks.delete(msg.id);
    }
    if (msg.method === 'Network.responseReceived') {
      if (msg.params.response.url.includes('dan-le')) {
        console.log('dan-le response:', msg.params.response.status, msg.params.response.url);
      }
    }
    if (msg.method === 'Network.loadingFailed') {
      console.log('loadingFailed:', msg.params.errorText, msg.params.canceled);
    }
  };
  const send = (method, params = {}) => new Promise(res => {
    const msgId = id++;
    callbacks.set(msgId, res);
    ws.send(JSON.stringify({ id: msgId, method, params }));
  });
  await new Promise(r => ws.onopen = r);
  await send('Page.enable');
  await send('Network.enable');

  await send('Page.navigate', { url: 'http://localhost:3000/ve-du-an' });
  await new Promise(r => setTimeout(r, 2000));

  const imgInfo = await send('Runtime.evaluate', {
    expression: `(() => {
      const img = document.querySelector('.team-portrait-v4-card.is-featured img');
      return {
        src: img ? img.src : null,
        currentSrc: img ? img.currentSrc : null,
        complete: img ? img.complete : null,
        naturalWidth: img ? img.naturalWidth : null,
        naturalHeight: img ? img.naturalHeight : null
      };
    })()`,
    returnByValue: true
  });
  console.log('dan-le img element info:', imgInfo.result.value);

  chrome.kill();
}

test().catch(console.error);
