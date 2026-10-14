const cp = require('child_process');
const fs = require('fs');

async function testFullJourney() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9288',
    '--no-sandbox',
    '--window-size=400,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9288/json/list').then(r => r.json());
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

  console.log('Navigating to /kham-pha...');
  await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
  await new Promise(r => setTimeout(r, 3500));

  // Dismiss modal
  await send('Runtime.evaluate', {
    expression: `
      const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('BỎ QUA'));
      if (b) b.click();
    `
  });
  await new Promise(r => setTimeout(r, 800));

  // Step 1: In simulator, click "Bắt đầu làm vóc"
  console.log('Step 1: Advancing to stage 1 (Làm vóc)...');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const advBtn = document.querySelector('button[class*="advanceButton"]');
        if (advBtn) advBtn.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 800));

  // Step 2: In stage 1, click "Sang sơn nền"
  console.log('Step 2: Advancing to stage 2 (Sơn nền)...');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const advBtn = document.querySelector('button[class*="advanceButton"]');
        if (advBtn) advBtn.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 800));

  // Step 3: In stage 2, click "Tiếp tục tạo hình"
  console.log('Step 3: Advancing to stage 3 (Tạo hình & trang trí)...');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const advBtn = document.querySelector('button[class*="advanceButton"]');
        if (advBtn) advBtn.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));

  // In stage 3: select material "Vàng quỳ" and motif "Hoa sen"
  console.log('Step 3 details: selecting Vàng quỳ and Hoa sen...');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const matBtns = Array.from(document.querySelectorAll('div[class*="materialChoices"] button'));
        const goldBtn = matBtns.find(b => b.textContent.includes('Vàng quỳ'));
        if (goldBtn) goldBtn.click();

        const motifBtns = Array.from(document.querySelectorAll('div[class*="motifChoices"] button'));
        const lotusBtn = motifBtns.find(b => b.textContent.includes('Hoa sen'));
        if (lotusBtn) lotusBtn.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));

  // Scroll to advance button in stage 3
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const card = document.querySelector('.studio_next_step_card') || document.querySelector('button[class*="advanceButton"]');
        if (card) card.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()
    `
  });
  await new Promise(r => setTimeout(r, 500));

  const shotStage3 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/journey_step3_decorated.png', Buffer.from(shotStage3.data, 'base64'));
  console.log('Saved scripts/journey_step3_decorated.png');

  // Step 4: Click "Bước tiếp theo: Phủ sơn & Mài nước"
  console.log('Step 4: Advancing to stage 4 (Phủ sơn & Mài nước)...');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Phủ sơn & Mài nước') || b.textContent.includes('Bước tiếp theo'));
        if (nextBtn) nextBtn.click();
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
  await new Promise(r => setTimeout(r, 600));

  const shotStage4Coated = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/journey_step4_coated.png', Buffer.from(shotStage4Coated.data, 'base64'));
  console.log('Saved scripts/journey_step4_coated.png');

  // Now click "💧 MÀI NƯỚC · NHẤN ĐỂ MÀI LỘ HOA VĂN" tap 1
  console.log('Tapping MÀI NƯỚC 1 time...');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const btn = document.querySelector('.studio_main_grind_btn');
        if (btn) btn.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 800));

  const shotStage4Tap1 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/journey_step4_tap1.png', Buffer.from(shotStage4Tap1.data, 'base64'));
  console.log('Saved scripts/journey_step4_tap1.png');

  // Tap MÀI NƯỚC 3 more times
  console.log('Tapping MÀI NƯỚC 3 more times...');
  for (let i = 0; i < 3; i++) {
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          const btn = document.querySelector('.studio_main_grind_btn');
          if (btn) btn.click();
        })()
      `
    });
    await new Promise(r => setTimeout(r, 600));
  }

  const shotStage4Tap4 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/journey_step4_tap4.png', Buffer.from(shotStage4Tap4.data, 'base64'));
  console.log('Saved scripts/journey_step4_tap4.png');

  // Tap MÀI NƯỚC to reach 100%
  console.log('Tapping MÀI NƯỚC to reach 100%...');
  for (let i = 0; i < 3; i++) {
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          const btn = document.querySelector('.studio_main_grind_btn');
          if (btn) btn.click();
        })()
      `
    });
    await new Promise(r => setTimeout(r, 500));
  }

  const shotStage4100 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/journey_step4_100percent.png', Buffer.from(shotStage4100.data, 'base64'));
  console.log('Saved scripts/journey_step4_100percent.png');

  ws.close();
  chrome.kill();
  console.log('Full journey test completed!');
}

testFullJourney().catch(e => {
  console.error('Test error:', e);
  process.exit(1);
});
