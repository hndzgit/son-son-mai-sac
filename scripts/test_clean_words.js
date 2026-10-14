const cp = require('child_process');
const fs = require('fs');

async function testWording() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9299',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1280,900'
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

    console.log('Navigating to http://localhost:3000/kham-pha#process-workshop-panel...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha#process-workshop-panel' });
    await new Promise(r => setTimeout(r, 3000));

    // Advance to Stage 4 (Phủ sơn & Mài nước)
    const resNav = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const btns = Array.from(document.querySelectorAll('button, nav div, [role="button"]'));
          for (const b of btns) {
            if (b.innerText && b.innerText.includes('Phủ sơn & Mài nước')) {
              b.click();
              return 'Clicked stage 4';
            }
          }
          return 'Stage 4 button not found';
        })()
      `,
      returnByValue: true
    });
    console.log('Stage 4 click result:', resNav.result?.value);
    await new Promise(r => setTimeout(r, 2000));

    // Scroll to grind card
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          const card = document.querySelector('.studio_grind_card');
          if (card) {
            card.scrollIntoView({ behavior: 'instant', block: 'center' });
            return true;
          }
          return false;
        })()
      `
    });
    await new Promise(r => setTimeout(r, 1000));

    // Inspect text in grind card & footnote
    const textCheck = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const card = document.querySelector('.studio_grind_card');
          const surfaceTitle = card?.querySelector('.studio_surface_preview_wrap span')?.innerText;
          const previewPill = card?.querySelector('.studio_surface_preview_wrap div:last-child span')?.innerText;
          const grindBtn = document.querySelector('.studio_main_grind_btn')?.innerText;
          const sliderSpan = card?.querySelector('label[class*="depthControl"] span')?.innerText;
          const footnote = document.querySelector('p[class*="boardFootnote"]')?.innerText;
          const h2s = Array.from(document.querySelectorAll('h1, h2, h3, span[class*="choiceLabel"]')).map(el => el.innerText);

          return {
            surfaceTitle,
            previewPill,
            grindBtn,
            sliderSpan,
            footnote,
            headings: h2s.filter(t => t.includes('MÀI') || t.includes('SƠN') || t.includes('ĐÁNH BÓNG'))
          };
        })()
      `,
      returnByValue: true
    });

    console.log('Text check result:\n', JSON.stringify(textCheck.result?.value, null, 2));

    // Take screenshot
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/check_ai_wording_result.png', Buffer.from(shot.data, 'base64'));
    console.log('Screenshot saved to scripts/check_ai_wording_result.png');

    ws.close();
  } finally {
    chrome.kill();
  }
}

testWording().catch(console.error);
