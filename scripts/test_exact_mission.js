const cp = require('child_process');
const fs = require('fs');

async function testAll() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9241',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9241/json/list').then(r => r.json());
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

    await send('Runtime.evaluate', {
      expression: `(() => {
        const sec = document.querySelector('.project_mission__f2EwM');
        if (sec) sec.scrollIntoView({ block: 'center' });
        const style = document.createElement('style');
        style.textContent = \`
          .project_mission__f2EwM {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: clamp(36px, 5vw, 64px) !important;
            padding: clamp(38px, 4.5vw, 56px) !important;
            border: 1px solid #c6a663 !important;
            border-radius: 16px !important;
            background: linear-gradient(145deg, rgba(255, 248, 235, 0.94), rgba(246, 234, 206, 0.78)) !important;
            box-shadow: 0 12px 32px rgba(76, 43, 20, 0.08) !important;
            max-width: 1220px !important;
            margin: 0 auto clamp(80px, 10vw, 142px) !important;
            box-sizing: border-box !important;
          }
          .project_mission__f2EwM > div {
            display: flex !important;
            flex-direction: column !important;
          }
          .project_mission__f2EwM > div:first-child {
            border-right: 1px solid rgba(198, 166, 99, 0.45) !important;
            padding-right: clamp(24px, 3.5vw, 44px) !important;
          }
          .project_mission__f2EwM h2,
          .project_mission__f2EwM h3 {
            font-family: "Project Display", "Playfair Display", Georgia, serif !important;
            font-size: clamp(21px, 1.75vw, 24px) !important;
            line-height: 1.35 !important;
            color: #8b2a2a !important;
            margin: 12px 0 20px !important;
            min-height: 65px !important;
            display: flex !important;
            align-items: flex-start !important;
          }
          .project_mission__f2EwM > div p {
            line-height: 1.8 !important;
            color: #574937 !important;
            margin: 0 0 16px !important;
          }
          .project_mission__f2EwM > div p:last-of-type {
            margin-bottom: 0 !important;
          }
          .project_mission__f2EwM > div:last-child a {
            margin-top: auto !important;
            padding-top: 16px !important;
          }
          @media (max-width: 820px) {
            .project_mission__f2EwM {
              grid-template-columns: 1fr !important;
              gap: 32px !important;
              padding: 32px 22px !important;
            }
            .project_mission__f2EwM > div:first-child {
              border-right: none !important;
              border-bottom: 1px solid rgba(198, 166, 99, 0.45) !important;
              padding-right: 0 !important;
              padding-bottom: 32px !important;
            }
            .project_mission__f2EwM h2,
            .project_mission__f2EwM h3 {
              min-height: 0 !important;
              font-size: 22px !important;
            }
          }
        \`;
        document.head.appendChild(style);
      })()`
    });
    await new Promise(r => setTimeout(r, 400));
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_mission_exact_desktop.png', Buffer.from(shot.data, 'base64'));
    console.log('Saved desktop');

    // Test mobile
    await send('Emulation.setDeviceMetricsOverride', {
      width: 414,
      height: 896,
      deviceScaleFactor: 1,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 400));
    const shotMobile = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_mission_exact_mobile.png', Buffer.from(shotMobile.data, 'base64'));
    console.log('Saved mobile');

    ws.close();
  } finally {
    chrome.kill();
  }
}
testAll();
