const cp = require('child_process');

async function testLiveHome() {
  console.log('--- Verifying live https://sonsonmaisac.id.vn ---');
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9294',
    '--no-sandbox',
    '--window-size=1280,1000'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch('http://localhost:9294/json/list').then(r => r.json());
      const page = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (page) { targets = [page]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  if (!targets || !targets[0]) {
    console.error('Failed to connect to headless Chrome');
    chrome.kill();
    return;
  }

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  let id = 1;
  const callbacks = new Map();
  const errors = [];

  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      errors.push(msg.params.args.map(a => a.value || a.description || '').join(' '));
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

  await send('Page.navigate', { url: 'https://sonsonmaisac.id.vn' });
  // Wait for initial load and splash screen
  await new Promise(r => setTimeout(r, 4500));

  // 1. Check Preloader Status & Skip if present
  const preloaderStatus = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const el = document.getElementById('ssms-entry-screen');
        return {
          exists: !!el,
          opacity: el ? window.getComputedStyle(el).opacity : null,
          visibility: el ? window.getComputedStyle(el).visibility : null,
          display: el ? window.getComputedStyle(el).display : null
        };
      })()
    `,
    returnByValue: true
  });
  console.log('Preloader status:', preloaderStatus.result?.value);

  // 2. Test Material Cards 01-06 Interactivity
  console.log('\n--- Testing Material Cards 01-06 ---');
  const cardTestResult = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const cards = document.querySelectorAll('button[data-card-index], [data-active][data-card-index], .MaterialCard_card__3_j7v, [data-material-card]');
        // Fallback: look for cards by text or index attribute
        let cardList = Array.from(document.querySelectorAll('[data-active]'));
        if (cardList.length === 0) {
          cardList = Array.from(document.querySelectorAll('button')).filter(b => b.textContent.includes('01') || b.textContent.includes('02') || b.textContent.includes('03'));
        }
        
        // Let's inspect the cards in Section "NHỮNG ĐẶC TRƯNG LÀM NÊN SƠN MÀI"
        const sectionHeading = Array.from(document.querySelectorAll('h2, h3, div')).find(el => el.textContent.includes('NHỮNG ĐẶC TRƯNG') || el.textContent.includes('ĐẶC TRƯNG LÀM NÊN SƠN MÀI'));
        
        let container = sectionHeading ? sectionHeading.closest('section') || sectionHeading.parentElement.parentElement : null;
        let interactiveCards = container ? Array.from(container.querySelectorAll('button[data-active], div[data-active], [role="button"]')) : [];
        if (interactiveCards.length === 0) {
          interactiveCards = Array.from(document.querySelectorAll('[data-active]'));
        }

        const initialStates = interactiveCards.map(c => c.getAttribute('data-active'));
        
        // Click each card and record active states
        const clickResults = [];
        for (let i = 0; i < Math.min(6, interactiveCards.length); i++) {
          interactiveCards[i].click();
          clickResults.push({
            clickedIndex: i,
            states: interactiveCards.map(c => c.getAttribute('data-active'))
          });
        }

        return {
          foundCards: interactiveCards.length,
          initialStates,
          clickResults
        };
      })()
    `,
    returnByValue: true
  });
  console.log('Card Test Results:', JSON.stringify(cardTestResult.result?.value, null, 2));

  // 3. Test 3D Lacquer Box Visualizer
  console.log('\n--- Testing 3D Lacquer Box Visualizer ---');
  // Wait another 2 seconds for WebGL model
  await new Promise(r => setTimeout(r, 2000));

  const box3dTestResult = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const canvas = document.querySelector('canvas');
        const loadingIndicator = Array.from(document.querySelectorAll('div, p, span')).find(el => el.textContent.includes('Đang dựng các lớp sắc minh hoạ'));
        
        // Step buttons: "01 Tách lớp", "02 Ghép lại"
        const stepButtons = Array.from(document.querySelectorAll('button')).filter(b => b.textContent.includes('Tách lớp') || b.textContent.includes('Ghép lại'));
        
        // Material buttons: "Cốt gỗ", "Sơn lót & Vóc", "Sơn màu", "Họa tiết khảm", "Lớp phủ trong"
        const materialNames = ['Cốt gỗ', 'Sơn lót', 'Sơn màu', 'Họa tiết khảm', 'Lớp phủ trong'];
        const materialButtons = Array.from(document.querySelectorAll('button')).filter(b => materialNames.some(m => b.textContent.includes(m)));

        const stepBefore = stepButtons.map(b => ({ text: b.textContent.trim(), pressed: b.getAttribute('aria-pressed') }));
        
        // Click "Ghép lại"
        const ghepLaiBtn = stepButtons.find(b => b.textContent.includes('Ghép lại'));
        if (ghepLaiBtn) ghepLaiBtn.click();
        
        const stepAfterGhep = stepButtons.map(b => ({ text: b.textContent.trim(), pressed: b.getAttribute('aria-pressed') }));

        // Click "Tách lớp"
        const tachLopBtn = stepButtons.find(b => b.textContent.includes('Tách lớp'));
        if (tachLopBtn) tachLopBtn.click();

        const stepAfterTach = stepButtons.map(b => ({ text: b.textContent.trim(), pressed: b.getAttribute('aria-pressed') }));

        // Click a material button
        const sonMauBtn = materialButtons.find(b => b.textContent.includes('Sơn màu'));
        if (sonMauBtn) sonMauBtn.click();

        return {
          canvasFound: !!canvas,
          canvasDimensions: canvas ? { width: canvas.width, height: canvas.height, clientWidth: canvas.clientWidth, clientHeight: canvas.clientHeight } : null,
          loadingPresent: !!loadingIndicator && window.getComputedStyle(loadingIndicator).display !== 'none',
          stepButtonsCount: stepButtons.length,
          stepBefore,
          stepAfterGhep,
          stepAfterTach,
          materialButtonsCount: materialButtons.length
        };
      })()
    `,
    returnByValue: true
  });
  console.log('3D Box Visualizer Results:', JSON.stringify(box3dTestResult.result?.value, null, 2));

  // 4. Check for Next.js error overlays or fatal errors
  const overlayCheck = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const nextOverlay = document.querySelector('nextjs-portal, [data-nextjs-dialog-overlay], #__next-build-watcher');
        const hasOverlay = !!nextOverlay;
        return {
          hasOverlay,
          bodyChildrenCount: document.body.children.length,
          firstBodyChild: document.body.firstElementChild ? document.body.firstElementChild.outerHTML.slice(0, 100) : null
        };
      })()
    `,
    returnByValue: true
  });
  console.log('\n--- Overlay & DOM Structure ---');
  console.log('Overlay Check:', overlayCheck.result?.value);
  console.log('Console Errors caught:', errors.length);
  if (errors.length > 0) {
    console.log('Errors:', errors.slice(0, 5));
  }

  // Capture screenshot to artifact scratch
  const screenshot = await send('Page.captureScreenshot', { format: 'png' });
  const fs = require('fs');
  fs.writeFileSync('scratch/live_prod_verification.png', Buffer.from(screenshot.data, 'base64'));
  console.log('Screenshot saved to scratch/live_prod_verification.png');

  ws.close();
  chrome.kill();
}

testLiveHome().catch(console.error);
