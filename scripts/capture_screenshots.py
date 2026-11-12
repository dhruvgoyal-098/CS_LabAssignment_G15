"""
Automated Screenshot Generation Script for SecureLab Evidence
Uses Microsoft Edge in headless mode to capture visual evidence of:
- Table 3 Dashboard
- All 5 Vulnerabilities in VULNERABLE mode (Working Exploits)
- All 5 Vulnerabilities in SECURE mode (Blocked Attacks)
"""

import os
import sys
import time
import subprocess
import requests

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SCREENSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "screenshots"))
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot(url, filename, wait_seconds=1):
    output_path = os.path.join(SCREENSHOT_DIR, filename)
    time.sleep(wait_seconds)
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        f"--window-size=1280,850",
        f"--screenshot={output_path}",
        url
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[+] Screenshot captured: {filename}")

def main():
    print("[*] Starting SecureLab background server for screenshot generation...")
    # Start flask app on port 5001 to avoid conflicting with anything
    env = os.environ.copy()
    server_process = subprocess.Popen(
        [sys.executable, "-c", "from app import app; app.run(host='127.0.0.1', port=5001, debug=False)"],
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    base_url = "http://127.0.0.1:5001"
    
    # Wait for server to come up
    for _ in range(15):
        try:
            r = requests.get(base_url)
            if r.status_code == 200:
                print("[*] Server is live and responding at:", base_url)
                break
        except Exception:
            time.sleep(0.5)

    try:
        # 0. Dashboard Screenshot
        take_screenshot(f"{base_url}/", "00_securelab_dashboard.png", wait_seconds=1)

        # ---------------------------------------------------------------------
        # 1. Dhruv: SQL Injection Auth Bypass
        # ---------------------------------------------------------------------
        # Set mode to vulnerable
        s = requests.Session()
        s.post(f"{base_url}/toggle-mode", data={"mode": "vulnerable", "redirect_to": f"{base_url}/sqli-auth"})
        # Send exploit payload
        s.post(f"{base_url}/sqli-auth", data={"username": "admin' --", "password": "any_password"})
        take_screenshot(f"{base_url}/sqli-auth", "01_dhruv_sqli_auth_vulnerable.png", wait_seconds=1)

        # Secure mode
        s.post(f"{base_url}/toggle-mode", data={"mode": "secure", "redirect_to": f"{base_url}/sqli-auth"})
        s.post(f"{base_url}/sqli-auth", data={"username": "admin' --", "password": "any_password"})
        take_screenshot(f"{base_url}/sqli-auth", "02_dhruv_sqli_auth_secure.png", wait_seconds=1)

        # ---------------------------------------------------------------------
        # 2. Aniket: SQL Injection UNION Extraction
        # ---------------------------------------------------------------------
        s.post(f"{base_url}/toggle-mode", data={"mode": "vulnerable", "redirect_to": f"{base_url}/sqli-union"})
        union_url = f"{base_url}/sqli-union?q=%27+UNION+SELECT+id%2C+username%2C+password%2C+role+FROM+users+--"
        take_screenshot(union_url, "03_aniket_sqli_union_vulnerable.png", wait_seconds=1)

        s.post(f"{base_url}/toggle-mode", data={"mode": "secure", "redirect_to": f"{base_url}/sqli-union"})
        take_screenshot(union_url, "04_aniket_sqli_union_secure.png", wait_seconds=1)

        # ---------------------------------------------------------------------
        # 3. Aditya: OS Command Injection
        # ---------------------------------------------------------------------
        s.post(f"{base_url}/toggle-mode", data={"mode": "vulnerable", "redirect_to": f"{base_url}/cmdi-inband"})
        s.post(f"{base_url}/cmdi-inband", data={"target": "127.0.0.1 && whoami"})
        take_screenshot(f"{base_url}/cmdi-inband", "05_aditya_cmdi_inband_vulnerable.png", wait_seconds=1)

        s.post(f"{base_url}/toggle-mode", data={"mode": "secure", "redirect_to": f"{base_url}/cmdi-inband"})
        s.post(f"{base_url}/cmdi-inband", data={"target": "127.0.0.1 && whoami"})
        take_screenshot(f"{base_url}/cmdi-inband", "06_aditya_cmdi_inband_secure.png", wait_seconds=1)

        # ---------------------------------------------------------------------
        # 4. Anubhav: Stored XSS
        # ---------------------------------------------------------------------
        s.post(f"{base_url}/toggle-mode", data={"mode": "vulnerable", "redirect_to": f"{base_url}/xss-stored"})
        s.post(f"{base_url}/xss-stored", data={"author": "Anubhav-Security", "comment": "<b style='color:#ff7b72'>[XSS Payload Rendered]</b> <script>console.log('Stored XSS Executed');</script>"})
        take_screenshot(f"{base_url}/xss-stored", "07_anubhav_xss_stored_vulnerable.png", wait_seconds=1)

        s.post(f"{base_url}/toggle-mode", data={"mode": "secure", "redirect_to": f"{base_url}/xss-stored"})
        take_screenshot(f"{base_url}/xss-stored", "08_anubhav_xss_stored_secure.png", wait_seconds=1)

        # ---------------------------------------------------------------------
        # 5. Sarvansh: CSRF POST
        # ---------------------------------------------------------------------
        take_screenshot(f"{base_url}/attacker-site", "09_sarvansh_csrf_attacker_page.png", wait_seconds=1)

        s.post(f"{base_url}/toggle-mode", data={"mode": "vulnerable", "redirect_to": f"{base_url}/csrf-post"})
        # Simulate CSRF auto-submission
        s.post(f"{base_url}/csrf-post/update", data={"email": "attacker_sarvansh@hacker.io", "new_password": "hackedPass!"})
        take_screenshot(f"{base_url}/csrf-post", "10_sarvansh_csrf_exploit_success.png", wait_seconds=1)

        s.post(f"{base_url}/toggle-mode", data={"mode": "secure", "redirect_to": f"{base_url}/csrf-post"})
        # Forged POST blocked in secure mode
        take_screenshot(f"{base_url}/csrf-post", "11_sarvansh_csrf_blocked_secure.png", wait_seconds=1)

        print("[*] All evidence screenshots successfully captured and stored in static/screenshots/")

    finally:
        server_process.terminate()
        print("[*] Background server stopped.")

if __name__ == "__main__":
    main()
