const cp = require('child_process');
const fs = require('fs');

async function testClick() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9229',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1080'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9229/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    let id = 1;
    const pending = new Map();
    const send = (method, params = {}) => new Promise(res => {
      const msgId = id++;
      pending.set(msgId, res);
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
    ws.onmessage = e => {
      const m = JSON.parse(e.data);
      if (m.id && pending.has(m.id)) {
        pending.get(m.id)(m.result);
        pending.delete(m.id);
      }
    };
    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');

    console.log('1. Navigating to homepage http://localhost:3000 ...');
    await send('Page.navigate', { url: 'http://localhost:3000' });
    await new Promise(r => setTimeout(r, 2200));

    // Test clicking Card 1 in the Hero: "Sơn mài là gì?"
    console.log('2. Clicking hero feature card: Sơn mài là gì? ...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const card = document.querySelector('a.homeHero_featureCard__BR7Jm[href="/son-mai-la-gi"]');
        if (card) {
          card.click();
          return true;
        }
        return false;
      })()`,
      returnByValue: true
    });

    await new Promise(r => setTimeout(r, 2000));

    const checkUrl = await send('Runtime.evaluate', {
      expression: 'window.location.href',
      returnByValue: true
    });
    console.log('3. Current URL after click:', checkUrl.result.value);

    const pageCheck = await send('Runtime.evaluate', {
      expression: `(() => {
        const h1 = document.querySelector('h1')?.textContent;
        const img = document.querySelector('.sonmai-masterpiece-frame img')?.src;
        return { h1, img };
      })()`,
      returnByValue: true
    });
    console.log('4. Page elements found:', JSON.stringify(pageCheck.result.value, null, 2));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/navigated_son_mai_la_gi.png', Buffer.from(shot.data, 'base64'));
    console.log('Screenshot saved to scripts/navigated_son_mai_la_gi.png');

  } finally {
    chrome.kill();
  }
}
testClick().catch(console.error);
