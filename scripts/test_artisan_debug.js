const cp = require('child_process');
const fs = require('fs');

async function testArtisans() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9246',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1200'
  ]);
  
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9246/json/list').then(r => r.json());
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
    
    await send('Page.navigate', { url: 'http://localhost:3000/cau-chuyen-son-mai' });
    await new Promise(r => setTimeout(r, 2500));
    
    // Check initial state of artisan section
    let check1 = await send('Runtime.evaluate', {
      expression: `(() => {
        const sec = document.querySelector('.story_inspiration__LM_OE');
        const cards = document.querySelectorAll('.artisan_zigzag_card');
        return {
          hasSec: !!sec,
          secHTML: sec ? sec.innerHTML.slice(0, 300) : null,
          cardCount: cards.length,
          cardOpacities: Array.from(cards).map(c => window.getComputedStyle(c).opacity)
        };
      })()`,
      returnByValue: true
    });
    console.log('INITIAL CHECK:', JSON.stringify(check1.result.value, null, 2));
    
    // Scroll down to the artisan section
    await send('Runtime.evaluate', {
      expression: `(() => {
        const sec = document.querySelector('.story_inspiration__LM_OE');
        if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()`
    });
    await new Promise(r => setTimeout(r, 1000));
    
    let check2 = await send('Runtime.evaluate', {
      expression: `(() => {
        const cards = document.querySelectorAll('.artisan_zigzag_card');
        return {
          cardCount: cards.length,
          cardOpacities: Array.from(cards).map(c => window.getComputedStyle(c).opacity),
          cardHeights: Array.from(cards).map(c => c.getBoundingClientRect().height)
        };
      })()`,
      returnByValue: true
    });
    console.log('AFTER SCROLL CHECK:', JSON.stringify(check2.result.value, null, 2));
    
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/artisan_inspect.png', Buffer.from(shot.data, 'base64'));
    console.log('Screenshot saved to scripts/artisan_inspect.png');
    
    // Now click timeline tab 4 (Làng nghề / Nghệ nhân)
    console.log('Clicking timeline-tab-4...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const tab4 = document.getElementById('timeline-tab-4');
        if (tab4) tab4.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 1000));
    
    let check3 = await send('Runtime.evaluate', {
      expression: `(() => {
        const sec = document.querySelector('.story_inspiration__LM_OE');
        const cards = document.querySelectorAll('.artisan_zigzag_card');
        return {
          hasSec: !!sec,
          secText: sec ? sec.innerText.slice(0, 200) : null,
          cardCount: cards.length,
          cardOpacities: Array.from(cards).map(c => window.getComputedStyle(c).opacity)
        };
      })()`,
      returnByValue: true
    });
    console.log('AFTER TAB 4 CLICK:', JSON.stringify(check3.result.value, null, 2));
    
    const shot2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/artisan_tab4_inspect.png', Buffer.from(shot2.data, 'base64'));
    console.log('Screenshot saved to scripts/artisan_tab4_inspect.png');
    
  } finally {
    chrome.kill();
  }
}

testArtisans();
