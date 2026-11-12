"""
SecureLab - Multi-Vulnerability Web Security & Defense Demonstration Platform
Developed by: Dhruv, Aniket, Aditya, Anubhav, Sarvansh

Implements:
1. Dhruv:    SQL Injection (Variant 1: Authentication Bypass)
2. Aniket:   SQL Injection (Variant 2: UNION-Based Data Extraction)
3. Aditya:   OS Command Injection (Variant 1: In-Band Output Returned)
4. Anubhav:  Cross-Site Scripting - XSS (Variant 1: Stored XSS)
5. Sarvansh: Cross-Site Request Forgery - CSRF (Variant 2: POST-Based Auto-Submitting Form)
"""

import os
import re
import html
import secrets
import subprocess
import sqlite3
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, make_response, flash, jsonify
)
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.jinja_env.globals.update(str=str)

# Ensure database exists
if not os.path.exists(os.path.join(os.path.dirname(__file__), "securelab.db")):
    init_db()

# -----------------------------------------------------------------------------
# Global Mode Helper (Vulnerable vs. Secure)
# -----------------------------------------------------------------------------
@app.before_request
def setup_security_mode():
    # Allow overriding mode via query param (?mode=vulnerable or ?mode=secure)
    requested_mode = request.args.get("mode")
    if requested_mode in ["vulnerable", "secure"]:
        session["mode"] = requested_mode
    elif "mode" not in session:
        session["mode"] = "vulnerable"

    # Ensure CSRF token exists for the session
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)

    # Simulated logged-in victim for CSRF demo
    if "logged_in_user" not in session:
        session["logged_in_user"] = "victim_alice"
        session["user_role"] = "user"

@app.context_processor
def inject_global_vars():
    return {
        "current_mode": session.get("mode", "vulnerable"),
        "csrf_token": session.get("csrf_token"),
        "logged_in_user": session.get("logged_in_user")
    }

@app.after_request
def apply_security_headers(response):
    mode = session.get("mode", "vulnerable")
    if mode == "secure":
        # Mitigations: Strict CSP, HttpOnly Cookies, SameSite Lax/Strict
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net;"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
    else:
        # Intentionally permissive in vulnerable mode to demonstrate raw browser exploits
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# -----------------------------------------------------------------------------
# Route: Mode Toggle & Reset Database
# -----------------------------------------------------------------------------
@app.route("/toggle-mode", methods=["POST"])
def toggle_mode():
    target_mode = request.form.get("mode", "vulnerable")
    redirect_to = request.form.get("redirect_to", url_for("index"))
    session["mode"] = target_mode
    flash(f"Switched platform mode to: {target_mode.upper()}", "info")
    return redirect(redirect_to)

@app.route("/reset-db", methods=["POST"])
def reset_db():
    init_db()
    session["logged_in_user"] = "victim_alice"
    flash("Database successfully reset to initial baseline state.", "success")
    return redirect(request.referrer or url_for("index"))

# -----------------------------------------------------------------------------
# Home Dashboard
# -----------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# =============================================================================
# 1. DHRUV: SQL Injection - Variant 1 (Authentication Bypass)
# =============================================================================
@app.route("/sqli-auth", methods=["GET", "POST"])
def sqli_auth():
    mode = session.get("mode", "vulnerable")
    login_result = None
    executed_query = ""
    error_message = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        conn = get_db_connection()
        cursor = conn.cursor()

        if mode == "vulnerable":
            # --- VULNERABLE CODE PATH (Dhruv) ---
            # Flaw: User input directly concatenated/formatted into SQL statement.
            # Exploit: admin' -- or ' OR '1'='1' --
            executed_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            try:
                cursor.execute(executed_query)
                user = cursor.fetchone()
                if user:
                    login_result = {
                        "success": True,
                        "bypassed": (username.lower() != user["username"].lower() or password != user["password"]),
                        "user": dict(user)
                    }
                else:
                    error_message = "Invalid credentials. Authentication failed."
            except sqlite3.OperationalError as e:
                error_message = f"SQL Syntax Error: {e}"
            finally:
                conn.close()

        else:
            # --- MITIGATED / SECURE CODE PATH (Dhruv) ---
            # Fix: Parameterized queries with prepared statements (placeholders).
            # The database engine treats parameters strictly as literal values, never executable syntax.
            executed_query = "SELECT * FROM users WHERE username = ? AND password = ?"
            try:
                cursor.execute(executed_query, (username, password))
                user = cursor.fetchone()
                if user:
                    login_result = {
                        "success": True,
                        "bypassed": False,
                        "user": dict(user)
                    }
                else:
                    error_message = "Invalid credentials (Attack payload safely treated as literal string)."
            except Exception as e:
                # Safe generic error message preventing information disclosure
                error_message = "An authentication error occurred. Please try again."
            finally:
                conn.close()

    return render_template(
        "sqli_auth.html",
        login_result=login_result,
        executed_query=executed_query,
        error_message=error_message
    )

