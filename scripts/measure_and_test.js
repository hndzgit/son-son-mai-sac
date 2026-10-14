const cp = require("child_process");
const fs = require("fs");

async function run() {
  const profileDir = `/tmp/chrome-clean-${Date.now()}`;
  const chrome = cp.spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", [
    "--headless=new", "--remote-debugging-port=9258", "--disable-gpu", "--no-sandbox",
    `--user-data-dir=${profileDir}`, "--window-size=1440,900"
  ]);

  let targets = null;
  for (let i = 0; i < 30; i++) {
    try {
      targets = await fetch("http://localhost:9258/json/list").then(r => r.json());
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
  await new Promise(r => setTimeout(r, 2000));

  // Let's test widths
  const widths = await send("Runtime.evaluate", {
    expression: `
      (() => {
        const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
        const results = [];
        for (const fs of [48, 44, 40, 36, 34, 32, 30, 28]) {
          const span = document.createElement("span");
          span.style.fontFamily = "\"Noto Serif\", Georgia, serif";
          span.style.fontSize = fs + "px";
          span.style.fontWeight = "400";
          span.style.letterSpacing = "-0.045em";
          span.style.textTransform = "uppercase";
          span.style.whiteSpace = "nowrap";
          span.innerText = "NHỮNG ĐẶC TRƯNG LÀM NÊN";
          document.body.appendChild(span);
          results.push({ fs, textWidth: span.offsetWidth, headerWidth: header.offsetWidth });
          span.remove();
        }
        return JSON.stringify(results);
      })()
    `,
    returnByValue: true
  });
  console.log("WIDTHS:", widths.result?.value);

  // Scroll to #gioi-thieu
  await send("Runtime.evaluate", {
    expression: `
      const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
      if (header) {
        const top = header.getBoundingClientRect().top + window.scrollY;
        window.scrollTo(0, top - 80);
      }
    `
  });
  await new Promise(r => setTimeout(r, 400));

  // Let's test rendering with 2 lines exactly:
  // We can increase header width or left column width slightly and adjust font-size
  await send("Runtime.evaluate", {
    expression: `
      (() => {
        const h2 = document.getElementById("layers-title");
        const header = document.querySelector(".coreIntroduction_layersLead__acYPE");
        const section = document.querySelector(".coreIntroduction_layersSection__G7C0S");
        const ps = Array.from(header.querySelectorAll("p"));

        // Increase left column from 0.43fr to 0.52fr so title has room to breathe
        if (section) {
          section.style.gridTemplateColumns = "minmax(380px, 0.5fr) minmax(0, 1fr)";
          section.style.gap = "48px";
        }
        header.style.maxWidth = "560px";

        // Title styling
        h2.innerHTML = '<span style="white-space:nowrap;display:block;">NHỮNG ĐẶC TRƯNG LÀM NÊN</span><span style="white-space:nowrap;display:block;">SƠN MÀI</span>';
        h2.style.fontSize = "clamp(30px, 2.65vw, 42px)";
        h2.style.lineHeight = "1.15";
        h2.style.letterSpacing = "-0.035em";
        h2.style.margin = "0 0 16px 0";

        // Paragraphs spacing - much closer and cleaner
        if (ps[0]) {
          ps[0].style.margin = "0 0 10px 0";
          ps[0].style.fontSize = "14.5px";
          ps[0].style.lineHeight = "1.6";
          ps[0].style.color = "#4a3c2c";
          ps[0].style.maxWidth = "440px";
        }
        if (ps[1]) {
          ps[1].style.margin = "0";
          ps[1].style.fontSize = "14px";
          ps[1].style.lineHeight = "1.6";
          ps[1].style.color = "#524432";
          ps[1].style.maxWidth = "440px";
        }
      })()
    `
  });
  await new Promise(r => setTimeout(r, 400));
  const shotA = await send("Page.captureScreenshot", { format: "png" });
  fs.writeFileSync("scripts/test_perfect_2lines.png", Buffer.from(shotA.data, "base64"));
  console.log("Saved scripts/test_perfect_2lines.png");

  // Check lines rendered
  const h2Info = await send("Runtime.evaluate", {
    expression: `
      (() => {
        const h2 = document.getElementById("layers-title");
        const spans = Array.from(h2.querySelectorAll("span"));
        return JSON.stringify({
          h2Height: h2.offsetHeight,
          span1Width: spans[0]?.offsetWidth,
          span2Width: spans[1]?.offsetWidth,
          headerWidth: document.querySelector(".coreIntroduction_layersLead__acYPE").offsetWidth
        });
      })()
    `,
    returnByValue: true
  });
  console.log("H2 INFO:", h2Info.result?.value);

  ws.close();
  chrome.kill("SIGKILL");
}

run().catch(console.error);
