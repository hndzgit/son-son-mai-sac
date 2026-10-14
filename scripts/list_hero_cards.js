const cp = require('child_process');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9232',
    '--disable-gpu',
    '--no-sandbox'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9232/json/list').then(r => r.json());
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
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

    const cards = await send('Runtime.evaluate', {
      expression: `Array.from(document.querySelectorAll('.homeHero_featureCards__ZFG_k a')).map(a => ({ href: a.href, html: a.innerHTML.slice(0, 100), text: a.textContent.trim() }))`,
      returnByValue: true
    });
    console.log('Hero feature cards:', JSON.stringify(cards.result.value, null, 2));
  } finally {
    chrome.kill();
  }
}
test();
