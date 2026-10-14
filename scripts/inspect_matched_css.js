const cp = require('child_process');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9246',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-extensions',
    '--window-size=1440,900'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9246/json/list').then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) {
        targets = [valid];
        break;
      }
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
    await send('DOM.enable');
    await send('CSS.enable');

    await send('Page.navigate', { url: 'http://localhost:3000/' });
    await new Promise(r => setTimeout(r, 2000));

    const doc = await send('DOM.getDocument');
    const node = await send('DOM.querySelector', {
      nodeId: doc.root.nodeId,
      selector: '.coreIntroduction_introCopy__c7o__'
    });

    const matched = await send('CSS.getMatchedStylesForNode', { nodeId: node.nodeId });
    console.log('Matched rules affecting opacity:');
    matched.matchedCSSRules.forEach(r => {
      const opacityProp = r.rule.style.cssProperties.find(p => p.name === 'opacity');
      if (opacityProp) {
        console.log(`Selector: ${r.rule.selectorList.text}`);
        console.log(`Opacity: ${opacityProp.value}`);
        console.log(`StylesheetId: ${r.rule.styleSheetId}`);
      }
    });

    // Also get stylesheet URL
    if (matched.matchedCSSRules.length) {
      const sheetId = matched.matchedCSSRules[0].rule.styleSheetId;
      const header = await send('CSS.getStyleSheetHeader', { styleSheetId: sheetId });
      console.log('StyleSheet SourceURL:', header?.header?.sourceURL);
    }

  } finally {
    chrome.kill();
  }
}

test().catch(console.error);
