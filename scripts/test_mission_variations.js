const cp = require('child_process');
const fs = require('fs');

async function testVariations() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9238',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9238/json/list').then(r => r.json());
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

    // Scroll to mission section
    await send('Runtime.evaluate', {
      expression: `(() => {
        const sec = document.querySelector('.project_mission__f2EwM');
        if (sec) sec.scrollIntoView({ block: 'center' });
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    // Option A: Single Box (One Box)
    await send('Runtime.evaluate', {
      expression: `(() => {
        const style = document.createElement('style');
        style.id = 'test-var-perfect';
        style.textContent = \`
          .project_mission__f2EwM {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: clamp(36px, 5vw, 64px) !important;
            padding: clamp(36px, 4.5vw, 56px) !important;
            border: 1px solid #c6a663 !important;
            border-radius: 16px !important;
            background: linear-gradient(145deg, rgba(255, 248, 235, 0.92), rgba(246, 234, 206, 0.75)) !important;
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
            font-size: clamp(23px, 1.9vw, 28px) !important;
            line-height: 1.35 !important;
            color: #8b2a2a !important;
            margin: 12px 0 20px !important;
            min-height: 76px !important;
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
        \`;
        document.head.appendChild(style);
      })()`
    });
    await new Promise(r => setTimeout(r, 400));
    const shot1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_mission_onebox_2lines.png', Buffer.from(shot1.data, 'base64'));
    console.log('Saved onebox 2lines');

    // Option B: Two separate cards
    await send('Runtime.evaluate', {
      expression: `(() => {
        const style = document.getElementById('test-var-perfect');
        style.textContent = \`
          .project_mission__f2EwM {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 28px !important;
            padding: 0 !important;
            border-block: none !important;
            max-width: 1220px !important;
            margin: 0 auto clamp(80px, 10vw, 142px) !important;
            box-sizing: border-box !important;
          }
          .project_mission__f2EwM > div {
            background: linear-gradient(145deg, rgba(255, 248, 235, 0.92), rgba(246, 234, 206, 0.75)) !important;
            border: 1px solid #c6a663 !important;
            border-radius: 16px !important;
            padding: clamp(32px, 3.5vw, 48px) !important;
            box-shadow: 0 12px 32px rgba(76, 43, 20, 0.08) !important;
            display: flex !important;
            flex-direction: column !important;
            box-sizing: border-box !important;
          }
          .project_mission__f2EwM h2,
          .project_mission__f2EwM h3 {
            font-family: "Project Display", "Playfair Display", Georgia, serif !important;
            font-size: clamp(23px, 1.9vw, 28px) !important;
            line-height: 1.35 !important;
            color: #8b2a2a !important;
            margin: 12px 0 20px !important;
            min-height: 76px !important;
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
        \`;
      })()`
    });
    await new Promise(r => setTimeout(r, 400));
    const shot2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_mission_twocards_2lines.png', Buffer.from(shot2.data, 'base64'));
    console.log('Saved twocards 2lines');

    ws.close();
  } finally {
    chrome.kill();
  }
}
testVariations();
