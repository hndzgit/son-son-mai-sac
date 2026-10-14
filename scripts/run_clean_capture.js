const cp = require('child_process');
const fs = require('fs');

async function main() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9298',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1100'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      const list = await fetch('http://localhost:9298/json/list').then(r => r.json());
      const page = list && list.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets) {
    chrome.kill();
    throw new Error('Chrome target not found');
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

    console.log('Navigating to http://localhost:3000/kham-pha...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 3000));

    // Scroll to workshop
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('.productExperience_studioWorkspace__is27_');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    // 1. Stage 01 Screenshot
    const s1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/stage01_verified.png', Buffer.from(s1.data, 'base64'));
    console.log('1. Captured stage01_verified.png');

    // 2. Stage 02: Click stage 2
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_stageList__k9Koe li')[1]?.click()`
    });
    await new Promise(r => setTimeout(r, 600));
    const s2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/stage02_verified.png', Buffer.from(s2.data, 'base64'));
    console.log('2. Captured stage02_verified.png');

    // 3. Stage 03: Click stage 3
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_stageList__k9Koe li')[2]?.click()`
    });
    await new Promise(r => setTimeout(r, 600));
    const s3 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/stage03_verified.png', Buffer.from(s3.data, 'base64'));
    console.log('3. Captured stage03_verified.png');

    // 4. Stage 04: Click stage 4
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_stageList__k9Koe li')[3]?.click()`
    });
    await new Promise(r => setTimeout(r, 600));
    const s4 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/stage04_verified.png', Buffer.from(s4.data, 'base64'));
    console.log('4. Captured stage04_verified.png');

    // 5. Stage 05: Click stage 5
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_stageList__k9Koe li')[4]?.click()`
    });
    await new Promise(r => setTimeout(r, 600));

    // Test clicking "Mài nước"
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Mài nước'));
        if (btn) btn.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 300));

    // Test clicking "Đánh bóng"
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Đánh bóng'));
        if (btn) btn.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 300));

    const s5 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/stage05_verified.png', Buffer.from(s5.data, 'base64'));
    console.log('5. Captured stage05_verified.png');

    const statusMsg = await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_message__RzW2A')?.innerText || ''`,
      returnByValue: true
    });
    console.log('Final Status Message:', statusMsg.result.value);

    ws.close();
    console.log('ALL COMPLETE!');
  } finally {
    chrome.kill();
  }
}

main().catch(console.error);
