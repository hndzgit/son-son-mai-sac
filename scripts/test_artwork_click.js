const cp = require('child_process');
const fs = require('fs');

async function testArtworkClick() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9233',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1080'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9233/json/list').then(r => r.json());
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

    console.log('1. Navigating to homepage...');
    await send('Page.navigate', { url: 'http://localhost:3000' });
    await new Promise(r => setTimeout(r, 2000));

    // Scroll to son-mai-la-gi section
    await send('Runtime.evaluate', {
      expression: 'document.getElementById("son-mai-la-gi")?.scrollIntoView({ behavior: "instant", block: "center" })'
    });
    await new Promise(r => setTimeout(r, 500));

    // Click artwork link
    console.log('2. Clicking artwork figure in section...');
    await send('Runtime.evaluate', {
      expression: 'document.querySelector(".coreIntroduction_artworkLink")?.click()'
    });
    await new Promise(r => setTimeout(r, 1500));

    const checkUrl = await send('Runtime.evaluate', {
      expression: 'window.location.href',
      returnByValue: true
    });
    console.log('3. Current URL after clicking artwork:', checkUrl.result.value);

    // Now test navigating back and clicking definition CTA
    console.log('4. Navigating back to homepage...');
    await send('Page.navigate', { url: 'http://localhost:3000' });
    await new Promise(r => setTimeout(r, 1500));

    console.log('5. Clicking definition CTA button...');
    await send('Runtime.evaluate', {
      expression: 'document.querySelector(".coreIntroduction_definitionCta")?.click()'
    });
    await new Promise(r => setTimeout(r, 1500));

    const checkUrl2 = await send('Runtime.evaluate', {
      expression: 'window.location.href',
      returnByValue: true
    });
    console.log('6. Current URL after clicking definition CTA:', checkUrl2.result.value);

  } finally {
    chrome.kill();
  }
}
testArtworkClick().catch(console.error);
