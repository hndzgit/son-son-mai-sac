const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9231',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);
  let targets = null;
  for (let i = 0; i < 20; i++) {
    try {
      targets = await fetch('http://localhost:9231/json/list').then(r => r.json());
      if (targets && targets.length) break;
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }
  try {
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const callbacks = new Map();
    const errors = [];
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg.result);
        callbacks.delete(msg.id);
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        errors.push(msg.params.exceptionDetails.text);
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
    await new Promise(r => setTimeout(r, 3000));

    const data = await send('Runtime.evaluate', {
      expression: `({
        heroTitle: document.querySelector('h1')?.innerText,
        cards: Array.from(document.querySelectorAll('.homeHero_featureCard__BR7Jm strong')).map(s => s.innerText)
      })`,
      returnByValue: true
    });
    console.log('Updated Page DOM:');
    console.log(JSON.stringify(data.result.value, null, 2));
    console.log('Runtime exceptions count:', errors.length);

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/screenshot_slide1_updated.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved screenshot_slide1_updated.png');
  } finally {
    chrome.kill();
  }
}
test().catch(console.error);
