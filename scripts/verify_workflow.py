import json
import os
import subprocess
import time
import urllib.request
import websocket
import base64

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def main():
    port = 9260
    user_data = f"/tmp/chrome_verify_{port}"
    
    proc = subprocess.Popen([
        CHROME_BIN,
        "--remote-allow-origins=*",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data}",
        "--headless=new",
        "--hide-scrollbars",
        "--window-size=393,852"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        time.sleep(1.2)
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list") as r:
            pages = json.loads(r.read())
            ws_url = [p['webSocketDebuggerUrl'] for p in pages if p['type'] == 'page'][0]

        ws = websocket.create_connection(ws_url, timeout=15)
        msg_id = 0

        def send(method, params=None):
            nonlocal msg_id
            msg_id += 1
            ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
            while True:
                resp = json.loads(ws.recv())
                if resp.get("id") == msg_id:
                    return resp.get("result", {})

        send("Emulation.setDeviceMetricsOverride", {
            "width": 393, "height": 852, "deviceScaleFactor": 3, "mobile": True, "touch": True
        })
        send("Runtime.enable")
        send("Page.enable")

        print("Navigating to http://localhost:3000/kham-pha...")
        send("Page.navigate", {"url": "http://localhost:3000/kham-pha"})
        time.sleep(4)

        # Scroll to canvas
        send("Runtime.evaluate", {
            "expression": "document.querySelector('canvas').scrollIntoView({block: 'center'});"
        })
        time.sleep(1)

        # 1. Bare core screenshot
        ss1 = send("Page.captureScreenshot", {"format": "png"})
        with open("scripts/verify_1_bare_core.png", "wb") as f:
            f.write(base64.b64decode(ss1["data"]))
        print("1. Saved verify_1_bare_core.png")

        # 2. Check fabric checkbox
        cb_res = send("Runtime.evaluate", {
            "expression": """(() => {
                const cb = document.querySelector('.studio_reinforce_check input');
                cb.click();
                return cb.checked;
            })()""",
            "returnByValue": True
        })
        print("2. Checked fabric checkbox:", cb_res.get("result", {}).get("value"))
        time.sleep(1.5)

        # Fabric wrapped screenshot
        ss2 = send("Page.captureScreenshot", {"format": "png"})
        with open("scripts/verify_2_fabric_wrapped.png", "wb") as f:
            f.write(base64.b64decode(ss2["data"]))
        print("2. Saved verify_2_fabric_wrapped.png")

        # 3. Simulate mobile touch orbit drag
        touch_res = send("Runtime.evaluate", {
            "expression": """(() => {
                const canvas = document.querySelector('canvas');
                const rect = canvas.getBoundingClientRect();
                const startX = rect.left + rect.width / 2;
                const startY = rect.top + rect.height / 2;

                canvas.dispatchEvent(new PointerEvent('pointerdown', {
                    bubbles: true, cancelable: true, clientX: startX, clientY: startY, button: 0, pointerId: 1, pointerType: 'touch'
                }));

                for (let i = 1; i <= 15; i++) {
                    canvas.dispatchEvent(new PointerEvent('pointermove', {
                        bubbles: true, cancelable: true, clientX: startX + i * 8, clientY: startY - i * 2, button: 0, pointerId: 1, pointerType: 'touch'
                    }));
                }

                canvas.dispatchEvent(new PointerEvent('pointerup', {
                    bubbles: true, cancelable: true, clientX: startX + 120, clientY: startY - 30, button: 0, pointerId: 1, pointerType: 'touch'
                }));

                const live = document.querySelector('.lacquer-surface-live');
                return {
                    rotationY: live.dataset.orbitRotationY,
                    rotationX: live.dataset.orbitRotationX,
                    orbitTouched: live.dataset.orbitTouched
                };
            })()""",
            "returnByValue": True
        })
        print("3. Mobile touch orbit result:", touch_res.get("result", {}).get("value"))
        time.sleep(1)

        ss3 = send("Page.captureScreenshot", {"format": "png"})
        with open("scripts/verify_3_touch_rotated.png", "wb") as f:
            f.write(base64.b64decode(ss3["data"]))
        print("3. Saved verify_3_touch_rotated.png")

        # 4. Uncheck fabric checkbox
        uncheck_res = send("Runtime.evaluate", {
            "expression": """(() => {
                const cb = document.querySelector('.studio_reinforce_check input');
                cb.click();
                return cb.checked;
            })()""",
            "returnByValue": True
        })
        print("4. Unchecked fabric checkbox:", uncheck_res.get("result", {}).get("value"))
        time.sleep(1.5)

        ss4 = send("Page.captureScreenshot", {"format": "png"})
        with open("scripts/verify_4_reverted_bare.png", "wb") as f:
            f.write(base64.b64decode(ss4["data"]))
        print("4. Saved verify_4_reverted_bare.png")

    finally:
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    main()
