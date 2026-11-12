# SecureLab: Web Server Vulnerabilities & Defense Demonstration Platform

A comprehensive security laboratory demonstrating and defending against four major web application vulnerability categories covered in class: **SQL Injection (SQLi)**, **OS Command Injection (CmdI)**, **Cross-Site Scripting (XSS)**, and **Cross-Site Request Forgery (CSRF)**.

Each variant is fully implemented with toggleable **Vulnerable Mode** and **Secure (Mitigated) Mode**, supported by automated test suites, visual evidence screenshots, and an interactive dark-themed dashboard.

---

## Table 3: Ownership Declaration

*As required by Course Specification Table 3 (for a 5-member team covering all 4 categories):*

| # | Member Name | Roll Number | Vulnerability Category | Variant Implemented | Target Endpoint |
|---|-------------|-------------|------------------------|---------------------|-----------------|
| 1 | **Dhruv** | `[Enter Dhruv's Roll No.]` | SQL Injection | **Variant 1:** Authentication bypass | `POST /sqli-auth` |
| 2 | **Aniket** | `[Enter Aniket's Roll No.]` | SQL Injection | **Variant 2:** UNION-based data extraction | `GET /sqli-union` |
| 3 | **Aditya** | `[Enter Aditya's Roll No.]` | OS Command Injection | **Variant 1:** In-band (command output returned) | `POST /cmdi-inband` |
| 4 | **Anubhav** | `[Enter Anubhav's Roll No.]` | Cross-Site Scripting (XSS) | **Variant 1:** Stored XSS | `POST /xss-stored` |
| 5 | **Sarvansh** | `[Enter Sarvansh's Roll No.]` | Cross-Site Request Forgery (CSRF) | **Variant 2:** POST-based forged action (auto-submitting form) | `POST /csrf-post/update` |

---

## Quick Start & Running the Project

### Prerequisites
- Python 3.8+ installed (Python 3.10+ recommended)
- Google Chrome, Microsoft Edge, or Firefox browser

### Setup Instructions
1. **Clone or Navigate to the Repository:**
   ```bash
   cd CS
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Web Application:**
   ```bash
   python run.py
   ```
   The platform will be live at: **`http://127.0.0.1:5000`**

4. **Run the Automated Exploitation & Defense Verification Test Suite:**
   ```bash
   python scripts/test_exploits.py
   ```
   *(Runs 10 automated unit tests confirming exploits work in vulnerable mode and are blocked in secure mode).*

5. **Re-generate Visual Evidence Screenshots (Optional):**
   ```bash
   python scripts/generate_screenshots.py
   ```

---

## Detailed Variant Documentation (Table 2 Compliance)

---

### Member 1: Dhruv
- **Category:** SQL Injection
- **Variant:** Variant 1 — Authentication Bypass
- **Target Endpoint:** `POST /sqli-auth`

#### (a) Vulnerable Implementation
In `app.py` within `sqli_auth()`:
```python
# String concatenation formats raw user input directly into SQL syntax
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
user = cursor.fetchone()
```

#### (b) Working Exploit
- **Payload:** `admin' --` (in the username field, with any password)
- **Resulting Server Query:**
  ```sql
  SELECT * FROM users WHERE username = 'admin' --' AND password = '...'
  ```
- **Execution Mechanism:** The single quote (`'`) breaks out of the username data field. The SQLite comment sequence (`--`) comments out the remainder of the query, completely eliminating password verification and logging in as the administrator without knowing the password.
- **Evidence Screenshots:**
  - Exploit Working (Vulnerable): [`static/screenshots/01_dhruv_sqli_auth_vulnerable.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/01_dhruv_sqli_auth_vulnerable.png)
  - Attack Blocked (Mitigated): [`static/screenshots/02_dhruv_sqli_auth_secure.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/02_dhruv_sqli_auth_secure.png)

