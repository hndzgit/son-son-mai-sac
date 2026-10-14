const cp = require('child_process');
const fs = require('fs');

async function test() {
  const chrome = cp.spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9225',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const targets = await fetch('http://localhost:9225/json/list').then(r => r.json());
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
    await new Promise(r => setTimeout(r, 2000));

    const evalResult = await send('Runtime.evaluate', {
      expression: `(() => {
        const hero = document.querySelector('.project_hero__Oebd7');
        const img = document.querySelector('.project_hero__Oebd7 > img');
        if (!hero || !img) return { error: 'Not found' };
        const heroRect = hero.getBoundingClientRect();
        const imgRect = img.getBoundingClientRect();
        const heroStyle = window.getComputedStyle(hero);
        const imgStyle = window.getComputedStyle(img);
        return {
          hero: {
            top: heroRect.top,
            bottom: heroRect.bottom,
            height: heroRect.height,
            width: heroRect.width,
            padding: heroStyle.padding,
            borderRadius: heroStyle.borderRadius
          },
          img: {
            top: imgRect.top,
            bottom: imgRect.bottom,
            height: imgRect.height,
            width: imgRect.width,
            left: imgRect.left,
            right: imgRect.right,
            position: imgStyle.position,
            topStyle: imgStyle.top,
            bottomStyle: imgStyle.bottom,
            rightStyle: imgStyle.right,
            objectFit: imgStyle.objectFit,
            objectPosition: imgStyle.objectPosition,
            borderRadius: imgStyle.borderRadius
          },
          relativeImgToHero: {
            topDiff: imgRect.top - heroRect.top,
            bottomDiff: heroRect.bottom - imgRect.bottom,
            rightDiff: heroRect.right - imgRect.right
          }
        };
      })()`,
      returnByValue: true
    });

    console.log('Inspection:', JSON.stringify(evalResult.result.value, null, 2));

    const heroClip = await send('Runtime.evaluate', {
      expression: `(() => {
        const hero = document.querySelector('.project_hero__Oebd7');
        const rect = hero.getBoundingClientRect();
        return { x: rect.x - 20, y: rect.y - 20, width: rect.width + 40, height: rect.height + 40, scale: 1 };
      })()`,
      returnByValue: true
    });

    const clip = heroClip.result.value;
    const shot = await send('Page.captureScreenshot', { format: 'png', clip });
    fs.writeFileSync('scripts/current_veduan_hero.png', Buffer.from(shot.data, 'base64'));
    console.log('Screenshot saved to scripts/current_veduan_hero.png');

    ws.close();
  } catch (err) {
    console.error(err);
  } finally {
    chrome.kill();
  }
}

test();
