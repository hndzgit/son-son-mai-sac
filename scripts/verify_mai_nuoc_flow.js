const cp = require('child_process');
const fs = require('fs');

async function testMobileAndTablet() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9287',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=390,844'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9287/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
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

    // 1. Mobile Test
    await send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true,
      fitWindow: false
    });

    console.log('Testing Mobile (390x844)...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 3500));

    // Dismiss preloader if present
    await send('Runtime.evaluate', {
      expression: `
        const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('BỎ QUA') || el.textContent.includes('Khám phá'));
        if (b) b.click();
      `
    });
    await new Promise(r => setTimeout(r, 1000));

    // Navigate to Stage 3
    await send('Runtime.evaluate', {
      expression: `
        const list = document.querySelectorAll('ol li');
        list.forEach((li, idx) => {
          if (idx === 3 || li.textContent.includes('TRANG TRÍ')) li.click();
        });
        const el = document.getElementById('studio-decoration');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
      `
    });
    await new Promise(r => setTimeout(r, 1200));

    // Scroll to the new "PHỦ SƠN & MÀI NƯỚC" card in Stage 3
    await send('Runtime.evaluate', {
      expression: `
        const card = document.querySelector('.studio_next_step_card');
        if (card) card.scrollIntoView({ behavior: 'instant', block: 'center' });
      `
    });
    await new Promise(r => setTimeout(r, 500));

    // Capture Stage 3 with new Phủ sơn & Mài nước card
    const shotStage3 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verified_mobile_stage3_card.png', Buffer.from(shotStage3.data, 'base64'));
    console.log('Saved scripts/verified_mobile_stage3_card.png');

    // Click "Bước tiếp theo: Phủ sơn & Mài nước →"
    const clickRes = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Phủ sơn & Mài nước'));
          if (btn) {
            btn.click();
            return { clicked: true, text: btn.textContent };
          }
          return { clicked: false };
        })()
      `,
      returnByValue: true
    });
    console.log('Click next result:', clickRes.result.value);
    await new Promise(r => setTimeout(r, 1500));

    // Capture Stage 4 right after transition
    const shotStage4 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verified_mobile_stage4_view.png', Buffer.from(shotStage4.data, 'base64'));
    console.log('Saved scripts/verified_mobile_stage4_view.png');

    // Scroll to grind card
    await send('Runtime.evaluate', {
      expression: `
        const grindCard = document.querySelector('.studio_grind_card');
        if (grindCard) grindCard.scrollIntoView({ behavior: 'instant', block: 'center' });
      `
    });
    await new Promise(r => setTimeout(r, 500));

    // Click Mài nước button
    const grindClick = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const grindBtn = document.querySelector('.studio_main_grind_btn');
          if (grindBtn) {
            grindBtn.click();
            return { clicked: true, text: grindBtn.textContent };
          }
          return { clicked: false };
        })()
      `,
      returnByValue: true
    });
    console.log('Grind button clicked:', grindClick.result.value);
    await new Promise(r => setTimeout(r, 1000));

    // Capture Stage 4 after grinding
    const shotGrinded = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verified_mobile_stage4_grinded.png', Buffer.from(shotGrinded.data, 'base64'));
    console.log('Saved scripts/verified_mobile_stage4_grinded.png');

    // 2. Tablet Test (768x1024)
    console.log('Testing Tablet (768x1024)...');
    await send('Emulation.setDeviceMetricsOverride', {
      width: 768,
      height: 1024,
      deviceScaleFactor: 2,
      mobile: false,
      fitWindow: false
    });
    await new Promise(r => setTimeout(r, 1000));
    const shotTablet = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verified_tablet_stage4.png', Buffer.from(shotTablet.data, 'base64'));
    console.log('Saved scripts/verified_tablet_stage4.png');

    // 3. Desktop Test (1440x900)
    console.log('Testing Desktop (1440x900)...');
    await send('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 2,
      mobile: false,
      fitWindow: false
    });
    await send('Runtime.evaluate', {
      expression: `document.getElementById('simulator')?.scrollIntoView({ behavior: 'instant', block: 'start' });`
    });
    await new Promise(r => setTimeout(r, 1000));
    const shotDesktop = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verified_desktop_stage4.png', Buffer.from(shotDesktop.data, 'base64'));
    console.log('Saved scripts/verified_desktop_stage4.png');

    ws.close();
  } catch(e) {
    console.error('Error during test:', e);
  } finally {
    chrome.kill();
  }
}

testMobileAndTablet();
