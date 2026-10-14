const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9250',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1200,800'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9250/json/list').then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) {
        targets = [valid];
        break;
      }
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

    await send('Page.navigate', { url: 'http://localhost:3000/tin-tuc-su-kien' });
    await new Promise(r => setTimeout(r, 2000));

    // Let's test with text-align: left vs text-align: center
    const checkBefore = await send('Runtime.evaluate', {
      expression: `(() => {
        const h1 = document.getElementById('news-title');
        const p = h1 ? h1.parentElement.querySelector('p') : null;
        
        // Get range rects for first word of h1 and first word of p
        const getFirstCharRect = (el) => {
          const range = document.createRange();
          range.setStart(el.firstChild, 0);
          range.setEnd(el.firstChild, 1);
          return range.getBoundingClientRect();
        };

        return {
          h1Char: getFirstCharRect(h1),
          pChar: getFirstCharRect(p),
          h1Rect: h1.getBoundingClientRect(),
          pRect: p.getBoundingClientRect(),
          h1TextAlign: window.getComputedStyle(h1).textAlign,
          pTextAlign: window.getComputedStyle(p).textAlign,
        };
      })()`,
      returnByValue: true
    });

    console.log("BEFORE applying text-align: left:", JSON.stringify(checkBefore.result.value, null, 2));

    // Now apply text-align: left to h1
    await send('Runtime.evaluate', {
      expression: `(() => {
        const h1 = document.getElementById('news-title');
        h1.style.setProperty('text-align', 'left', 'important');
      })()`
    });

    const checkAfter = await send('Runtime.evaluate', {
      expression: `(() => {
        const h1 = document.getElementById('news-title');
        const p = h1 ? h1.parentElement.querySelector('p') : null;
        
        const getFirstCharRect = (el) => {
          const range = document.createRange();
          range.setStart(el.firstChild, 0);
          range.setEnd(el.firstChild, 1);
          return range.getBoundingClientRect();
        };

        return {
          h1Char: getFirstCharRect(h1),
          pChar: getFirstCharRect(p),
          h1Rect: h1.getBoundingClientRect(),
          pRect: p.getBoundingClientRect(),
          h1TextAlign: window.getComputedStyle(h1).textAlign,
          pTextAlign: window.getComputedStyle(p).textAlign,
        };
      })()`,
      returnByValue: true
    });

    console.log("AFTER applying text-align: left:", JSON.stringify(checkAfter.result.value, null, 2));

    const clipResult = await send('Runtime.evaluate', {
      expression: `(() => {
        const hero = document.querySelector('.events_hero__3INKQ');
        if (!hero) return null;
        const r = hero.getBoundingClientRect();
        return { x: r.left, y: r.top, width: r.width, height: r.height, scale: 1 };
      })()`,
      returnByValue: true
    });

    const shot = await send('Page.captureScreenshot', {
      format: 'png',
      clip: clipResult.result.value ? clipResult.result.value : undefined
    });
    fs.writeFileSync('scripts/crop_news_hero_after_test.png', Buffer.from(shot.data, 'base64'));

    ws.close();
  } catch(e) {
    console.error(e);
  } finally {
    chrome.kill();
  }
}

test();
