const cp = require('child_process');
const fs = require('fs');

async function test() {
  const profileDir = `/tmp/chrome-clean-${Date.now()}`;
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9241',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    `--user-data-dir=${profileDir}`,
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9241/json/list').then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) {
        targets = [valid];
        break;
      }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets.length) {
    chrome.kill();
    console.error('Failed to connect to Chrome debugging port');
    return;
  }

  try {
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const callbacks = new Map();
    const consoleLogs = [];
    const errors = [];
    const failedRequests = [];

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
      if (msg.method === 'Network.loadingFailed') {
        failedRequests.push({ url: msg.params.requestId, error: msg.params.errorText });
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

    // Wait 4 seconds for hydration and loading
    await new Promise(r => setTimeout(r, 4000));

    // Inspect state
    const evalResult = await send('Runtime.evaluate', {
      expression: `(() => {
        const docEl = document.documentElement;
        const body = document.body;
        const entryScreen = document.querySelector('.entry-screen, .core-v4-preloader, [class*="preloader"], [class*="entry"]');
        const overlay = document.elementFromPoint(720, 450);
        
        // Check sections
        const sections = Array.from(document.querySelectorAll('section, main > div, [data-presentation-slide]')).map(s => ({
          id: s.id,
          class: s.className,
          display: window.getComputedStyle(s).display,
          opacity: window.getComputedStyle(s).opacity,
          visibility: window.getComputedStyle(s).visibility,
          transform: window.getComputedStyle(s).transform,
          rect: s.getBoundingClientRect()
        }));

        const reveals = Array.from(document.querySelectorAll('[data-reveal]')).slice(0, 10).map(r => ({
          visible: r.getAttribute('data-visible'),
          opacity: window.getComputedStyle(r).opacity,
          transform: window.getComputedStyle(r).transform,
          cls: r.className
        }));

        return {
          title: document.title,
          scrollY: window.scrollY,
          locationHref: window.location.href,
          bodyOverflow: window.getComputedStyle(body).overflow,
          bodyPointerEvents: window.getComputedStyle(body).pointerEvents,
          docOverflow: window.getComputedStyle(docEl).overflow,
          entryScreenFound: !!entryScreen,
          entryScreenDisplay: entryScreen ? window.getComputedStyle(entryScreen).display : null,
          entryScreenOpacity: entryScreen ? window.getComputedStyle(entryScreen).opacity : null,
          entryScreenPointerEvents: entryScreen ? window.getComputedStyle(entryScreen).pointerEvents : null,
          topElementAtCenter: overlay ? {
            tagName: overlay.tagName,
            id: overlay.id,
            className: overlay.className,
            opacity: window.getComputedStyle(overlay).opacity,
            pointerEvents: window.getComputedStyle(overlay).pointerEvents,
            zIndex: window.getComputedStyle(overlay).zIndex,
            background: window.getComputedStyle(overlay).backgroundColor
          } : null,
          revealsSample: reveals,
          sectionsSample: sections.slice(0, 5)
        };
      })()`,
      returnByValue: true
    });

    console.log('\n--- State Inspection ---');
    console.log(JSON.stringify(evalResult.result.value, null, 2));

    console.log('\n--- Errors (' + errors.length + ') ---');
    errors.forEach(e => console.log('ERROR:', e));

    console.log('\n--- Console Logs (' + consoleLogs.length + ') ---');
    consoleLogs.slice(-20).forEach(c => console.log('LOG:', c));

    // Capture screenshot
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/screenshot_hang_test.png', Buffer.from(shot.data, 'base64'));
    console.log('\nScreenshot saved to scripts/screenshot_hang_test.png');

  } finally {
    chrome.kill();
    fs.rmSync(profileDir, { recursive: true, force: true });
  }
}

test().catch(console.error);
