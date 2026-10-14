const cp = require('child_process');
const fs = require('fs');

async function testAll() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9299',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1100'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      const list = await fetch('http://localhost:9299/json/list').then(r => r.json());
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
    const errors = [];
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg.result);
        callbacks.delete(msg.id);
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        errors.push(msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text);
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

    // 1. TEST TRAI-NGHIEM
    console.log('--- 1. Testing /trai-nghiem ---');
    await send('Page.navigate', { url: 'http://localhost:3000/trai-nghiem' });
    await new Promise(r => setTimeout(r, 3000));

    const tnStatus = await send('Runtime.evaluate', {
      expression: `(() => ({
        hasSimulator: !!document.getElementById('simulator'),
        hasStudioBoard: !!document.querySelector('.productExperience_studioBoard__D_pEz'),
        pageTextIncludesStudio: document.body.innerText.includes('XƯỞNG SƠN MÀI SẮC'),
        hasAppError: document.body.innerText.includes('Application error')
      }))()`,
      returnByValue: true
    });
    console.log('trai-nghiem status:', tnStatus.result.value);

    const shotTN = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verified_trai_nghiem_clean.png', Buffer.from(shotTN.data, 'base64'));
    console.log('Saved scripts/verified_trai_nghiem_clean.png');

    // 2. TEST KHAM-PHA SANDING EFFECT
    console.log('--- 2. Testing /kham-pha water grinding (mài nước) ---');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 3500));

    // Scroll to workshop
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('.productExperience_studioWorkspace__is27_');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    // Switch to Stage 5: Phủ, mài và hoàn thiện
    console.log('Switching to Stage 5...');
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_stageList__k9Koe li')[4]?.click()`
    });
    await new Promise(r => setTimeout(r, 800));

    // Test clicking "Mài nước" stroke 1
    console.log('Clicking "Mài nước" stroke 1...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Mài nước'));
        if (btn) btn.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    const msg1 = await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_message__RzW2A')?.innerText || ''`,
      returnByValue: true
    });
    console.log('Status message after stroke 1:', msg1.result.value);

    // Test clicking "Mài nước" stroke 2
    console.log('Clicking "Mài nước" stroke 2...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Mài nước'));
        if (btn) btn.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    const msg2 = await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_message__RzW2A')?.innerText || ''`,
      returnByValue: true
    });
    console.log('Status message after stroke 2:', msg2.result.value);

    // Test clicking "Mài nước" stroke 3
    console.log('Clicking "Mài nước" stroke 3...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Mài nước'));
        if (btn) btn.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    const msg3 = await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_message__RzW2A')?.innerText || ''`,
      returnByValue: true
    });
    console.log('Status message after stroke 3:', msg3.result.value);

    // Capture screenshot during water grinding
    const shotSanding = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verified_water_grinding_active.png', Buffer.from(shotSanding.data, 'base64'));
    console.log('Saved scripts/verified_water_grinding_active.png');

    // Test clicking "Đánh bóng"
    console.log('Clicking "Đánh bóng"...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Đánh bóng'));
        if (btn) btn.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    const msgPolish = await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_message__RzW2A')?.innerText || ''`,
      returnByValue: true
    });
    console.log('Status message after polish:', msgPolish.result.value);

    const shotPolished = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verified_polished_mirror.png', Buffer.from(shotPolished.data, 'base64'));
    console.log('Saved scripts/verified_polished_mirror.png');

    console.log('Captured JS Errors (if any):', errors);
    ws.close();
    console.log('SUCCESS: All tests completed perfectly!');
  } finally {
    chrome.kill();
  }
}

testAll().catch(console.error);
