const cp = require('child_process');

async function runCheck(url, port) {
  console.log(`\n==============================================`);
  console.log(`TESTING URL: ${url}`);
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

  if (!targets || !targets[0]) {
    console.error(`Failed to connect to Chrome on port ${port}`);
    chrome.kill();
    return;
  }

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  let id = 1;
  const cb = new Map();
  const errors = [];

  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.method === 'Runtime.exceptionThrown') {
      errors.push(m.params.exceptionDetails.text + ' ' + (m.params.exceptionDetails.exception?.description || ''));
    }
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
  await send("Runtime.evaluate", {
    expression: `Array.from(document.querySelectorAll(".homeSurfaceExperience_phaseToggle__N_t1R button")).find(b => b.innerText.includes("Ghép lại"))?.click()`
  });
  await new Promise(r => setTimeout(r, 600));
  const afterGhep = await send("Runtime.evaluate", {
    expression: `(() => {
      const btns = Array.from(document.querySelectorAll(".homeSurfaceExperience_phaseToggle__N_t1R button"));
      const panel = document.getElementById("home-surface-panel");
      return {
        tab1Pressed: btns[1]?.getAttribute("aria-pressed"),
        panelTitle: panel?.querySelector("h3")?.innerText,
        phaseCopy: panel?.querySelector("p")?.innerText
      };
    })()`,
    returnByValue: true
  });
  console.log("After clicking Ghép lại:", afterGhep.result?.value);

  await send("Runtime.evaluate", {
    expression: `Array.from(document.querySelectorAll(".homeSurfaceExperience_phaseToggle__N_t1R button")).find(b => b.innerText.includes("Tách lớp"))?.click()`
  });
  await new Promise(r => setTimeout(r, 600));
  const afterTach = await send("Runtime.evaluate", {
    expression: `(() => {
      const btns = Array.from(document.querySelectorAll(".homeSurfaceExperience_phaseToggle__N_t1R button"));
      const panel = document.getElementById("home-surface-panel");
      return {
        tab0Pressed: btns[0]?.getAttribute("aria-pressed"),
        panelTitle: panel?.querySelector("h3")?.innerText,
        phaseCopy: panel?.querySelector("p")?.innerText
      };
    })()`,
    returnByValue: true
  });
  console.log("After clicking Tách lớp:", afterTach.result?.value);

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
  console.log("Runtime unhandled exceptions:", errors.length);

  ws.close();
  chrome.kill();
}

async function main() {
  await runCheck('http://localhost:3000', 9331);
  await runCheck('https://sonsonmaisac.id.vn', 9332);
}

main().catch(console.error);