#### (c) Root Cause
**Lack of separation between control and data:** Untrusted user input is directly concatenated into the SQL command buffer. The database engine cannot differentiate between developer-intended SQL control syntax and user-supplied data, allowing input characters to alter the syntactic structure of the query.

#### (d) Mitigation Implemented
**Parameterized Queries (Prepared Statements):**
```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```
- **Why it works:** The database engine compiles the query blueprint upfront. When the attacker inputs `admin' --`, the engine binds the entire string literally to the `username` field. The single quote and dashes have zero syntactic meaning, so authentication cleanly fails with `Invalid credentials`.

#### (e) Other Mitigations (Theory)
- **Input validation with allow-lists:** Reject any input containing quotes, semicolons, or dashes using strict regex (e.g. `^[a-zA-Z0-9_]{3,30}$`).
- **Least-privilege database accounts:** Grant the web application connection only the minimal necessary privileges (e.g., read-only access to specific tables).
- **Safe generic errors:** Suppress database engine error messages to prevent error-based SQLi reconnaissance.
- **Password hashing:** Comparing salted hashes (bcrypt/Argon2) prevents direct plain-text password query comparisons.

---

### Member 2: Aniket
- **Category:** SQL Injection
- **Variant:** Variant 2 — UNION-Based Data Extraction
- **Target Endpoint:** `GET /sqli-union`

#### (a) Vulnerable Implementation
In `app.py` within `sqli_union()`:
```python
# Search term concatenated directly into LIKE clause
query_str = f"SELECT id, name, category, price FROM products WHERE name LIKE '%{search_query}%'"
cursor.execute(query_str)
```

#### (b) Working Exploit
- **Payload:** `' UNION SELECT id, username, password, role FROM users --`
- **Resulting Server Query:**
  ```sql
  SELECT id, name, category, price FROM products WHERE name LIKE '%' UNION SELECT id, username, password, role FROM users --%'
  ```
- **Execution Mechanism:** The single quote breaks out of the `LIKE` pattern. The `UNION` operator appends results from the sensitive `users` table (which has matching 4 columns) into the public product search result table, exposing all credentials and roles to the attacker.
- **Evidence Screenshots:**
  - Exploit Working (Vulnerable): [`static/screenshots/03_aniket_sqli_union_vulnerable.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/03_aniket_sqli_union_vulnerable.png)
  - Attack Blocked (Mitigated): [`static/screenshots/04_aniket_sqli_union_secure.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/04_aniket_sqli_union_secure.png)

#### (c) Root Cause
**Unsanitized SQL concatenation in read queries:** The query permits external injection of additional `SELECT` queries via set operators (`UNION`). The application renders the merged result set directly into the client response without schema partitioning.

#### (d) Mitigation Implemented
**Parameterized Wildcard Binding:**
```python
query_str = "SELECT id, name, category, price FROM products WHERE name LIKE ?"
cursor.execute(query_str, (f"%{search_query}%",))
```
- **Why it works:** The placeholder `?` treats the entire attacker payload as literal search text inside the wildcard. No secondary SQL query can be injected.

#### (e) Other Mitigations (Theory)
- **Input allow-list validation:** Enforce alphanumeric constraints on search keywords.
- **Least-privilege permissions:** Web application database user must not have read (`SELECT`) privileges on internal administrative tables like `users`.
- **Object-Relational Mapping (ORM):** Standardize database access through ORMs (e.g. SQLAlchemy) that enforce parameterization natively.
- **Column count & error hardening:** Suppress error stack traces that assist attackers in matching column counts during reconnaissance.

---

### Member 3: Aditya
- **Category:** OS Command Injection
- **Variant:** Variant 1 — In-Band (Command Output Returned)
- **Target Endpoint:** `POST /cmdi-inband`

#### (a) Vulnerable Implementation
In `app.py` within `cmdi_inband()`:
```python
# Spawns a system shell with unsanitized user input
ping_cmd = f"ping -n 1 {target_host}"
result = subprocess.run(ping_cmd, shell=True, capture_output=True, text=True)
command_output = result.stdout  # Directly returned to the user interface
```

