const cp = require('child_process');
const fs = require('fs');

async function testGrindingVisual() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9286',
    '--no-sandbox',
    '--window-size=400,900' // Test mobile viewport size just like the user's screenshot!
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9286/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

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

  console.log('Navigating to kham-pha...');
  await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
  await new Promise(r => setTimeout(r, 3500));

  // Dismiss intro modal if any
  await send('Runtime.evaluate', {
    expression: `
      const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('BỎ QUA'));
      if (b) b.click();
    `
  });
  await new Promise(r => setTimeout(r, 800));

  // Go directly to stage 4 (Phủ sơn & Mài nước)
  console.log('Navigating to stage 4 (Phủ sơn & Mài nước)...');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const stageListItems = document.querySelectorAll('ol[class*="stageList"] li');
        if (stageListItems && stageListItems[4]) {
          stageListItems[4].click();
        }
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1200));

  // Scroll to studio_grind_card
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const card = document.querySelector('.studio_grind_card');
        if (card) card.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()
    `
  });
  await new Promise(r => setTimeout(r, 800));

  // Capture Screenshot 1: Coated state (before clicking Mài nước)
  const shot1 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/test_mai_nuoc_step1_coated.png', Buffer.from(shot1.data, 'base64'));
  console.log('Saved scripts/test_mai_nuoc_step1_coated.png');

  // Click Mài nước 1 time
  console.log('Clicking Mài nước tap 1...');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const btn = document.querySelector('.studio_main_grind_btn');
        if (btn) btn.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));

  const shot2 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/test_mai_nuoc_step2_tap1.png', Buffer.from(shot2.data, 'base64'));
  console.log('Saved scripts/test_mai_nuoc_step2_tap1.png');

  // Click Mài nước 2 more times (total 3 taps)
  console.log('Clicking Mài nước tap 2 & 3...');
  for (let i = 0; i < 2; i++) {
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          const btn = document.querySelector('.studio_main_grind_btn');
          if (btn) btn.click();
        })()
      `
    });
    await new Promise(r => setTimeout(r, 800));
  }

  const shot3 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/test_mai_nuoc_step3_tap3.png', Buffer.from(shot3.data, 'base64'));
  console.log('Saved scripts/test_mai_nuoc_step3_tap3.png');

  // Move slider to 100%
  console.log('Setting depth slider to 100%...');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const range = document.querySelector('.studio_grind_card input[type="range"]');
        if (range) {
          range.value = 100;
          range.dispatchEvent(new Event('input', { bubbles: true }));
          range.dispatchEvent(new Event('change', { bubbles: true }));
        }
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));

  const shot4 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/test_mai_nuoc_step4_100percent.png', Buffer.from(shot4.data, 'base64'));
  console.log('Saved scripts/test_mai_nuoc_step4_100percent.png');

  // Also scroll up to check the 3D model
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const v = document.querySelector('div[class*="viewer"]');
        if (v) v.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()
    `
  });
  await new Promise(r => setTimeout(r, 800));

  const shot5 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/test_mai_nuoc_step5_3d_view.png', Buffer.from(shot5.data, 'base64'));
  console.log('Saved scripts/test_mai_nuoc_step5_3d_view.png');

  ws.close();
  chrome.kill();
  console.log('Test completed successfully!');
}

testGrindingVisual().catch(e => {
  console.error('Error:', e);
  process.exit(1);
});
