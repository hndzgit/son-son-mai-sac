const cp = require("child_process");
const fs = require("fs");

async function testDesign() {
  const profileDir = `/tmp/chrome-clean-${Date.now()}`;
  const chrome = cp.spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", [
    "--headless=new", "--remote-debugging-port=9260", "--disable-gpu", "--no-sandbox",
    `--user-data-dir=${profileDir}`, "--window-size=1440,900"
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch("http://localhost:9260/json/list").then(r => r.json());
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

  // Scroll to #gioi-thieu
  await send("Runtime.evaluate", {
    expression: `
      const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
      if (header) {
        const top = header.getBoundingClientRect().top + window.scrollY;
        window.scrollTo(0, top - 60);
      }
    `
  });
  await new Promise(r => setTimeout(r, 400));

  // Let's test font sizes: 32px, 34px, 36px, with left column minmax(360px, 0.45fr) and gap 36px
  const sizes = [
    { name: "32px", fontSize: "32px", lineHeight: "1.18" },
    { name: "34px", fontSize: "34px", lineHeight: "1.16" },
    { name: "36px", fontSize: "36px", lineHeight: "1.15" },
    { name: "clamp_30_38", fontSize: "clamp(30px, 2.4vw, 38px)", lineHeight: "1.16" }
  ];

  for (const s of sizes) {
    await send("Runtime.evaluate", {
      expression: `
        (() => {
          const h2 = document.getElementById("layers-title");
          const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
          const section = document.querySelector(".coreIntroduction_layersSection__G7C0S");
          const ps = Array.from(header.querySelectorAll("p"));

          if (section) {
            section.style.gridTemplateColumns = "minmax(340px, 0.44fr) minmax(0, 1fr)";
            section.style.gap = "clamp(24px, 2.5vw, 44px)";
          }
          header.style.maxWidth = "480px";

          h2.innerHTML = '<span style="display:block;white-space:nowrap;">NHỮNG ĐẶC TRƯNG LÀM NÊN</span><span style="display:block;white-space:nowrap;">SƠN MÀI</span>';
          h2.style.fontSize = "${s.fontSize}";
          h2.style.lineHeight = "${s.lineHeight}";
          h2.style.letterSpacing = "-0.03em";
          h2.style.margin = "0 0 16px 0";

          if (ps[0]) {
            ps[0].style.margin = "0 0 12px 0";
            ps[0].style.fontSize = "14.5px";
            ps[0].style.lineHeight = "1.65";
            ps[0].style.color = "#4a3c2c";
            ps[0].style.maxWidth = "420px";
          }
          if (ps[1]) {
            ps[1].style.margin = "0";
            ps[1].style.fontSize = "14px";
            ps[1].style.lineHeight = "1.65";
            ps[1].style.color = "#524432";
            ps[1].style.maxWidth = "420px";
          }
        })()
      `
    });
    await new Promise(r => setTimeout(r, 300));
    const shot = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(`scripts/design_${s.name}.png`, Buffer.from(shot.data, "base64"));
    console.log(`Saved scripts/design_${s.name}.png`);
  }

  ws.close();
  chrome.kill("SIGKILL");
}

testDesign().catch(console.error);
