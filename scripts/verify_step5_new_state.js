const cp = require('child_process');
const fs = require('fs');

async function verify() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9298',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1100'
  ]);
  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9298/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
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

    console.log('--- 1. Testing /kham-pha#process-workshop-panel Step 1 & 5 ---');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha#process-workshop-panel' });
    await new Promise(r => setTimeout(r, 3000));

    // Scroll to simulator
    await send('Runtime.evaluate', {
      expression: `document.getElementById('simulator')?.scrollIntoView({ behavior: 'instant', block: 'start' })`
    });
    await new Promise(r => setTimeout(r, 1000));

    // Check Step 1 styles
    const step1Styles = await send('Runtime.evaluate', {
      expression: `(() => {
        const boardContext = document.querySelector('.productExperience_boardContext__7W1Go');
        const choiceBtn = document.querySelector('.productExperience_studioChoices__jssx6 button');
        const board = document.querySelector('.productExperience_studioBoard__D_pEz');
        return {
          boardContextBg: boardContext ? window.getComputedStyle(boardContext).backgroundColor : null,
          choiceBtnBg: choiceBtn ? window.getComputedStyle(choiceBtn).backgroundColor : null,
          boardBg: board ? window.getComputedStyle(board).backgroundColor : null
        };
      })()`,
      returnByValue: true
    });
    console.log('Step 1 computed styles:', step1Styles.result.value);

    let shot1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_step1_golden_red.png', Buffer.from(shot1.data, 'base64'));
    console.log('Saved scripts/verify_step1_golden_red.png');

    // Advance to Step 5
    // Step 1: click shape & mat, advance
    await send('Runtime.evaluate', {
      expression: `(() => {
        document.querySelector('.productExperience_studioChoices__jssx6 button')?.click();
        document.querySelector('.productExperience_materialChoices__hbtcl button')?.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 500));
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_advanceButton__QVqIC')?.click()`
    });
    await new Promise(r => setTimeout(r, 1000));

    // Step 2: click all 4 tasks, advance
    for (let t = 0; t < 4; t++) {
      await send('Runtime.evaluate', {
        expression: `document.querySelectorAll('.productExperience_vocTasks__wd_6j button')[${t}]?.click()`
      });
      await new Promise(r => setTimeout(r, 400));
    }
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_advanceButton__QVqIC')?.click()`
    });
    await new Promise(r => setTimeout(r, 1000));

    // Step 3: click color and advance
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_colorChoices__sVGIt button')?.click()`
    });
    await new Promise(r => setTimeout(r, 400));
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_advanceButton__QVqIC')?.click()`
    });
    await new Promise(r => setTimeout(r, 1000));

    // Step 4: advance to step 5
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_advanceButton__QVqIC')?.click()`
    });
    await new Promise(r => setTimeout(r, 1200));

    // Check Step 5 buttons
    const step5Buttons = await send('Runtime.evaluate', {
      expression: `(() => {
        const finishActions = document.querySelector('.productExperience_finishActions___wK4h');
        if (!finishActions) return 'No finishActions found';
        const btns = Array.from(finishActions.querySelectorAll('button'));
        return btns.map(b => ({
          text: b.innerText.split('\\n')[0].trim(),
          sub: b.querySelector('small')?.innerText,
          disabled: b.disabled,
          bg: window.getComputedStyle(b).backgroundColor,
          color: window.getComputedStyle(b).color
        }));
      })()`,
      returnByValue: true
    });
    console.log('Step 5 buttons list:', JSON.stringify(step5Buttons.result.value, null, 2));

    // Scroll to controls and capture step 5
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_galleryControls__WppUe')?.scrollIntoView({ behavior: 'instant', block: 'center' })`
    });
    await new Promise(r => setTimeout(r, 800));
    let shot5 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_step5_single_coat_button.png', Buffer.from(shot5.data, 'base64'));
    console.log('Saved scripts/verify_step5_single_coat_button.png');

    // Test clicking "Phủ lớp sơn trong" to verify it unlocks "Mài nước"
    const clickCoatRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const coatBtn = document.querySelector('.productExperience_finishActions___wK4h button');
        if (coatBtn) {
          coatBtn.click();
          return 'Clicked coatBtn';
        }
        return 'No coatBtn';
      })()`,
      returnByValue: true
    });
    console.log('Coat button click result:', clickCoatRes.result.value);
    await new Promise(r => setTimeout(r, 800));

    const step5AfterCoat = await send('Runtime.evaluate', {
      expression: `(() => {
        const finishActions = document.querySelector('.productExperience_finishActions___wK4h');
        const btns = Array.from(finishActions.querySelectorAll('button'));
        return btns.map(b => ({
          text: b.innerText.split('\\n')[0].trim(),
          disabled: b.disabled
        }));
      })()`,
      returnByValue: true
    });
    console.log('Step 5 buttons after clicking coat:', step5AfterCoat.result.value);

    console.log('--- 2. Testing /kham-pha Workshop section ---');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 3000));

    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('.processWorkshop_workshop__zFp89') || document.getElementById('5-cong-doan');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
      })()`
    });
    await new Promise(r => setTimeout(r, 1000));

    let shotKhamPha = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_khampha_workshop_golden.png', Buffer.from(shotKhamPha.data, 'base64'));
    console.log('Saved scripts/verify_khampha_workshop_golden.png');

  } finally {
    chrome.kill();
  }
}

verify().catch(console.error);
