const cp = require('child_process');

async function checkSite(url) {
  console.log(`\n=== Checking ${url} ===`);
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9291',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1280,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9291/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets) {
    chrome.kill();
    console.log('Failed to start Chrome');
    return;
  }

  try {
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const callbacks = new Map();
    const errors = [];
    const failedRequests = [];

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.method === 'Runtime.exceptionThrown') {
        errors.push(msg.params.exceptionDetails);
      }
      if (msg.method === 'Log.entryAdded' && msg.params.entry.level === 'error') {
        errors.push(msg.params.entry.text);
      }
      if (msg.method === 'Network.loadingFailed') {
        failedRequests.push({ url: msg.params.url, errorText: msg.params.errorText });
      }
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
    await send('Log.enable');
    await send('Network.enable');

    const navRes = await send('Page.navigate', { url });
    console.log('Navigate response:', navRes);
    await new Promise(r => setTimeout(r, 4000));

    const title = await send('Runtime.evaluate', { expression: 'document.title', returnByValue: true });
    console.log('Page title:', title.result?.value);
    console.log('Errors caught:', errors.length);
    if (errors.length) console.log('Errors details:', JSON.stringify(errors.slice(0, 5), null, 2));
    console.log('Failed network requests:', failedRequests.length);
    if (failedRequests.length) console.log('Failed requests:', JSON.stringify(failedRequests.slice(0, 5), null, 2));

    ws.close();
  } finally {
    chrome.kill();
  }
}

async function run() {
  await checkSite('http://localhost:3000/');
  await checkSite('http://localhost:3000/kham-pha');
  await checkSite('https://son-son-mai-sac-orpin.vercel.app/');
  await checkSite('https://son-son-mai-sac-orpin.vercel.app/kham-pha');
}

run().catch(console.error);
