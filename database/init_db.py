# I will create the database tavle here.

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'tickets.db')

# function to create table.

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'staff', 'admin'))
    );
    ''')  

    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        staff_id INTEGER,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        category TEXT NOT NULL,
        attachments TEXT,
        priority TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (staff_id) REFERENCES users(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS it_staff (
        id INTEGER PRIMARY KEY,
        staff_role TEXT,
        FOREIGN KEY (id) REFERENCES users(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES users(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_name TEXT NOT NULL,
        serial_number TEXT UNIQUE NOT NULL,
        location TEXT NOT NULL,
        date_purchased TEXT NOT NULL,
        assigned_to INTEGER,
        FOREIGN KEY (assigned_to) REFERENCES users(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ticket_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL,
        message_read INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (ticket_id) REFERENCES tickets(id)
    );
        
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS assets_issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        asset_name TEXT NOT NULL,
        issue_description TEXT NOT NULL,
        serial_number TEXT NOT NULL,
        created_at TEXT NOT NULL,
        location TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    
    );
    ''')