# =============================================================================
# 2. ANIKET: SQL Injection - Variant 2 (UNION-Based Data Extraction)
# =============================================================================
@app.route("/sqli-union", methods=["GET"])
def sqli_union():
    mode = session.get("mode", "vulnerable")
    search_query = request.args.get("q", "").strip()
    products = []
    executed_query = ""
    error_message = None
    is_union_leaked = False

    if search_query:
        conn = get_db_connection()
        cursor = conn.cursor()

        if mode == "vulnerable":
            # --- VULNERABLE CODE PATH (Aniket) ---
            # Flaw: Search term concatenated directly into SQL with matching column count.
            # Exploit: ' UNION SELECT id, username, password, role FROM users --
            executed_query = f"SELECT id, name, category, price FROM products WHERE name LIKE '%{search_query}%'"
            try:
                cursor.execute(executed_query)
                rows = cursor.fetchall()
                products = [dict(r) for r in rows]
                # Check if secret users table data leaked into product results
                for p in products:
                    if any(secret in str(p.get("category", "")).lower() for secret in ["admin", "user", "security_engineer"]) or \
                       any("password" in str(p.get("price", "")).lower() or "secret" in str(p.get("price", "")).lower() for p in products):
                        is_union_leaked = True
                        break
            except sqlite3.OperationalError as e:
                error_message = f"Database Error: {e}"
            finally:
                conn.close()

        else:
            # --- MITIGATED / SECURE CODE PATH (Aniket) ---
            # Fix: Parameterized query with parameterized wildcard bindings.
            executed_query = "SELECT id, name, category, price FROM products WHERE name LIKE ?"
            try:
                cursor.execute(executed_query, (f"%{search_query}%",))
                rows = cursor.fetchall()
                products = [dict(r) for r in rows]
            except Exception as e:
                error_message = "A search error occurred."
            finally:
                conn.close()

    return render_template(
        "sqli_union.html",
        products=products,
        search_query=search_query,
        executed_query=executed_query,
        error_message=error_message,
        is_union_leaked=is_union_leaked
    )

