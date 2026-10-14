const cp = require("child_process");
const fs = require("fs");

async function testGrid() {
  const profileDir = `/tmp/chrome-clean-${Date.now()}`;
  const chrome = cp.spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", [
    "--headless=new", "--remote-debugging-port=9262", "--disable-gpu", "--no-sandbox",
    `--user-data-dir=${profileDir}`, "--window-size=1440,900"
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch("http://localhost:9262/json/list").then(r => r.json());
      const valid = targets && targets.find(t => t.type === 'page' && !t.url.startsWith('chrome-extension'));
      if (valid) { targets = [valid]; break; }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 200));
  }

  const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);

  let id = 1;
  const callbacks = new Map();
  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.id && callbacks.has(msg.id)) {
      callbacks.get(msg.id)(msg.result);
      callbacks.delete(msg.id);
    }
  };

  const send = (method, params = {}) => new Promise((resolve) => {
    const msgId = id++;
    callbacks.set(msgId, resolve);
    ws.send(JSON.stringify({ id: msgId, method, params }));
  });

  await send("Page.enable");
  await send("Runtime.enable");
  await send("Page.navigate", { url: "http://localhost:3000/#gioi-thieu" });
  await new Promise(r => setTimeout(r, 1500));

  await send("Runtime.evaluate", {
    expression: `
      const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
      if (header) {
        const top = header.getBoundingClientRect().top + window.scrollY;
        window.scrollTo(0, top - 60);
      }
    `
  });
  await new Promise(r => setTimeout(r, 300));

  // Let's test two layouts:
  // Layout A: Break after "nên" -> NHỮNG ĐẶC TRƯNG LÀM NÊN <br/> SƠN MÀI
  // with section grid-template-columns: minmax(440px, 0.48fr) minmax(0, 1fr)
  // and cards container having min-width: 0
  await send("Runtime.evaluate", {
    expression: `
      (() => {
        const h2 = document.getElementById("layers-title");
        const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
        const section = document.querySelector(".coreIntroduction_layersSection__G7C0S");
        const cards = document.querySelector(".materialGallery_cards__zJgmU");
        const ps = Array.from(header.querySelectorAll("p"));

        if (section) {
          section.style.gridTemplateColumns = "minmax(420px, 0.42fr) minmax(0, 1fr)";
          section.style.gap = "40px";
          section.style.padding = "70px 48px";
        }
        if (header) {
          header.style.maxWidth = "460px";
        }

        h2.innerHTML = '<span style="display:block;white-space:nowrap;">NHỮNG ĐẶC TRƯNG LÀM NÊN</span><span style="display:block;white-space:nowrap;">SƠN MÀI</span>';
        h2.style.fontSize = "31px";
        h2.style.lineHeight = "1.2";
        h2.style.letterSpacing = "-0.035em";
        h2.style.margin = "0 0 16px 0";

        if (ps[0]) {
          ps[0].style.margin = "0 0 10px 0";
          ps[0].style.fontSize = "14.5px";
          ps[0].style.lineHeight = "1.65";
          ps[0].style.color = "#4a3c2c";
          ps[0].style.maxWidth = "410px";
        }
        if (ps[1]) {
          ps[1].style.margin = "0";
          ps[1].style.fontSize = "14px";
          ps[1].style.lineHeight = "1.65";
          ps[1].style.color = "#524432";
          ps[1].style.maxWidth = "410px";
        }
      })()
    `
  });
  await new Promise(r => setTimeout(r, 300));
  let shot = await send("Page.captureScreenshot", { format: "png" });
  fs.writeFileSync("scripts/test_grid_layout_A_break_nen.png", Buffer.from(shot.data, "base64"));
  console.log("Saved scripts/test_grid_layout_A_break_nen.png");

  // Layout B: What if font-size is 34px with 460px column?
  await send("Runtime.evaluate", {
    expression: `
      (() => {
        const h2 = document.getElementById("layers-title");
        const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
        const section = document.querySelector(".coreIntroduction_layersSection__G7C0S");

        if (section) {
          section.style.gridTemplateColumns = "minmax(460px, 0.45fr) minmax(0, 1fr)";
          section.style.gap = "44px";
        }
        header.style.maxWidth = "480px";
        h2.style.fontSize = "33px";
      })()
    `
  });
  await new Promise(r => setTimeout(r, 300));
  shot = await send("Page.captureScreenshot", { format: "png" });
  fs.writeFileSync("scripts/test_grid_layout_B_33px.png", Buffer.from(shot.data, "base64"));
  console.log("Saved scripts/test_grid_layout_B_33px.png");

  // Layout C: Break after "sơn" -> NHỮNG ĐẶC TRƯNG LÀM NÊN SƠN <br/> MÀI
  await send("Runtime.evaluate", {
    expression: `
      (() => {
        const h2 = document.getElementById("layers-title");
        h2.innerHTML = '<span style="display:block;white-space:nowrap;">NHỮNG ĐẶC TRƯNG LÀM NÊN SƠN</span><span style="display:block;white-space:nowrap;">MÀI</span>';
        h2.style.fontSize = "28px";
      })()
    `
  });
  await new Promise(r => setTimeout(r, 300));
  shot = await send("Page.captureScreenshot", { format: "png" });
  fs.writeFileSync("scripts/test_grid_layout_C_break_son.png", Buffer.from(shot.data, "base64"));
  console.log("Saved scripts/test_grid_layout_C_break_son.png");

  ws.close();
  chrome.kill("SIGKILL");
}

testGrid().catch(console.error);
