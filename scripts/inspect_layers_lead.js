const cp = require('child_process');
const fs = require('fs');

async function test() {
  const profileDir = `/tmp/chrome-clean-${Date.now()}`;
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9255',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    `--user-data-dir=${profileDir}`,
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9255/json/list').then(r => r.json());
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
    await new Promise((resolve, reject) => {
      ws.onopen = resolve;
      ws.onerror = reject;
    });
    let id = 1;
    const callbacks = new Map();

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg.result);
        callbacks.delete(msg.id);
      }
    };

    const send = (method, params = {}) => new Promise((resolve) => {
      const msgId = id++;
      callbacks.set(msgId, resolve);
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });

    await send('Page.enable');
    await send('Runtime.enable');
    await send('Page.navigate', { url: 'http://localhost:3000/#gioi-thieu' });
    await new Promise(r => setTimeout(r, 2000));

    // Scroll to #gioi-thieu
    await send('Runtime.evaluate', {
      expression: `
        const el = document.getElementById("gioi-thieu");
        if (el) el.scrollIntoView({ behavior: "instant" });
      `
    });
    await new Promise(r => setTimeout(r, 500));

    const info = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
          const h2 = document.getElementById("layers-title");
          const ps = Array.from(header.querySelectorAll("p"));
          return JSON.stringify({
            headerWidth: header.offsetWidth,
            headerMaxWidth: window.getComputedStyle(header).maxWidth,
            h2Styles: {
              fontSize: window.getComputedStyle(h2).fontSize,
              lineHeight: window.getComputedStyle(h2).lineHeight,
              margin: window.getComputedStyle(h2).margin,
              fontFamily: window.getComputedStyle(h2).fontFamily,
              innerText: h2.innerText
            },
            ps: ps.map(p => ({
              text: p.innerText,
              margin: window.getComputedStyle(p).margin,
              fontSize: window.getComputedStyle(p).fontSize,
              lineHeight: window.getComputedStyle(p).lineHeight
            }))
          });
        })()
      `,
      returnByValue: true
    });
    console.log("INFO:", info.result?.value);

    // Scroll so header is nicely in view
    await send('Runtime.evaluate', {
      expression: `
        const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
        if (header) {
          const top = header.getBoundingClientRect().top + window.scrollY;
          window.scrollTo(0, top - 80);
        }
      `
    });
    await new Promise(r => setTimeout(r, 600));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/current_layers_lead.png', Buffer.from(shot.data, 'base64'));
    console.log("Saved full viewport screenshot scripts/current_layers_lead.png");

    ws.close();
  } finally {
    chrome.kill('SIGKILL');
  }
}

test().catch(console.error);
