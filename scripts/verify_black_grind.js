const cp = require('child_process');
const fs = require('fs');

async function verifyBlackGrind() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9293',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1280,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9293/json/list').then(r => r.json());
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

    console.log('Navigating to http://localhost:3000/kham-pha#process-workshop-panel...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha#process-workshop-panel' });
    await new Promise(r => setTimeout(r, 2500));

    // Advance 4 stages
    for (let stage = 0; stage < 4; stage++) {
      await send('Runtime.evaluate', {
        expression: `
          (() => {
            const advBtn = document.querySelector('button[class*="advanceButton"]') ||
              Array.from(document.querySelectorAll('button')).find(b => 
                b.textContent.includes('tiếp theo') || 
                b.textContent.includes('Hoàn tất') || 
                b.textContent.includes('Tiếp tục') ||
                b.textContent.includes('Bước tiếp') ||
                b.textContent.includes('Phủ then') ||
                b.textContent.includes('Phủ sơn')
              );
            if (advBtn) advBtn.click();
          })()
        `
      });
      await new Promise(r => setTimeout(r, 800));
    }

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

    // Check INITIAL State (0% - black lacquer covering surface)
    const initial = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const card = document.querySelector('.studio_grind_card');
          const surfaceTitle = card?.querySelector('.studio_surface_preview_wrap span')?.innerText;
          const previewPill = card?.querySelector('.studio_surface_preview_wrap div:last-child span')?.innerText;
          const grindBtn = document.querySelector('.studio_main_grind_btn')?.innerText;
          const sec1Title = Array.from(document.querySelectorAll('span[class*="choiceLabel"]')).map(el => el.innerText);
          const polishBtn = document.querySelector('.studio_polish_btn')?.innerText;

          return { surfaceTitle, previewPill, grindBtn, sec1Title, polishBtn };
        })()
      `,
      returnByValue: true
    });

    console.log('INITIAL STAGE 4 STATE:\n', JSON.stringify(initial.result?.value, null, 2));

    const shot1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/check_black_initial_state.png', Buffer.from(shot1.data, 'base64'));
    console.log('Saved scripts/check_black_initial_state.png');

    // Click Mài Nước twice
    console.log('Clicking Mài nước 1...');
    await send('Runtime.evaluate', { expression: `document.querySelector('.studio_main_grind_btn')?.click()` });
    await new Promise(r => setTimeout(r, 600));

    console.log('Clicking Mài nước 2...');
    await send('Runtime.evaluate', { expression: `document.querySelector('.studio_main_grind_btn')?.click()` });
    await new Promise(r => setTimeout(r, 600));

    const afterGrind = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const card = document.querySelector('.studio_grind_card');
          const surfaceTitle = card?.querySelector('.studio_surface_preview_wrap span')?.innerText;
          const previewPill = card?.querySelector('.studio_surface_preview_wrap div:last-child span')?.innerText;
          const grindBtn = document.querySelector('.studio_main_grind_btn')?.innerText;
          return { surfaceTitle, previewPill, grindBtn };
        })()
      `,
      returnByValue: true
    });

    console.log('AFTER 2 GRIND ACTIONS:\n', JSON.stringify(afterGrind.result?.value, null, 2));

    const shot2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/check_black_grinded_state.png', Buffer.from(shot2.data, 'base64'));
    console.log('Saved scripts/check_black_grinded_state.png');

    ws.close();
  } finally {
    chrome.kill();
  }
}

verifyBlackGrind().catch(console.error);
