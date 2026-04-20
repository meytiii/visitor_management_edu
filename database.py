import sqlite3
import random
import hashlib
import binascii
import os
import threading
import time
from datetime import datetime
import jdatetime
from tkinter import messagebox
import config

DB_PATH = config.DB_PATH
DEPARTMENT_LIST = config.DEPARTMENT_LIST

# --- CACHE CONFIGURATION ---
_cache = {
    "employees": {
        "data": [], 
        "timestamp": 0
    }
}
CACHE_DURATION = 300

# --- CONNECTION POOLING SETUP ---
_thread_local = threading.local()

def _get_connection():
    if not hasattr(_thread_local, "connection"):
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
        except: pass
        _thread_local.connection = conn
    return _thread_local.connection

class DBConnection:
    def __enter__(self):
        self.conn = _get_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

# --- HASHING UTILS ---
def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    try:
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    except:
        return False

# --- DATABASE SETUP ---
def setup_database():
    with DBConnection() as conn:
        cursor = conn.cursor()
        
        try: cursor.execute("ALTER TABLE visitors ADD COLUMN shamsi_date TEXT;")
        except sqlite3.OperationalError: pass
        
        try: cursor.execute("ALTER TABLE visitors ADD COLUMN created_by TEXT;")
        except sqlite3.OperationalError: pass
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT, visitor_name TEXT NOT NULL,
                national_id TEXT NOT NULL, employee_to_meet TEXT NOT NULL,
                department TEXT NOT NULL, entry_time TEXT NOT NULL,
                shamsi_date TEXT, exit_time TEXT,
                created_by TEXT
            )''')
        
        # Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_national_id ON visitors (national_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_shamsi_date ON visitors (shamsi_date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_visitor_name ON visitors (visitor_name);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_employee ON visitors (employee_to_meet);")
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT
            )''')
        
        try: cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT;")
        except sqlite3.OperationalError: pass
        
        cursor.execute("SELECT count(*) FROM users WHERE role='admin'")
        if cursor.fetchone()[0] == 0:
            default_pass = hash_password("admin")
            cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)", 
                           ("admin", default_pass, "admin", "مدیر سیستم"))
            print("Default Admin created")

# --- CACHED DATA FETCHING ---
def get_employee_suggestions(force_refresh=False):
    """
    Fetches employee names sorted by popularity.
    Uses memory caching to avoid hitting the DB too often.
    """
    global _cache
    now = time.time()
    
    if not force_refresh and (now - _cache["employees"]["timestamp"] < CACHE_DURATION):
        return _cache["employees"]["data"]

    try:
        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT employee_to_meet, COUNT(*) as cnt 
                FROM visitors 
                WHERE employee_to_meet != '' 
                GROUP BY employee_to_meet 
                ORDER BY cnt DESC
            ''')
            names = [row[0] for row in cursor.fetchall()]
            
            _cache["employees"]["data"] = names
            _cache["employees"]["timestamp"] = now
            return names
    except:
        return []

# --- USER MANAGEMENT ---
def authenticate_user(username, password):
    with DBConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password, role, full_name FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        
        if row:
            stored_hash, role, full_name_db = row
            full_name = full_name_db if full_name_db else username
            
            if verify_password(stored_hash, password):
                return True, role, full_name
                
    return False, None, None

def create_user(username, password, full_name, role="guard"):
    try:
        hashed = hash_password(password)
        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)", 
                           (username, hashed, role, full_name))
        return True, ""
    except sqlite3.IntegrityError:
        return False, "نام کاربری تکراری است"
    except Exception as e:
        return False, str(e)

def delete_user(username):
    with DBConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=?", (username,))
        target_role = cursor.fetchone()
        
        if target_role and target_role[0] == 'admin':
            cursor.execute("SELECT count(*) FROM users WHERE role='admin'")
            if cursor.fetchone()[0] <= 1:
                return False, "نمی‌توان آخرین مدیر سیستم را حذف کرد"
                
        try:
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            return True, ""
        except Exception as e:
            return False, str(e)

def get_all_users():
    with DBConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, role, full_name FROM users")
        return cursor.fetchall()

def change_user_password(username, new_password):
    try:
        hashed = hash_password(new_password)
        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
        return True
    except:
        return False

# --- DATA GENERATION ---
def delete_all_records():
    if not messagebox.askyesno("Danger Zone", "آیا از حذف تمامی اطلاعات پایگاه داده اطمینان دارید؟\n\n!این غیرقابل بازگشت می‌باشد"):
        return
    try:
        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM visitors")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='visitors'")
        messagebox.showinfo("Developer Mode", ".تمامی اطلاعات پایگاه داده حذف شدند")
    except Exception as e:
        messagebox.showerror("Error", f"حذف اطلاعات با شکست مواجه شد {e}")

def add_dummy_data():
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
            except: continue 
            dept = random.choice(DEPARTMENT_LIST)
            dummy_records.append({
                "visitor_name": visitor_name, "national_id": nid, "employee_to_meet": employee_name, 
                "department": dept, "entry_time": entry_time_gregorian, "shamsi_date": shamsi_date
            })
        dummy_records.sort(key=lambda x: x['entry_time'])
        
        with DBConnection() as conn:
            cursor = conn.cursor()
            for r in dummy_records:
                cursor.execute(
                '''INSERT INTO visitors (visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, created_by) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (r['visitor_name'], r['national_id'], r['employee_to_meet'], r['department'], r['entry_time'], r['shamsi_date'], 'dev_debug')
                )

        messagebox.showinfo("Developer Mode", "100 Random Records (Full Data) Added Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate data: {e}")

