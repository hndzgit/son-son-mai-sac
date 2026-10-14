const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9225',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1200'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9225/json/list').then(r => r.json());
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

    console.log('Navigating to http://localhost:3000/cau-chuyen-son-mai...');
    await send('Page.navigate', { url: 'http://localhost:3000/cau-chuyen-son-mai' });
    await new Promise(r => setTimeout(r, 2000));

    // Test 1: Count cards initially
    const check1 = await send('Runtime.evaluate', {
      expression: 'document.querySelectorAll(".artisan_zigzag_card").length',
      returnByValue: true
    });
    console.log('1. Initial card count:', check1.result.value);

    // Test 2: Click tab 4 (Làng nghề / Nghệ nhân)
    console.log('2. Clicking tab 4...');
    await send('Runtime.evaluate', {
      expression: 'document.getElementById("timeline-tab-4")?.click()'
    });
    await new Promise(r => setTimeout(r, 500));

    const check2 = await send('Runtime.evaluate', {
      expression: 'document.querySelectorAll(".artisan_zigzag_card").length',
      returnByValue: true
    });
    console.log('After tab 4 click, card count:', check2.result.value);

    // Test 3: Scroll to artisan section
    console.log('3. Scrolling to artisan section...');
    await send('Runtime.evaluate', {
      expression: 'document.querySelector(".story_inspiration__LM_OE")?.scrollIntoView({ behavior: "instant", block: "center" })'
    });
    await new Promise(r => setTimeout(r, 500));

    const check3 = await send('Runtime.evaluate', {
      expression: `Array.from(document.querySelectorAll(".artisan_zigzag_card")).map(c => ({
        name: c.querySelector(".artisan_name")?.textContent,
        opacity: window.getComputedStyle(c).opacity,
        display: window.getComputedStyle(c).display,
        visibility: window.getComputedStyle(c).visibility,
        height: c.getBoundingClientRect().height
      }))`,
      returnByValue: true
    });
    console.log('Cards details:', JSON.stringify(check3.result.value, null, 2));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/artisan_verified_stable.png', Buffer.from(shot.data, 'base64'));
    console.log('Screenshot saved to scripts/artisan_verified_stable.png');

  } finally {
    chrome.kill();
  }
}
test().catch(console.error);
