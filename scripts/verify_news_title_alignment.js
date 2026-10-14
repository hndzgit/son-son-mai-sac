const cp = require('child_process');
const fs = require('fs');

async function verify() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9251',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9251/json/list').then(r => r.json());
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
    await new Promise(r => setTimeout(r, 2500));

    const evalResult = await send('Runtime.evaluate', {
      expression: `(() => {
        const h1 = document.getElementById('news-title');
        const p = h1 ? h1.parentElement.querySelector('p') : null;
        const container = h1 ? h1.parentElement : null;

        const getInfo = (el) => {
          if (!el) return null;
          const r = el.getBoundingClientRect();
          const s = window.getComputedStyle(el);
          return {
            rect: { left: r.left, top: r.top, width: r.width, height: r.height },
            textAlign: s.textAlign,
            paddingLeft: s.paddingLeft,
            marginLeft: s.marginLeft,
            fontFamily: s.fontFamily,
            fontSize: s.fontSize
          };
        };

        return {
          h1: getInfo(h1),
          p: getInfo(p),
          container: getInfo(container),
          isLeftAligned: h1 && window.getComputedStyle(h1).textAlign === 'left',
          sameLeft: h1 && p && Math.abs(h1.getBoundingClientRect().left - p.getBoundingClientRect().left) < 1
        };
      })()`,
      returnByValue: true
    });

    console.log("Desktop Verification:", JSON.stringify(evalResult.result.value, null, 2));

    const clipResult = await send('Runtime.evaluate', {
      expression: `(() => {
        const hero = document.querySelector('.events_hero__3INKQ');
        if (!hero) return null;
        const r = hero.getBoundingClientRect();
        return { x: r.left, y: r.top, width: r.width, height: r.height, scale: 1 };
      })()`,
      returnByValue: true
    });

    const shotDesktop = await send('Page.captureScreenshot', {
      format: 'png',
      clip: clipResult.result.value ? clipResult.result.value : undefined
    });
    fs.writeFileSync('scripts/verified_news_hero_desktop.png', Buffer.from(shotDesktop.data, 'base64'));
    console.log("Saved scripts/verified_news_hero_desktop.png");

    // Also test tablet/mobile viewport
    await send('Emulation.setDeviceMetricsOverride', {
      width: 768,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });
    await new Promise(r => setTimeout(r, 1000));

    const evalTablet = await send('Runtime.evaluate', {
      expression: `(() => {
        const h1 = document.getElementById('news-title');
        const p = h1 ? h1.parentElement.querySelector('p') : null;
        return {
          h1Left: h1 ? h1.getBoundingClientRect().left : null,
          pLeft: p ? p.getBoundingClientRect().left : null,
          h1TextAlign: h1 ? window.getComputedStyle(h1).textAlign : null,
          pTextAlign: p ? window.getComputedStyle(p).textAlign : null
        };
      })()`,
      returnByValue: true
    });
    console.log("Tablet Verification (768px):", JSON.stringify(evalTablet.result.value, null, 2));

    const clipTablet = await send('Runtime.evaluate', {
      expression: `(() => {
        const hero = document.querySelector('.events_hero__3INKQ');
        if (!hero) return null;
        const r = hero.getBoundingClientRect();
        return { x: r.left, y: r.top, width: r.width, height: r.height, scale: 1 };
      })()`,
      returnByValue: true
    });

    const shotTablet = await send('Page.captureScreenshot', {
      format: 'png',
      clip: clipTablet.result.value ? clipTablet.result.value : undefined
    });
    fs.writeFileSync('scripts/verified_news_hero_tablet.png', Buffer.from(shotTablet.data, 'base64'));
    console.log("Saved scripts/verified_news_hero_tablet.png");

    ws.close();
  } catch(e) {
    console.error(e);
  } finally {
    chrome.kill();
  }
}

verify();
