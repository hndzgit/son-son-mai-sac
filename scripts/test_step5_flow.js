const cp = require('child_process');
const fs = require('fs');

async function testFlow() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9288',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1100'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9288/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets) {
    chrome.kill();
    throw new Error('Chrome target not found');
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

    console.log('Navigating to http://localhost:3000/kham-pha#process-workshop-panel...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha#process-workshop-panel' });
    await new Promise(r => setTimeout(r, 2500));

    // Scroll to simulator
    await send('Runtime.evaluate', {
      expression: `document.getElementById('simulator')?.scrollIntoView({ behavior: 'instant', block: 'start' })`
    });
    await new Promise(r => setTimeout(r, 800));

    // Step 0: Cốt mộc
    console.log('Interacting with Step 0...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const shapeBtns = document.querySelectorAll('.productExperience_studioChoices__jssx6 button');
        const matBtns = document.querySelectorAll('.productExperience_materialChoices__hbtcl button');
        if (shapeBtns[0]) shapeBtns[0].click();
        if (matBtns[0]) matBtns[0].click();
      })()`
    });
    await new Promise(r => setTimeout(r, 400));
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_advanceButton__QVqIC')?.click()`
    });
    await new Promise(r => setTimeout(r, 600));

    // Step 1: Làm vóc (4 tasks)
    console.log('Interacting with Step 1 (Làm vóc)...');
    for (let t = 0; t < 4; t++) {
      await send('Runtime.evaluate', {
        expression: `document.querySelectorAll('.productExperience_vocTasks__wd_6j button')[${t}]?.click()`
      });
      await new Promise(r => setTimeout(r, 300));
    }
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_advanceButton__QVqIC')?.click()`
    });
    await new Promise(r => setTimeout(r, 600));

    // Step 2: Sơn nền
    console.log('Interacting with Step 2 (Sơn nền)...');
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_colorChoices__sVGIt button')?.click()`
    });
    await new Promise(r => setTimeout(r, 300));
    for (let t = 0; t < 2; t++) {
      await send('Runtime.evaluate', {
        expression: `document.querySelectorAll('.productExperience_vocTasks__wd_6j button')[${t}]?.click()`
      });
      await new Promise(r => setTimeout(r, 300));
    }
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_advanceButton__QVqIC')?.click()`
    });
    await new Promise(r => setTimeout(r, 600));

    // Step 3: Tạo hình -> Advance to Step 4 (Công đoạn 05)
    console.log('Advancing to Step 4 (Công đoạn 05 / 05)...');
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_advanceButton__QVqIC')?.click()`
    });
    await new Promise(r => setTimeout(r, 1000));

    // Scroll controls into view
    await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_galleryControls__WppUe')?.scrollIntoView({ behavior: 'instant', block: 'center' })`
    });
    await new Promise(r => setTimeout(r, 600));

    // Check Initial Step 5 buttons
    const initialStep5 = await send('Runtime.evaluate', {
      expression: `(() => {
        const finishActions = document.querySelector('.productExperience_finishActions___wK4h');
        const btns = finishActions ? Array.from(finishActions.querySelectorAll('button')).map(b => ({
          text: b.innerText.split('\\n')[0].trim(),
          sub: b.querySelector('small')?.innerText,
          disabled: b.disabled,
          bg: window.getComputedStyle(b).backgroundColor,
          color: window.getComputedStyle(b).color
        })) : null;
        return { buttons: btns };
      })()`,
      returnByValue: true
    });
    console.log('Initial Step 5 buttons:', JSON.stringify(initialStep5.result.value, null, 2));

    let shotInitial = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/step5_4buttons_initial.png', Buffer.from(shotInitial.data, 'base64'));
    console.log('Saved scripts/step5_4buttons_initial.png');

    // 1. Click "Phủ lớp sơn trong"
    console.log('1. Clicking "Phủ lớp sơn trong"...');
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_finishActions___wK4h button')[0]?.click()`
    });
    await new Promise(r => setTimeout(r, 800));

    const stateAfterCoat = await send('Runtime.evaluate', {
      expression: `(() => {
        const btns = Array.from(document.querySelectorAll('.productExperience_finishActions___wK4h button')).map(b => ({
          text: b.innerText.split('\\n')[0].trim(),
          sub: b.querySelector('small')?.innerText,
          disabled: b.disabled
        }));
        return btns;
      })()`,
      returnByValue: true
    });
    console.log('Buttons after coat:', JSON.stringify(stateAfterCoat.result.value, null, 2));

    let shotCoated = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/step5_4buttons_coated.png', Buffer.from(shotCoated.data, 'base64'));
    console.log('Saved scripts/step5_4buttons_coated.png');

    // 2. Click "Ủ khô"
    console.log('2. Clicking "Ủ khô"...');
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_finishActions___wK4h button')[1]?.click()`
    });
    await new Promise(r => setTimeout(r, 800));

    const stateAfterDry = await send('Runtime.evaluate', {
      expression: `(() => {
        const btns = Array.from(document.querySelectorAll('.productExperience_finishActions___wK4h button')).map(b => ({
          text: b.innerText.split('\\n')[0].trim(),
          sub: b.querySelector('small')?.innerText,
          disabled: b.disabled
        }));
        return btns;
      })()`,
      returnByValue: true
    });
    console.log('Buttons after dry:', JSON.stringify(stateAfterDry.result.value, null, 2));

    let shotDried = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/step5_4buttons_dried.png', Buffer.from(shotDried.data, 'base64'));
    console.log('Saved scripts/step5_4buttons_dried.png');

    // 3. Click "Mài nước"
    console.log('3. Clicking "Mài nước"...');
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_finishActions___wK4h button')[2]?.click()`
    });
    await new Promise(r => setTimeout(r, 800));

    const stateAfterSand = await send('Runtime.evaluate', {
      expression: `(() => {
        const btns = Array.from(document.querySelectorAll('.productExperience_finishActions___wK4h button')).map(b => ({
          text: b.innerText.split('\\n')[0].trim(),
          sub: b.querySelector('small')?.innerText,
          disabled: b.disabled
        }));
        return btns;
      })()`,
      returnByValue: true
    });
    console.log('Buttons after sand:', JSON.stringify(stateAfterSand.result.value, null, 2));

  } finally {
    chrome.kill();
  }
}

testFlow().catch(console.error);
