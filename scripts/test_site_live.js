const cp = require('child_process');

async function test(url) {
  console.log(`Checking ${url}...`);
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9290',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1280,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9290/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
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

    const start = Date.now();
    await send('Page.navigate', { url });
    await new Promise(r => setTimeout(r, 3000));

    const evalRes = await send('Runtime.evaluate', {
      expression: '({ title: document.title, url: window.location.href, readyState: document.readyState })',
      returnByValue: true
    });
    console.log(`Result (${Date.now() - start}ms):`, evalRes.result?.value);
    ws.close();
  } finally {
    chrome.kill();
  }
}

async function main() {
  await test('http://localhost:3000/kham-pha#son-mai-la-gi');
  await test('https://son-son-mai-sac-orpin.vercel.app/kham-pha#son-mai-la-gi');
}
main().catch(console.error);
