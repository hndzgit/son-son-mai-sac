import json
import os
import subprocess
import time
import urllib.request
import websocket
import base64

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def main():
    port = 9245
    user_data = f"/tmp/chrome_diag_{port}"
    
    proc = subprocess.Popen([
        CHROME_BIN,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data}",
        "--headless=new",
        "--remote-allow-origins=*",
        "--use-gl=angle",
        "--use-angle=metal",
        "--window-size=393,852"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        time.sleep(1)
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
                if "method" in resp and resp["method"] == "Runtime.consoleAPICalled":
                    args = resp["params"].get("args", [])
                    print("[Browser Console]", [a.get("value") for a in args])
                if resp.get("id") == msg_id:
                    return resp.get("result", {})

        send("Emulation.setDeviceMetricsOverride", {
            "width": 393, "height": 852, "deviceScaleFactor": 3, "mobile": True, "touch": True
        })
        send("Runtime.enable")
        send("Page.enable")

        print("Navigating to http://localhost:3000/kham-pha...")
        send("Page.navigate", {"url": "http://localhost:3000/kham-pha"})

        # Wait for page and 3D scripts to hydrate
        for i in range(10):
            time.sleep(1)
            eval_res = send("Runtime.evaluate", {
                "expression": """(() => {
                    const canvas = document.querySelector('canvas');
                    const live = document.querySelector('.lacquer-surface-live');
                    const fallback = document.querySelector('.productExperience_viewerFallback__0883U') || document.querySelector('.viewerFallback');
                    const err = document.querySelector('.surface-error');
                    return {
                        hasCanvas: !!canvas,
                        hasLive: !!live,
                        fallbackText: fallback?.textContent,
                        errText: err?.textContent,
                        canvasWidth: canvas?.width,
                        canvasHeight: canvas?.height
                    };
                })()""",
                "returnByValue": True
            })
            info = eval_res.get("result", {}).get("value", {})
            print(f"Second {i+1}:", info)
            if info.get("hasCanvas"):
                break

        # Capture screenshot of viewer
        send("Runtime.evaluate", {
            "expression": "const c = document.querySelector('canvas') || document.querySelector('.productExperience_viewer__V3Heb'); if(c) c.scrollIntoView({block:'center'});"
        })
        time.sleep(1)
        ss1 = send("Page.captureScreenshot", {"format": "png"})
        with open("scripts/diag_before_check.png", "wb") as f:
            f.write(base64.b64decode(ss1["data"]))
        print("Captured diag_before_check.png")

        # Now click fabric checkbox
        cb_info = send("Runtime.evaluate", {
            "expression": """(() => {
                const cb = document.querySelector('.studio_reinforce_check input');
                if (!cb) return 'No checkbox found';
                cb.click();
                return 'Clicked! checked = ' + cb.checked;
            })()""",
            "returnByValue": True
        })
        print("Checkbox click:", cb_info.get("result", {}).get("value"))

        time.sleep(2)
        ss2 = send("Page.captureScreenshot", {"format": "png"})
        with open("scripts/diag_after_check.png", "wb") as f:
            f.write(base64.b64decode(ss2["data"]))
        print("Captured diag_after_check.png")

    finally:
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    main()
