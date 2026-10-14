const cp = require('child_process');
const fs = require('fs');

async function run() {
  const profileDir = `/tmp/chrome-clean-${Date.now()}`;
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9256',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    `--user-data-dir=${profileDir}`,
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9256/json/list').then(r => r.json());
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
        const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
        if (header) {
          const top = header.getBoundingClientRect().top + window.scrollY;
          window.scrollTo(0, top - 80);
        }
      `
    });
    await new Promise(r => setTimeout(r, 400));

    // --- TEST OPTION 1: Break after "LÀM NÊN" ---
    // NHỮNG ĐẶC TRƯNG LÀM NÊN<br/>SƠN MÀI
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          const h2 = document.getElementById("layers-title");
          const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
          const section = document.querySelector(".coreIntroduction_layersSection__G7C0S");
          const ps = Array.from(header.querySelectorAll("p"));

          // Apply Option 1 Title
          h2.innerHTML = 'NHỮNG ĐẶC TRƯNG LÀM NÊN<br/>SƠN MÀI';
          h2.style.fontSize = 'clamp(36px, 3.4vw, 50px)';
          h2.style.lineHeight = '1.12';
          h2.style.letterSpacing = '-0.03em';
          h2.style.margin = '0 0 16px 0';
          h2.style.wordBreak = 'keep-all';
          h2.style.whiteSpace = 'normal';

          // Allow header to fit the text comfortably
          header.style.maxWidth = '580px';
          if (section) {
            section.style.gridTemplateColumns = 'minmax(340px, 0.48fr) minmax(0, 1fr)';
          }

          // Spacing for paragraphs
          if (ps[0]) {
            ps[0].style.margin = '0 0 12px 0';
            ps[0].style.fontSize = '14.5px';
            ps[0].style.lineHeight = '1.65';
            ps[0].style.maxWidth = '460px';
          }
          if (ps[1]) {
            ps[1].style.margin = '0';
            ps[1].style.fontSize = '14px';
            ps[1].style.lineHeight = '1.65';
            ps[1].style.maxWidth = '460px';
          }
        })()
      `
    });
    await new Promise(r => setTimeout(r, 300));
    let shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_option1_break_nen.png', Buffer.from(shot.data, 'base64'));
    console.log("Saved scripts/test_option1_break_nen.png");

    // Check lines of h2
    let evalLines = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const h2 = document.getElementById("layers-title");
          return JSON.stringify({
            offsetHeight: h2.offsetHeight,
            innerText: h2.innerText
          });
        })()
      `,
      returnByValue: true
    });
    console.log("Option 1 h2:", evalLines.result?.value);

    // --- TEST OPTION 2: Break after "SƠN" ---
    // NHỮNG ĐẶC TRƯNG LÀM NÊN SƠN<br/>MÀI
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          const h2 = document.getElementById("layers-title");
          h2.innerHTML = 'NHỮNG ĐẶC TRƯNG LÀM NÊN SƠN<br/>MÀI';
        })()
      `
    });
    await new Promise(r => setTimeout(r, 300));
    shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_option2_break_son.png', Buffer.from(shot.data, 'base64'));
    console.log("Saved scripts/test_option2_break_son.png");

    evalLines = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const h2 = document.getElementById("layers-title");
          return JSON.stringify({
            offsetHeight: h2.offsetHeight,
            innerText: h2.innerText
          });
        })()
      `,
      returnByValue: true
    });
    console.log("Option 2 h2:", evalLines.result?.value);

    ws.close();
  } finally {
    chrome.kill('SIGKILL');
  }
}

run().catch(console.error);
