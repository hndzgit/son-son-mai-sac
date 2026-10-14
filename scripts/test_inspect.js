const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9240',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);
  let targets = null;
  for (let i = 0; i < 20; i++) {
    try {
      targets = await fetch('http://localhost:9240/json/list').then(r => r.json());
      if (targets && targets.length) break;
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

    // Inspect kham-pha
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 1500));

    const kpData = await send('Runtime.evaluate', {
      expression: `(() => {
        const h1 = document.querySelector('.explore_intro__ycC8w h1');
        const cs = window.getComputedStyle(h1);
        return {
          text: h1.innerText,
          fontFamily: cs.fontFamily,
          fontWeight: cs.fontWeight,
          fontSize: cs.fontSize,
          letterSpacing: cs.letterSpacing,
          lineHeight: cs.lineHeight
        };
      })()`,
      returnByValue: true
    });
    console.log('kham-pha h1 computed style:', kpData.result.value);

    // Inspect home
    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 1500));

    const homeData = await send('Runtime.evaluate', {
      expression: `(() => {
        const h1 = document.querySelector('#core-v4-home-title') || document.querySelector('.homeHero_journeyTitle__c4_vR') || document.querySelector('h1');
        const cs = window.getComputedStyle(h1);
        return {
          id: h1.id,
          className: h1.className,
          text: h1.innerText,
          fontFamily: cs.fontFamily,
          fontWeight: cs.fontWeight,
          fontSize: cs.fontSize,
          letterSpacing: cs.letterSpacing,
          lineHeight: cs.lineHeight
        };
      })()`,
      returnByValue: true
    });
    console.log('home h1 computed style:', homeData.result.value);

  } finally {
    chrome.kill();
  }
}
test().catch(console.error);
