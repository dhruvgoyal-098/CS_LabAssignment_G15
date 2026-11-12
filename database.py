"""
SecureLab Database Management
Initializes SQLite database with sample data for vulnerability demonstrations.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "securelab.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop existing tables to start fresh
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS feedback")

    # 1. Users Table (used for SQLi Auth Bypass and CSRF victim)
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            balance REAL DEFAULT 1000.0
        )
    """)

    # Populate users: plain text passwords for vulnerable demo, but also demonstrating secure hashing
    users_data = [
        ("admin", "AdminSuperSecret2026!", "admin@securelab.local", "administrator", 99999.0),
        ("victim_alice", "password123", "alice@company.org", "user", 1500.0),
        ("dhruv", "dhruvPass2026", "dhruv@securelab.local", "security_engineer", 2500.0),
        ("aniket", "aniketPass2026", "aniket@securelab.local", "security_engineer", 2500.0),
        ("aditya", "adityaPass2026", "aditya@securelab.local", "security_engineer", 2500.0),
        ("anubhav", "anubhavPass2026", "anubhav@securelab.local", "security_engineer", 2500.0),
        ("sarvansh", "sarvanshPass2026", "sarvansh@securelab.local", "security_engineer", 2500.0)
    ]
    cursor.executemany(
        "INSERT INTO users (username, password, email, role, balance) VALUES (?, ?, ?, ?, ?)",
        users_data
    )

    # 2. Products Table (used for SQLi UNION extraction demo)
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    products_data = [
        ("Firewall Appliance X1", "Network Security", 1299.99, 15),
        ("Hardware Security Key Y2", "Authentication", 49.99, 120),
        ("Encrypted USB Drive 128GB", "Storage", 79.99, 45),
        ("Security Camera Pro HD", "Surveillance", 199.99, 30),
        ("Managed VPN Router V4", "Networking", 349.99, 25),
        ("Biometric Access Scanner", "Physical Security", 499.99, 10)
    ]
    cursor.executemany(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        products_data
    )

    # 3. Feedback Table (used for Stored XSS)
    cursor.execute("""
        CREATE TABLE feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    feedback_data = [
        ("John Doe", "Great products and reliable delivery!"),
        ("Sarah Connor", "Customer support answered my questions promptly.")
    ]
    cursor.executemany(
        "INSERT INTO feedback (author, comment) VALUES (?, ?)",
        feedback_data
    )

    conn.commit()
    conn.close()
    print("[*] Database initialized successfully at:", DB_PATH)

if __name__ == "__main__":
    init_db()
