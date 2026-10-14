const cp = require('child_process');
const fs = require('fs');

async function testContactText() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9244',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);
  await new Promise(r => setTimeout(r, 1200));
  try {
    const targets = await fetch('http://localhost:9244/json/list').then(r => r.json());
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    let id = 1;
    const pending = new Map();
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const msgId = id++;
      pending.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id).resolve(msg.result);
        pending.delete(msg.id);
      }
    };
    await new Promise(r => ws.onopen = r);
    await send('Page.enable');
    await send('Runtime.enable');
    await send('Page.navigate', { url: 'http://localhost:3000/ve-du-an' });
    await new Promise(r => setTimeout(r, 1500));

    // Scroll to contact section
    await send('Runtime.evaluate', {
      expression: `(() => {
        const sec = document.querySelector('.project_contact__MjYrS');
        if (sec) sec.scrollIntoView({ block: 'center' });
        const h2 = document.querySelector('.project_contactIntro__eES4_ h2');
        const p = document.querySelector('.project_contactIntro__eES4_ p:not(.eyebrow)');
        if (h2) h2.innerHTML = 'CÙNG NỐI TIẾP<br/>HÀNH TRÌNH SƠN MÀI.';
        if (p) p.textContent = 'Liên hệ với Sơn Son Mài Sắc để cùng kết nối, đồng hành và lan tỏa những giá trị của sơn mài Việt.';
        
        const style = document.createElement('style');
        style.id = 'test-contact-css';
        style.textContent = \`
          .project_contact__MjYrS h2 {
            max-width: none !important;
            font-size: clamp(30px, 3.2vw, 46px) !important;
            line-height: 1.15 !important;
            letter-spacing: -0.01em !important;
            font-family: "Project Display", "Playfair Display", Georgia, serif !important;
            margin: 14px 0 18px !important;
          }
          .project_contact__MjYrS .project_contactIntro__eES4_ p:not(.eyebrow) {
            max-width: 480px !important;
            line-height: 1.7 !important;
            color: #f1d9aa !important;
            font-size: 16px !important;
          }
          @media (max-width: 760px) {
            .project_contact__MjYrS h2 {
              font-size: 28px !important;
              line-height: 1.2 !important;
            }
          }
        \`;
        document.head.appendChild(style);
      })()`
    });
    await new Promise(r => setTimeout(r, 400));

    // Test mobile
    await send('Emulation.setDeviceMetricsOverride', {
      width: 414,
      height: 896,
      deviceScaleFactor: 1,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 400));
    const shotMobile = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('scripts/test_contact_mobile.png', Buffer.from(shotMobile.data, 'base64'));
    console.log('Saved test_contact_mobile.png');

    ws.close();
  } finally {
    chrome.kill();
  }
}
testContactText();
