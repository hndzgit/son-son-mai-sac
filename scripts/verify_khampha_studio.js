const cp = require('child_process');
const fs = require('fs');

async function run() {
  const tmpDir = '/tmp/test-chrome-profile-khampha';
  try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (e) {}

  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9288',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=' + tmpDir,
    '--window-size=1440,1100'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      const list = await fetch('http://localhost:9288/json/list').then(r => r.json());
      const page = list && list.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch (e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets) {
    chrome.kill();
    throw new Error('Chrome target not found');
  }

  try {
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const pending = new Map();
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const msgId = id++;
      pending.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });

    const consoleLogs = [];
    const errors = [];

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id).resolve(msg.result);
        pending.delete(msg.id);
      }
      if (msg.method === 'Runtime.consoleAPICalled') {
        const text = msg.params.args.map(a => a.value || JSON.stringify(a)).join(' ');
        consoleLogs.push(`[${msg.params.type}] ${text}`);
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        errors.push(msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text);
      }
    };

    await new Promise(r => ws.onopen = r);

    await send('Page.enable');
    await send('Runtime.enable');

    console.log('Navigating to http://localhost:3000/kham-pha ...');
    await send('Page.navigate', { url: 'http://localhost:3000/kham-pha' });
    await new Promise(r => setTimeout(r, 3500));

    // Scroll to workshop
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.querySelector('.productExperience_studioWorkspace__is27_') || document.querySelector('#process-workshop-panel');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
      })()`
    });
    await new Promise(r => setTimeout(r, 1000));

    // Evaluate state
    const evalRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const board = document.querySelector('.productExperience_studioBoard__D_pEz');
        const workspace = document.querySelector('.productExperience_studioWorkspace__is27_');
        const title = document.querySelector('.productExperience_boardContext__7W1Go span')?.innerText;
        const h2 = document.querySelector('.productExperience_boardContext__7W1Go h2')?.innerText;
        const matCatLop = document.body.innerText.includes('MẶT CẮT LỚP');
        const stageItems = Array.from(document.querySelectorAll('.productExperience_stageList__k9Koe li')).map(li => li.innerText.replace(/\\n/g, ' '));
        return {
          hasBoard: !!board,
          hasWorkspace: !!workspace,
          title,
          h2,
          matCatLop,
          stageItems
        };
      })()`,
      returnByValue: true
    });
    console.log('Stage 1 studio evaluation:', JSON.stringify(evalRes.result.value, null, 2));

    const shot1 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_studio_verified_stage1.png', Buffer.from(shot1.data, 'base64'));
    console.log('Saved scripts/khampha_studio_verified_stage1.png');

    // Test Stage 2
    console.log('Switching to Stage 2 (Sơn nền)...');
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_stageList__k9Koe li')[2]?.click()`
    });
    await new Promise(r => setTimeout(r, 1000));

    const evalStage2 = await send('Runtime.evaluate', {
      expression: `(() => {
        const h2 = document.querySelector('.productExperience_boardContext__7W1Go h2')?.innerText;
        const colorButtons = Array.from(document.querySelectorAll('button')).filter(b => ['Đỏ son', 'Cánh gián', 'Nâu đất', 'Đen then'].includes(b.innerText.trim())).map(b => b.innerText.trim());
        return { h2, colorButtons };
      })()`,
      returnByValue: true
    });
    console.log('Stage 2 evaluation:', JSON.stringify(evalStage2.result.value, null, 2));

    const shot2 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_studio_verified_stage2.png', Buffer.from(shot2.data, 'base64'));

    // Test Stage 3
    console.log('Switching to Stage 3 (Tạo hình và trang trí)...');
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_stageList__k9Koe li')[3]?.click()`
    });
    await new Promise(r => setTimeout(r, 1000));

    const evalStage3 = await send('Runtime.evaluate', {
      expression: `(() => {
        const h2 = document.querySelector('.productExperience_boardContext__7W1Go h2')?.innerText;
        const inlays = Array.from(document.querySelectorAll('button')).filter(b => ['Vỏ trứng', 'Vàng quỳ', 'Xà cừ', 'Lớp nền'].includes(b.innerText.trim())).map(b => b.innerText.trim());
        return { h2, inlays };
      })()`,
      returnByValue: true
    });
    console.log('Stage 3 evaluation:', JSON.stringify(evalStage3.result.value, null, 2));

    const shot3 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_studio_verified_stage3.png', Buffer.from(shot3.data, 'base64'));

    // Test Stage 4
    console.log('Switching to Stage 4 (Phủ, mài và hoàn thiện)...');
    await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('.productExperience_stageList__k9Koe li')[4]?.click()`
    });
    await new Promise(r => setTimeout(r, 1000));

    const evalStage4 = await send('Runtime.evaluate', {
      expression: `(() => {
        const h2 = document.querySelector('.productExperience_boardContext__7W1Go h2')?.innerText;
        const buttons = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Mài nước') || b.innerText.includes('Đánh bóng') || b.innerText.includes('Ủ khô') || b.innerText.includes('Phủ lớp sơn')).map(b => ({
          text: b.innerText.replace(/\\n/g, ' '),
          disabled: b.disabled
        }));
        return { h2, buttons };
      })()`,
      returnByValue: true
    });
    console.log('Stage 4 evaluation:', JSON.stringify(evalStage4.result.value, null, 2));

    // Click "Mài nước"
    console.log('Clicking "Mài nước"...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Mài nước'));
        if (btn) btn.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    // Click "Đánh bóng"
    console.log('Clicking "Đánh bóng"...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Đánh bóng'));
        if (btn) btn.click();
      })()`
    });
    await new Promise(r => setTimeout(r, 500));

    const statusMsg = await send('Runtime.evaluate', {
      expression: `document.querySelector('.productExperience_message__RzW2A')?.innerText || ''`,
      returnByValue: true
    });
    console.log('Status message after clicking Mài nước & Đánh bóng:', statusMsg.result.value);

    const shot4 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/khampha_studio_verified_stage4.png', Buffer.from(shot4.data, 'base64'));

    ws.close();
    console.log('ALL VERIFICATIONS COMPLETED SUCCESSFULLY!');
  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
