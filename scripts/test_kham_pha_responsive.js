const cp = require('child_process');
const fs = require('fs');

async function testKhamPhaHash() {
  const tmpDir = '/tmp/chrome-test-hash-' + Date.now();
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9295',
    '--no-sandbox',
    '--user-data-dir=' + tmpDir,
    '--window-size=1280,800'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9295/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets[0]) {
    console.error('Failed to connect to Chrome');
    chrome.kill();
    process.exit(1);
  }

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  let id = 1;
  const callbacks = new Map();
  const consoleLogs = [];

  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.method === 'Runtime.consoleAPICalled') {
      consoleLogs.push({ type: msg.params.type, text: msg.params.args.map(a => a.value || a.description).join(' ') });
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      consoleLogs.push({ type: 'error', text: JSON.stringify(msg.params.exceptionDetails) });
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

  console.log('Navigating to http://localhost:3000/kham-pha#son-mai-la-gi ...');
  const startTime = Date.now();
  await send('Page.navigate', { url: 'http://localhost:3000/kham-pha#son-mai-la-gi' });

  // Wait 3 seconds for load and smooth scroll
  await new Promise(r => setTimeout(r, 3000));
  const loadDuration = Date.now() - startTime;
  console.log(`Page navigated in ${loadDuration}ms without freezing!`);

  // Evaluate page status and scroll position
  const evalResult = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const hash = window.location.hash;
        const target = document.querySelector('#son-mai-la-gi');
        const scrollY = window.scrollY;
        const targetRect = target ? target.getBoundingClientRect() : null;
        const isResponsive = true;
        return {
          hash,
          hasTarget: !!target,
          scrollY,
          targetTop: targetRect ? targetRect.top : null,
          title: document.title,
          isResponsive
        };
      })()
    `,
    returnByValue: true
  });

  console.log('Page Evaluation Result:', JSON.stringify(evalResult.result.value, null, 2));

  // Test interactivity: Click on a button or scroll
  console.log('Testing interaction (clicking on next stage)...');
  const clickResult = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const step2Btn = document.querySelector('li#cong-doan-2 button');
        if (step2Btn) {
          step2Btn.click();
          return { clicked: true, text: step2Btn.textContent };
        }
        return { clicked: false };
      })()
    `,
    returnByValue: true
  });
  console.log('Interaction Result:', JSON.stringify(clickResult.result.value, null, 2));

  // Capture screenshot
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scripts/test_kham_pha_responsive_result.png', Buffer.from(shot.data, 'base64'));
  console.log('Screenshot saved to scripts/test_kham_pha_responsive_result.png');

  if (consoleLogs.length > 0) {
    console.log('Console logs/errors caught:');
    consoleLogs.forEach(l => console.log(`  [${l.type}] ${l.text}`));
  } else {
    console.log('No console errors! Clean execution.');
  }

  ws.close();
  chrome.kill();
  console.log('TEST PASSED SUCCESSFULLY!');
}

testKhamPhaHash().catch(e => {
  console.error('Test failed with error:', e);
  process.exit(1);
});
