const cp = require('child_process');

async function testStage5() {
  console.log('--- Starting Chrome to test Stage 5 on http://localhost:3000/kham-pha ---');
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9292',
    '--no-sandbox',
    '--window-size=1280,1000'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9292/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets[0]) {
    console.error('Failed to connect to Chrome debugging port 9292');
    chrome.kill();
    process.exit(1);
  }

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  let id = 1;
  const callbacks = new Map();
  const errors = [];
  const logs = [];

  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.method === 'Runtime.consoleAPICalled') {
      const text = msg.params.args.map(a => a.value || a.description || '').join(' ');
      if (msg.params.type === 'error') {
        errors.push(text);
      } else {
        logs.push(text);
      }
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      errors.push(msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || ''));
    }
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

  await send('Page.navigate', { url: 'http://localhost:3000/kham-pha#cong-doan-5' });
  await new Promise(r => setTimeout(r, 3000));

  // Dismiss any guide modal if present
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('BỎ QUA'));
        if (b) b.click();
      })()
    `
  });
  await new Promise(r => setTimeout(r, 600));

  // 1. Check 5 Stages section
  const stageInfo = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const item5 = document.querySelector('#cong-doan-5');
        const btn = item5 ? item5.querySelector('button') : null;
        if (btn) btn.click();
        const titleEl = item5 ? item5.querySelector('.core-v4-step-title') : null;
        const shortEl = item5 ? item5.querySelector('.core-v4-step-short') : null;
        const detailEl = document.querySelector('#core-v4-process-detail p');
        return {
          title: titleEl ? titleEl.textContent : '',
          short: shortEl ? shortEl.textContent : '',
          detail: detailEl ? detailEl.textContent : ''
        };
      })()
    `,
    returnByValue: true
  });
  console.log('\n=== 1. Stage 5 (5 Chặng Quy Trình) Info ===');
  console.log('Title :', stageInfo.result?.value?.title);
  console.log('Short :', stageInfo.result?.value?.short);
  console.log('Detail:', stageInfo.result?.value?.detail);

  // 2. Advance studio to Stage 4 (Công đoạn 5)
  console.log('\n=== 2. Opening Studio Stage 4 (Công đoạn 5) ===');
  await send('Runtime.evaluate', {
    expression: `
      (() => {
        const stageItems = document.querySelectorAll('ol[class*="stageList"] li');
        if (stageItems && stageItems[4]) {
          stageItems[4].click();
        }
      })()
    `
  });
  await new Promise(r => setTimeout(r, 1000));

  // 3. Inspect the buttons and sections in Stage 4
  const studioInfo = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const container = document.querySelector('#studio-finish') || document.querySelector('div[class*="galleryControls"]');
        if (!container) return { found: false };

        const labels = Array.from(container.querySelectorAll('span[class*="choiceLabel"]')).map(el => el.textContent.trim());
        const buttons = Array.from(container.querySelectorAll('div[class*="finishActions"] button, button[class*="studio_main_grind_btn"]')).map(btn => ({
          strong: btn.querySelector('strong')?.textContent?.trim() || btn.textContent?.trim(),
          small: btn.querySelector('small')?.textContent?.trim() || ''
        }));
        const guide = container.querySelector('.studio_core_guide')?.textContent?.trim() || '';

        return {
          found: true,
          labels,
          buttons,
          guide
        };
      })()
    `,
    returnByValue: true
  });
  console.log('Studio Found:', studioInfo.result?.value?.found);
  console.log('Section labels:', studioInfo.result?.value?.labels);
  console.log('Buttons:', studioInfo.result?.value?.buttons);
  console.log('Guide text:', studioInfo.result?.value?.guide);

  // 4. Test clicking the sequence: Mài nước -> Phủ lớp sơn trong -> Ủ khô -> Đánh bóng
  console.log('\n=== 3. Testing Click Sequence in Stage 4 ===');
  
  // Step 2: Mài nước click
  const grindRes = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const grindBtn = document.querySelector('button[class*="studio_main_grind_btn"]');
        if (grindBtn) {
          grindBtn.click();
          return { clicked: true, text: grindBtn.textContent.trim() };
        }
        return { clicked: false };
      })()
    `,
    returnByValue: true
  });
  console.log('Clicked Mài nước:', grindRes.result?.value);
  await new Promise(r => setTimeout(r, 600));

  // Step 3: Phủ lớp sơn trong click
  const clearCoatRes = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button[class*="studio_coat_btn"]'));
        // Find the clear coat button (second coat btn or one with 'trong')
        const clearCoatBtn = btns.find(b => b.textContent.includes('trong')) || btns[btns.length - 1];
        if (clearCoatBtn) {
          clearCoatBtn.click();
          return { clicked: true, text: clearCoatBtn.textContent.trim() };
        }
        return { clicked: false };
      })()
    `,
    returnByValue: true
  });
  console.log('Clicked Phủ lớp sơn trong:', clearCoatRes.result?.value);
  await new Promise(r => setTimeout(r, 600));

  // Step 3: Ủ khô click
  const dryRes = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const btns = Array.from(document.querySelectorAll('button[class*="studio_dry_btn"]'));
        // Find the dry button for clear coat
        const dryBtn = btns[btns.length - 1];
        if (dryBtn) {
          dryBtn.click();
          return { clicked: true, text: dryBtn.textContent.trim() };
        }
        return { clicked: false };
      })()
    `,
    returnByValue: true
  });
  console.log('Clicked Ủ khô:', dryRes.result?.value);
  await new Promise(r => setTimeout(r, 600));

  // Step 4: Đánh bóng hoàn thiện click
  const polishRes = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const polishBtn = document.querySelector('button[class*="studio_polish_btn"]');
        if (polishBtn) {
          polishBtn.click();
          return { clicked: true, text: polishBtn.textContent.trim() };
        }
        return { clicked: false };
      })()
    `,
    returnByValue: true
  });
  console.log('Clicked Đánh bóng hoàn thiện:', polishRes.result?.value);
  await new Promise(r => setTimeout(r, 600));

  // Check notice message
  const msgRes = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const msgEl = document.querySelector('p[class*="message"]') || document.querySelector('[role="status"]');
        return msgEl ? msgEl.textContent.trim() : '';
      })()
    `,
    returnByValue: true
  });
  console.log('Status message after full sequence:', msgRes.result?.value);

  // Verify errors
  console.log('\n=== 4. Error Check ===');
  console.log('Total Console Errors:', errors.length);
  if (errors.length > 0) {
    errors.forEach((err, idx) => console.log(`  [Error ${idx+1}]`, err));
  } else {
    console.log('SUCCESS: 0 console errors, 0 exceptions, 0 hydration warnings!');
  }

  ws.close();
  chrome.kill();
}

testStage5().catch(e => {
  console.error(e);
  process.exit(1);
});
