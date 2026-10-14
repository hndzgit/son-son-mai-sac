const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9299',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=390,844'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9299/json/list').then(r => r.json());
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
    await send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true,
      fitWindow: false
    });

    console.log('Navigating to http://localhost:3000/kham-pha...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 4000));

    // Dismiss preloader if present
    await send('Runtime.evaluate', {
      expression: `
        const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('BỎ QUA') || el.textContent.includes('Khám phá'));
        if (b) b.click();
      `
    });
    await new Promise(r => setTimeout(r, 1000));

    // Go to stage 3
    const resStage3 = await send('Runtime.evaluate', {
      expression: `
        (() => {
          // Find stage 3 button in stageList or call state
          const list = document.querySelectorAll('ol li');
          let found = false;
          list.forEach((li, idx) => {
            if (li.textContent.includes('TRANG TRÍ') || idx === 3) {
              li.click();
              found = true;
            }
          });
          const el = document.getElementById('studio-decoration');
          if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
          return { found, hasDec: !!el };
        })()
      `,
      returnByValue: true
    });
    console.log('Stage 3 click:', resStage3.result.value);
    await new Promise(r => setTimeout(r, 1000));

    // Screenshot of stage 3
    const shot3 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/shot_stage3_screen.png', Buffer.from(shot3.data, 'base64'));
    console.log('Saved scripts/shot_stage3_screen.png');

    // Click "Bước tiếp theo →"
    const clickNext = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const btns = Array.from(document.querySelectorAll('button'));
          const nextBtn = btns.find(b => b.textContent.includes('Bước tiếp theo'));
          if (nextBtn) {
            nextBtn.click();
            return { clicked: true, text: nextBtn.textContent };
          }
          return { clicked: false };
        })()
      `,
      returnByValue: true
    });
    console.log('Next button click:', clickNext.result.value);
    await new Promise(r => setTimeout(r, 1500));

    // What is visible now?
    const stateAfter = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const h1 = document.querySelector('div[aria-live="polite"] h1')?.textContent;
          const label = document.querySelector('.choiceLabel, p[class*="choiceLabel"]')?.textContent;
          const finishBtns = Array.from(document.querySelectorAll('div[class*="finishActions"] button')).map(b => b.textContent);
          const scrollY = window.scrollY;
          return { h1, label, finishBtns, scrollY };
        })()
      `,
      returnByValue: true
    });
    console.log('State after click:', stateAfter.result.value);

    // Screenshot right after click
    const shot4_immediate = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/shot_stage4_immediate.png', Buffer.from(shot4_immediate.data, 'base64'));
    console.log('Saved scripts/shot_stage4_immediate.png');

    // Scroll to finish actions and screenshot
    await send('Runtime.evaluate', {
      expression: `
        const actions = document.querySelector('div[class*="finishActions"]');
        if (actions) actions.scrollIntoView({ behavior: 'instant', block: 'center' });
      `
    });
    await new Promise(r => setTimeout(r, 500));
    const shot4_scrolled = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/shot_stage4_scrolled.png', Buffer.from(shot4_scrolled.data, 'base64'));
    console.log('Saved scripts/shot_stage4_scrolled.png');

    ws.close();
  } catch(e) {
    console.error('Error:', e);
  } finally {
    chrome.kill();
  }
}

run();
