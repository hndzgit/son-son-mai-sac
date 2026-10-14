const cp = require('child_process');
const fs = require('fs');

async function snapSections() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9256',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,1100'
  ]);

  for (let i = 0; i < 30; i++) {
    try {
      const targets = await fetch('http://localhost:9256/json/list').then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) break;
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  const targets = await fetch('http://localhost:9256/json/list').then(r => r.json());
  const validTarget = targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
  const ws = new WebSocket(validTarget.webSocketDebuggerUrl);

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

  await send('Page.navigate', { url: 'http://localhost:3000/ve-du-an' });
  await new Promise(r => setTimeout(r, 2000));

  const sections = [
    { id: 'gioi-thieu-du-an', name: 'section_1_story.png' },
    { id: 'su-menh', name: 'section_2_mission.png' },
    { id: 'doi-ngu', name: 'section_3_team.png' },
    { id: 'lien-he', name: 'section_4_contact.png' }
  ];

  for (const s of sections) {
    await send('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('${s.id}');
        if (el) el.scrollIntoView({ block: 'start', behavior: 'instant' });
      })()`
    });
    await new Promise(r => setTimeout(r, 800));
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(`scripts/${s.name}`, Buffer.from(shot.data, 'base64'));
    console.log(`Saved scripts/${s.name}`);
  }

  chrome.kill();
}

snapSections().catch(console.error);
