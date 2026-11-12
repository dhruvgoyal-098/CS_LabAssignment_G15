"""
SecureLab Entry Point Runner
Usage:
    python run.py
"""

from app import app
from database import init_db
import os

if __name__ == "__main__":
    db_file = os.path.join(os.path.dirname(__file__), "securelab.db")
    if not os.path.exists(db_file):
        print("[*] Initializing SecureLab database with baseline seed data...")
        init_db()

    print("=" * 70)
    print("      SECURELAB - WEB VULNERABILITIES & DEFENSE PLATFORM")
    print("   Developed for Cyber Security Lab Demonstration & Viva")
    print("   Team: Dhruv, Aniket, Aditya, Anubhav, Sarvansh")
    print("=" * 70)
    print(">> Open your browser at: http://127.0.0.1:5000")
    print(">> Press Ctrl+C to terminate the server.\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
