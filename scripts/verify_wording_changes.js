const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9226',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=390,844',
    '--user-data-dir=/tmp/chrome-test-wording'
  ]);

  await new Promise(r => setTimeout(r, 1200));

  try {
    const targets = await fetch('http://127.0.0.1:9226/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension')) || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

    let id = 1;
    const pending = new Map();
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const msgId = id++;
      pending.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id).resolve(msg.result);
        pending.delete(msg.id);
      }
    };

    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');
    await send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true
    });

    console.log('1. Navigating to http://localhost:3000/kham-pha#5-cong-doan on Mobile ...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha#5-cong-doan' });
    await new Promise(r => setTimeout(r, 2000));

    // Scroll directly into view of #5-cong-doan heading
    await send('Runtime.evaluate', {
      expression: `
        const el = document.getElementById('core-v4-process-title');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
      `
    });
    await new Promise(r => setTimeout(r, 500));

    // Check title text
    const titleEval = await send('Runtime.evaluate', {
      expression: `
        const el = document.getElementById('core-v4-process-title');
        el ? el.innerText.trim() : 'NOT_FOUND';
      `
    });
    console.log('Title text evaluated:', titleEval.result.value);

    // Capture screenshot of the heading on mobile
    const ss1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_mobile_heading.png', Buffer.from(ss1.data, 'base64'));
    console.log('Saved scripts/verify_mobile_heading.png');

    // Scroll to top and open mobile navbar menu
    console.log('\n2. Testing Mobile Navbar menu ...');
    await send('Runtime.evaluate', { expression: `window.scrollTo(0, 0);` });
    await new Promise(r => setTimeout(r, 300));

    // Click menu toggle button
    await send('Runtime.evaluate', {
      expression: `
        const toggleBtn = document.querySelector('.Navbar_toggle__eiZd0') || document.querySelector('button[aria-label*=\"menu\"]');
        if (toggleBtn) toggleBtn.click();
        
        // Also ensure details[open] for Kham pha
        const details = document.querySelector('details.Navbar_group__cCL2W');
        if (details) details.setAttribute('open', '');
      `
    });
    await new Promise(r => setTimeout(r, 500));

    // Read menu link text
    const menuEval = await send('Runtime.evaluate', {
      expression: `
        const link = document.querySelector('a[href=\"/kham-pha#5-cong-doan\"]');
        link ? link.innerText.trim() : 'NOT_FOUND';
      `
    });
    console.log('Menu link text evaluated:', menuEval.result.value);

    // Capture screenshot of mobile menu
    const ss2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_mobile_menu.png', Buffer.from(ss2.data, 'base64'));
    console.log('Saved scripts/verify_mobile_menu.png');

    // 3. Test Desktop
    console.log('\n3. Testing Desktop View ...');
    await send('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });
    await send('Runtime.evaluate', {
      expression: `
        // Close mobile menu and open dropdown
        const details = document.querySelector('details.Navbar_group__cCL2W');
        if (details) details.setAttribute('open', '');
      `
    });
    await new Promise(r => setTimeout(r, 500));

    const ss3 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_desktop_menu.png', Buffer.from(ss3.data, 'base64'));
    console.log('Saved scripts/verify_desktop_menu.png');

    ws.close();
  } catch (err) {
    console.error('Error during test:', err);
  } finally {
    chrome.kill();
  }
}

run();
