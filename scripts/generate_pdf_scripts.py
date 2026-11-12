"""
Generates the comprehensive PDF:
'SecureLab_Video_Demo_Scripts_and_Viva_Guide.pdf'
Contains:
- Table 3 Ownership Declaration
- 2-3 minute timed spoken scripts for Dhruv, Aniket, Aditya, Anubhav, Sarvansh
- Step-by-step on-screen action cues
- Embedded visual screenshots of working exploits & blocked defenses
- Table 2 technical explanations (a-e) and viva preparation questions
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "static", "screenshots")
PDF_OUTPUT_PATH = os.path.join(BASE_DIR, "SecureLab_Video_Demo_Scripts_and_Viva_Guide.pdf")

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0f172a'),
        alignment=1, # Center
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )

    script_style = ParagraphStyle(
        'Script_Quote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e1b4b'),
        backColor=colors.HexColor('#f5f3ff'),
        borderColor=colors.HexColor('#8b5cf6'),
        borderWidth=1,
        borderPadding=8,
        spaceBefore=5,
        spaceAfter=8,
        borderRadius=4
    )

    action_style = ParagraphStyle(
        'Action_Cue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#9a3412'),
        backColor=colors.HexColor('#fff7ed'),
        borderColor=colors.HexColor('#f97316'),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6,
        borderRadius=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a'),
        backColor=colors.HexColor('#f1f5f9'),
        borderPadding=5,
        spaceBefore=3,
        spaceAfter=5
    )

    story = []

    # -------------------------------------------------------------------------
    # COVER / HEADER
    # -------------------------------------------------------------------------
    story.append(Paragraph("SecureLab: Video Demonstration Scripts & Viva Guide", title_style))
    story.append(Paragraph("Hands-on Web Server Security: SQLi, OS Command Injection, XSS, and CSRF<br/><b>Group Members:</b> Dhruv, Aniket, Aditya, Anubhav, Sarvansh", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#cbd5e1'), spaceAfter=12))

    # Table 3
    story.append(Paragraph("<b>Table 3: Ownership Declaration (Course Compliance)</b>", h2_style))
    table3_data = [
        [Paragraph("<b>#</b>", body_style), Paragraph("<b>Member Name</b>", body_style), Paragraph("<b>Category</b>", body_style), Paragraph("<b>Variant Implemented</b>", body_style), Paragraph("<b>Timing</b>", body_style)],
        [Paragraph("1", body_style), Paragraph("<b>Dhruv</b>", body_style), Paragraph("SQL Injection", body_style), Paragraph("Variant 1: Authentication bypass", body_style), Paragraph("2.5 mins (0:00 - 2:30)", body_style)],
        [Paragraph("2", body_style), Paragraph("<b>Aniket</b>", body_style), Paragraph("SQL Injection", body_style), Paragraph("Variant 2: UNION-based data extraction", body_style), Paragraph("2.5 mins (2:30 - 5:00)", body_style)],
        [Paragraph("3", body_style), Paragraph("<b>Aditya</b>", body_style), Paragraph("OS Command Injection", body_style), Paragraph("Variant 1: In-band (command output returned)", body_style), Paragraph("2.5 mins (5:00 - 7:30)", body_style)],
        [Paragraph("4", body_style), Paragraph("<b>Anubhav</b>", body_style), Paragraph("Cross-Site Scripting (XSS)", body_style), Paragraph("Variant 1: Stored XSS", body_style), Paragraph("2.5 mins (7:30 - 10:00)", body_style)],
        [Paragraph("5", body_style), Paragraph("<b>Sarvansh</b>", body_style), Paragraph("CSRF", body_style), Paragraph("Variant 2: POST-based forged action (auto-submit)", body_style), Paragraph("2.5 mins (10:00 - 12:30)", body_style)],
    ]
    t3 = Table(table3_data, colWidths=[25, 80, 120, 205, 110])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t3)
    story.append(Spacer(1, 10))

    # Dashboard screenshot
    dash_img_path = os.path.join(SCREENSHOT_DIR, "00_securelab_dashboard.png")
    if os.path.exists(dash_img_path):
        story.append(Paragraph("<b>Figure 1:</b> SecureLab Interactive Security Dashboard & Table 3 Live Portal", body_style))
        story.append(RLImage(dash_img_path, width=540, height=270))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # MEMBER 1: DHRUV
    # -------------------------------------------------------------------------
    story.append(Paragraph("Member 1: Dhruv — SQL Injection (Auth Bypass)", h1_style))
    story.append(Paragraph("<b>Target Variant:</b> SQL Injection — Variant 1 (Authentication Bypass) &bull; <b>Time:</b> ~2.5 Minutes", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Step-by-Step Spoken Script & Actions (Video Voice-Over):</b>", h2_style))
    
    story.append(Paragraph("<b>ACTION 1:</b> [Screen shows SecureLab Dashboard, mouse points to Dhruv's row in Table 3, clicks 'Demo Auth Bypass']", action_style))
    story.append(Paragraph(
        "\"Hello everyone. My name is Dhruv, and I am demonstrating Variant 1 of SQL Injection: Authentication Bypass. "
        "As seen on our project dashboard, I personally implemented and secured this module on target endpoint <code>POST /sqli-auth</code>.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 2:</b> [Ensure the navbar displays 'VULNERABLE MODE'. In the Username field, type <code>admin' --</code>. In Password, type <code>anyPassword123</code>. Click 'Attempt Authentication'.]", action_style))
    story.append(Paragraph(
        "\"First, I will demonstrate the flaw under our application's Vulnerable Mode. I enter <code>admin' --</code> in the username field, "
        "and provide any random password. When I click Login, notice the red alert: we have successfully bypassed authentication and logged in as "
        "the administrator without knowing the password!\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 3:</b> [Scroll down to the server-executed query box showing the raw SQL statement.]", action_style))
    story.append(Paragraph(
        "\"The root cause is unvalidated string interpolation. The server formats raw user input into: "
        "<code>SELECT * FROM users WHERE username = 'admin' --' AND password = '...'</code>. "
        "The single quote prematurely terminates the username string, and the double-dash instructs the SQLite engine to treat everything following it as a comment, "
        "completely short-circuiting the password verification logic.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 4:</b> [Click the top navbar button 'Click to Secure'. Show the green banner 'SECURE / MITIGATED MODE'. Type the exact same payload <code>admin' --</code> and click Login.]", action_style))
    story.append(Paragraph(
        "\"Now, I activate our implemented defense by toggling the platform into Secure Mode. I submit the exact same exploit payload: <code>admin' --</code>. "
        "Notice that authentication is blocked with 'Invalid credentials'. Our mitigation is <b>Parameterized Queries with Prepared Statements</b> using positional placeholders. "
        "The database pre-compiles the query tree, and treats <code>admin' --</code> purely as a literal string value, not executable SQL syntax.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 5:</b> [Summarize other lecture mitigations for 20 seconds to conclude.]", action_style))
    story.append(Paragraph(
        "\"Beyond prepared statements, other mitigations discussed in class include strict alphanumeric allow-lists to reject quotes upfront, "
        "least-privilege database user accounts, suppressing error messages, and storing salted password hashes using bcrypt or PBKDF2. "
        "I now hand over to Aniket for Variant 2.\"",
        script_style
    ))

    # Screenshots for Dhruv
    story.append(Spacer(1, 4))
    img_dhruv_vuln = os.path.join(SCREENSHOT_DIR, "01_dhruv_sqli_auth_vulnerable.png")
    img_dhruv_sec = os.path.join(SCREENSHOT_DIR, "02_dhruv_sqli_auth_secure.png")
    if os.path.exists(img_dhruv_vuln) and os.path.exists(img_dhruv_sec):
        story.append(Paragraph("<b>Evidence 1 (Left: Exploit Working &bull; Right: Attack Blocked by Prepared Statements):</b>", body_style))
        t_dhruv_imgs = Table([
            [RLImage(img_dhruv_vuln, width=265, height=140), RLImage(img_dhruv_sec, width=265, height=140)]
        ], colWidths=[270, 270])
        story.append(t_dhruv_imgs)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # MEMBER 2: ANIKET
    # -------------------------------------------------------------------------
    story.append(Paragraph("Member 2: Aniket — SQL Injection (UNION Data Extraction)", h1_style))
    story.append(Paragraph("<b>Target Variant:</b> SQL Injection — Variant 2 (UNION-Based Data Extraction) &bull; <b>Time:</b> ~2.5 Minutes", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Step-by-Step Spoken Script & Actions (Video Voice-Over):</b>", h2_style))

    story.append(Paragraph("<b>ACTION 1:</b> [Screen navigates to <code>/sqli-union</code> (Product Catalog Search), showing Table 3 row for Aniket.]", action_style))
    story.append(Paragraph(
        "\"Hello everyone. My name is Aniket, and I am presenting Variant 2 of SQL Injection: UNION-Based Data Extraction. "
        "While Dhruv bypassed authentication logic, my implementation demonstrates how an attacker extracts unauthorized database records into public tables.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 2:</b> [Ensure Vulnerable Mode is active. Enter normal search 'Camera' first, then paste payload: <code>' UNION SELECT id, username, password, role FROM users --</code> and click Search.]", action_style))
    story.append(Paragraph(
        "\"In our vulnerable implementation, the search parameter is concatenated directly into the product query's LIKE clause. "
        "A normal search returns product appliances. But when I inject: "
        "<code>' UNION SELECT id, username, password, role FROM users --</code> and click Search, look at the results table: "
        "the database executes both queries and appends secret user records, passwords, and administrative roles directly into the public product columns!\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 3:</b> [Highlight the executed query box and explain root cause.]", action_style))
    story.append(Paragraph(
        "\"The root cause is that SQLite allows the set operator <code>UNION</code> to combine results from two queries having matching column counts (4 columns here). "
        "Because user input was not parameterized, the attacker forces the database to disclose confidential internal tables.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 4:</b> [Toggle system to Secure Mode. Submit the exact same UNION payload in search box.]", action_style))
    story.append(Paragraph(
        "\"To secure this endpoint, I implemented <b>Parameterized Wildcard Binding</b> using <code>cursor.execute('... WHERE name LIKE ?', (f'%{q}%',))</code>. "
        "When I run the exact same UNION attack in Secure Mode, the database treats the entire payload as literal text. "
        "Zero sensitive rows are leaked, and the search simply reports 'No matching records returned'.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 5:</b> [Summarize lecture mitigations.]", action_style))
    story.append(Paragraph(
        "\"Additional mitigations from our lecture include configuring least-privilege database user permissions—so the web search user has zero SELECT access on the users table—using "
        "Object-Relational Mappers (ORMs), and suppressing column mismatch errors. I now pass over to Aditya for OS Command Injection.\"",
        script_style
    ))

    # Screenshots for Aniket
    story.append(Spacer(1, 4))
    img_aniket_vuln = os.path.join(SCREENSHOT_DIR, "03_aniket_sqli_union_vulnerable.png")
    img_aniket_sec = os.path.join(SCREENSHOT_DIR, "04_aniket_sqli_union_secure.png")
    if os.path.exists(img_aniket_vuln) and os.path.exists(img_aniket_sec):
        story.append(Paragraph("<b>Evidence 2 (Left: Leaked Passwords via UNION &bull; Right: Attack Neutralized by Parameterized Query):</b>", body_style))
        t_aniket_imgs = Table([
            [RLImage(img_aniket_vuln, width=265, height=140), RLImage(img_aniket_sec, width=265, height=140)]
        ], colWidths=[270, 270])
        story.append(t_aniket_imgs)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # MEMBER 3: ADITYA
    # -------------------------------------------------------------------------
    story.append(Paragraph("Member 3: Aditya — OS Command Injection (In-Band)", h1_style))
    story.append(Paragraph("<b>Target Variant:</b> OS Command Injection — Variant 1 (In-Band Output Returned) &bull; <b>Time:</b> ~2.5 Minutes", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Step-by-Step Spoken Script & Actions (Video Voice-Over):</b>", h2_style))

    story.append(Paragraph("<b>ACTION 1:</b> [Screen navigates to <code>/cmdi-inband</code> (Network Diagnostic Utility / Ping Tool).]", action_style))
    story.append(Paragraph(
        "\"Hello, I am Aditya. I am demonstrating Variant 1 of OS Command Injection: In-Band execution, on target endpoint <code>POST /cmdi-inband</code>. "
        "This category occurs when a web application executes operating system commands on the server using unsanitized user inputs.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 2:</b> [Ensure Vulnerable Mode is active. Enter <code>127.0.0.1 && whoami</code> in the target host field and click Execute Ping.]", action_style))
    story.append(Paragraph(
        "\"In Vulnerable Mode, our diagnostic utility takes an IP address and executes <code>ping -n 1 {target}</code> with Python's <code>subprocess.run(cmd, shell=True)</code>. "
        "I submit the payload <code>127.0.0.1 && whoami</code>. "
        "As you can see in the in-band terminal output, after pinging localhost, the server immediately executes <code>whoami</code> and prints the operating system user account "
        "directly onto our webpage! This is an <b>in-band exploit</b> because the command output is returned in the application's normal HTTP response channel.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 3:</b> [Explain root cause clearly.]", action_style))
    story.append(Paragraph(
        "\"The root cause is invoking a system shell with <code>shell=True</code>. The shell interpreter evaluates characters like <code>&&</code>, <code>&</code>, <code>;</code>, and <code>|</code> "
        "as command chaining separators, allowing arbitrary unauthorized commands to run with the privileges of the web server process.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 4:</b> [Toggle platform to Secure Mode. Submit the exact same payload: <code>127.0.0.1 && whoami</code>.]", action_style))
    story.append(Paragraph(
        "\"Now I switch to Secure Mode. I run the exact same payload: <code>127.0.0.1 && whoami</code>. "
        "Notice the red security banner: <b>SECURITY BLOCKED</b>. My implemented mitigation employs two layers of defense: "
        "First, <b>strict regex allow-list validation</b> using <code>^[a-zA-Z0-9.-]+$</code> which instantly rejects all shell metacharacters. "
        "Second, <b>avoiding the shell</b> by setting <code>shell=False</code> and passing an argument vector array <code>['ping', '-n', '1', target]</code> directly to the OS kernel.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 5:</b> [Summarize lecture mitigations.]", action_style))
    story.append(Paragraph(
        "\"Other mitigations from class include avoiding system binary execution altogether by using native language APIs like Python's <code>socket</code> library, "
        "and running web processes under heavily restricted, unprivileged service accounts or Docker containers. Next is Anubhav with Stored XSS.\"",
        script_style
    ))

    # Screenshots for Aditya
    story.append(Spacer(1, 4))
    img_aditya_vuln = os.path.join(SCREENSHOT_DIR, "05_aditya_cmdi_inband_vulnerable.png")
    img_aditya_sec = os.path.join(SCREENSHOT_DIR, "06_aditya_cmdi_inband_secure.png")
    if os.path.exists(img_aditya_vuln) and os.path.exists(img_aditya_sec):
        story.append(Paragraph("<b>Evidence 3 (Left: In-Band Command Output Returned &bull; Right: Blocked by Allow-List & Argument Vector):</b>", body_style))
        t_aditya_imgs = Table([
            [RLImage(img_aditya_vuln, width=265, height=140), RLImage(img_aditya_sec, width=265, height=140)]
        ], colWidths=[270, 270])
        story.append(t_aditya_imgs)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # MEMBER 4: ANUBHAV
    # -------------------------------------------------------------------------
    story.append(Paragraph("Member 4: Anubhav — Cross-Site Scripting (Stored XSS)", h1_style))
    story.append(Paragraph("<b>Target Variant:</b> Cross-Site Scripting (XSS) — Variant 1 (Stored XSS) &bull; <b>Time:</b> ~2.5 Minutes", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Step-by-Step Spoken Script & Actions (Video Voice-Over):</b>", h2_style))

    story.append(Paragraph("<b>ACTION 1:</b> [Screen navigates to <code>/xss-stored</code> (Community Feedback Board).]", action_style))
    story.append(Paragraph(
        "\"Hello everyone. My name is Anubhav, and I am demonstrating Variant 1 of Cross-Site Scripting: Stored XSS, on target endpoint <code>POST /xss-stored</code>. "
        "Stored XSS is the most dangerous form of XSS because the malicious script is persisted in the server database and delivered to every visitor.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 2:</b> [Ensure Vulnerable Mode is active. In comment field, enter: <code>&lt;script&gt;alert('Stored XSS Executed by Anubhav! Stolen Cookie: ' + document.cookie);&lt;/script&gt;</code> and click Submit.]", action_style))
    story.append(Paragraph(
        "\"In Vulnerable Mode, user feedback is rendered using Jinja2's <code>| safe</code> filter, which disables HTML escaping. "
        "I submit this payload containing a script tag that reads <code>document.cookie</code>. "
        "Upon submission—and whenever any user visits or refreshes this page—the browser automatically parses and executes the attacker's script, "
        "displaying an alert box with the victim's session cookie! An attacker could transmit this cookie to an external server to hijack the session.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 3:</b> [Explain root cause.]", action_style))
    story.append(Paragraph(
        "\"The root cause is rendering untrusted user-controlled data into HTML without context-aware output encoding. "
        "The browser cannot distinguish between legitimate scripts written by the developer and malicious scripts injected by users.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 4:</b> [Toggle to Secure Mode. Submit the exact same XSS script payload. Show safe rendering.]", action_style))
    story.append(Paragraph(
        "\"Now I activate Secure Mode. I submit the exact same script payload. "
        "Notice that no alert pop-up appears! Instead, the text is safely displayed as literal characters: <code>&amp;lt;script&amp;gt;</code>. "
        "Our implemented mitigation removes the <code>| safe</code> filter, enforcing <b>Context-Aware HTML Entity Auto-Escaping</b>. "
        "Furthermore, our server sets the <code>HttpOnly</code> cookie flag and enforces a <b>Content Security Policy (CSP)</b> header blocking inline scripts.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 5:</b> [Summarize other lecture mitigations.]", action_style))
    story.append(Paragraph(
        "\"Other mitigations covered in the lecture include rich HTML sanitizers like DOMPurify or Bleach for formatted text, "
        "and utilizing safe DOM sinks like <code>textContent</code> instead of dangerous sinks like <code>innerHTML</code> or <code>eval()</code>. "
        "Finally, Sarvansh will demonstrate CSRF.\"",
        script_style
    ))

    # Screenshots for Anubhav
    story.append(Spacer(1, 4))
    img_anubhav_vuln = os.path.join(SCREENSHOT_DIR, "07_anubhav_xss_stored_vulnerable.png")
    img_anubhav_sec = os.path.join(SCREENSHOT_DIR, "08_anubhav_xss_stored_secure.png")
    if os.path.exists(img_anubhav_vuln) and os.path.exists(img_anubhav_sec):
        story.append(Paragraph("<b>Evidence 4 (Left: Stored Script Executing with Cookie &bull; Right: Defended via HTML Escaping & CSP):</b>", body_style))
        t_anubhav_imgs = Table([
            [RLImage(img_anubhav_vuln, width=265, height=140), RLImage(img_anubhav_sec, width=265, height=140)]
        ], colWidths=[270, 270])
        story.append(t_anubhav_imgs)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # MEMBER 5: SARVANSH
    # -------------------------------------------------------------------------
    story.append(Paragraph("Member 5: Sarvansh — CSRF (POST-Based Auto-Submitting Form)", h1_style))
    story.append(Paragraph("<b>Target Variant:</b> CSRF — Variant 2 (POST-Based Forged Action via Auto-Submitting Form) &bull; <b>Time:</b> ~2.5 Minutes", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Step-by-Step Spoken Script & Actions (Video Voice-Over):</b>", h2_style))

    story.append(Paragraph("<b>ACTION 1:</b> [Screen shows <code>/csrf-post</code> with logged-in user <code>victim_alice</code> and email <code>alice@company.org</code>.]", action_style))
    story.append(Paragraph(
        "\"Hello everyone. My name is Sarvansh, and I am presenting Variant 2 of Cross-Site Request Forgery (CSRF): POST-based forged action with an auto-submitting form. "
        "CSRF exploits the ambient trust a web application places in a user's browser session.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 2:</b> [Ensure Vulnerable Mode is active. Open a new browser tab to <code>/attacker-site</code> (simulating an external phishing page).]", action_style))
    story.append(Paragraph(
        "\"Notice Alice is logged into SecureLab with email <code>alice@company.org</code>. In Vulnerable Mode, the server's update endpoint does not verify CSRF tokens. "
        "Now, Alice visits an external hostile website hosted on a simulated attacker domain—a fake prize page at <code>/attacker-site</code>. "
        "This page contains a hidden HTML form targeting SecureLab with an auto-submitting JavaScript function: <code>document.getElementById('csrfForm').submit()</code>.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 3:</b> [The hostile page auto-submits. Redirect back to <code>/csrf-post</code>. Show email changed to <code>attacker_sarvansh@hacker.io</code>.]", action_style))
    story.append(Paragraph(
        "\"Because Alice's browser has an active session, it automatically attaches her session cookies to the cross-site POST request. "
        "Look at Alice's profile now: her email has been compromised and changed to <code>attacker_sarvansh@hacker.io</code>! "
        "The root cause is that the server processed a state-changing request without proof of user intent, blindly trusting ambient cookie authentication.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 4:</b> [Toggle system to Secure Mode. Trigger the hostile attacker page again. Show HTTP 403 Forbidden.]", action_style))
    story.append(Paragraph(
        "\"To defend against this, I implemented the <b>Synchronizer Token Pattern</b> and <b>SameSite Cookies</b>. "
        "The server issues a cryptographically random, per-session <code>csrf_token</code> embedded only in legitimate forms. "
        "When the attacker's external page attempts the exact same cross-origin POST, the request is rejected with <b>HTTP 403 Forbidden: Forged CSRF Request Blocked</b>! "
        "Because of the browser's Same-Origin Policy (SOP), the hostile site cannot read Alice's token, making forgery impossible.\"",
        script_style
    ))

    story.append(Paragraph("<b>ACTION 5:</b> [Summarize lecture mitigations and conclude.]", action_style))
    story.append(Paragraph(
        "\"Other mitigations discussed in the lecture include configuring <code>SameSite=Strict</code> or <code>Lax</code> on session cookies, "
        "requiring re-authentication (current password/2FA) for sensitive actions, and avoiding state-changing GET requests. "
        "This concludes our group's video demonstration covering all four categories.\"",
        script_style
    ))

    # Screenshots for Sarvansh
    story.append(Spacer(1, 4))
    img_sarv_att = os.path.join(SCREENSHOT_DIR, "09_sarvansh_csrf_attacker_page.png")
    img_sarv_suc = os.path.join(SCREENSHOT_DIR, "10_sarvansh_csrf_exploit_success.png")
    img_sarv_blk = os.path.join(SCREENSHOT_DIR, "11_sarvansh_csrf_blocked_secure.png")
    if os.path.exists(img_sarv_att) and os.path.exists(img_sarv_suc) and os.path.exists(img_sarv_blk):
        story.append(Paragraph("<b>Evidence 5 (Attacker Hostile Page &bull; Exploit Success &bull; Blocked by Synchronizer Token):</b>", body_style))
        t_sarv_imgs = Table([
            [RLImage(img_sarv_att, width=175, height=95), RLImage(img_sarv_suc, width=175, height=95), RLImage(img_sarv_blk, width=175, height=95)]
        ], colWidths=[180, 180, 180])
        story.append(t_sarv_imgs)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # VIVA DEFENSE PREPARATION & QUESTIONS CHEAT SHEET
    # -------------------------------------------------------------------------
    story.append(Paragraph("Viva Voce Defense Guide & Expected Questions", h1_style))
    story.append(Paragraph("Be ready to answer the following questions individually during the oral viva:", body_style))
    story.append(Spacer(1, 6))

    viva_qas = [
        ("Dhruv (SQLi Auth Bypass)", 
         "Q: Why does a prepared statement physically prevent SQL injection?\n"
         "A: In a prepared statement, the database compiles the query execution blueprint before any user data is bound. Parameters are passed out-of-band and inserted strictly as literal data nodes, meaning user metacharacters (quotes, dashes) can never alter the syntax tree or logic operators."),
        
        ("Aniket (SQLi UNION Extraction)", 
         "Q: What conditions must be satisfied for a UNION-based attack to succeed?\n"
         "A: Two conditions: (1) The injected query must return the exact same number of columns as the original query (4 columns in our case). (2) The data types of each corresponding column must be compatible with the original columns."),
        
        ("Aditya (OS Command Injection)", 
         "Q: Why is shell=False safer than shell=True in Python's subprocess?\n"
         "A: shell=True passes the entire command string to cmd.exe or /bin/sh, which parses metacharacters (&&, |, ;) as command delimiters. With shell=False, Python invokes CreateProcess or execve directly with an argument vector array, so arguments cannot spawn new command processes."),
        
        ("Anubhav (Stored XSS)", 
         "Q: If HttpOnly is enabled on cookies, does that completely fix XSS?\n"
         "A: No. HttpOnly only protects session cookies from being read via document.cookie. An attacker with XSS execution can still perform arbitrary actions within the DOM, deface pages, log keystrokes, and initiate authenticated requests on behalf of the victim. Context-aware output encoding and CSP are mandatory."),
        
        ("Sarvansh (CSRF POST Auto-Submit)", 
         "Q: Why can an external attacker site not simply steal the Anti-CSRF token?\n"
         "A: Because of the browser's Same-Origin Policy (SOP). Scripts on external hostile domains (e.g. evil.com) are strictly prohibited from reading HTTP responses or DOM state from another origin (localhost:5000), unless explicitly permitted by CORS headers. Since the attacker cannot read the token, they cannot forge a valid request.")
    ]

    for member_title, qa_text in viva_qas:
        story.append(Paragraph(f"<b>{member_title}</b>", h2_style))
        for line in qa_text.split("\n"):
            if line.startswith("Q:"):
                story.append(Paragraph(f"<b>{line}</b>", body_style))
            else:
                story.append(Paragraph(f"<font color='#0f766e'>{line}</font>", body_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    print(f"[*] Successfully generated PDF document at: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
