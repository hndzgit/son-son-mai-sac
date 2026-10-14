const cp = require('child_process');
const fs = require('fs');

async function main() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9262',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);

  await new Promise(r => setTimeout(r, 1200));

  try {
    const targets = await fetch('http://localhost:9262/json/list').then(r => r.json());
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);

    await new Promise(res => { ws.onopen = res; });
    let id = 1;
    const send = (m, p = {}) => new Promise(res => {
      const i = id++;
      const h = (e) => {
        const d = JSON.parse(e.data);
        if (d.id === i) { ws.removeEventListener('message', h); res(d.result); }
      };
      ws.addEventListener('message', h);
      ws.send(JSON.stringify({ id: i, method: m, params: p }));
    });

    await send('Page.enable');
    await send('Runtime.enable');
    await send('Page.navigate', { url: 'https://sonsonmaisac.site/' });

    // Check at 400ms
    await new Promise(r => setTimeout(r, 1200));
    const r1 = await send('Runtime.evaluate', {
      expression: `(() => {
        const p = document.querySelector(".entry-screen, .core-v4-preloader");
        
        const el = document.getElementById("ssms-entry-screen");
        return {
          innerHTML: el ? el.innerHTML : null,

          exists: !!p,
          display: p ? window.getComputedStyle(p).display : null,
          opacity: p ? window.getComputedStyle(p).opacity : null,
          text: p ? p.textContent : null
        };
      })()`,
      returnByValue: true
    });
    console.log('Preloader at 400ms:', JSON.stringify(r1.result.value));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_preloader_captured.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved scripts/test_preloader_captured.png');

    // Wait 3.5s
    await new Promise(r => setTimeout(r, 3500));
    const r2 = await send('Runtime.evaluate', {
      expression: `(() => {
        const p = document.querySelector(".entry-screen, .core-v4-preloader");
        
        const el = document.getElementById("ssms-entry-screen");
        return {
          innerHTML: el ? el.innerHTML : null,

          exists: !!p,
          heroVisible: !!document.querySelector("#mo-dau")
        };
      })()`,
      returnByValue: true
    });
    console.log('After 3.5s:', JSON.stringify(r2.result.value));

  } finally {
    chrome.kill();
  }
}

main().catch(console.error);
