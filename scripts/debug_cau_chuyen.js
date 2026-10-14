const cp = require('child_process');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9228',
    '--disable-gpu',
    '--no-sandbox'
  ]);
  await new Promise(r => setTimeout(r, 1000));
  try {
    const targets = await fetch('http://localhost:9228/json/list').then(r => r.json());
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const callbacks = new Map();
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg.result);
        callbacks.delete(msg.id);
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        console.log('--- RUNTIME EXCEPTION ---');
        console.log(msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text);
      }
      if (msg.method === 'Runtime.consoleAPICalled') {
        console.log(`[CONSOLE ${msg.params.type}]`, msg.params.args.map(a => a.value || JSON.stringify(a)).join(' '));
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
    console.log('Navigating to http://localhost:3000/cau-chuyen-son-mai ...');
    await send('Page.navigate', { url: 'http://localhost:3000/cau-chuyen-son-mai' });
    await new Promise(r => setTimeout(r, 4000));

    console.log('\nNow checking live https://son-son-mai-sac-orpin.vercel.app/cau-chuyen-son-mai ...');
    await send('Page.navigate', { url: 'https://son-son-mai-sac-orpin.vercel.app/cau-chuyen-son-mai' });
    await new Promise(r => setTimeout(r, 4000));

  } finally {
    chrome.kill();
  }
}
run().catch(console.error);
