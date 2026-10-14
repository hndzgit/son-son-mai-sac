const cp = require('child_process');
const fs = require('fs');

async function debug3D() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9285',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1200,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9285/json/list').then(r => r.json());
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

  console.log('Navigating...');
  await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
  await new Promise(r => setTimeout(r, 4000));

  // Dismiss preloader
  await send('Runtime.evaluate', {
    expression: `
      const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('BỎ QUA'));
      if (b) b.click();
    `
  });
  await new Promise(r => setTimeout(r, 1000));

  // Check 3D status
  const status1 = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const viewer = document.querySelector('div[class*="viewer"]');
        const canvas = viewer?.querySelector('canvas');
        const fallback = viewer?.textContent;
        return {
          hasViewer: !!viewer,
          hasCanvas: !!canvas,
          canvasW: canvas?.width,
          canvasH: canvas?.height,
          fallback
        };
      })()
    `,
    returnByValue: true
  });
  console.log('Viewer status:', status1.result.value);

  // Scroll to simulator
  await send('Runtime.evaluate', {
    expression: `document.getElementById('simulator')?.scrollIntoView({ behavior: 'instant', block: 'start' });`
  });
  await new Promise(r => setTimeout(r, 1000));

  const shotInit = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/debug_3d_init.png', Buffer.from(shotInit.data, 'base64'));
  console.log('Saved scripts/debug_3d_init.png');

  // Go to stage 3, select Inlay (Xà cừ), select Motif (Hoa sen or Hoa lá)
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const list = document.querySelectorAll('ol li');
        list[3]?.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1500));

  // Click inlay Xà cừ, motif Hoa sen
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const matBtns = Array.from(document.querySelectorAll('div[class*="materialChoices"] button'));
        const pearlBtn = matBtns.find(b => b.textContent.includes('Xà cừ'));
        if (pearlBtn) pearlBtn.click();

        const motifBtns = Array.from(document.querySelectorAll('div[class*="motifChoices"] button'));
        const lotusBtn = motifBtns.find(b => b.textContent.includes('Hoa sen') || b.textContent.includes('Hoa lá'));
        if (lotusBtn) lotusBtn.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1500));

  const shotStage3 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/debug_3d_stage3.png', Buffer.from(shotStage3.data, 'base64'));
  console.log('Saved scripts/debug_3d_stage3.png');

  // Now go to Stage 4 (Phủ & Mài)
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Phủ sơn & Mài nước') || b.textContent.includes('Bước tiếp theo'));
        if (nextBtn) nextBtn.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1500));

  const shotStage4BeforeSand = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/debug_3d_stage4_before_sand.png', Buffer.from(shotStage4BeforeSand.data, 'base64'));
  console.log('Saved scripts/debug_3d_stage4_before_sand.png');

  // Now click "MÀI NƯỚC" multiple times!
  for (let i = 1; i <= 5; i++) {
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          const grindBtn = document.querySelector('.studio_main_grind_btn') || Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Mài nước'));
          if (grindBtn) grindBtn.click();
        })()
      `
    });
    await new Promise(r => setTimeout(r, 800));
  }

  const shotStage4AfterSand = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/debug_3d_stage4_after_sand.png', Buffer.from(shotStage4AfterSand.data, 'base64'));
  console.log('Saved scripts/debug_3d_stage4_after_sand.png');

  ws.close();
  chrome.kill();
}

debug3D();
