const cp = require('child_process');

async function testLiveStudio() {
  console.log('--- Testing live studio on https://sonsonmaisac.id.vn/kham-pha ---');
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9294',
    '--no-sandbox',
    '--window-size=1280,1000'
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

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  let id = 1;
  const callbacks = new Map();
  const errors = [];

  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      errors.push(msg.params.args.map(a => a.value || a.description || '').join(' '));
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      errors.push(msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || ''));
    }
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

  await send('Page.navigate', { url: 'https://sonsonmaisac.id.vn/kham-pha' });
  await new Promise(r => setTimeout(r, 4000));

  // Dismiss modal
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('BỎ QUA'));
        if (b) b.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 600));

  // Click stage 5 in aside
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const stageItems = document.querySelectorAll('ol[class*="stageList"] li');
        if (stageItems && stageItems[4]) stageItems[4].click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));

  // Inspect buttons
  const res = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const container = document.querySelector('#studio-finish') || document.querySelector('div[class*="galleryControls"]');
        const labels = Array.from(container.querySelectorAll('span[class*="choiceLabel"]')).map(el => el.textContent.trim());
        const btns = Array.from(container.querySelectorAll('div[class*="finishActions"] button, button[class*="studio_main_grind_btn"]')).map(b => b.textContent.trim());
        return { labels, btns };
      })()
    `,
    returnByValue: true
  });

  console.log('Live Studio Section Labels:', res.result?.value?.labels);
  console.log('Live Studio Buttons:', res.result?.value?.btns);
  console.log('Live Studio Errors:', errors.length);

  ws.close();
  chrome.kill();
}

testLiveStudio().catch(console.error);
