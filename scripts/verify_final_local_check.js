const cp = require('child_process');
const fs = require('fs');

async function testDesktopAndMobile() {
  // 1. Mobile verification
  console.log('--- Testing Mobile View (390x844) ---');
  const chromeMob = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9289',
    '--no-sandbox',
    '--window-size=390,844'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9289/json/list').then(r => r.json());
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

  // Advance stages to Stage 3
  for (let s = 0; s < 3; s++) {
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          const advBtn = document.querySelector('button[class*="advanceButton"]');
          if (advBtn) advBtn.click();
        })()
      `
    });
    await new Promise(r => setTimeout(r, 700));
  }

  // Select Lotus motif and Gold inlay
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
  await new Promise(r => setTimeout(r, 800));

  // Advance to Stage 4 (Phủ sơn & Mài nước)
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Phủ sơn & Mài nước') || b.textContent.includes('Bước tiếp theo'));
        if (nextBtn) nextBtn.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));

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

  const shotMobCoated = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/check_mobile_stage4_coated.png', Buffer.from(shotMobCoated.data, 'base64'));
  console.log('Saved scripts/check_mobile_stage4_coated.png');

  // Click MÀI NƯỚC twice
  for (let i = 0; i < 2; i++) {
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

  const shotMobMid = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/check_mobile_stage4_grinding.png', Buffer.from(shotMobMid.data, 'base64'));
  console.log('Saved scripts/check_mobile_stage4_grinding.png');

  // Slide to 100%
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
  await new Promise(r => setTimeout(r, 800));

  const shotMobDone = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/check_mobile_stage4_done.png', Buffer.from(shotMobDone.data, 'base64'));
  console.log('Saved scripts/check_mobile_stage4_done.png');

  ws.close();
  chromeMob.kill();
  console.log('Mobile verification finished successfully!');
}

testDesktopAndMobile().catch(e => {
  console.error('Check error:', e);
  process.exit(1);
});
