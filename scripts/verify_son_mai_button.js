const cp = require('child_process');
const fs = require('fs');

async function testButton() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9257',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9257/json/list').then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) {
        targets = [valid];
        break;
      }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets[0]) {
    console.error('Failed to get chrome target');
    chrome.kill();
    return;
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
    await send('DOM.enable');

    // Test 1: Home page (http://localhost:3000/)
    console.log('Testing Home page (/)...\n');
    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 2500)); // allow React hydration

    const homeCheck = await send('Runtime.evaluate', {
      expression: `(() => {
        const cta = document.querySelector('.coreIntroduction_definitionCta');
        const section = document.querySelector('#son-mai-la-gi');
        if (section) section.scrollIntoView({ behavior: 'instant' });
        return {
          exists: !!cta,
          href: cta ? cta.getAttribute('href') : null,
          text: cta ? cta.innerText : null,
          visible: cta ? (cta.offsetWidth > 0 && cta.offsetHeight > 0) : false
        };
      })()`,
      returnByValue: true
    });
    console.log('Home check result:', homeCheck.result.value);

    await new Promise(r => setTimeout(r, 600));

    // Capture screenshot of #son-mai-la-gi on home
    const clipHome = await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('#son-mai-la-gi');
        if (!el) return null;
        const rect = el.getBoundingClientRect();
        return { x: rect.left, y: rect.top, width: rect.width, height: rect.height };
      })()`,
      returnByValue: true
    });
    if (clipHome?.result?.value) {
      const shot = await send('Page.captureScreenshot', { clip: { ...clipHome.result.value, scale: 1 } });
      fs.writeFileSync('scripts/home_son_mai_button.png', Buffer.from(shot.data, 'base64'));
      console.log('Saved scripts/home_son_mai_button.png');
    }

    // Test 2: Trai-nghiem page (http://localhost:3000/trai-nghiem)
    console.log('\nTesting Trai-nghiem page (/trai-nghiem)...\n');
    await send('Page.navigate', { url: 'http://localhost:3000/trai-nghiem' });
    await new Promise(r => setTimeout(r, 2500)); // allow React hydration

    const tnCheck = await send('Runtime.evaluate', {
      expression: `(() => {
        const cta = document.querySelector('.coreIntroduction_definitionCta');
        const section = document.querySelector('#son-mai-la-gi');
        if (section) section.scrollIntoView({ behavior: 'instant' });
        return {
          exists: !!cta,
          href: cta ? cta.getAttribute('href') : null,
          text: cta ? cta.innerText : null,
          visible: cta ? (cta.offsetWidth > 0 && cta.offsetHeight > 0) : false
        };
      })()`,
      returnByValue: true
    });
    console.log('Trai-nghiem check result:', tnCheck.result.value);

    await new Promise(r => setTimeout(r, 600));

    const clipTn = await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('#son-mai-la-gi');
        if (!el) return null;
        const rect = el.getBoundingClientRect();
        return { x: rect.left, y: rect.top, width: rect.width, height: rect.height };
      })()`,
      returnByValue: true
    });
    if (clipTn?.result?.value) {
      const shot = await send('Page.captureScreenshot', { clip: { ...clipTn.result.value, scale: 1 } });
      fs.writeFileSync('scripts/trainghiem_son_mai_button.png', Buffer.from(shot.data, 'base64'));
      console.log('Saved scripts/trainghiem_son_mai_button.png');
    }

    ws.close();
  } catch(e) {
    console.error('Error during test:', e);
  } finally {
    chrome.kill();
  }
}

testButton();
