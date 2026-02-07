import sqlite3
import random
from datetime import datetime
import jdatetime
from tkinter import messagebox
import config

DB_PATH = config.DB_PATH
DEPARTMENT_LIST = config.DEPARTMENT_LIST
DEFAULT_DEV_PASSWORD = config.DEFAULT_DEV_PASSWORD

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try: 
        cursor.execute("ALTER TABLE visitors ADD COLUMN shamsi_date TEXT;")
    except sqlite3.OperationalError: 
        pass
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT, visitor_name TEXT NOT NULL,
            national_id TEXT NOT NULL, employee_to_meet TEXT NOT NULL,
            department TEXT NOT NULL, entry_time TEXT NOT NULL,
            shamsi_date TEXT, exit_time TEXT
        )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shift_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_text TEXT NOT NULL,
            created_at TEXT NOT NULL,
            shamsi_date TEXT NOT NULL
        )''')
    conn.commit()
    conn.close()

def get_current_password():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM config WHERE key='dev_password'")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else DEFAULT_DEV_PASSWORD
    except: return DEFAULT_DEV_PASSWORD

def set_new_password(new_pass):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES ('dev_password', ?)", (new_pass,))
    conn.commit(); conn.close()

def delete_all_records():
    """Deletes ALL data from the database and resets the ID counter."""
    if not messagebox.askyesno("Danger Zone", "Are you sure you want to DELETE ALL records?\n\nThis cannot be undone!"):
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM visitors")
        
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='visitors'")
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Developer Mode", "Database has been completely cleared.")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete data: {e}")

def add_dummy_data():
    """Generates 100 random records with random Visitors AND Employees."""
    try:
        first_names = ["علی", "محمد", "رضا", "حسین", "محسن", "احمد", "مهدی", "سارا", "مریم", "زهرا", "فاطمه", "نرگس", "نیما", "کاوه", "امید", "پیمان", "سعید", "بهرام", "نازنین"]
        last_names = ["محمدی", "حسینی", "رضایی", "کریمی", "احمدی", "موسوی", "جعفری", "صادقی", "رحیمی", "عباسی", "باقری", "زاهدی", "میرزایی", "غفاری", "تهرانی", "راد"]
        
        dummy_records = []
        
        for _ in range(100):
            visitor_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            employee_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            nid = str(random.randint(1000000000, 9999999999))
            year = random.choice([1403, 1404])
            month = random.randint(1, 12)
            if month <= 6: day = random.randint(1, 31)
            elif month <= 11: day = random.randint(1, 30)
            else: day = random.randint(1, 29)
            
            shamsi_date = f"{year}/{month:02d}/{day:02d}"
            
            hour = random.randint(7, 14) 
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
            
            try:
                g_date = jdatetime.date(year, month, day).togregorian()
                entry_time_gregorian = f"{g_date.year}-{g_date.month:02d}-{g_date.day:02d} {time_str}"
            except:
                continue 
            
            dept = random.choice(DEPARTMENT_LIST)
            
            dummy_records.append({
                "visitor_name": visitor_name, 
                "national_id": nid, 
                "employee_to_meet": employee_name, 
                "department": dept, 
                "entry_time": entry_time_gregorian, 
                "shamsi_date": shamsi_date
            })
            
        dummy_records.sort(key=lambda x: x['entry_time'])
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for r in dummy_records:
            cursor.execute('''
                INSERT INTO visitors (visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (r['visitor_name'], r['national_id'], r['employee_to_meet'], r['department'], r['entry_time'], r['shamsi_date']))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Developer Mode", "100 Random Records (Full Data) Added Successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate data: {e}")