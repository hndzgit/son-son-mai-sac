const cp = require('child_process');
const fs = require('fs');

async function checkClick() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9294',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1280,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9294/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
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
    await new Promise(r => setTimeout(r, 600));

    // Click MÀI NƯỚC button 3 times
    for (let c = 1; c <= 3; c++) {
      console.log(`Clicking Mài nước ${c}...`);
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

    const state = await send('Runtime.evaluate', {
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

    console.log('After 3 clicks:\n', JSON.stringify(state.result?.value, null, 2));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/check_clicked_grind.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved scripts/check_clicked_grind.png');

    ws.close();
  } finally {
    chrome.kill();
  }
}

checkClick().catch(console.error);
