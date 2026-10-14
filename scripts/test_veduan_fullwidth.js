const cp = require('child_process');
const fs = require('fs');

async function testLayout() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9229',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);
  await new Promise(r => setTimeout(r, 1500));
  try {
    const targets = await fetch('http://localhost:9229/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
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
    await send('Page.navigate', { url: 'http://localhost:3000/ve-du-an' });
    await new Promise(r => setTimeout(r, 1500));

    // Try variation 1: Full-width edge-to-edge
    await send('Runtime.evaluate', {
      expression: `(() => {
        const style = document.createElement('style');
        style.id = 'test-fullwidth';
        style.textContent = \`
          .project_page__UA7p9 {
            padding: 0 0 76px !important;
          }
          .project_page__UA7p9 > section:not(.project_hero__Oebd7) {
            padding-left: max(5vw, 20px) !important;
            padding-right: max(5vw, 20px) !important;
          }
          .project_hero__Oebd7 {
            max-width: 100% !important;
            width: 100% !important;
            border-left: none !important;
            border-right: none !important;
            border-radius: 0 !important;
            margin: 0 0 clamp(64px, 8vw, 110px) !important;
            padding: 0 clamp(24px, 5vw, 72px) !important;
          }
        \`;
        document.head.appendChild(style);
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    const shot1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_veduan_fullwidth_v1.png', Buffer.from(shot1.data, 'base64'));
    console.log('Saved test_veduan_fullwidth_v1.png');

    // Variation 2: with inset: 10px frame border like homeHero
    await send('Runtime.evaluate', {
      expression: `(() => {
        const style = document.getElementById('test-fullwidth');
        style.textContent = \`
          .project_page__UA7p9 {
            padding: 0 0 76px !important;
          }
          .project_page__UA7p9 > section:not(.project_hero__Oebd7) {
            padding-left: max(5vw, 20px) !important;
            padding-right: max(5vw, 20px) !important;
          }
          .project_hero__Oebd7 {
            max-width: 100% !important;
            width: 100% !important;
            border: none !important;
            border-radius: 0 !important;
            margin: 0 0 clamp(64px, 8vw, 110px) !important;
            padding: 12px clamp(24px, 4.5vw, 68px) !important;
            position: relative !important;
          }
          .project_hero__Oebd7:before {
            position: absolute !important;
            z-index: 0 !important;
            inset: 10px !important;
            border: 1px solid rgba(76, 43, 20, 0.32) !important;
            content: "" !important;
            pointer-events: none !important;
          }
        \`;
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    const shot2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_veduan_fullwidth_v2.png', Buffer.from(shot2.data, 'base64'));
    console.log('Saved test_veduan_fullwidth_v2.png');

    ws.close();
  } finally {
    chrome.kill();
  }
}
testLayout();
