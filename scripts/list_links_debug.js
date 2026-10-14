const cp = require('child_process');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9231',
    '--disable-gpu',
    '--no-sandbox'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9231/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    let id = 1;
    const pending = new Map();
    const send = (m, p = {}) => new Promise(res => {
      const mid = id++; pending.set(mid, res); ws.send(JSON.stringify({ id: mid, method: m, params: p }));
    });
    ws.onmessage = e => {
      const m = JSON.parse(e.data);
      if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
    };
    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');
    await send('Page.navigate', { url: 'http://localhost:3000' });
    await new Promise(r => setTimeout(r, 2000));

    const links = await send('Runtime.evaluate', {
      expression: `Array.from(document.querySelectorAll('a')).map(a => ({ href: a.href, text: a.textContent.trim(), cls: a.className })).filter(a => a.href.includes('son-mai'))`,
      returnByValue: true
    });
    console.log('Son mai links in page:', JSON.stringify(links.result.value, null, 2));
  } finally {
    chrome.kill();
  }
}
test();
