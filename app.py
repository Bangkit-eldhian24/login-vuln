from flask import Flask, render_template, request, redirect, url_for, session, make_response
import sqlite3
import os
import html

app = Flask(__name__)
app.secret_key = 'dev-key-do-not-use-in-production'

# Configuration - CHANGE THIS TO SWITCH BETWEEN MODES
MODE = "vulnerable"  # Change to "secure" for protected version

# Database configuration
DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Context processor to make MODE available to all templates
@app.context_processor
def inject_mode():
    return {'mode': MODE}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Basic validation
        if not password:
            error = "Password required!"
            return render_template('login.html', error=error)
        
        try:
            if MODE == "vulnerable":
                # VULNERABLE: SQL Injection through string interpolation
                conn = get_db_connection()
                # Clean the inputs slightly to avoid immediate syntax errors
                clean_username = username.replace('"', '').replace("'", "''")
                clean_password = password.replace('"', '').replace("'", "''")
                query = f"SELECT * FROM users WHERE username = '{clean_username}' AND password = '{clean_password}'"
                print(f"[VULNERABLE] Executing query: {query}")  # Debug output
                user = conn.execute(query).fetchone()
                conn.close()
            else:
                # SECURE: Parameterized queries
                conn = get_db_connection()
                user = conn.execute(
                    'SELECT * FROM users WHERE username = ? AND password = ?',
                    (username, password)
                ).fetchone()
                conn.close()
            
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['logged_in'] = True
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid username or password."
                
        except sqlite3.OperationalError as e:
            error = f"Database error: {str(e)}"
            print(f"SQL Error: {e}")
        except Exception as e:
            error = f"An error occurred: {str(e)}"
            print(f"General Error: {e}")
    
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Reflected XSS vulnerability in vulnerable mode only
    message = request.args.get('msg', '')
    
    if MODE == "vulnerable":
        # VULNERABLE: No output escaping - reflected XSS
        display_message = message if message else f"Welcome, {session['username']}!"
    else:
        # SECURE: Proper output escaping
        display_message = html.escape(message) if message else f"Welcome, {html.escape(session['username'])}!"
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         message=display_message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print(f"🚨 RUNNING IN {MODE.upper()} MODE - DO NOT DEPLOY TO INTERNET 🚨")
    print("📱 Access the application at: http://localhost:5000")
    print("🔒 Test accounts: admin/password123, alice/alicepass, etc.")
    app.run(host='0.0.0.0', port=5000, debug=True)