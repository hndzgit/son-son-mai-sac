const cp = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9230',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1200',
    '--user-data-dir=/tmp/chrome-test-stage14'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const targets = await fetch('http://127.0.0.1:9230/json/list').then(r => r.json());
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

    console.log('Navigating to http://localhost:3000/kham-pha ...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 4500));

    // 1. Verify Stage 1 checkbox text
    const s1Info = await send('Runtime.evaluate', {
      expression: `(() => {
        const check = document.querySelector('.studio_reinforce_check');
        return {
          checkText: check ? check.textContent.trim() : null
        };
      })()`
    });
    console.log('Stage 1 Checkbox Text:', s1Info.result?.value);

    // Scroll to simulator panel and capture Stage 1 screenshot
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('process-workshop-panel');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
      })()`
    });
    await new Promise(r => setTimeout(r, 800));

    let shot1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_stage1_after_fix.png', Buffer.from(shot1.data, 'base64'));
    console.log('Saved scripts/verify_stage1_after_fix.png');

    // 2. Navigate to Stage 4
    console.log('Clicking to Stage 4...');
    const navResult = await send('Runtime.evaluate', {
      expression: `(() => {
        // Find stage list item for stage 4
        const stageListItems = document.querySelectorAll('.productExperience_stageList__k9Koe li, ol[aria-label="Tiến trình thực hiện"] li');
        let s4Btn = null;
        stageListItems.forEach((li, idx) => {
          if (idx === 3 || li.textContent.includes('TẠO HÌNH VÀ TRANG TRÍ')) {
            s4Btn = li.querySelector('button') || li;
          }
        });
        if (s4Btn) {
          s4Btn.disabled = false;
          s4Btn.click();
          return { clicked: true };
        }
        return { clicked: false, count: stageListItems.length };
      })()`
    });
    console.log('Navigated to Stage 4:', navResult.result?.value);

    await new Promise(r => setTimeout(r, 1200));

    // Inspect Stage 4 DOM elements
    const s4Info = await send('Runtime.evaluate', {
      expression: `(() => {
        const guide = document.querySelector('.studio_core_guide');
        const callout = document.querySelector('.studio_core_callout');
        const dots = document.querySelectorAll('.studio_material_dot');
        const check = document.querySelector('.studio_reinforce_check');
        const status = document.querySelector('.studio_stage_status');
        const motifNote = document.querySelector('.studio_motif_subnote');
        return {
          guide: guide ? guide.textContent.trim() : null,
          calloutStrong: callout ? callout.querySelector('strong')?.textContent : null,
          calloutP: callout ? callout.querySelector('p')?.textContent : null,
          dotsCount: dots.length,
          checkText: check ? check.textContent.trim() : null,
          statusText: status ? status.textContent.trim() : null,
          motifNote: motifNote ? motifNote.textContent.trim() : null
        };
      })()`
    });
    console.log('Stage 4 Elements:', s4Info.result?.value);

    // Capture Stage 4 screenshot
    let shot4 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_stage4_rich_controls.png', Buffer.from(shot4.data, 'base64'));
    console.log('Saved scripts/verify_stage4_rich_controls.png');

    // Test clicking material "Vàng quỳ"
    await send('Runtime.evaluate', {
      expression: `(() => {
        const matButtons = document.querySelectorAll('.productExperience_materialChoices__hbtcl button');
        matButtons.forEach(btn => {
          if (btn.textContent.includes('Vàng quỳ')) btn.click();
        });
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    const s4VangInfo = await send('Runtime.evaluate', {
      expression: `(() => {
        const callout = document.querySelector('.studio_core_callout');
        return {
          calloutStrong: callout ? callout.querySelector('strong')?.textContent : null,
          calloutP: callout ? callout.querySelector('p')?.textContent : null
        };
      })()`
    });
    console.log('After clicking Vàng quỳ:', s4VangInfo.result?.value);

    let shotVang = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_stage4_gold_selected.png', Buffer.from(shotVang.data, 'base64'));
    console.log('Saved scripts/verify_stage4_gold_selected.png');

  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
