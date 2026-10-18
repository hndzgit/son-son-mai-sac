const cp = require('child_process');

async function testLiveOnly() {
  const url = 'https://sonsonmaisac.id.vn';
  const port = 9335;
  console.log(`\n==============================================`);
  console.log(`TESTING LIVE PRODUCTION: ${url}`);
  console.log(`==============================================`);

  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--no-sandbox',
    '--window-size=1280,1000'
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch(`http://localhost:${port}/json/list`).then(r => r.json());
      const p = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (p) { targets = [p]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  let id = 1;
  const cb = new Map();
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.id && cb.has(m.id)) {
      cb.get(m.id)(m.result);
      cb.delete(m.id);
    }
  };

  const send = (m, p = {}) => new Promise(res => {
    const i = id++;
    cb.set(i, res);
    ws.send(JSON.stringify({ id: i, method: m, params: p }));
  });

  await new Promise(r => ws.onopen = r);
  await send('Page.enable');
  await send('Runtime.enable');

  await send('Page.navigate', { url });
  await new Promise(r => setTimeout(r, 4500));

  console.log("=== TEST 1: MATERIAL CARDS CLICK (01 to 06) ===");
  const cardNames = ["01 Sơn then", "02 Sơn son", "03 Vỏ trứng", "04 Vàng", "05 Bạc", "06 Xà cừ"];
  for (let i = 0; i < 6; i++) {
    await send("Runtime.evaluate", { expression: `document.querySelectorAll(".materialGallery_card__sP88f")[${i}].click()` });
    await new Promise(r => setTimeout(r, 600));
    const active = await send("Runtime.evaluate", {
      expression: `Array.from(document.querySelectorAll(".materialGallery_card__sP88f")).map(c => c.getAttribute("data-active"))`,
      returnByValue: true
    });
    console.log(`Clicked Card ${i} (${cardNames[i]}):`, active.result?.value);
  }

  console.log("\n=== TEST 2: 3D SURFACE STEP TABS (Tách lớp / Ghép lại) ===");
  // Click Tab 1: Ghép lại
  await send("Runtime.evaluate", { expression: `document.querySelectorAll(".homeSurfaceExperience_steps__BjAaL button")[1].click()` });
  await new Promise(r => setTimeout(r, 800));
  const tab1 = await send("Runtime.evaluate", {
    expression: `(() => {
      const panel = document.getElementById("home-surface-panel");
      return {
        tab1Pressed: document.querySelectorAll(".homeSurfaceExperience_steps__BjAaL button")[1].getAttribute("aria-pressed"),
        panelTitle: panel?.querySelector("h3")?.innerText,
        phaseCopy: panel?.querySelector(".homeSurfaceExperience_phaseCopy__bEkf4")?.innerText
      };
    })()`,
    returnByValue: true
  });
  console.log("After clicking Ghép lại:", tab1.result?.value);

  // Click Tab 0: Tách lớp
  await send("Runtime.evaluate", { expression: `document.querySelectorAll(".homeSurfaceExperience_steps__BjAaL button")[0].click()` });
  await new Promise(r => setTimeout(r, 800));
  const tab0 = await send("Runtime.evaluate", {
    expression: `(() => {
      const panel = document.getElementById("home-surface-panel");
      return {
        tab0Pressed: document.querySelectorAll(".homeSurfaceExperience_steps__BjAaL button")[0].getAttribute("aria-pressed"),
        panelTitle: panel?.querySelector("h3")?.innerText,
        phaseCopy: panel?.querySelector(".homeSurfaceExperience_phaseCopy__bEkf4")?.innerText
      };
    })()`,
    returnByValue: true
  });
  console.log("After clicking Tách lớp:", tab0.result?.value);

  console.log("\n=== TEST 3: 3D MATERIAL BUTTONS ===");
  const matLayers = ["0. Cốt gỗ", "1. Sơn lót & Vóc", "2. Sơn màu", "3. Họa tiết khảm", "4. Lớp phủ trong"];
  for (let m = 0; m < 5; m++) {
    await send("Runtime.evaluate", { expression: `document.querySelectorAll(".homeSurfaceExperience_materials__aPFzc button")[${m}].click()` });
    await new Promise(r => setTimeout(r, 500));
    const matState = await send("Runtime.evaluate", {
      expression: `(() => {
        const btns = Array.from(document.querySelectorAll(".homeSurfaceExperience_materials__aPFzc button"));
        const panel = document.getElementById("home-surface-panel");
        return {
          activeBtn: btns.find(b => b.getAttribute("aria-pressed") === "true")?.innerText,
          panelTitle: panel?.querySelector("h3")?.innerText
        };
      })()`,
      returnByValue: true
    });
    console.log(`Clicked Mat ${m} (${matLayers[m]}):`, matState.result?.value);
  }

  console.log("\n=== TEST 4: 3D WEBGL CANVAS & STATUS ===");
  const canvasFinal = await send("Runtime.evaluate", {
    expression: `(() => {
      const viewer = document.querySelector(".homeSurfaceExperience_viewer__Afl_z");
      const canvas = document.querySelector("canvas");
      const loading = document.querySelector(".homeSurfaceExperience_loading__Z83fF");
      return {
        canvasFound: !!canvas,
        canvasWidth: canvas?.width,
        canvasHeight: canvas?.height,
        loadingPresent: !!loading
      };
    })()`,
    returnByValue: true
  });
  console.log("Canvas final state:", canvasFinal.result?.value);

  // Check all subpages status
  console.log("\n=== TEST 5: SUBPAGES STATUS ===");
  const subpages = ['/kham-pha', '/cau-chuyen-son-mai', '/san-pham', '/tin-tuc-su-kien', '/ve-du-an', '/son-mai-la-gi'];
  for (const page of subpages) {
    await send('Page.navigate', { url: `https://sonsonmaisac.id.vn${page}` });
    await new Promise(r => setTimeout(r, 1200));
    const pageCheck = await send('Runtime.evaluate', {
      expression: `(() => {
        return {
          title: document.title,
          h1: document.querySelector('h1')?.innerText,
          hasError: !!document.querySelector('nextjs-portal, [data-nextjs-dialog-overlay]')
        };
      })()`,
      returnByValue: true
    });
    console.log(`Subpage ${page}:`, pageCheck.result?.value);
  }

  ws.close();
  chrome.kill();
}

testLiveOnly().catch(console.error);
