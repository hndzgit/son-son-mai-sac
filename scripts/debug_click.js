const cp = require('child_process');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9230',
    '--disable-gpu',
    '--no-sandbox'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9230/json/list').then(r => r.json());
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    let id = 1;
    const pending = new Map();
    const send = (m, p = {}) => new Promise(res => {
      const mid = id++; pending.set(mid, res); ws.send(JSON.stringify({ id: mid, method: m, params: p }));
    });
    ws.onmessage = e => {
      const m = JSON.parse(e.data);
      if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
      if (m.method === 'Runtime.consoleAPICalled') console.log('LOG:', m.params.args.map(a => a.value).join(' '));
    };
    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');
    await send('Page.navigate', { url: 'http://localhost:3000' });
    await new Promise(r => setTimeout(r, 2000));
    const evalRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const card = document.querySelector('a.homeHero_featureCard__BR7Jm[href="/son-mai-la-gi"]');
        console.log('Card found:', !!card, card ? card.href : null);
        if (card) {
          card.click();
          return { clicked: true, currentHref: window.location.href };
        }
        return { clicked: false };
      })()`,
      returnByValue: true
    });
    console.log('Eval result:', evalRes.result.value);
    await new Promise(r => setTimeout(r, 1500));
    const finalUrl = await send('Runtime.evaluate', { expression: 'window.location.href', returnByValue: true });
    console.log('Final url:', finalUrl.result.value);
  } finally {
    chrome.kill();
  }
}
test();
