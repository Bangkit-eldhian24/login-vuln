import sqlite3
import os

def init_db():
    # Remove existing database if any
    if os.path.exists('users.db'):
        os.remove('users.db')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Insert clean test accounts - NO PAYLOADS
    users = [
        ('admin', 'password123'),
        ('alice', 'alicepass'),
        ('bob', 'bobpass'),
        ('charlie', 'charlie123'),
        ('diana', 'diana456')
    ]
    
    cursor.executemany(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        users
    )
    
    conn.commit()
    conn.close()
    
    print("Database initialized with 5 test accounts:")
    for username, password in users:
        print(f"  {username} / {password}")

if __name__ == '__main__':
    init_db()