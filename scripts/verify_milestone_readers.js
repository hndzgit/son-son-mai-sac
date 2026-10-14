const cp = require('child_process');
const fs = require('fs');

async function test() {
  const profileDir = `/tmp/chrome-milestones-${Date.now()}`;
  const port = 9251;
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    `--user-data-dir=${profileDir}`,
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch(`http://localhost:${port}/json/list`).then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) {
        targets = [valid];
        break;
      }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets[0]) {
    console.error("Could not connect to Chrome");
    chrome.kill();
    process.exit(1);
  }

  try {
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const callbacks = new Map();

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg.result);
        callbacks.delete(msg.id);
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

    console.log("Navigating to http://localhost:3000/cau-chuyen-son-mai ...");
    await send('Page.navigate', { url: 'http://localhost:3000/cau-chuyen-son-mai' });
    await new Promise(r => setTimeout(r, 2000));

    // Test 6 tabs
    for (let i = 0; i < 6; i++) {
      await send('Runtime.evaluate', {
        expression: `document.getElementById('timeline-tab-${i}').click();`
      });
      await new Promise(r => setTimeout(r, 200));

      const evalRes = await send('Runtime.evaluate', {
        expression: `
          (() => {
            const btn = document.querySelector('.story_readToggle__Fczbq');
            return JSON.stringify({
              text: btn ? btn.textContent.trim() : null,
              href: btn ? btn.getAttribute('href') : null
            });
          })()
        `,
        returnByValue: true
      });
      const parsed = JSON.parse(evalRes.result.value);
      console.log(`[Tab ${i + 1}] Button Text: "${parsed.text}", Link: "${parsed.href}"`);
    }

    // Capture screenshot of timeline
    const ss1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_timeline_result.png', Buffer.from(ss1.data, 'base64'));
    console.log("Screenshot saved to scripts/verify_timeline_result.png");

    // Click on button for Tab 0 (Milestone 1)
    console.log("Clicking button to open dedicated milestone reader...");
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.story_readToggle__Fczbq').click();`
    });
    await new Promise(r => setTimeout(r, 1500));

    const pageRes = await send('Runtime.evaluate', {
      expression: `
        (() => {
          return JSON.stringify({
            url: window.location.href,
            title: document.title,
            kicker: document.getElementById('art-kicker')?.textContent?.trim(),
            heading: document.getElementById('art-heading')?.textContent?.trim(),
            badge: document.getElementById('art-badge-org')?.textContent?.trim()
          });
        })()
      `,
      returnByValue: true
    });
    console.log("Reader page opened:", JSON.parse(pageRes.result.value));

    const ss2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_reader_result.png', Buffer.from(ss2.data, 'base64'));
    console.log("Screenshot saved to scripts/verify_reader_result.png");

    // Also test direct navigation to milestone 4
    console.log("Navigating to http://localhost:3000/cau-chuyen-son-mai/bai-viet/4 ...");
    await send('Page.navigate', { url: 'http://localhost:3000/cau-chuyen-son-mai/bai-viet/4' });
    await new Promise(r => setTimeout(r, 1500));

    const m4Res = await send('Runtime.evaluate', {
      expression: `
        (() => {
          return JSON.stringify({
            url: window.location.href,
            title: document.title,
            heading: document.getElementById('art-heading')?.textContent?.trim(),
            kicker: document.getElementById('art-kicker')?.textContent?.trim()
          });
        })()
      `,
      returnByValue: true
    });
    console.log("Milestone 4 reader details:", JSON.parse(m4Res.result.value));

    ws.close();
  } finally {
    chrome.kill();
    fs.rmSync(profileDir, { recursive: true, force: true });
  }
}

test().catch(e => {
  console.error("Test error:", e);
  process.exit(1);
});
