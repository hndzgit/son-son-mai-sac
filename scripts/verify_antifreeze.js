const cp = require('child_process');
const fs = require('fs');

async function test() {
  const profileDir = `/tmp/chrome-clean-${Date.now()}`;
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9249',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    `--user-data-dir=${profileDir}`,
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9249/json/list').then(r => r.json());
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
    const consoleLogs = [];
    const errors = [];

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg.result);
        callbacks.delete(msg.id);
      }
      if (msg.method === 'Runtime.consoleAPICalled') {
        const text = msg.params.args.map(a => a.value || JSON.stringify(a)).join(' ');
        consoleLogs.push(`[${msg.params.type}] ${text}`);
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        errors.push(msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text);
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
    await send('Network.enable');

    console.log('Navigating to http://localhost:3000/ ...');
    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 2000));

    // Capture Top / Hero screenshot
    const shotTop = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_hero_top.png', Buffer.from(shotTop.data, 'base64'));
    console.log('Saved scripts/verify_hero_top.png');

    // Scroll to 800px (Sơn mài là gì?)
    await send('Runtime.evaluate', { expression: 'window.scrollTo({ top: 800, behavior: "instant" })' });
    await new Promise(r => setTimeout(r, 800));

    const shot800 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_son_mai_la_gi.png', Buffer.from(shot800.data, 'base64'));
    console.log('Saved scripts/verify_son_mai_la_gi.png');

    // Scroll to 1500px (Năm chặng)
    await send('Runtime.evaluate', { expression: 'window.scrollTo({ top: 1500, behavior: "instant" })' });
    await new Promise(r => setTimeout(r, 800));

    const shot1500 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_nam_chang.png', Buffer.from(shot1500.data, 'base64'));
    console.log('Saved scripts/verify_nam_chang.png');

    // Inspect reveal states and opacity
    const state = await send('Runtime.evaluate', {
      expression: `(() => {
        const reveals = Array.from(document.querySelectorAll('[data-reveal]')).map(el => ({
          tag: el.tagName,
          id: el.id,
          cls: el.className.split(' ')[0],
          visible: el.getAttribute('data-visible'),
          opacity: window.getComputedStyle(el).opacity,
          transform: window.getComputedStyle(el).transform
        }));

        const preloader = document.querySelector('.entry-screen, .core-v4-preloader');
        const overlay = document.elementFromPoint(720, 450);

        return {
          preloaderFound: !!preloader,
          preloaderDisplay: preloader ? window.getComputedStyle(preloader).display : null,
          allOpacitiesAreOne: reveals.every(r => parseFloat(r.opacity) >= 0.99),
          revealsSummary: reveals
        };
      })()`,
      returnByValue: true
    });

    console.log('\n--- State Inspection Result ---');
    console.log(JSON.stringify(state.result.value, null, 2));

    console.log('\nErrors:', errors.length);
    errors.forEach(e => console.log('  ', e));

  } finally {
    chrome.kill();
    fs.rmSync(profileDir, { recursive: true, force: true });
  }
}

test().catch(console.error);
