import json
import os
import subprocess
import time
import urllib.request
import websocket

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def run_test():
    port = 9244
    user_data = f"/tmp/chrome_test_3d_{port}"
    
    # Launch Chrome headless with remote debugging
    chrome_proc = subprocess.Popen([
        CHROME_BIN,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data}",
        "--headless=new",
        "--remote-allow-origins=*",
        "--hide-scrollbars",
        "--enable-webgl",
        "--ignore-gpu-blocklist",
        "--window-size=393,852"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ws = None
    try:
        # Wait for debugging endpoint
        ws_url = None
        for _ in range(30):
            time.sleep(0.3)
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list") as r:
                    pages = json.loads(r.read())
                    for p in pages:
                        if p.get("type") == "page" and p.get("webSocketDebuggerUrl"):
                            ws_url = p.get("webSocketDebuggerUrl")
                            break
                    if ws_url:
                        break
            except Exception:
                pass

        if not ws_url:
            print("Failed to get Chrome page ws url")
            return

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

        # Set mobile emulation: iPhone 14 Pro
        send("Emulation.setDeviceMetricsOverride", {
            "width": 393,
            "height": 852,
            "deviceScaleFactor": 3,
            "mobile": True,
            "touch": True
        })
        send("Emulation.setTouchEmulationEnabled", {"enabled": True})
        send("Page.enable")
        send("Runtime.enable")

        # Navigate to /kham-pha
        print("Navigating to http://localhost:3000/kham-pha...")
        send("Page.navigate", {"url": "http://localhost:3000/kham-pha"})
        
        # Wait 4 seconds for 3D engine to initialize
        time.sleep(4)

        # Check for errors in console
        res = send("Runtime.evaluate", {
            "expression": "document.querySelector('canvas') ? 'Canvas found: ' + document.querySelector('canvas').style.touchAction : 'No canvas'"
        })
        print("Canvas status:", res.get("result", {}).get("value"))

        # Scroll down to 3D viewer
        send("Runtime.evaluate", {
            "expression": "const v = document.querySelector('.productExperience_galleryView__p7LNe') || document.querySelector('canvas'); if(v) v.scrollIntoView({block: 'center'});"
        })
        time.sleep(1.5)

        # Take screenshot 1: Before checking fabric
        screenshot1 = send("Page.captureScreenshot", {"format": "png"})
        import base64
        with open("scripts/screenshot_core_before.png", "wb") as f:
            f.write(base64.b64decode(screenshot1["data"]))
        print("Saved screenshot_core_before.png")

        # Click the fabric checkbox
        check_res = send("Runtime.evaluate", {
            "expression": """(() => {
                const cb = document.querySelector('.studio_reinforce_check input') || document.querySelector('input[type=\"checkbox\"]');
                if (!cb) return 'No checkbox found';
                cb.click();
                return 'Clicked checkbox, new checked = ' + cb.checked;
            })()"""
        })
        print("Checkbox action:", check_res.get("result", {}).get("value"))

        # Wait 2 seconds for texture to re-render
        time.sleep(2)

        # Take screenshot 2: After checking fabric
        screenshot2 = send("Page.captureScreenshot", {"format": "png"})
        with open("scripts/screenshot_fabric_after.png", "wb") as f:
            f.write(base64.b64decode(screenshot2["data"]))
        print("Saved screenshot_fabric_after.png")

        # Now test 3D touch orbit drag
        touch_test = send("Runtime.evaluate", {
            "expression": """(() => {
                const canvas = document.querySelector('canvas');
                if (!canvas) return 'No canvas';
                const rect = canvas.getBoundingClientRect();
                const startX = rect.left + rect.width / 2;
                const startY = rect.top + rect.height / 2;
                
                // Dispatch pointerdown
                canvas.dispatchEvent(new PointerEvent('pointerdown', {
                    bubbles: true, cancelable: true, clientX: startX, clientY: startY, button: 0, pointerId: 1, pointerType: 'touch'
                }));
                
                // Dispatch multiple pointermove events across 80 pixels
                for (let i = 1; i <= 8; i++) {
                    canvas.dispatchEvent(new PointerEvent('pointermove', {
                        bubbles: true, cancelable: true, clientX: startX + i * 10, clientY: startY + i * 3, button: 0, pointerId: 1, pointerType: 'touch'
                    }));
                }
                
                // Dispatch pointerup
                canvas.dispatchEvent(new PointerEvent('pointerup', {
                    bubbles: true, cancelable: true, clientX: startX + 80, clientY: startY + 24, button: 0, pointerId: 1, pointerType: 'touch'
                }));

                const surfaceLive = document.querySelector('.lacquer-surface-live');
                return {
                    orbitTouched: surfaceLive ? surfaceLive.dataset.orbitTouched : null,
                    orbitRotationY: surfaceLive ? surfaceLive.dataset.orbitRotationY : null
                };
            })()""",
            "returnByValue": True
        })
        print("Orbit Touch Test Result:", touch_test.get("result", {}).get("value"))

        # Wait a moment and take screenshot 3: After orbit rotation
        time.sleep(1)
        screenshot3 = send("Page.captureScreenshot", {"format": "png"})
        with open("scripts/screenshot_orbit_rotated.png", "wb") as f:
            f.write(base64.b64decode(screenshot3["data"]))
        print("Saved screenshot_orbit_rotated.png")

    finally:
        if ws:
            ws.close()
        chrome_proc.terminate()
        chrome_proc.wait()

if __name__ == '__main__':
    run_test()
