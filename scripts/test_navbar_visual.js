const cp = require('child_process');
const fs = require('fs');

async function testNavbar() {
  const port = 9226;
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--no-sandbox',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch(`http://localhost:${port}/json/list`).then(r => r.json());
      const p = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (p) { targets = [p]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets[0]) {
    console.error('Failed to connect to Chrome');
    chrome.kill();
    return;
  }

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  let id = 1;
  const cb = new Map();
  const errors = [];

  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.method === 'Runtime.exceptionThrown') {
      errors.push(m.params.exceptionDetails.text + ' ' + (m.params.exceptionDetails.exception?.description || ''));
    }
    if (m.id && cb.has(m.id)) {
      cb.get(m.id)(m.result);
      cb.delete(m.id);
    }
  };

  const send = (method, params = {}) => new Promise(res => {
    const curId = id++;
    cb.set(curId, res);
    ws.send(JSON.stringify({ id: curId, method, params }));
  });

  await new Promise(r => ws.onopen = r);

  await send('Page.enable');
  await send('Runtime.enable');

  console.log('Navigating to http://localhost:3000...');
  await send('Page.navigate', { url: 'http://localhost:3000' });
  await new Promise(r => setTimeout(r, 1200));

  // Dismiss splash preloader
  await send('Runtime.evaluate', {
    expression: `(() => {
      const p = document.getElementById('ssms-preloader');
      if (p) { p.style.display = 'none'; document.body.classList.remove('preloader-active'); }
    })()`
  });

  // Open first dropdown menu
  const openRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const summary = document.querySelector('.Navbar_group__cCL2W summary');
      if (summary) {
        summary.click();
        const group = document.querySelector('.Navbar_group__cCL2W');
        return {
          clicked: true,
          isOpen: group ? group.hasAttribute('open') : false,
          summaryText: summary.textContent.trim()
        };
      }
      return { clicked: false };
    })()`,
    returnByValue: true
  });
  console.log('Dropdown open result:', openRes.result.value);

  await new Promise(r => setTimeout(r, 500));

  // Take screenshot
  const screenshotRes = await send('Page.captureScreenshot', {
    clip: { x: 0, y: 0, width: 1440, height: 450, scale: 1 }
  });

  if (screenshotRes && screenshotRes.data) {
    fs.writeFileSync('scripts/navbar_dropdown.png', Buffer.from(screenshotRes.data, 'base64'));
    console.log('Saved screenshot to scripts/navbar_dropdown.png');
  }

  ws.close();
  chrome.kill();
  console.log('All errors encountered:', errors);
}

testNavbar();
