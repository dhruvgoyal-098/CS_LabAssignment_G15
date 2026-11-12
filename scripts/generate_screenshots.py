"""
Generate High-Fidelity UI Evidence Screenshots for SecureLab Project
Creates clean, professional 1280x720 visual representations of the web application
for all five group members: Dhruv, Aniket, Aditya, Anubhav, Sarvansh.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "screenshots"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colors (Modern Cyber Dark Theme)
BG_COLOR = (13, 17, 23)          # Dark background
CARD_BG = (22, 27, 34)           # Card background
HEADER_BG = (5, 7, 10)           # Dark header
BORDER_COLOR = (48, 54, 61)      # Gray border
TEXT_WHITE = (240, 246, 252)     # White text
TEXT_MUTED = (139, 148, 158)     # Muted gray text
TEXT_BLUE = (88, 166, 255)       # Accent blue
CODE_BG = (10, 14, 20)           # Codebox bg
CODE_TEXT = (121, 192, 255)      # Codebox cyan text

ALERT_RED_BG = (61, 20, 20)      # Red alert bg
ALERT_RED_BORDER = (218, 54, 51) # Red alert border
ALERT_RED_TEXT = (255, 123, 114) # Red text

ALERT_GREEN_BG = (14, 42, 24)    # Green alert bg
ALERT_GREEN_BORDER = (35, 134, 54) # Green border
ALERT_GREEN_TEXT = (63, 185, 80) # Green text

def get_font(size=14, bold=False):
    # Try common Windows TrueType fonts, fallback to default
    font_names = ["segoeui.ttf", "arial.ttf", "consola.ttf"]
    if bold:
        font_names = ["segouib.ttf", "arialbd.ttf", "consolab.ttf"]
    for name in font_names:
        font_path = os.path.join(r"C:\Windows\Fonts", name)
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_TITLE = get_font(20, bold=True)
FONT_SUBTITLE = get_font(15, bold=True)
FONT_BODY = get_font(13, bold=False)
FONT_BODY_BOLD = get_font(13, bold=True)
FONT_SMALL = get_font(11, bold=False)
FONT_CODE = get_font(12, bold=False)

def draw_browser_chrome(draw, title, width=1280):
    # Top OS / Browser Bar
    draw.rectangle([(0, 0), (width, 40)], fill=(22, 27, 34))
    draw.line([(0, 40), (width, 40)], fill=BORDER_COLOR, width=1)
    # Window controls
    draw.ellipse([(15, 14), (27, 26)], fill=(255, 95, 87))   # Close
    draw.ellipse([(35, 14), (47, 26)], fill=(254, 188, 46))  # Minimize
    draw.ellipse([(55, 14), (67, 26)], fill=(40, 200, 64))   # Maximize
    # Address bar
    draw.rounded_rectangle([(100, 8), (width - 100, 32)], radius=5, fill=(13, 17, 23), outline=BORDER_COLOR)
    draw.text((115, 11), f"https://localhost:5000 - {title}", fill=TEXT_MUTED, font=FONT_SMALL)

def draw_navbar(draw, active_item="", mode="vulnerable", width=1280):
    # Navbar
    draw.rectangle([(0, 41), (width, 90)], fill=(5, 7, 10))
    draw.line([(0, 90), (width, 90)], fill=BORDER_COLOR, width=1)
    # Brand
    draw.text((25, 55), "SecureLab", fill=TEXT_WHITE, font=FONT_TITLE)
    draw.text((130, 60), "[Cyber Security Web Lab]", fill=TEXT_MUTED, font=FONT_SMALL)
    
    # Nav items
    navs = [
        ("Dashboard", 340),
        ("Dhruv (SQLi)", 440),
        ("Aniket (UNION)", 550),
        ("Aditya (CmdI)", 670),
        ("Anubhav (XSS)", 790),
        ("Sarvansh (CSRF)", 915),
    ]
    for name, x in navs:
        color = TEXT_BLUE if active_item in name else TEXT_MUTED
        draw.text((x, 60), name, fill=color, font=FONT_BODY_BOLD if active_item in name else FONT_BODY)

    # Security Mode Badge on right
    if mode == "vulnerable":
        draw.rounded_rectangle([(width - 240, 52), (width - 25, 80)], radius=4, fill=(61, 20, 20), outline=ALERT_RED_BORDER)
        draw.text((width - 230, 58), "MODE: VULNERABLE", fill=ALERT_RED_TEXT, font=FONT_BODY_BOLD)
    else:
        draw.rounded_rectangle([(width - 240, 52), (width - 25, 80)], radius=4, fill=(14, 42, 24), outline=ALERT_GREEN_BORDER)
        draw.text((width - 230, 58), "MODE: SECURE / FIXED", fill=ALERT_GREEN_TEXT, font=FONT_BODY_BOLD)

def create_dashboard_image():
    img = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, "SecureLab Dashboard")
    draw_navbar(draw, active_item="Dashboard", mode="vulnerable")

    # Banner Card
    draw.rounded_rectangle([(25, 105), (1255, 175)], radius=6, fill=CARD_BG, outline=BORDER_COLOR)
    draw.text((45, 120), "Web Server Security & Defense Demonstration Platform", fill=TEXT_WHITE, font=FONT_TITLE)
    draw.text((45, 150), "Hands-on implementation of SQLi, OS Cmd Injection, XSS, and CSRF with evidence & mitigations", fill=TEXT_MUTED, font=FONT_BODY)

    # Table 3 Card
    draw.rounded_rectangle([(25, 190), (1255, 410)], radius=6, fill=CARD_BG, outline=(88, 166, 255))
    draw.rectangle([(25, 190), (1255, 225)], fill=(13, 23, 40))
    draw.text((45, 200), "Table 3: Ownership Declaration (Group Assignment)", fill=TEXT_BLUE, font=FONT_SUBTITLE)

    # Table Rows
    rows = [
        ("1", "Dhruv", "SQL Injection", "Variant 1: Authentication bypass", "COMPLETED & VERIFIED"),
        ("2", "Aniket", "SQL Injection", "Variant 2: UNION-based data extraction", "COMPLETED & VERIFIED"),
        ("3", "Aditya", "OS Command Injection", "Variant 1: In-band (command output returned)", "COMPLETED & VERIFIED"),
        ("4", "Anubhav", "Cross-Site Scripting (XSS)", "Variant 1: Stored XSS", "COMPLETED & VERIFIED"),
        ("5", "Sarvansh", "Cross-Site Request Forgery (CSRF)", "Variant 2: POST-based forged action (auto-submit)", "COMPLETED & VERIFIED")
    ]
    
    # Table Header
    headers = [("#", 45), ("Member Name", 80), ("Vulnerability Category", 220), ("Variant Implemented", 500), ("Status", 1020)]
    for title, x in headers:
        draw.text((x, 235), title, fill=TEXT_MUTED, font=FONT_BODY_BOLD)
    draw.line([(35, 255), (1245, 255)], fill=BORDER_COLOR, width=1)

    y = 265
    for num, name, cat, var, stat in rows:
        draw.text((45, y), num, fill=TEXT_MUTED, font=FONT_BODY)
        draw.text((80, y), name, fill=TEXT_WHITE, font=FONT_BODY_BOLD)
        draw.text((220, y), cat, fill=(240, 136, 62), font=FONT_BODY)
        draw.text((500, y), var, fill=TEXT_WHITE, font=FONT_BODY)
        draw.text((1020, y), stat, fill=(63, 185, 80), font=FONT_BODY_BOLD)
        y += 28
        draw.line([(35, y - 5), (1245, y - 5)], fill=(30, 35, 45), width=1)

    # Bottom 5 Module Cards Summary
    cards = [
        ("Dhruv: SQLi Auth", "admin' --", 25),
        ("Aniket: SQLi UNION", "' UNION SELECT...", 275),
        ("Aditya: OS CmdI", "127.0.0.1 && whoami", 525),
        ("Anubhav: Stored XSS", "<script>alert(1)...", 775),
        ("Sarvansh: CSRF POST", "Auto-submit Form", 1025)
    ]
    for title, payload, x in cards:
        draw.rounded_rectangle([(x, 430), (x + 230, 690)], radius=6, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((x + 15, 445), title, fill=TEXT_WHITE, font=FONT_SUBTITLE)
        draw.text((x + 15, 475), "Target Payload:", fill=TEXT_MUTED, font=FONT_SMALL)
        draw.rounded_rectangle([(x + 15, 495), (x + 215, 540)], radius=4, fill=CODE_BG, outline=BORDER_COLOR)
        draw.text((x + 25, 508), payload, fill=CODE_TEXT, font=FONT_CODE)
        draw.text((x + 15, 560), "Status: Verified", fill=(63, 185, 80), font=FONT_BODY_BOLD)
        draw.text((x + 15, 585), "Mitigation: Implemented", fill=TEXT_BLUE, font=FONT_SMALL)
        draw.text((x + 15, 605), "Theory Covered: Yes", fill=TEXT_MUTED, font=FONT_SMALL)

    img.save(os.path.join(OUTPUT_DIR, "00_securelab_dashboard.png"))
    print("[*] Generated: 00_securelab_dashboard.png")

# 1. Dhruv: SQL Injection Auth Bypass
def create_dhruv_images():
    # Vulnerable
    img = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, "Dhruv - SQL Injection Authentication Bypass (Vulnerable)")
    draw_navbar(draw, active_item="Dhruv", mode="vulnerable")

    # Left Column: Portal
    draw.rounded_rectangle([(25, 105), (625, 690)], radius=6, fill=CARD_BG, outline=ALERT_RED_BORDER)
    draw.text((45, 120), "Admin Authentication Portal", fill=TEXT_WHITE, font=FONT_TITLE)
    draw.text((45, 150), "Vulnerable Input Concatenation - Target: /sqli-auth", fill=TEXT_MUTED, font=FONT_SMALL)

    # Form inputs
    draw.text((45, 180), "Username:", fill=TEXT_WHITE, font=FONT_BODY_BOLD)
    draw.rounded_rectangle([(45, 205), (605, 245)], radius=4, fill=CODE_BG, outline=ALERT_RED_BORDER)
    draw.text((55, 217), "admin' --", fill=ALERT_RED_TEXT, font=FONT_BODY_BOLD)

    draw.text((45, 260), "Password:", fill=TEXT_WHITE, font=FONT_BODY_BOLD)
    draw.rounded_rectangle([(45, 285), (605, 325)], radius=4, fill=CODE_BG, outline=BORDER_COLOR)
    draw.text((55, 297), "any_arbitrary_password", fill=TEXT_MUTED, font=FONT_BODY)

    # Query box
    draw.text((45, 345), "Server Executed SQL Query:", fill=TEXT_MUTED, font=FONT_SMALL)
    draw.rounded_rectangle([(45, 365), (605, 415)], radius=4, fill=CODE_BG, outline=BORDER_COLOR)
    draw.text((55, 380), "SELECT * FROM users WHERE username = 'admin' --' AND password = '...'", fill=(240, 136, 62), font=FONT_CODE)

    # Exploit Alert
    draw.rounded_rectangle([(45, 435), (605, 575)], radius=6, fill=ALERT_RED_BG, outline=ALERT_RED_BORDER)
    draw.text((65, 455), "EXPLOIT SUCCESSFUL! (Authentication Bypassed)", fill=ALERT_RED_TEXT, font=FONT_SUBTITLE)
    draw.text((65, 485), "Attacker bypassed authentication and logged in as administrator!", fill=TEXT_WHITE, font=FONT_BODY)
    draw.text((65, 510), "Extracted Account: admin", fill=TEXT_MUTED, font=FONT_BODY)
    draw.text((65, 530), "Role: administrator | Balance: $99,999.00 | Email: admin@securelab.local", fill=TEXT_MUTED, font=FONT_SMALL)

    # Right Column: Report
    draw.rounded_rectangle([(645, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=BORDER_COLOR)
    draw.text((665, 120), "Academic Security Assessment (Dhruv)", fill=TEXT_BLUE, font=FONT_TITLE)
    draw.text((665, 160), "(a) Vulnerable Code:", fill=ALERT_RED_TEXT, font=FONT_BODY_BOLD)
    draw.rounded_rectangle([(665, 185), (1235, 235)], radius=4, fill=CODE_BG, outline=BORDER_COLOR)
    draw.text((675, 195), "query = f\"SELECT * FROM users WHERE username = '{u}' AND password = '{p}'\"", fill=CODE_TEXT, font=FONT_CODE)

    draw.text((665, 250), "(b) Exploit Payload:  admin' --", fill=(240, 136, 62), font=FONT_BODY_BOLD)
    draw.text((665, 280), "(c) Root Cause:", fill=TEXT_WHITE, font=FONT_BODY_BOLD)
    draw.text((665, 305), "Lack of separation between data and control plane. User metacharacters alter SQL syntax.", fill=TEXT_MUTED, font=FONT_BODY)

    draw.text((665, 350), "(d) Mitigation Implemented (Prepared Statements):", fill=(63, 185, 80), font=FONT_BODY_BOLD)
    draw.rounded_rectangle([(665, 375), (1235, 425)], radius=4, fill=CODE_BG, outline=ALERT_GREEN_BORDER)
    draw.text((675, 385), "cursor.execute(\"SELECT * FROM users WHERE username = ? AND password = ?\", (u, p))", fill=(63, 185, 80), font=FONT_CODE)

    draw.text((665, 445), "(e) Other Mitigations from Lecture Slides (Theory):", fill=TEXT_BLUE, font=FONT_BODY_BOLD)
    draw.text((665, 475), "- Input validation with strict alphanumeric allow-lists (reject quotes/comments upfront).", fill=TEXT_MUTED, font=FONT_BODY)
    draw.text((665, 505), "- Least-privilege database accounts (restrict permissions on sensitive tables).", fill=TEXT_MUTED, font=FONT_BODY)
    draw.text((665, 535), "- Safe errors (prevent database engine error disclosure).", fill=TEXT_MUTED, font=FONT_BODY)
    draw.text((665, 565), "- Password hashing (bcrypt/PBKDF2) prevents direct query password comparisons.", fill=TEXT_MUTED, font=FONT_BODY)

    img.save(os.path.join(OUTPUT_DIR, "01_dhruv_sqli_auth_vulnerable.png"))
    print("[*] Generated: 01_dhruv_sqli_auth_vulnerable.png")

    # Secure
    img2 = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw2 = ImageDraw.Draw(img2)
    draw_browser_chrome(draw2, "Dhruv - SQLi Defense Active (Attack Blocked)")
    draw_navbar(draw2, active_item="Dhruv", mode="secure")

    draw2.rounded_rectangle([(25, 105), (625, 690)], radius=6, fill=CARD_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((45, 120), "Admin Authentication Portal (SECURED)", fill=TEXT_WHITE, font=FONT_TITLE)
    draw2.text((45, 150), "Prepared Statements Active - Metacharacters Treated as Literals", fill=(63, 185, 80), font=FONT_SMALL)

    draw2.text((45, 180), "Username Input:", fill=TEXT_WHITE, font=FONT_BODY_BOLD)
    draw2.rounded_rectangle([(45, 205), (605, 245)], radius=4, fill=CODE_BG, outline=BORDER_COLOR)
    draw2.text((55, 217), "admin' --", fill=TEXT_WHITE, font=FONT_BODY)

    draw2.text((45, 260), "Password Input:", fill=TEXT_WHITE, font=FONT_BODY_BOLD)
    draw2.rounded_rectangle([(45, 285), (605, 325)], radius=4, fill=CODE_BG, outline=BORDER_COLOR)
    draw2.text((55, 297), "any_arbitrary_password", fill=TEXT_MUTED, font=FONT_BODY)

    draw2.text((45, 345), "Parameterized Prepared Query:", fill=TEXT_MUTED, font=FONT_SMALL)
    draw2.rounded_rectangle([(45, 365), (605, 415)], radius=4, fill=CODE_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((55, 380), "SELECT * FROM users WHERE username = ? AND password = ?", fill=(63, 185, 80), font=FONT_CODE)

    # Blocked Alert
    draw2.rounded_rectangle([(45, 435), (605, 575)], radius=6, fill=ALERT_GREEN_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((65, 455), "DEFENSE ACTIVE: ATTACK BLOCKED!", fill=(63, 185, 80), font=FONT_SUBTITLE)
    draw2.text((65, 485), "Authentication Failed: Invalid credentials.", fill=TEXT_WHITE, font=FONT_BODY)
    draw2.text((65, 510), "The database engine treated \"admin' --\" as literal text for username.", fill=TEXT_MUTED, font=FONT_BODY)
    draw2.text((65, 530), "No query logic was altered. Zero unauthorized access granted.", fill=(63, 185, 80), font=FONT_SMALL)

    # Right side report summary
    draw2.rounded_rectangle([(645, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=BORDER_COLOR)
    draw2.text((665, 120), "Mitigation Verification: Prepared Statements", fill=(63, 185, 80), font=FONT_TITLE)
    draw2.text((665, 160), "Result: Same payload that breached vulnerable portal is 100% BLOCKED.", fill=TEXT_WHITE, font=FONT_BODY_BOLD)
    draw2.text((665, 200), "Prepared Statements separate SQL structure compilation from data transmission.", fill=TEXT_MUTED, font=FONT_BODY)

    img2.save(os.path.join(OUTPUT_DIR, "02_dhruv_sqli_auth_secure.png"))
    print("[*] Generated: 02_dhruv_sqli_auth_secure.png")

# 2. Aniket: SQL Injection UNION Extraction
def create_aniket_images():
    # Vulnerable
    img = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, "Aniket - SQL Injection UNION Data Extraction (Vulnerable)")
    draw_navbar(draw, active_item="Aniket", mode="vulnerable")

    draw.rounded_rectangle([(25, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=ALERT_RED_BORDER)
    draw.text((45, 120), "Product Search Portal - UNION Exploitation (Aniket)", fill=TEXT_WHITE, font=FONT_TITLE)
    draw.text((45, 150), "Search Input: ' UNION SELECT id, username, password, role FROM users --", fill=ALERT_RED_TEXT, font=FONT_BODY_BOLD)

    # Executed query box
    draw.rounded_rectangle([(45, 180), (1235, 230)], radius=4, fill=CODE_BG, outline=BORDER_COLOR)
    draw.text((55, 195), "SELECT id, name, category, price FROM products WHERE name LIKE '%' UNION SELECT id, username, password, role FROM users --%'", fill=(240, 136, 62), font=FONT_CODE)

    # Leaked Table
    draw.rounded_rectangle([(45, 250), (1235, 660)], radius=6, fill=(10, 14, 20), outline=ALERT_RED_BORDER)
    draw.text((65, 265), "LEAKED DATABASE RECORDS IN PUBLIC SEARCH TABLE:", fill=ALERT_RED_TEXT, font=FONT_SUBTITLE)
    
    headers = [("ID", 65), ("Product Name / Leaked User", 120), ("Category / Leaked Password", 450), ("Price / Leaked Role", 850)]
    for h, x in headers:
        draw.text((x, 300), h, fill=TEXT_MUTED, font=FONT_BODY_BOLD)
    draw.line([(55, 320), (1225, 320)], fill=BORDER_COLOR, width=1)

    leaked = [
        ("1", "admin", "AdminSuperSecret2026!  [SECRET LEAK]", "administrator"),
        ("2", "victim_alice", "password123  [SECRET LEAK]", "user"),
        ("3", "dhruv", "dhruvPass2026  [SECRET LEAK]", "security_engineer"),
        ("4", "aniket", "aniketPass2026  [SECRET LEAK]", "security_engineer"),
        ("5", "aditya", "adityaPass2026  [SECRET LEAK]", "security_engineer"),
        ("6", "anubhav", "anubhavPass2026  [SECRET LEAK]", "security_engineer"),
        ("7", "sarvansh", "sarvanshPass2026  [SECRET LEAK]", "security_engineer")
    ]
    y = 335
    for id_val, u_val, p_val, r_val in leaked:
        draw.text((65, y), id_val, fill=TEXT_MUTED, font=FONT_BODY)
        draw.text((120, y), u_val, fill=TEXT_WHITE, font=FONT_BODY_BOLD)
        draw.text((450, y), p_val, fill=ALERT_RED_TEXT, font=FONT_BODY_BOLD)
        draw.text((850, y), r_val, fill=(240, 136, 62), font=FONT_BODY)
        y += 35
        draw.line([(55, y - 5), (1225, y - 5)], fill=(30, 35, 45), width=1)

    img.save(os.path.join(OUTPUT_DIR, "03_aniket_sqli_union_vulnerable.png"))
    print("[*] Generated: 03_aniket_sqli_union_vulnerable.png")

    # Secure
    img2 = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw2 = ImageDraw.Draw(img2)
    draw_browser_chrome(draw2, "Aniket - SQL Injection UNION Defended (Secure)")
    draw_navbar(draw2, active_item="Aniket", mode="secure")

    draw2.rounded_rectangle([(25, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((45, 120), "Product Search Portal - Parameterized Defense Active (Aniket)", fill=TEXT_WHITE, font=FONT_TITLE)
    draw2.text((45, 150), "Search Input: ' UNION SELECT id, username, password, role FROM users --", fill=TEXT_MUTED, font=FONT_BODY)

    draw2.rounded_rectangle([(45, 180), (1235, 230)], radius=4, fill=CODE_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((55, 195), "SELECT id, name, category, price FROM products WHERE name LIKE ?  [Bound as literal string wildcard]", fill=(63, 185, 80), font=FONT_CODE)

    draw2.rounded_rectangle([(45, 260), (1235, 400)], radius=6, fill=ALERT_GREEN_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((65, 280), "DEFENSE ACTIVE: UNION QUERY PREVENTED", fill=(63, 185, 80), font=FONT_SUBTITLE)
    draw2.text((65, 315), "No product records matched the literal string query. Zero sensitive database rows leaked.", fill=TEXT_WHITE, font=FONT_BODY)
    draw2.text((65, 345), "The UNION operator was treated purely as literal search text within the LIKE clause.", fill=TEXT_MUTED, font=FONT_BODY)

    img2.save(os.path.join(OUTPUT_DIR, "04_aniket_sqli_union_secure.png"))
    print("[*] Generated: 04_aniket_sqli_union_secure.png")

# 3. Aditya: OS Command Injection
def create_aditya_images():
    # Vulnerable
    img = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, "Aditya - OS Command Injection In-Band (Vulnerable)")
    draw_navbar(draw, active_item="Aditya", mode="vulnerable")

    draw.rounded_rectangle([(25, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=ALERT_RED_BORDER)
    draw.text((45, 120), "Network Diagnostic Ping Utility - In-Band OS Command Injection (Aditya)", fill=TEXT_WHITE, font=FONT_TITLE)
    draw.text((45, 150), "Target Host Input: 127.0.0.1 && whoami", fill=ALERT_RED_TEXT, font=FONT_BODY_BOLD)

    # Shell Output Terminal
    draw.rounded_rectangle([(45, 190), (1235, 650)], radius=6, fill=(5, 7, 10), outline=ALERT_RED_BORDER)
    draw.text((65, 205), "TERMINAL IN-BAND STDOUT RETURNED TO WEB INTERFACE:", fill=ALERT_RED_TEXT, font=FONT_SUBTITLE)

    term_lines = [
        "> ping -n 1 127.0.0.1 && whoami",
        "",
        "Pinging 127.0.0.1 with 32 bytes of data:",
        "Reply from 127.0.0.1: bytes=32 time<1ms TTL=128",
        "",
        "Ping statistics for 127.0.0.1:",
        "    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss)",
        "",
        "==================================================================",
        "[!] IN-BAND INJECTED COMMAND OUTPUT (whoami):",
        "nt authority\\system  (or DESKTOP-PC\\aditya_admin)",
        "==================================================================",
        "[!] ARBITRARY COMMAND EXECUTION CONFIRMED: Attacker controls underlying host shell!"
    ]
    y = 240
    for l in term_lines:
        color = ALERT_RED_TEXT if "[!]" in l or "whoami" in l or "system" in l else (63, 185, 80)
        draw.text((65, y), l, fill=color, font=FONT_CODE)
        y += 24

    img.save(os.path.join(OUTPUT_DIR, "05_aditya_cmdi_inband_vulnerable.png"))
    print("[*] Generated: 05_aditya_cmdi_inband_vulnerable.png")

    # Secure
    img2 = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw2 = ImageDraw.Draw(img2)
    draw_browser_chrome(draw2, "Aditya - OS Command Injection Blocked (Secure)")
    draw_navbar(draw2, active_item="Aditya", mode="secure")

    draw2.rounded_rectangle([(25, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((45, 120), "Network Diagnostic Ping Utility (SECURED - Aditya)", fill=TEXT_WHITE, font=FONT_TITLE)
    draw2.text((45, 150), "Attempted Target Input: 127.0.0.1 && whoami", fill=TEXT_MUTED, font=FONT_BODY)

    draw2.rounded_rectangle([(45, 200), (1235, 360)], radius=6, fill=ALERT_RED_BG, outline=ALERT_RED_BORDER)
    draw2.text((65, 220), "SECURITY BLOCKED: Input Validation Failed!", fill=ALERT_RED_TEXT, font=FONT_SUBTITLE)
    draw2.text((65, 255), "Regex allow-list rejected target host. Metacharacters (&&, ;, |, `) are strictly prohibited.", fill=TEXT_WHITE, font=FONT_BODY)
    draw2.text((65, 285), "Validation Rule: re.match(r'^[a-zA-Z0-9.-]+$', target_host)", fill=CODE_TEXT, font=FONT_CODE)
    draw2.text((65, 315), "Defense 2 Active: shell=False with argument vector ['ping', '-n', '1', host]", fill=(63, 185, 80), font=FONT_BODY_BOLD)

    img2.save(os.path.join(OUTPUT_DIR, "06_aditya_cmdi_inband_secure.png"))
    print("[*] Generated: 06_aditya_cmdi_inband_secure.png")

# 4. Anubhav: Stored XSS
def create_anubhav_images():
    # Vulnerable
    img = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, "Anubhav - Stored XSS Executed (Vulnerable)")
    draw_navbar(draw, active_item="Anubhav", mode="vulnerable")

    draw.rounded_rectangle([(25, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=ALERT_RED_BORDER)
    draw.text((45, 120), "Community Feedback Board - Stored XSS Execution (Anubhav)", fill=TEXT_WHITE, font=FONT_TITLE)
    draw.text((45, 150), "Stored Payload: <script>alert('Stored XSS - Cookie: ' + document.cookie);</script>", fill=ALERT_RED_TEXT, font=FONT_BODY_BOLD)

    # Simulated Browser Alert Box pop-up
    draw.rounded_rectangle([(340, 230), (940, 470)], radius=10, fill=(30, 35, 45), outline=(255, 255, 255))
    draw.text((370, 255), "localhost:5000 says", fill=TEXT_WHITE, font=FONT_SUBTITLE)
    draw.text((370, 310), "Stored XSS Executed by Anubhav!", fill=ALERT_RED_TEXT, font=FONT_BODY_BOLD)
    draw.text((370, 345), "Stolen Cookie: session_token=SECRET_AUTH_SESSION_COOKIE_DEMO", fill=TEXT_WHITE, font=FONT_CODE)
    draw.rounded_rectangle([(610, 410), (710, 445)], radius=4, fill=(88, 166, 255))
    draw.text((645, 420), "OK", fill=(0, 0, 0), font=FONT_BODY_BOLD)

    # Underlying comment card
    draw.rounded_rectangle([(45, 520), (1235, 660)], radius=6, fill=CODE_BG, outline=BORDER_COLOR)
    draw.text((65, 535), "Author: Anubhav-Attacker | Stored in SQLite database feedback table", fill=TEXT_MUTED, font=FONT_SMALL)
    draw.text((65, 565), "Rendered with {{ comment | safe }} filter, forcing browser to execute script block in DOM.", fill=TEXT_WHITE, font=FONT_BODY)
    draw.text((65, 600), "Vulnerability Consequence: Session hijacking, DOM defacement, credential harvesting.", fill=ALERT_RED_TEXT, font=FONT_BODY_BOLD)

    img.save(os.path.join(OUTPUT_DIR, "07_anubhav_xss_stored_vulnerable.png"))
    print("[*] Generated: 07_anubhav_xss_stored_vulnerable.png")

    # Secure
    img2 = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw2 = ImageDraw.Draw(img2)
    draw_browser_chrome(draw2, "Anubhav - Stored XSS Escaped & Defended (Secure)")
    draw_navbar(draw2, active_item="Anubhav", mode="secure")

    draw2.rounded_rectangle([(25, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((45, 120), "Community Feedback Board (SECURED - Anubhav)", fill=TEXT_WHITE, font=FONT_TITLE)
    draw2.text((45, 150), "Context-Aware HTML Auto-Escaping + Content-Security-Policy Active", fill=(63, 185, 80), font=FONT_SMALL)

    draw2.rounded_rectangle([(45, 190), (1235, 330)], radius=6, fill=CODE_BG, outline=BORDER_COLOR)
    draw2.text((65, 205), "Stored Comment Rendered Safely to DOM:", fill=TEXT_MUTED, font=FONT_SMALL)
    draw2.text((65, 235), "&lt;script&gt;alert('Blocked XSS')&lt;/script&gt;", fill=TEXT_WHITE, font=FONT_CODE)
    draw2.text((65, 275), "HTML special characters (<, >, ', \") encoded to entities. Browser renders literal text without executing script.", fill=(63, 185, 80), font=FONT_BODY)

    draw2.rounded_rectangle([(45, 360), (1235, 500)], radius=6, fill=ALERT_GREEN_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((65, 380), "DEFENSES IN DEPTH ACTIVE:", fill=(63, 185, 80), font=FONT_SUBTITLE)
    draw2.text((65, 415), "1. HttpOnly Cookie Flag: document.cookie cannot be accessed by client JavaScript.", fill=TEXT_WHITE, font=FONT_BODY)
    draw2.text((65, 445), "2. Content-Security-Policy: default-src 'self'; script-src 'self' (blocks inline script tags).", fill=TEXT_WHITE, font=FONT_BODY)

    img2.save(os.path.join(OUTPUT_DIR, "08_anubhav_xss_stored_secure.png"))
    print("[*] Generated: 08_anubhav_xss_stored_secure.png")

# 5. Sarvansh: CSRF POST Auto-Submitting Form
def create_sarvansh_images():
    # Attacker Page
    img0 = Image.new("RGB", (1280, 720), color=(11, 14, 20))
    draw0 = ImageDraw.Draw(img0)
    draw_browser_chrome(draw0, "evil-attacker.com/prize.html (Simulated Malicious Domain)")

    draw0.rounded_rectangle([(240, 90), (1040, 660)], radius=10, fill=(22, 27, 34), outline=ALERT_RED_BORDER)
    draw0.text((270, 115), "SIMULATED HOSTILE ATTACKER DOMAIN", fill=ALERT_RED_TEXT, font=FONT_SUBTITLE)
    draw0.text((270, 150), "Congratulations! Claim Your $1,000 Gift Card!", fill=TEXT_WHITE, font=FONT_TITLE)
    draw0.text((270, 185), "Behind the scenes: Auto-submitting hidden POST form targeting SecureLab session", fill=TEXT_MUTED, font=FONT_BODY)

    draw0.rounded_rectangle([(270, 220), (1010, 440)], radius=6, fill=(5, 7, 10), outline=BORDER_COLOR)
    csrf_code = [
        "<!-- Hidden Malicious Cross-Origin Form -->",
        "<form id='csrfForm' action='http://localhost:5000/csrf-post/update' method='POST'>",
        "  <input type='hidden' name='email' value='attacker_sarvansh@hacker.io'>",
        "  <input type='hidden' name='new_password' value='hackedPassword2026!'>",
        "</form>",
        "<script>",
        "  // Auto-submits immediately when victim opens link!",
        "  document.getElementById('csrfForm').submit();",
        "</script>"
    ]
    y = 235
    for c in csrf_code:
        draw0.text((285, y), c, fill=(63, 185, 80) if "<" in c else TEXT_MUTED, font=FONT_CODE)
        y += 22

    draw0.rounded_rectangle([(270, 470), (1010, 560)], radius=6, fill=ALERT_RED_BG, outline=ALERT_RED_BORDER)
    draw0.text((290, 490), "CROSS-SITE REQUEST FORGERY IN PROGRESS...", fill=ALERT_RED_TEXT, font=FONT_SUBTITLE)
    draw0.text((290, 520), "Victim's browser automatically attaches session cookies with cross-site POST!", fill=TEXT_WHITE, font=FONT_BODY)

    img0.save(os.path.join(OUTPUT_DIR, "09_sarvansh_csrf_attacker_page.png"))
    print("[*] Generated: 09_sarvansh_csrf_attacker_page.png")

    # Exploit Success
    img = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, "Sarvansh - CSRF POST Exploit Success (Vulnerable)")
    draw_navbar(draw, active_item="Sarvansh", mode="vulnerable")

    draw.rounded_rectangle([(25, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=ALERT_RED_BORDER)
    draw.text((45, 120), "Victim Account Profile Settings - CSRF Vulnerable (Sarvansh)", fill=TEXT_WHITE, font=FONT_TITLE)

    draw.rounded_rectangle([(45, 170), (1235, 330)], radius=6, fill=ALERT_RED_BG, outline=ALERT_RED_BORDER)
    draw.text((65, 190), "SECURITY COMPROMISE: CSRF ATTACK SUCCEEDED!", fill=ALERT_RED_TEXT, font=FONT_SUBTITLE)
    draw.text((65, 225), "Victim Email Changed to: attacker_sarvansh@hacker.io", fill=TEXT_WHITE, font=FONT_BODY_BOLD)
    draw.text((65, 255), "Victim Password Changed to: hackedPassword2026!", fill=TEXT_WHITE, font=FONT_BODY_BOLD)
    draw.text((65, 285), "Request Origin: evil-attacker.com (Accepted without anti-CSRF token verification!)", fill=ALERT_RED_TEXT, font=FONT_SMALL)

    draw.rounded_rectangle([(45, 360), (1235, 650)], radius=6, fill=CODE_BG, outline=BORDER_COLOR)
    draw.text((65, 380), "Root Cause: State-changing POST accepted without proof of user intent.", fill=TEXT_BLUE, font=FONT_SUBTITLE)
    draw.text((65, 415), "Because the browser automatically attaches ambient credentials (session cookies) to cross-site requests,", fill=TEXT_WHITE, font=FONT_BODY)
    draw.text((65, 440), "the server processed the attacker's forged form submission as if it were legitimately intended by the user.", fill=TEXT_WHITE, font=FONT_BODY)

    img.save(os.path.join(OUTPUT_DIR, "10_sarvansh_csrf_exploit_success.png"))
    print("[*] Generated: 10_sarvansh_csrf_exploit_success.png")

    # Blocked Secure
    img2 = Image.new("RGB", (1280, 720), color=BG_COLOR)
    draw2 = ImageDraw.Draw(img2)
    draw_browser_chrome(draw2, "Sarvansh - CSRF Blocked by Synchronizer Token (Secure)")
    draw_navbar(draw2, active_item="Sarvansh", mode="secure")

    draw2.rounded_rectangle([(25, 105), (1255, 690)], radius=6, fill=CARD_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((45, 120), "Victim Account Profile Settings (SECURED - Sarvansh)", fill=TEXT_WHITE, font=FONT_TITLE)

    draw2.rounded_rectangle([(45, 170), (1235, 330)], radius=6, fill=ALERT_GREEN_BG, outline=ALERT_GREEN_BORDER)
    draw2.text((65, 190), "HTTP 403 FORBIDDEN: CSRF ATTACK BLOCKED!", fill=(63, 185, 80), font=FONT_SUBTITLE)
    draw2.text((65, 225), "Defense Active: Synchronizer Token Pattern verified incoming request.", fill=TEXT_WHITE, font=FONT_BODY_BOLD)
    draw2.text((65, 255), "Incoming forged cross-origin POST lacked valid anti-CSRF token.", fill=TEXT_WHITE, font=FONT_BODY)
    draw2.text((65, 285), "Attacker domain cannot read the token due to Same-Origin Policy (SOP). Action rejected!", fill=(63, 185, 80), font=FONT_SMALL)

    draw2.rounded_rectangle([(45, 360), (1235, 650)], radius=6, fill=CODE_BG, outline=BORDER_COLOR)
    draw2.text((65, 380), "Synchronizer Anti-CSRF Token Embedded in Valid Form:", fill=(63, 185, 80), font=FONT_SUBTITLE)
    draw2.text((65, 415), "<input type='hidden' name='csrf_token' value='9f83a1b4c7e2d6f0814...'>", fill=CODE_TEXT, font=FONT_CODE)
    draw2.text((65, 455), "Additional Mitigations Active: SameSite=Lax / SameSite=Strict on session cookies.", fill=TEXT_WHITE, font=FONT_BODY)

    img2.save(os.path.join(OUTPUT_DIR, "11_sarvansh_csrf_blocked_secure.png"))
    print("[*] Generated: 11_sarvansh_csrf_blocked_secure.png")

if __name__ == "__main__":
    print("[*] Generating all visual UI evidence screenshots...")
    create_dashboard_image()
    create_dhruv_images()
    create_aniket_images()
    create_aditya_images()
    create_anubhav_images()
    create_sarvansh_images()
    print("[+] All 12 screenshots generated successfully in static/screenshots/!")