def delete_dev_records():
    try:
        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM visitors WHERE created_by = 'dev_debug'")
            deleted_count = cursor.rowcount
        messagebox.showinfo("Developer Mode", f"{deleted_count} : تعداد رکورد های آزمایشی حذف شده ")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete dev records: {e}")

# ─── Audit Log ────────────────────────────────────────────────
def setup_audit_table():
    with DBConnection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                shamsi_date  TEXT    NOT NULL,
                shamsi_time  TEXT    NOT NULL,
                event_type   TEXT    NOT NULL,
                user_name    TEXT,
                visitor_id   INTEGER,
                visitor_name TEXT,
                national_id  TEXT,
                employee_to_meet TEXT,
                department   TEXT,
                details      TEXT,
                created_at   TEXT    NOT NULL
            )
        ''')
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_date ON audit_log (shamsi_date);"
        )

def log_audit(event_type: str, user=None, **kwargs):
    if event_type not in config.AUDIT_EVENT_TYPES:
        print(f"[Audit Log Error] Invalid event type: {event_type}")
        return
    
    try:
        import jdatetime
        now_j = jdatetime.datetime.now()
        sh_date = now_j.strftime("%Y/%m/%d")
        sh_time = now_j.strftime("%H:%M:%S")
        created_at = datetime.now().isoformat(timespec="seconds")
        
        if user is None:
            user = "System"
        
        visitor_id = kwargs.get("visitor_id")
        visitor_name = kwargs.get("visitor_name")
        national_id = kwargs.get("national_id")
        employee_to_meet = kwargs.get("employee_to_meet")
        department = kwargs.get("department")
        details = kwargs.get("details") or kwargs.get("error") or "No details provided"
        
        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_log
                    (shamsi_date, shamsi_time, event_type, user_name,
                     visitor_id, visitor_name, national_id,
                     employee_to_meet, department, details, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sh_date, sh_time, event_type, user,
                visitor_id, visitor_name, national_id,
                employee_to_meet, department, details, created_at,
            ))
    except Exception as e:
        print(f"[Audit Log Error] {e}")

def get_audit_logs(start_date: str, end_date: str) -> list:
    with DBConnection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, shamsi_date, shamsi_time, event_type,
                   user_name, visitor_id, visitor_name,
                   national_id, employee_to_meet, department, details, created_at
            FROM   audit_log
            WHERE  shamsi_date BETWEEN ? AND ?
            ORDER  BY shamsi_date, shamsi_time
        ''', (start_date, end_date))
        return cursor.fetchall()
