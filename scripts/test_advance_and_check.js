const cp = require('child_process');
const fs = require('fs');

async function checkJourney() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9292',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1280,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9292/json/list').then(r => r.json());
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

    // Advance Stage 0 -> 1 -> 2 -> 3 -> 4
    for (let stage = 0; stage < 4; stage++) {
      console.log(`Advancing past stage ${stage}...`);
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
            if (advBtn) { advBtn.click(); return advBtn.textContent.trim(); }
            return 'not found';
          })()
        `,
        returnByValue: true
      });
      await new Promise(r => setTimeout(r, 800));
    }

    // Scroll to studio_grind_card
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

    // Extract exact texts
    const res = await send('Runtime.evaluate', {
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
            cardFound: !!card,
            surfaceTitle,
            previewPill,
            grindBtn,
            sliderSpan,
            footnote,
            headings: h2s.filter(t => t.includes('MÀI') || t.includes('SƠN') || t.includes('ĐÁNH BÓNG') || t.includes('Ủ'))
          };
        })()
      `,
      returnByValue: true
    });

    console.log('Inspection result:\n', JSON.stringify(res.result?.value, null, 2));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/check_ai_wording_result.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved screenshot to scripts/check_ai_wording_result.png');

    ws.close();
  } finally {
    chrome.kill();
  }
}

checkJourney().catch(console.error);
