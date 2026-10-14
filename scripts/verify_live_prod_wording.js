const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9229',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=/tmp/chrome-test-wording-prod3'
  ]);

  await new Promise(r => setTimeout(r, 1200));

  try {
    const targets = await fetch('http://127.0.0.1:9229/json/list').then(r => r.json());
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);

    let id = 1;
    const send = (method, params = {}) => new Promise((resolve) => {
      const mid = id++;
      const handler = (e) => {
        const d = JSON.parse(e.data);
        if (d.id === mid) { ws.removeEventListener('message', handler); resolve(d.result); }
      };
      ws.addEventListener('message', handler);
      ws.send(JSON.stringify({ id: mid, method, params }));
    });

    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');

    // 1. Mobile view
    await send('Emulation.setDeviceMetricsOverride', {
      width: 414,
      height: 896,
      deviceScaleFactor: 2,
      mobile: true
    });

    await send('Page.navigate', { url: 'https://son-son-mai-sac-orpin.vercel.app/kham-pha' });
    await new Promise(r => setTimeout(r, 3500));

    // Scroll directly to the process section heading
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('core-v4-process-title');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()`
    });
    await new Promise(r => setTimeout(r, 800));

    const ssMobile = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/prod_verified_heading_mobile.png', Buffer.from(ssMobile.data, 'base64'));
    console.log('Saved scripts/prod_verified_heading_mobile.png');

    // 2. Desktop View
    await send('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 2,
      mobile: false
    });

    // Scroll to top and open navbar details dropdown
    await send('Runtime.evaluate', {
      expression: `(() => {
        window.scrollTo(0, 0);
        const details = document.querySelector('details.Navbar_group__cCL2W');
        if (details) details.setAttribute('open', '');
      })()`
    });
    await new Promise(r => setTimeout(r, 800));

    const ssDesktopMenu = await send('Page.captureScreenshot', {
      format: 'png',
      clip: { x: 0, y: 0, width: 1440, height: 420, scale: 1 }
    });
    fs.writeFileSync('scripts/prod_verified_desktop_menu.png', Buffer.from(ssDesktopMenu.data, 'base64'));
    console.log('Saved scripts/prod_verified_desktop_menu.png');

    // Desktop heading view
    await send('Runtime.evaluate', {
      expression: `(() => {
        const details = document.querySelector('details.Navbar_group__cCL2W');
        if (details) details.removeAttribute('open');
        const el = document.getElementById('core-v4-process-title');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()`
    });
    await new Promise(r => setTimeout(r, 800));

    const ssDesktopHeading = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/prod_verified_desktop_heading.png', Buffer.from(ssDesktopHeading.data, 'base64'));
    console.log('Saved scripts/prod_verified_desktop_heading.png');

    ws.close();
  } catch (err) {
    console.error('Error during screenshot capture:', err);
  } finally {
    chrome.kill();
  }
}

run();