#### (b) Working Exploit
- **Payload:** `127.0.0.1 && whoami` (or `127.0.0.1 & dir`)
- **Execution Mechanism:** The shell command separator `&&` instructs `cmd.exe` / `/bin/sh` to run the `ping` utility first, followed immediately by the injected command (`whoami`). The application captures `stdout` and prints it directly in the web UI (**in-band**).
- **Evidence Screenshots:**
  - Exploit Working (Vulnerable): [`static/screenshots/05_aditya_cmdi_inband_vulnerable.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/05_aditya_cmdi_inband_vulnerable.png)
  - Attack Blocked (Mitigated): [`static/screenshots/06_aditya_cmdi_inband_secure.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/06_aditya_cmdi_inband_secure.png)

#### (c) Root Cause
**Passing unsanitized input to an interactive system command interpreter (`shell=True`):** The underlying shell evaluates metacharacters (`&&`, `&`, `;`, `|`, `` ` ``) as control delimiters rather than raw argument strings.

#### (d) Mitigation Implemented
**Dual Defense: Regex Allow-list Validation + Parameterized Execution (shell=False):**
```python
# 1. Strict regex allow-list
if not re.match(r"^[a-zA-Z0-9.-]+$", target_host):
    raise ValueError("Invalid target format: Only alphanumeric characters, dots, and hyphens permitted.")

# 2. Avoid the shell; execute binary directly with argument vector
arg_vector = ["ping", "-n", "1", target_host]
result = subprocess.run(arg_vector, shell=False, capture_output=True, text=True)
```
- **Why it works:** Metacharacters are rejected by input validation. Even if an argument is passed, `shell=False` passes arguments directly to the OS kernel `CreateProcess` / `execve` system call without invoking an intermediary command interpreter.

#### (e) Other Mitigations (Theory)
- **Avoid invoking the shell:** Use native platform APIs (e.g. Python's `socket` library or ICMP ping modules) instead of spawning OS subprocesses.
- **Least privilege:** Run the web application under a locked-down service account with no access to administrative tools (`cmd.exe`, `powershell.exe`, `sh`).
- **Containerization & sandboxing:** Execute application workers inside read-only chroot jails or isolated Docker containers.

---

### Member 4: Anubhav
- **Category:** Cross-Site Scripting (XSS)
- **Variant:** Variant 1 — Stored XSS
- **Target Endpoint:** `POST /xss-stored`

#### (a) Vulnerable Implementation
In `templates/xss_stored.html`:
```html
<!-- Untrusted user-submitted comment rendered with raw unescaped | safe filter -->
<div class="comment-content">
  {{ item.comment | safe }}
</div>
```

#### (b) Working Exploit
- **Payload:** `<script>alert('Stored XSS Executed by Anubhav! Stolen Cookie: ' + document.cookie);</script>`
- **Execution Mechanism:** The attacker posts the malicious script into the feedback board. It is permanently stored in the SQLite database. Whenever any user or administrator visits or refreshes the page, the browser parses and executes the JavaScript payload in the context of the victim's session, enabling session hijacking and DOM manipulation.
- **Evidence Screenshots:**
  - Exploit Working (Vulnerable): [`static/screenshots/07_anubhav_xss_stored_vulnerable.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/07_anubhav_xss_stored_vulnerable.png)
  - Attack Blocked (Mitigated): [`static/screenshots/08_anubhav_xss_stored_secure.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/08_anubhav_xss_stored_secure.png)

#### (c) Root Cause
**Rendering untrusted database content without context-aware output encoding:** The browser cannot differentiate between legitimate scripts written by the application author and malicious scripts injected into HTML response bodies by third parties.

#### (d) Mitigation Implemented
**Context-Aware Output Encoding + Content Security Policy (CSP) + HttpOnly Cookies:**
```html
<!-- Jinja2 default context-aware auto-escaping (removing | safe) -->
<div class="comment-content">
  {{ item.comment }}
</div>
```
```python
# Content Security Policy HTTP Response Header
response.headers["Content-Security-Policy"] = (
    "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net;"
)
# Cookie security
resp.set_cookie("session_token", "...", httponly=True, samesite="Lax")
```
- **Why it works:** Special characters (`<`, `>`, `&`, `"`, `'`) are automatically converted into harmless HTML entities (`&lt;`, `&gt;`). The browser displays them as visible text without interpreting them as markup. In addition, `HttpOnly` blocks JavaScript from accessing session cookies via `document.cookie`.

#### (e) Other Mitigations (Theory)
- **Content Security Policy (CSP):** Disallowing inline scripts (`unsafe-inline`) prevents malicious script blocks from running even if injected.
- **HTML Sanitizers:** For rich-text fields (WYSIWYG editors), sanitize inputs using DOMPurify or Python `bleach` to strip malicious tags.
- **Safe DOM Sinks:** Use `textContent` instead of dangerous sinks like `innerHTML` or `eval()`.

---

### Member 5: Sarvansh
- **Category:** Cross-Site Request Forgery (CSRF)
- **Variant:** Variant 2 — POST-Based Forged Action (Auto-Submitting Form)
- **Target Endpoint:** `POST /csrf-post/update`

#### (a) Vulnerable Implementation
In `app.py` within `csrf_update_email()`:
```python
# State-changing endpoint accepts POST requests relying solely on session cookie
new_email = request.form.get("email")
cursor.execute("UPDATE users SET email = ? WHERE username = ?", (new_email, username))
conn.commit()
```

#### (b) Working Exploit
- **Attacker Hostile Page (`templates/attacker/csrf_exploit.html`):**
  ```html
  <form id="csrfForm" action="http://localhost:5000/csrf-post/update" method="POST">
    <input type="hidden" name="email" value="attacker_sarvansh@hacker.io">
    <input type="hidden" name="new_password" value="hackedPassword2026!">
  </form>
  <script>
    // Auto-submits immediately behind the victim's back!
    document.getElementById('csrfForm').submit();
  </script>
  ```
- **Execution Mechanism:** The victim logs into SecureLab. An attacker lures the victim to `http://localhost:5000/attacker-site`. The hostile page contains a hidden form that auto-submits via JavaScript. The victim's browser automatically attaches ambient session cookies to the cross-origin request. Without a CSRF token, the server accepts the forged request and changes the victim's email/password without their consent.
- **Evidence Screenshots:**
  - Simulated Attacker Site: [`static/screenshots/09_sarvansh_csrf_attacker_page.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/09_sarvansh_csrf_attacker_page.png)
  - Exploit Working (Vulnerable): [`static/screenshots/10_sarvansh_csrf_exploit_success.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/10_sarvansh_csrf_exploit_success.png)
  - Attack Blocked (Mitigated): [`static/screenshots/11_sarvansh_csrf_blocked_secure.png`](file:///c:/Users/Dhruv%20Goyal/Downloads/CS/static/screenshots/11_sarvansh_csrf_blocked_secure.png)

#### (c) Root Cause
**State-changing request processed without proof of user intent:** Web browsers automatically include ambient credentials (cookies) in cross-site requests. Without an anti-CSRF token or `SameSite` cookie restrictions, the server cannot distinguish between legitimate user actions and unauthorized requests forged by hostile domains.

#### (d) Mitigation Implemented
**Synchronizer Token Pattern & SameSite Cookie Enforcement:**
```python
# Server validates cryptographically random per-session token
session_token = session.get("csrf_token")
submitted_token = request.form.get("csrf_token")

if not submitted_token or not secrets.compare_digest(submitted_token, session_token or ""):
    return "CSRF Attack Blocked: Invalid Token", 403
```
- **Why it works:** The server generates a unique, unpredictable token stored in the session. Legitimate forms include this token in a hidden field. Because of the browser's **Same-Origin Policy (SOP)**, external attacker pages cannot read the token and therefore cannot forge a valid request. Forged submissions are rejected with **HTTP 403 Forbidden**.

#### (e) Other Mitigations (Theory)
- **SameSite Cookie Attribute:** Setting `SameSite=Strict` or `SameSite=Lax` instructs browsers not to attach session cookies to cross-site requests.
- **Re-authentication for sensitive actions:** Prompt for the current password or a 2FA code before executing critical changes (password, email, or financial transfers).
- **Avoid state-changing GET requests:** Ensure GET requests are strictly idempotent.
- **Origin / Referer header validation:** Verify that the request's `Origin` matches the target server domain.

---

## Video Demonstration Script (2–3 Minutes Per Member)

When recording the group video demonstration, follow this standardized flow:

1. **Dhruv (SQLi Auth Bypass):**
   - Show Table 3 in the dashboard.
   - Switch mode to **Vulnerable**. Enter `admin' --` in the username field. Click Login. Show the red banner: *"EXPLOIT SUCCESSFUL! Bypassed as Administrator"*.
   - Click the mode toggle to switch to **Secure**. Enter the exact same payload `admin' --`. Click Login. Show that the login fails with *"Invalid credentials"*. Explain prepared statements.

2. **Aniket (SQLi UNION Extraction):**
   - Navigate to `/sqli-union`.
   - In **Vulnerable** mode, enter `' UNION SELECT id, username, password, role FROM users --`. Click Search. Show the sensitive user passwords and roles leaking into the public product table.
   - Switch to **Secure** mode. Run the exact same query. Show that zero records are leaked. Explain parameterized wildcard queries.

3. **Aditya (In-Band OS Command Injection):**
   - Navigate to `/cmdi-inband`.
   - In **Vulnerable** mode, enter `127.0.0.1 && whoami`. Click Ping. Show the terminal output returning `whoami` stdout in-band.
   - Switch to **Secure** mode. Enter the exact same payload. Show the red security banner: *"SECURITY BLOCKED: Input validation failed!"*. Explain regex allow-listing and `shell=False` argument vectors.

4. **Anubhav (Stored XSS):**
   - Navigate to `/xss-stored`.
   - In **Vulnerable** mode, enter `<script>alert('Stored XSS - Cookie: ' + document.cookie);</script>`. Submit the comment. Refresh the page to show the JavaScript alert executing and displaying the cookie.
   - Switch to **Secure** mode. Show that the comment is rendered safely as `&lt;script&gt;` text, with `HttpOnly` and CSP headers active.

5. **Sarvansh (CSRF POST Auto-Submitting Form):**
   - Navigate to `/csrf-post`. Show victim profile (`victim_alice` with legitimate email).
   - In **Vulnerable** mode, open the hostile attacker page at `/attacker-site`. Show the form auto-submitting. Redirect back to profile to show the email changed to `attacker_sarvansh@hacker.io`.
   - Switch to **Secure** mode. Re-trigger the attacker page. Show that the server rejects the request with **HTTP 403 Forbidden** due to the missing Anti-CSRF Synchronizer Token.

---

## Viva Preparation Guide (Questions & Answers)

### General Questions
- **Q: Why does the web server need both input validation and output encoding?**
  - **A:** Input validation (allow-lists) ensures data conforms to expected formats before processing (preventing injection into queries and commands). Output encoding ensures that when data is rendered back to the user, the browser interprets it as data, not executable markup (preventing XSS).

### SQL Injection (Dhruv & Aniket)
- **Q: How does a prepared statement physically prevent SQL injection?**
  - **A:** In a prepared statement, the database parser compiles the query execution tree *before* parameter values are supplied. The parameters are transmitted out-of-band and inserted strictly as literal data nodes into the pre-compiled execution plan, meaning input metacharacters can never alter the syntax or logic tree.
- **Q: What is the difference between In-band, Blind, and Out-of-band SQLi?**
  - **A:** In-band (e.g. UNION-based or error-based) returns extracted data directly through the application's normal HTTP response channel. Blind SQLi (boolean or time-based) extracts data bit-by-bit by observing server true/false responses or induced sleep delays. Out-of-band SQLi extracts data via an alternate protocol (e.g. DNS or HTTP lookups to an external attacker-controlled server).

### OS Command Injection (Aditya)
- **Q: Why is `shell=False` safer than `shell=True` in Python's subprocess?**
  - **A:** With `shell=True`, the Python process passes the command string to an operating system shell (`cmd.exe` or `/bin/sh`), which parses and interprets shell metacharacters (`&&`, `|`, `;`). With `shell=False`, arguments are passed directly as an array (argument vector) to the OS process creation API without invoking a command interpreter, preventing metacharacters from spawning new commands.

### Cross-Site Scripting (Anubhav)
- **Q: Why is the `HttpOnly` flag not a complete fix for XSS?**
  - **A:** `HttpOnly` prevents client-side scripts from reading the `document.cookie` property, defending against cookie theft. However, an attacker with XSS execution can still perform actions on behalf of the user (DOM manipulation, keylogging, initiating authenticated AJAX requests, or defacing the interface). Output encoding and CSP remain mandatory.

### Cross-Site Request Forgery (Sarvansh)
- **Q: Why can an attacker not just read the Anti-CSRF token from the victim's session?**
  - **A:** Because of the browser's **Same-Origin Policy (SOP)**. A script running on `attacker.com` cannot read the HTML or JavaScript state of pages on `localhost:5000` unless explicit cross-origin resource sharing (CORS) permissions are granted. Therefore, the attacker cannot steal the synchronizer token to embed it in their forged request.

---

## Project Structure

```
c:\Users\Dhruv Goyal\Downloads\CS/
├── app.py                     # Main Flask application with vulnerable & secure routes
├── database.py                # Database initialisation, migrations, and seed data
├── run.py                     # Main runner entrypoint
├── requirements.txt           # Python library dependencies
├── README.md                  # Complete project documentation, Table 3, and viva guide
├── scripts/
│   ├── test_exploits.py       # Automated unit test suite verifying all 10 states
│   ├── generate_screenshots.py # Script generating 12 high-resolution UI evidence screenshots
│   └── capture_screenshots.py # Headless browser screenshot capture utility
├── static/
│   ├── css/
│   │   └── style.css          # Dark cyber-security theme
│   └── screenshots/           # Evidence screenshots (Table 3, Vulnerable, Secure)
│       ├── 00_securelab_dashboard.png
│       ├── 01_dhruv_sqli_auth_vulnerable.png
│       ├── 02_dhruv_sqli_auth_secure.png
│       ├── 03_aniket_sqli_union_vulnerable.png
│       ├── 04_aniket_sqli_union_secure.png
│       ├── 05_aditya_cmdi_inband_vulnerable.png
│       ├── 06_aditya_cmdi_inband_secure.png
│       ├── 07_anubhav_xss_stored_vulnerable.png
│       ├── 08_anubhav_xss_stored_secure.png
│       ├── 09_sarvansh_csrf_attacker_page.png
│       ├── 10_sarvansh_csrf_exploit_success.png
│       └── 11_sarvansh_csrf_blocked_secure.png
└── templates/
    ├── base.html              # Layout, navbar, and security mode toggle
    ├── index.html             # Table 3 declaration, architecture, and module cards
    ├── sqli_auth.html         # Dhruv's module (SQLi Auth Bypass)
    ├── sqli_union.html        # Aniket's module (SQLi UNION Extraction)
    ├── cmdi_inband.html       # Aditya's module (In-Band OS Command Injection)
    ├── xss_stored.html        # Anubhav's module (Stored XSS)
    ├── csrf_post.html         # Sarvansh's module (POST CSRF)
    └── attacker/
        └── csrf_exploit.html  # Simulated hostile third-party attacker domain
```
