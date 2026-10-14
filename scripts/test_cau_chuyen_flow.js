const cp = require('child_process');
const fs = require('fs');

async function runTest() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9245',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,1080'
  ]);

  let targets = null;
  for (let i = 0; i < 25; i++) {
    try {
      targets = await fetch('http://localhost:9245/json/list').then(r => r.json());
      if (targets && targets.length) break;
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets.length) {
    console.error('Could not connect to Chrome debugging port.');
    chrome.kill();
    return;
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

    console.log('1. Navigating to /cau-chuyen-son-mai...');
    await send('Page.navigate', { url: 'http://localhost:3000/cau-chuyen-son-mai' });
    await new Promise(r => setTimeout(r, 2200));

    // Cuộn tới dòng thời gian
    await send('Runtime.evaluate', {
      expression: `
        const el = document.getElementById('dong-thoi-gian');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
      `
    });
    await new Promise(r => setTimeout(r, 800));

    // Chụp ảnh nút "Đọc bài viết chi tiết →" trên timeline
    const shotTimeline = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_timeline_button.png', Buffer.from(shotTimeline.data, 'base64'));
    console.log('Saved scripts/verify_timeline_button.png');

    // Lấy thông tin nút đọc bài viết
    const btnInfo = await send('Runtime.evaluate', {
      expression: `
        const btn = document.querySelector('.story_readToggle__Fczbq');
        btn ? { tag: btn.tagName, text: btn.textContent, href: btn.href } : null;
      `,
      returnByValue: true
    });
    console.log('Read article button info:', btnInfo.result.value);

    // Click nút đọc bài viết
    console.log('2. Clicking read article button...');
    await send('Runtime.evaluate', {
      expression: `
        const btn = document.querySelector('.story_readToggle__Fczbq');
        if (btn) btn.click();
      `
    });
    await new Promise(r => setTimeout(r, 2000));

    // Lấy URL hiện tại
    const currentUrl = await send('Runtime.evaluate', {
      expression: `window.location.href`,
      returnByValue: true
    });
    console.log('Current URL after click:', currentUrl.result.value);

    // Chụp ảnh trang đọc bài viết vừa mở
    const shotReader = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_navigated_reader.png', Buffer.from(shotReader.data, 'base64'));
    console.log('Saved scripts/verify_navigated_reader.png');

    // Test chuyển sang mốc 3 (Nghệ thuật hiện đại) trên ruy băng của trang bài viết
    console.log('3. Testing switching to milestone 3 on reader ribbon...');
    await send('Runtime.evaluate', {
      expression: `
        switchArticle(3);
      `
    });
    await new Promise(r => setTimeout(r, 1000));

    const shotReader3 = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/verify_reader_milestone3.png', Buffer.from(shotReader3.data, 'base64'));
    console.log('Saved scripts/verify_reader_milestone3.png');

    const heading3 = await send('Runtime.evaluate', {
      expression: `document.getElementById('art-heading').textContent`,
      returnByValue: true
    });
    console.log('Milestone 3 heading rendered:', heading3.result.value);

  } finally {
    chrome.kill();
  }
}

runTest();