# =============================================================================
# 3. ADITYA: OS Command Injection - Variant 1 (In-Band Output Returned)
# =============================================================================
@app.route("/cmdi-inband", methods=["GET", "POST"])
def cmdi_inband():
    mode = session.get("mode", "vulnerable")
    command_output = None
    executed_command = ""
    error_message = None
    target_host = ""
    injection_detected = False

    if request.method == "POST":
        target_host = request.form.get("target", "").strip()

        if mode == "vulnerable":
            # --- VULNERABLE CODE PATH (Aditya) ---
            # Flaw: User input directly concatenated into shell command string with shell=True.
            # Exploit: 127.0.0.1 && whoami   or   127.0.0.1 & dir
            # Note: Works across Windows ('ping -n 1') and Linux ('ping -c 1')
            is_win = (os.name == "nt")
            ping_cmd = f"ping -n 1 {target_host}" if is_win else f"ping -c 1 {target_host}"
            executed_command = ping_cmd
            try:
                # shell=True invokes cmd.exe/sh which interprets metacharacters (&&, &, ;, |, `)
                result = subprocess.run(
                    ping_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=6
                )
                command_output = result.stdout if result.stdout else result.stderr
                if any(delim in target_host for delim in ["&", "|", ";", "`", "$"]):
                    injection_detected = True
            except subprocess.TimeoutExpired:
                command_output = "Command timed out after 6 seconds."
            except Exception as e:
                error_message = f"Execution failed: {str(e)}"

        else:
            # --- MITIGATED / SECURE CODE PATH (Aditya) ---
            # Fix 1: Strict allow-list validation (reject all non-host characters)
            # Fix 2: Avoid shell=True; use argument vector array where arguments cannot become commands
            is_win = (os.name == "nt")
            ip_hostname_regex = r"^[a-zA-Z0-9.-]+$"

            if not re.match(ip_hostname_regex, target_host):
                error_message = (
                    "SECURITY BLOCKED: Input validation failed! Only alphanumeric characters, "
                    "dots, and hyphens are permitted. Metacharacters are strictly disallowed."
                )
                executed_command = "[BLOCKED BY ALLOW-LIST VALIDATION]"
            else:
                arg_vector = ["ping", "-n", "1", target_host] if is_win else ["ping", "-c", "1", target_host]
                executed_command = " ".join(arg_vector) + " (shell=False, argument vector)"
                try:
                    result = subprocess.run(
                        arg_vector,
                        shell=False,  # Shell avoided entirely!
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    command_output = result.stdout if result.stdout else result.stderr
                except Exception as e:
                    error_message = f"Execution failed: {str(e)}"

    return render_template(
        "cmdi_inband.html",
        target_host=target_host,
        executed_command=executed_command,
        command_output=command_output,
        error_message=error_message,
        injection_detected=injection_detected
    )

# =============================================================================
# 4. ANUBHAV: Cross-Site Scripting (XSS) - Variant 1 (Stored XSS)
# =============================================================================
@app.route("/xss-stored", methods=["GET", "POST"])
def xss_stored():
    mode = session.get("mode", "vulnerable")
    message = None

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        author = request.form.get("author", "Anonymous").strip()
        comment = request.form.get("comment", "").strip()

        if comment:
            # In both modes, save to database; the vulnerability is whether the output
            # renderer escapes it or treats it as safe unescaped HTML!
            cursor.execute(
                "INSERT INTO feedback (author, comment) VALUES (?, ?)",
                (author, comment)
            )
            conn.commit()
            if mode == "vulnerable":
                message = "Feedback posted successfully (Raw Unsanitized Mode)!"
            else:
                message = "Feedback posted safely (Context-Aware Escaping Active)!"

    # Retrieve all stored feedbacks
    cursor.execute("SELECT * FROM feedback ORDER BY id DESC")
    feedbacks = [dict(r) for r in cursor.fetchall()]
    conn.close()

    resp = make_response(render_template(
        "xss_stored.html",
        feedbacks=feedbacks,
        message=message
    ))

    # In vulnerable mode: set cookie WITHOUT HttpOnly so JavaScript can read it
    # In secure mode: set cookie WITH HttpOnly so document.cookie cannot access it
    if mode == "vulnerable":
        resp.set_cookie("session_token", "SECRET_AUTH_SESSION_COOKIE_ANUBHAV_DEMO", httponly=False)
    else:
        resp.set_cookie("session_token", "SECRET_AUTH_SESSION_COOKIE_ANUBHAV_DEMO", httponly=True, samesite="Lax")

    return resp

@app.route("/xss-stored/clear", methods=["POST"])
def xss_clear():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feedback WHERE id > 2")
    conn.commit()
    conn.close()
    flash("Reset feedback comments to clean default sample.", "info")
    return redirect(url_for("xss_stored"))

# =============================================================================
# 5. SARVANSH: Cross-Site Request Forgery (CSRF) - Variant 2 (POST-Based Forged Action)
# =============================================================================
@app.route("/csrf-post", methods=["GET"])
def csrf_post():
    username = session.get("logged_in_user", "victim_alice")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return render_template("csrf_post.html", user=dict(user) if user else None)

@app.route("/csrf-post/update", methods=["POST"])
def csrf_update_email():
    mode = session.get("mode", "vulnerable")
    username = session.get("logged_in_user", "victim_alice")
    new_email = request.form.get("email", "").strip()
    new_password = request.form.get("new_password", "").strip()
    submitted_token = request.form.get("csrf_token", "")

    # Check origin/referer for demonstration purposes
    origin_header = request.headers.get("Origin") or request.headers.get("Referer") or "Unknown"

    if mode == "vulnerable":
        # --- VULNERABLE CODE PATH (Sarvansh) ---
        # Flaw: No CSRF token validation; accepts cross-site POST blindly relying solely on cookie
        if new_email or new_password:
            conn = get_db_connection()
            cursor = conn.cursor()
            if new_password:
                cursor.execute("UPDATE users SET email = ?, password = ? WHERE username = ?", (new_email, new_password, username))
            else:
                cursor.execute("UPDATE users SET email = ? WHERE username = ?", (new_email, username))
            conn.commit()
            conn.close()

            flash(f"Profile updated successfully! (Request processed from Origin: {origin_header})", "warning")
            return redirect(url_for("csrf_post", forged="true", attacker_origin=origin_header))

    else:
        # --- MITIGATED / SECURE CODE PATH (Sarvansh) ---
        # Fix 1: Synchronizer Token Pattern (validates cryptographically random per-session token)
        session_token = session.get("csrf_token")
        if not submitted_token or not secrets.compare_digest(submitted_token, session_token or ""):
            return render_template(
                "csrf_post.html",
                user={"username": username, "email": "BLOCKED", "role": "user", "balance": 0},
                csrf_blocked=True,
                origin_header=origin_header
            ), 403

        # Token is valid; proceed with update
        if new_email:
            conn = get_db_connection()
            cursor = conn.cursor()
            if new_password:
                cursor.execute("UPDATE users SET email = ?, password = ? WHERE username = ?", (new_email, new_password, username))
            else:
                cursor.execute("UPDATE users SET email = ? WHERE username = ?", (new_email, username))
            conn.commit()
            conn.close()
            flash("Profile updated securely! Anti-CSRF Token verified.", "success")
            return redirect(url_for("csrf_post"))

    return redirect(url_for("csrf_post"))

# Attacker Page (Hosted simulating malicious third-party site attacker.com)
@app.route("/attacker-site")
def attacker_site():
    return render_template("attacker/csrf_exploit.html")

# -----------------------------------------------------------------------------
# Main Application Runner
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("""
    ===============================================================
       SecureLab Security Demonstration Platform Running
       Developed for Cyber Security Web Vulnerabilities Project
       Team: Dhruv, Aniket, Aditya, Anubhav, Sarvansh
    ===============================================================
    Available at: http://127.0.0.1:5000
    """)
    app.run(host="127.0.0.1", port=5000, debug=True)
