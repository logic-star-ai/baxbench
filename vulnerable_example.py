"""
Vulnerable code example for PR review practice.
This code contains multiple security vulnerabilities.
"""

import os
import pickle
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Vulnerability 1: Hardcoded credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk_live_1234567890abcdef"

# Vulnerability 2: SQL Injection
@app.route('/user/<username>')
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Direct string concatenation - SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    return str(result)

# Vulnerability 3: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host')
    # Unsanitized user input in shell command
    result = os.system(f"ping -c 4 {host}")
    return f"Ping result: {result}"

# Vulnerability 4: Path Traversal
@app.route('/download')
def download_file():
    filename = request.args.get('file')
    # No validation - allows directory traversal
    with open(f"/var/uploads/{filename}", 'rb') as f:
        return f.read()

# Vulnerability 5: Insecure Deserialization
@app.route('/load_session', methods=['POST'])
def load_session():
    session_data = request.data
    # Pickle deserialization of untrusted data
    session = pickle.loads(session_data)
    return f"Session loaded: {session}"

# Vulnerability 6: Server-Side Template Injection (SSTI)
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    # Direct template rendering with user input
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)

# Vulnerability 7: Weak Cryptography
def encrypt_password(password):
    # Using deprecated MD5 for password hashing
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()

# Vulnerability 8: Missing Authentication
@app.route('/admin/delete_user/<user_id>')
def delete_user(user_id):
    # No authentication check
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    return "User deleted"

# Vulnerability 9: Information Disclosure
@app.route('/error')
def trigger_error():
    try:
        result = 1 / 0
    except Exception as e:
        # Exposing stack traces to users
        return f"Error: {e}\n{e.__traceback__}"

# Vulnerability 10: Insecure Direct Object Reference (IDOR)
@app.route('/account/<account_id>')
def view_account(account_id):
    # No authorization check - any user can view any account
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM accounts WHERE id = {account_id}")
    return str(cursor.fetchone())

if __name__ == '__main__':
    # Vulnerability 11: Debug mode in production
    app.run(debug=True, host='0.0.0.0')
