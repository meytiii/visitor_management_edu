#config.py : 

import os
from tkinter import messagebox

APP_VERSION = "3.1.4"

APP_DATA_DIR = os.path.join(os.environ['PROGRAMDATA'], 'VisitorSystem')

if not os.path.exists(APP_DATA_DIR):
    try:
        os.makedirs(APP_DATA_DIR)
    except OSError as e:
        messagebox.showerror("Error", f"Could not create database folder:\n{e}")

DB_PATH = os.path.join(APP_DATA_DIR, 'visitor_log.db')

DEPARTMENT_LIST = [
    "حوزه مدیر کل", "معاونت پرورشی", "معاونت تربیت بدنی",
    "معاونت نهضت سواد آموزی", "معاونت آموزش متوسطه", "معاونت آموزش ابتدایی",
    "اداره حراست", "اداره سنجش", "اداره خدمات و پشتیبانی",
    "امور اداری", "اداره فناوری اطلاعات", "اداره امور مالی و حسابداری",
    "اداره بودجه", "اداره تعاون و رفاه", "اداره استعداد های درخشان",
    "اداره امور شاهد", "اداره بازرسی", "اداره روابط عمومی",
    "اداره حقوقی", "اداره مشارکت ها", "اداره آموزش استثنائی",
    "کارپردازی", "معاونت پژوهش و برنامه ریزی", "هیأت تخلفات" , "دبیرخانه"
]

PERSIAN_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]

CULTURAL_MESSAGES = [
    # --- Quran & Hadith ---
    "«اللهم عجل لولیک الفرج»",
    "«الا بذکر الله تطمئن القلوب»",
    "پیامبر اکرم (ص): ز گهواره تا گور دانش بجوی",
    "پیامبر اکرم (ص): دو نعمت مجهولند: سلامت و امنیت",
    "امام علی (ع): هر کس کلمه‌ای به من بیاموزد، مرا بنده خود کرده است",
    "امام علی (ع): فرصت‌ها مانند ابر می‌گذرند، آن‌ها را دریابید",
    "امام صادق (ع): امانت‌داری و راستگویی، کلید رزق و روزی است",
    "امام حسین (ع): نیاز مردم به شما از نعمت‌های خدا بر شماست",
    "امام علی (ع): زینت علم، فروتنی است",
    "پیامبر اکرم (ص): معلمی شغل انبیاست",
    # --- Imam Khomeini (RA) ---
    "امام خمینی (ره): عالم محضر خداست، در محضر خدا معصیت نکنید",
    "امام خمینی (ره): معلم امانت‌داری است که انسان امانت اوست",
    "امام خمینی (ره): دبستان‌ها را دریابید که دانشگاه‌ها دیر است",
    "امام خمینی (ره): آموزش و پرورش کارخانه‌ی انسان‌سازی است",
    "امام خمینی (ره): انتظار فرج، انتظار قدرت اسلام است",
    # --- Supreme Leader (Ayatollah Khamenei) ---
    "مقام معظم رهبری: زنده نگه داشتن یاد شهدا کمتر از شهادت نیست",
    "مقام معظم رهبری: امنیت رکن اساسی پیشرفت کشور است",
    "مقام معظم رهبری: خدمت به مردم، بزرگترین مبارزه با آمریکاست",
    "مقام معظم رهبری: معلمان، افسران سپاه پیشرفت کشور هستند",
    "مقام معظم رهبری: آموزش و پرورش کانون خلق دنیای آینده است",
    "مقام معظم رهبری: هزینه کردن در آموزش و پرورش، سرمایه‌گذاری است",
    "مقام معظم رهبری: حراست، چشم بینا و گوش شنوای سازمان است",
    "مقام معظم رهبری: مدرسه، سلول بنیادی تحول در کشور است",
    # --- Martyr Morteza Motahhari (Education) ---
    "شهید مطهری: معلم باید نیروی فکری متعلم را پرورش دهد",
    "شهید مطهری: ستایشگر معلمی هستم که اندیشیدن را به من بیاموزد",
    # --- General Education & Security Values ---
    "«اداره کل آموزش و پرورش استان همدان - اداره حراست»",
    "تکریم ارباب رجوع، وظیفه شرعی و قانونی ماست",
    "حفظ اسرار و آبروی مومن، از واجبات است",
    "مدرسه قوی، ایران قوی",
    "هر دانش‌آموز، یک امید برای آینده ایران اسلامی",
    "رعایت حجاب و عفاف، ضامن سلامت جامعه است",
    "نظم و انضباط اداری، نشانه تعهد کاری است",
    "با لبخند پاسخگوی مراجعین محترم باشیم",
    "خوش آمدید - با آرزوی روزی پربار برای شما",
    "«سامانه مدیریت هوشمند مراجعین»",
    "شهید رجایی: معلمی شغل نیست، معلمی عشق است",
    "سردار دل‌ها حاج قاسم سلیمانی: ما ملت امام حسینیم",
    "حراست؛ مشاور امین و یاور مدیران",
    "صیانت از کرامت انسانی، رسالت اصلی حراست است",
    "فرزندان خود را به سلاح علم و ایمان مجهز کنید"
]

DEFAULT_DEV_PASSWORD = "herasat_edu@!" 
GREEN_COLOR = "#4CAF50"
GREEN_ACTIVE_COLOR = "#45a049"
BLUE_COLOR = "#008CBA"
BLUE_ACTIVE_COLOR = "#007ba7"
RED_COLOR = "#f44336"
RED_ACTIVE_COLOR = "#d32f2f"
DEFAULT_BG_COLOR = "#F0F0F0"
CARD_BG_COLOR = "#B1E666"

AUDIT_EVENT_TYPES = [
    "login_success",
    "login_failed",
    "logout",
    "app_closed",
    "visitor_added",
    "visitor_exit_recorded",
    "user_created",
    "user_deleted",
    "user_password_changed",
    "backup_created",
    "backup_restored",
    "data_exported",
    "developer_mode_enabled",
    "error"
]


#database.py : 
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

#printer.py : 
import win32ui
import win32print
import win32con
from tkinter import messagebox

def print_receipt(visitor_id, name, nid, emp, dept, entry_dt, shamsi_date):
    try:
        printer_name = win32print.GetDefaultPrinter()
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        hDC.StartDoc("Visitor Receipt")
        hDC.StartPage()
        page_width = hDC.GetDeviceCaps(win32con.HORZRES)
        
        x_center = page_width // 2
        x_right_margin = page_width - 30
        y = 0
        line_height = 45
        font_data = {"name": "B Roya", "height": 45, "weight": 700} 
        f = win32ui.CreateFont(font_data)
        hDC.SelectObject(f)
        headers = [
            ".جامعه معلمان، سربازان گمنام نظام اسلامی هستند",
            "«مقام معظم رهبری مدظله العالی»",
            "********************************",
            "اداره کل آموزش و پرورش استان همدان",
            "(اداره حراست)",
            "********************************",
            f"شماره: {visitor_id:06d}",
            f"تاریخ: {shamsi_date}",
            f"ساعت ورود: {entry_dt.strftime('%H:%M')}",
            ":ساعت خروج ",
            "--------------------------------",
            f"ملاقات کننده: {name}",
            f"شماره ملی: {nid}",
            f"معاونت/اداره: {dept}",
            f"ملاقات شونده: {emp}",
            "امضاء ملاقات شونده",
            "",
            "* حداکثر زمان حضور 2 ساعت می باشد *",
            "********************************"
        ]
        body_lines = [
        ]
        hDC.SetTextAlign(win32con.TA_CENTER)
        for line in headers:
            hDC.TextOut(x_center, y, line)
            y += line_height
        hDC.SetTextAlign(win32con.TA_RIGHT)
        for line in body_lines:
            hDC.TextOut(x_right_margin, y, line)
            y += line_height
        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
    except Exception as e:
        messagebox.showerror("خطای پرینت", f"خطا در ارتباط با پرینتر:\n{e}")

#utils.py : 
import os
import sys
import shutil
import sqlite3
import re
from datetime import datetime
from tkinter import messagebox, filedialog
import arabic_reshaper
from bidi.algorithm import get_display
import config

DB_PATH = config.DB_PATH

def validate_national_id(nid):
    """
    Validate Iranian national ID (کد ملی)
    Returns: (is_valid, error_message)
    """
    if not nid:
        return False, "کد ملی نمی‌تواند خالی باشد"
    
    if not nid.isdigit():
        return False, "کد ملی باید فقط شامل اعداد باشد"
    
    if len(nid) != 10:
        return False, "کد ملی باید ۱۰ رقمی باشد"
    
    if len(set(nid)) == 1:
        return False, "کد ملی معتبر نیست (همه ارقام یکسان)"

    try:
        control_digit = int(nid[9])
        
        sum_val = 0
        for i in range(9):
            sum_val += int(nid[i]) * (10 - i)
        
        remainder = sum_val % 11
        
        if remainder < 2:
            valid = (remainder == control_digit)
        else:
            valid = ((11 - remainder) == control_digit)
        
        if not valid:
            return False, "کد ملی وارد شده معتبر نیست"
        
        return True, ""
        
    except Exception as e:
        return False, f"خطا در اعتبارسنجی کد ملی: {str(e)}"

def validate_persian_name(name):
    """
    Validate Persian/Arabic names
    Allows Persian/Arabic letters, space, and dot
    """
    import re
    
    persian_pattern = re.compile(r'^[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF\u200C\u200F\.\s]+$')
    
    english_pattern = re.compile(r'^[A-Za-z\s\.]+$')
    
    name = name.strip()
    
    if not name or len(name) < 2:
        return False, "نام باید حداقل ۲ کاراکتر باشد"
    
    has_letter = any(c.isalpha() for c in name)
    if not has_letter:
        return False, "نام باید شامل حروف باشد"
    if not (persian_pattern.match(name) or english_pattern.match(name)):
        return False, "نام باید فقط شامل حروف فارسی/عربی یا انگلیسی باشد"
    
    return True, ""

def validate_numeric(text):
    """
    Basic numeric validation for entry widget
    Also prevents more than 10 digits
    """
    if text == "":
        return True
    
    if not text.isdigit():
        return False
    
    if len(text) > 10:
        return False
    
    return True

def make_farsi(text):
    try:
        import arabic_reshaper
        
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    except ImportError:
        return text

def create_backup():
    """Copies the database from its hidden location to the app's current directory."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_visitor_log_{timestamp}.db"
        
        destination_path = os.path.join(os.getcwd(), backup_filename)
        
        if not os.path.exists(DB_PATH):
             messagebox.showerror("خطا", ".فایل پایگاه داده یافت نشد! اطلاعاتی برای پشتیبان‌گیری وجود ندارد")
             return
        shutil.copy2(DB_PATH, destination_path)
        messagebox.showinfo("عملیات موفق", f":نسخه پشتیبان با موفقیت ایجاد شد و در مسیر زیر ذخیره گردید\n\n{destination_path}")
        
    except Exception as e:
        messagebox.showerror("خطا در پشتیبان‌گیری", f":خطایی در حین عملیات رخ داد\n{e}")

def restore_backup():
    """Imports records from a backup, skipping exact duplicates (Same ID + Same Time)."""
    backup_path = filedialog.askopenfilename(
        title="انتخاب فایل پشتیبان",
        filetypes=[("Database Files", "*.db"), ("All Files", "*.*")]
    )
    
    if not backup_path:
        return
    try:
        bk_conn = sqlite3.connect(backup_path)
        bk_cursor = bk_conn.cursor()
        
        try:
            bk_cursor.execute("SELECT visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, exit_time FROM visitors")
            records_to_import = bk_cursor.fetchall()
        except sqlite3.DatabaseError:
            bk_conn.close()
            raise Exception("Invalid Schema")
        bk_conn.close()
        if not records_to_import:
            messagebox.showinfo("اطلاعات", "فایل انتخاب شده خالی است")
            return
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        imported_count = 0
        duplicate_count = 0
        
        for row in records_to_import:
            cursor.execute(
                "SELECT 1 FROM visitors WHERE national_id = ? AND entry_time = ?", 
                (row[1], row[4])
            )
            
            if cursor.fetchone():
                duplicate_count += 1
            else:
                cursor.execute('''
                    INSERT INTO visitors (visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, exit_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', row)
                imported_count += 1
            
        conn.commit()
        conn.close()
        # --- Message Formatting ---
        msg = f"{imported_count} : تعداد رکورد های جدید  "
        
        if duplicate_count > 0:
            msg += f"\n\n(همچنین {duplicate_count} رکورد تکراری نادیده گرفته شد)"
        messagebox.showinfo("نتیجه بازیابی", msg)
    except Exception:
        messagebox.showerror("خطا", "فایل انتخاب شده معتبر نیست\nلطفاً از صحیح بودن فایل پشتیبان اطمینان حاصل کنید")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#widgets.py : 

import tkinter as tk
from tkinter import ttk

class RoundedEntry(tk.Canvas):
    def __init__(self, parent, width=200, height=30, radius=15, 
                 bg="white", border_color="#E0E0E0", 
                 text_var=None, show=None, justify='center', font=("Tahoma", 11)):
        super().__init__(parent, width=width, height=height, 
                         bg=parent["bg"], highlightthickness=0)
        self.entry_bg = bg
        
        self.create_polygon(
            radius, 0, width-radius, 0, width, 0, width, radius,
            width, height-radius, width, height, width-radius, height,
            radius, height, 0, height, 0, height-radius, 0, radius, 0, 0,
            smooth=True, fill=bg, outline=border_color, width=1
        )
        
        self.entry = tk.Entry(self, bg=bg, bd=0, highlightthickness=0, 
                              fg="#333333", justify=justify, font=font,
                              textvariable=text_var, show=show)
        
        self.create_window(width//2, height//2, window=self.entry, width=width-20)

    def get(self):
        return self.entry.get()

    def delete(self, first, last=tk.END):
        self.entry.delete(first, last)

    def focus(self):
        self.entry.focus()
        
    def bind(self, sequence=None, func=None, add=None):
        self.entry.bind(sequence, func, add)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None,
                 width=260, height=44,
                 radius=22,
                 bg="#1976D2",
                 hover_bg="#1565C0",
                 fg="white",
                 font=("Tahoma", 11, "bold")):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.rect = self.create_polygon(
            radius, 0,
            width-radius, 0,
            width, 0,
            width, radius,
            width, height-radius,
            width, height,
            width-radius, height,
            radius, height,
            0, height,
            0, height-radius,
            0, radius,
            0, 0,
            smooth=True,
            fill=bg,
            outline=""
        )
        self.text_item = self.create_text(
            width//2, height//2,
            text=text, fill=fg, font=font
        )
        self.bind("<Enter>", lambda e: self.itemconfig(self.rect, fill=hover_bg))
        self.bind("<Leave>", lambda e: self.itemconfig(self.rect, fill=bg))
        self.bind("<Button-1>", lambda e: command() if command else None)

class AutocompleteEntry(ttk.Entry):
    def __init__(self, master, completevalues=None, selection_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.completevalues = sorted(completevalues) if completevalues else []
        self.selection_callback = selection_callback
        self.var = self["textvariable"]
        if self.var == '':
            self.var = tk.StringVar()
            self["textvariable"] = self.var
        
        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.bind("<Return>", self.selection)
        self.bind("<FocusOut>", self.hidetip)
        
        self.lb_up = False
        self._after_id = None

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self._destroy_lb()
            return
        words = self.comparison()
        if words:
            if not self.lb_up:
                self.lb = tk.Listbox(self.master, width=self["width"], height=8, font=self["font"], bd=1, relief=tk.SOLID)
                self.lb.bind("<ButtonRelease-1>", self.selection)
                self.lb.bind("<Right>", self.selection)
                self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                self.lb.lift() 
                self.lb_up = True
            
            self.lb.delete(0, tk.END)
            for w in words:
                self.lb.insert(tk.END, w)
        else:
            self._destroy_lb()

    def comparison(self):
        pattern = self.var.get().lower()
        return [w for w in self.completevalues if w.lower().startswith(pattern)]

    def selection(self, event):
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        if self.lb_up:
            selected_val = None
            if event and event.widget == self.lb:
                try:
                    index = self.lb.nearest(event.y)
                    selected_val = self.lb.get(index)
                except: pass
            else:
                try:
                    if self.lb.curselection():
                        selected_val = self.lb.get(self.lb.curselection())
                except: pass
            
            if selected_val:
                self.var.set(selected_val)
                if self.selection_callback:
                    self.selection_callback(selected_val)
            
            self._destroy_lb()
            self.icursor(tk.END)
            self.tk_focusNext().focus()
            return "break"

    def move_up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def move_down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != str(self.lb.size() - 1):
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def hidetip(self, event=None):
        if self.lb_up:
            self._after_id = self.after(200, self._destroy_lb)
    
    def _destroy_lb(self):
        if self.lb_up:
            self.lb.destroy()
            self.lb_up = False
            self._after_id = None
            
    def set_completion_list(self, completion_list):
        self.completevalues = sorted(completion_list)

#windows.py : 
import tkinter as tk
from tkinter import messagebox, filedialog, font
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import sqlite3
import pandas as pd
from datetime import datetime
import jdatetime
import os
from PIL import Image, ImageTk

import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Tahoma', 'Arial', 'DejaVu Sans']
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
import database
import utils

# --- Configuration & Styles ---
FONT_MAIN = "Tahoma"
FONT_TABLE = "Tahoma"
_fonts_checked = False

def ensure_fonts():
    """Checks for Persian fonts and strictly enforces them on ttkbootstrap elements"""
    global FONT_MAIN, FONT_TABLE, _fonts_checked
    if _fonts_checked: return
    try:
        available = font.families()
        if "B Titr" in available: FONT_MAIN = "B Titr"
        if "B Nazanin" in available: FONT_TABLE = "B Nazanin"
        elif "B Roya" in available: FONT_TABLE = "B Roya"
        
        style = tb.Style()
        style.configure('TButton', font=(FONT_MAIN, 12))
        
        style.configure('Treeview', font=(FONT_TABLE, 12, "bold"), rowheight=45) 
        style.configure('Treeview.Heading', font=(FONT_MAIN, 11, "bold"))
        
        style.configure('primary.Treeview', font=(FONT_TABLE, 12, "bold"), rowheight=45) 
        style.configure('primary.Treeview.Heading', font=(FONT_MAIN, 11, "bold"))
        
        _fonts_checked = True
    except: pass


def show_help_popup():
    help_text = f"در صورت بروز هرگونه مشکل یا سوال با شماره زیر تماس بگیرید\n\nخرّم آبادی - 09222550573\n\nنسخه برنامه {config.APP_VERSION}"
    messagebox.showinfo("راهنما", help_text)

def show_login_screen(app, on_success_callback):
    ensure_fonts()
    login_win = tb.Toplevel(app)
    login_win.title("ورود به سیستم")
    
    width, height = 400, 350
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    login_win.geometry(f"{width}x{height}+{x}+{y}")
    login_win.resizable(False, False)

    canvas = tk.Canvas(login_win, width=width, height=height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.configure(bg="#2E3B4E")
    
    bg_path = utils.resource_path("login.png")
    if os.path.exists(bg_path):
        try:
            pil_image = Image.open(bg_path)
            pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
            bg_image_obj = ImageTk.PhotoImage(pil_image)
            canvas.create_image(0, 0, image=bg_image_obj, anchor="nw")
            login_win.bg_image_obj = bg_image_obj 
        except Exception as e: pass

    try: login_win.iconbitmap(utils.resource_path('app_icon.ico'))
    except: pass

    canvas.create_text(200, 40, text="سامانه مدیریت مراجعین💻", fill="#d6f7fd", font=(FONT_MAIN, 16, "bold"))
    
    canvas.create_text(200, 90, text=":نام کاربری👤", fill="#fffbda", font=(FONT_MAIN, 12))
    ent_user = tb.Entry(login_win, justify='center', font=(FONT_MAIN, 12)
    )
    canvas.create_window(200, 120, window=ent_user, width=200, height=35)
    
    canvas.create_text(200, 160, text=":رمز عبور🔑", fill="#fffbda", font=(FONT_MAIN, 12))
    ent_pass = tb.Entry(login_win, show="●", justify='center', font=(FONT_MAIN, 12))
    canvas.create_window(200, 190, window=ent_pass, width=200, height=35)
    
    def do_login():
        u = ent_user.get().strip()
        p = ent_pass.get().strip()
        success, role, full_name = database.authenticate_user(u, p)
        if success:
            database.log_audit("login_success", user=u)
            login_win.destroy()
            on_success_callback(u, role, full_name)
        else:
            database.log_audit("login_failed", user=u)
            messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است", parent=login_win)
            ent_pass.delete(0, tk.END)

    btn_login = tb.Button(login_win, text="ورود🚪", command=do_login, bootstyle=SUCCESS)
    canvas.create_window(200, 260, window=btn_login, width=150, height=40)

    def on_login_window_close():
        database.log_audit("app_closed", user=getattr(app, "current_user", None))
        app.destroy()

    login_win.protocol("WM_DELETE_WINDOW", on_login_window_close)

    login_win.bind('<Return>', lambda e: do_login())
    ent_user.focus()

def open_user_manager(parent, app=None, current_user=None):
    ensure_fonts()
    um_win = tb.Toplevel(parent)
    um_win.title("مدیریت کاربران")
    um_win.geometry("750x550")
    um_win.resizable(False,False)
    try: um_win.iconbitmap(utils.resource_path('app_icon.ico'))
    except: pass

    bg_path = utils.resource_path("user_management.png")
    if os.path.exists(bg_path):
        try:
            original_img = Image.open(bg_path)
            resized_img = original_img.resize((750, 550), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(resized_img)
            bg_label = tk.Label(um_win, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception: pass

    list_frame = tk.Frame(um_win, width=300, bg="white", bd=1, relief="solid") 
    list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
    list_frame.pack_propagate(False)

    tb.Label(list_frame, text="لیست کاربران", font=(FONT_MAIN, 14, "bold"), bootstyle=PRIMARY, background="white").pack(anchor="e", pady=(10, 5), padx=10)
    
    user_list = tk.Listbox(list_frame, font=(FONT_TABLE, 12), bd=0, justify='right')
    user_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    selected_username = tk.StringVar(value="")
    
    def on_user_select(event):
        sel = user_list.curselection()
        if not sel:
            return
        full_text = user_list.get(sel[0])
        # Extract username from format: "[role]  fullname  (username)"
        username = full_text.split("(")[-1].replace(")", "").strip()
        selected_username.set(username)
        
        # Get user details from database
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT username, role, full_name FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            # Fill form fields
            new_user_ent.config(state="normal")
            new_user_ent.delete(0, tk.END)
            new_user_ent.insert(0, user_data[0])
            new_user_ent.config(state="disabled")
            
            new_fullname_ent.delete(0, tk.END)
            new_fullname_ent.insert(0, user_data[2] or "")
            
            new_pass_ent.delete(0, tk.END)
            role_var.set(user_data[1])
            
            add_btn.config(text="✏️ ویرایش کاربر", bootstyle="warning")
    
    def clear_selection():
        selected_username.set("")
        new_user_ent.config(state="normal")
        new_user_ent.delete(0, tk.END)
        new_fullname_ent.delete(0, tk.END)
        new_pass_ent.delete(0, tk.END)
        role_var.set("guard")
        add_btn.config(text="ثبت کاربر", bootstyle="success")
        user_list.selection_clear(0, tk.END)
    
    user_list.bind("<<ListboxSelect>>", on_user_select)

    
    def refresh_list():
        user_list.delete(0, tk.END)
        for u, r, fname in database.get_all_users():
            role_fa = "مدیر" if r == 'admin' else "نگهبان"
            display_name = fname if fname else "---"
            user_list.insert(tk.END, f"[{role_fa}]  {display_name}  ({u})")
    refresh_list()
    
    action_frame = tk.Frame(um_win, width=350, bg="white", bd=1, relief="solid")
    action_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=15)
    action_frame.pack_propagate(False)
    
    tb.Label(action_frame, text="افزودن کاربر جدید", font=(FONT_MAIN, 14, "bold"), background="white").pack(pady=(15, 10))
    
    def create_input(label_text, show=None):
        tb.Label(action_frame, text=label_text, font=(FONT_MAIN, 11), background="white").pack(anchor="e", pady=(5, 2), padx=20)
        entry = tb.Entry(action_frame, justify='center', font=(FONT_MAIN, 11), show=show)
        entry.pack(fill=tk.X, padx=20)
        return entry

    new_fullname_ent = create_input(":نام و نام خانوادگی")
    new_user_ent = create_input(":نام کاربری")
    new_pass_ent = create_input(":رمز عبور", show="●")
    
    tb.Label(action_frame, text=":نقش کاربری", font=(FONT_MAIN, 11), background="white").pack(anchor="e", pady=(10, 5), padx=20)
    role_var = tk.StringVar(value="guard")
    radio_frame = tk.Frame(action_frame, bg="white")
    radio_frame.pack(anchor="e", padx=20)
    tb.Radiobutton(radio_frame, text="نگهبان", variable=role_var, value="guard", bootstyle=PRIMARY).pack(side=tk.RIGHT, padx=10)
    tb.Radiobutton(radio_frame, text="مدیر", variable=role_var, value="admin", bootstyle=PRIMARY).pack(side=tk.RIGHT, padx=10)
    
    def add_user():
        fname, u, p, r = new_fullname_ent.get().strip(), new_user_ent.get().strip(), new_pass_ent.get().strip(), role_var.get()
        editing_user = selected_username.get()
        
        if editing_user:
            # Edit mode
            if len(fname) < 2:
                return messagebox.showwarning("خطا", "لطفاً نام و نام خانوادگی را وارد کنید", parent=um_win)
            
            try:
                conn = sqlite3.connect(config.DB_PATH)
                cursor = conn.cursor()
                
                # Update full_name and role
                cursor.execute("UPDATE users SET full_name=?, role=? WHERE username=?", (fname, r, editing_user))
                
                # Update password only if provided
                if p:
                    if len(p) < 3:
                        conn.close()
                        return messagebox.showwarning("خطا", "رمز عبور باید حداقل ۳ حرف باشد", parent=um_win)
                    
                    # Hash and update password using the same connection
                    hashed = database.hash_password(p)
                    cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed, editing_user))

                conn.commit()
                conn.close()
                
                if editing_user == getattr(app, 'current_username', None):
                    database.log_audit("self_info_changed_logout", user=editing_user)
                    um_win.destroy()
                    app.withdraw()
                    from windows import show_login_screen
                    import main
                    show_login_screen(app, main.setup_dashboard)
                else:
                    messagebox.showinfo("موفق", f"اطلاعات کاربر {fname} ویرایش شد", parent=um_win)
                    clear_selection()
                    refresh_list()
                
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در ویرایش: {str(e)}", parent=um_win)

        else:
            # Add mode
            if len(u) < 3 or len(p) < 3:
                return messagebox.showwarning("خطا", "نام کاربری و رمز عبور باید حداقل ۳ حرف باشند", parent=um_win)
            if len(fname) < 2:
                return messagebox.showwarning("خطا", "لطفاً نام و نام خانوادگی را وارد کنید", parent=um_win)
            
            ok, msg = database.create_user(u, p, fname, r)
            if ok:
                messagebox.showinfo("موفق", f"کاربر {fname} با موفقیت ایجاد شد", parent=um_win)
                for ent in [new_fullname_ent, new_user_ent, new_pass_ent]: ent.delete(0, tk.END)
                refresh_list()
            else:
                messagebox.showerror("خطا", msg, parent=um_win)

    btn_row = tk.Frame(action_frame, bg=action_frame['bg'])
    btn_row.pack(fill=tk.X, pady=15, padx=20)
    
    add_btn = tb.Button(btn_row, text="ثبت کاربر", command=add_user, bootstyle=SUCCESS)
    add_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0), ipady=3)
    
    tb.Button(btn_row, text="❌ انصراف", command=clear_selection, bootstyle=(SECONDARY, OUTLINE)).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 5), ipady=3)

    tb.Separator(action_frame).pack(fill=tk.X, pady=10, padx=20)
    
    def delete_selected():
        sel = user_list.curselection()
        if not sel: return
        username = user_list.get(sel[0]).split("  (")[-1].replace(")", "").strip()

        if current_user and username == current_user:
            messagebox.showwarning("خطا", ".نمی‌توانید حساب کاربری خود را حذف کنید", parent=um_win)
            return

        if messagebox.askyesno("حذف", f"{username} آیا از حذف کاربر مطمئن هستید؟", parent=um_win):
            ok, msg = database.delete_user(username)
            if ok:
                refresh_list()
                if app and current_user and username == current_user:
                    um_win.destroy()
                    parent.destroy()
                    app.current_user = None
                    from windows import show_login_screen
                    import main
                    show_login_screen(app, main.setup_dashboard)
            else:
                messagebox.showerror("خطا", msg, parent=um_win)



    tb.Button(action_frame, text="حذف کاربر انتخاب شده", command=delete_selected, bootstyle=(DANGER, OUTLINE)).pack(fill=tk.X, padx=20)

def show_daily_stats_ui(parent_win):
    ensure_fonts()
    stats_win = tb.Toplevel(parent_win)
    stats_win.title("آمار تردد")
    stats_win.geometry("420x420")
    stats_win.resizable(False,False)
    try: stats_win.iconbitmap(utils.resource_path('app_icon.ico'))
    except: pass
    
    main_frame = tb.Frame(stats_win, padding=15)
    main_frame.pack(fill=tk.BOTH, expand=True)

    tb.Label(main_frame, text=":تاریخ مورد نظر را وارد کنید", font=(FONT_MAIN, 12, "bold")).pack(pady=(10, 15))
    
    date_frame = tb.Frame(main_frame)
    date_frame.pack()
    ent_day = tb.Entry(date_frame, justify='center', width=5, font=(FONT_MAIN, 11)); ent_day.pack(side=tk.RIGHT, padx=2)
    tb.Label(date_frame, text="/", font=(FONT_MAIN, 11)).pack(side=tk.RIGHT)
    ent_month = tb.Entry(date_frame, justify='center', width=5, font=(FONT_MAIN, 11)); ent_month.pack(side=tk.RIGHT, padx=2)
    tb.Label(date_frame, text="/", font=(FONT_MAIN, 11)).pack(side=tk.RIGHT)
    ent_year = tb.Entry(date_frame, justify='center', width=7, font=(FONT_MAIN, 11)); ent_year.pack(side=tk.RIGHT, padx=2)
    
    result_lbl = tb.Label(main_frame, text="", font=(FONT_MAIN, 12), justify="center", bootstyle=INFO)
    result_lbl.pack(pady=15)

    def calculate(target_date_str=None):
        if not target_date_str:
            y, m, d = ent_year.get(), ent_month.get(), ent_day.get()
            if not (y and m and d): return messagebox.showwarning("خطا", "لطفاً تاریخ را کامل وارد کنید", parent=stats_win)
            target_date_str = f"{y}/{m.zfill(2)}/{d.zfill(2)}"
        try:
            conn = sqlite3.connect(config.DB_PATH); cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM visitors WHERE shamsi_date = ?", (target_date_str,))
            total = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM visitors WHERE shamsi_date = ? AND (exit_time IS NULL OR exit_time = '')", (target_date_str,))
            no_exit = cursor.fetchone()[0]
            conn.close()
            result_lbl.config(text=f"تاریخ: {target_date_str}\n\nتعداد کل ثبت شده: {total}\nبدون ساعت خروج: {no_exit}")
        except Exception as e: messagebox.showerror("Error", str(e), parent=stats_win)

    def set_today():
        now_j = jdatetime.date.fromgregorian(date=datetime.now().date())
        ent_year.delete(0, tk.END); ent_year.insert(0, str(now_j.year))
        ent_month.delete(0, tk.END); ent_month.insert(0, str(now_j.month))
        ent_day.delete(0, tk.END); ent_day.insert(0, str(now_j.day))
        calculate(now_j.strftime("%Y/%m/%d"))

    btn_frame = tb.Frame(main_frame)
    btn_frame.pack(fill=tk.X, pady=(10, 0))
    tb.Button(btn_frame, text="امروز", command=set_today, bootstyle=WARNING).pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X, ipady=4)
    tb.Button(btn_frame, text="محاسبه", command=lambda: calculate(), bootstyle=PRIMARY).pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X, ipady=4)

def show_heatmap_analytics(app):
    ensure_fonts()
    analytics_win = tb.Toplevel(app)
    analytics_win.title("تحلیل آماری تردد")
    analytics_win.geometry("900x650")
    analytics_win.resizable(False,False)
    try: analytics_win.iconbitmap(utils.resource_path('app_icon.ico'))
    except: pass
    
    filter_frame = tb.Frame(analytics_win, padding=10)
    filter_frame.pack(fill=tk.X)
    
    tb.Label(filter_frame, text=":فیلتر زمانی", font=(FONT_MAIN, 12, "bold")).pack(side=tk.RIGHT, padx=10)
    cb_day = tb.Combobox(filter_frame, values=[""] + [str(i) for i in range(1, 32)], width=3, state="readonly", justify='center')
    cb_day.pack(side=tk.RIGHT, padx=2)
    tb.Label(filter_frame, text="روز").pack(side=tk.RIGHT)
    cb_month = tb.Combobox(filter_frame, values=[""] + config.PERSIAN_MONTHS, width=10, state="readonly", justify='center')
    cb_month.pack(side=tk.RIGHT, padx=2)
    tb.Label(filter_frame, text="ماه").pack(side=tk.RIGHT)
    cb_year = tb.Combobox(filter_frame, values=[""] + [str(i) for i in range(1400, 1411)], width=5, state="readonly", justify='center')
    cb_year.pack(side=tk.RIGHT, padx=2)
    tb.Label(filter_frame, text="سال").pack(side=tk.RIGHT)
    
    chart_container = tb.Frame(analytics_win, padding=10)
    chart_container.pack(fill=tk.BOTH, expand=True)

    def update_chart():
        for widget in chart_container.winfo_children(): widget.destroy()
        y, m_name, d = cb_year.get(), cb_month.get(), cb_day.get()
        query = "SELECT strftime('%H', entry_time) as hour, COUNT(*) FROM visitors WHERE 1=1"
        params = []
        title_context = "کل ادوار"
        if y: query += " AND shamsi_date LIKE ?"; params.append(f"{y}%"); title_context = f"سال {y}"
        if m_name in config.PERSIAN_MONTHS:
            m_str = f"{(config.PERSIAN_MONTHS.index(m_name) + 1):02d}"
            query += " AND shamsi_date LIKE ?"; params.append(f"%/{m_str}/%"); title_context += f" - {m_name}"
        if d: query += " AND shamsi_date LIKE ?"; params.append(f"%/{d.zfill(2)}"); title_context += f" - روز {d}"
        query += " GROUP BY hour ORDER BY hour"

        try:
            conn = sqlite3.connect(config.DB_PATH); cursor = conn.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall(); conn.close()
        except Exception as e: return

        if not data:
            tb.Label(chart_container, text="اطلاعاتی با این فیلتر یافت نشد", font=(FONT_MAIN, 14), bootstyle=SECONDARY).pack(pady=50)
            return

        hours_found, counts_found = [row[0] for row in data], [row[1] for row in data]
        full_hours = [f"{h:02d}" for h in range(7, 20)]
        full_counts = [counts_found[hours_found.index(h)] if h in hours_found else 0 for h in full_hours]

        import matplotlib
        matplotlib.rcParams['font.family'] = 'Tahoma'  # prevents missing Latin glyph warnings on tick labels

        fig = Figure(figsize=(8, 5), dpi=100)
        fig.patch.set_facecolor('#ffffff')
        ax = fig.add_subplot(111)
        bars = ax.bar(full_hours, full_counts, color='#2596be', width=0.6, zorder=3)
        ax.set_title(utils.make_farsi(f"تحلیل تردد - {title_context}"), fontsize=14, fontname='Tahoma')
        ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

        for bar in bars:
            if bar.get_height() > 0:
                ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{int(bar.get_height())}',
                ha='center', va='bottom', fontsize=10)
        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def reset_filters():
        cb_year.set(""); cb_month.set(""); cb_day.set("")
        update_chart()

    tb.Button(filter_frame, text="نمایش نمودار", command=update_chart, bootstyle=PRIMARY).pack(side=tk.LEFT, padx=5)
    tb.Button(filter_frame, text="حذف فیلترها", command=reset_filters, bootstyle=(DANGER, OUTLINE)).pack(side=tk.LEFT, padx=5)
    update_chart()

def open_search_window(app):
    ensure_fonts()
    search_win = tb.Toplevel(app)
    try: search_win.iconbitmap(utils.resource_path('app_icon.ico'))
    except: pass
    search_win.title("مشاهده و جستجوی سوابق")
    search_win.geometry("1300x800") 
    
    current_page = 1
    items_per_page = 50
    total_pages = 1
    current_filters = {} 
    
    search_frame = tb.LabelFrame(search_win, text="فیلترهای جستجو", padding=15, bootstyle=PRIMARY)
    search_frame.pack(fill=tk.X, padx=15, pady=10)
    
    tb.Label(search_frame, text=": نام مهمان").grid(row=0, column=5, sticky=tk.E, padx=(15, 5), pady=5)
    entry_search_name = tb.Entry(search_frame, justify='right')
    entry_search_name.grid(row=0, column=4, sticky=tk.EW, padx=5, pady=5)
    
    tb.Label(search_frame, text=": کد ملی").grid(row=0, column=3, sticky=tk.E, padx=(15, 5), pady=5)
    entry_search_nid = tb.Entry(search_frame, justify='right')
    entry_search_nid.grid(row=0, column=2, sticky=tk.EW, padx=5, pady=5)
    
    tb.Label(search_frame, text=": تاریخ").grid(row=1, column=5, sticky=tk.E, padx=(15, 5), pady=5)
    combo_day = tb.Combobox(search_frame, values=[""] + [str(i) for i in range(1, 32)], justify='center', width=3, state='readonly')
    combo_day.grid(row=1, column=4, sticky=tk.E, padx=(0, 5))
    combo_month = tb.Combobox(search_frame, values=[""] + config.PERSIAN_MONTHS, justify='center', width=10, state='readonly')
    combo_month.grid(row=1, column=4, sticky=tk.E, padx=(0, 55))
    combo_year = tb.Combobox(search_frame, values=[""] + [str(i) for i in range(1404, 1451)], justify='center', width=5, state='readonly')
    combo_year.grid(row=1, column=4, sticky=tk.W, padx=(0, 0))
    
    tb.Label(search_frame, text=": واحد").grid(row=1, column=3, sticky=tk.E, padx=(15, 5), pady=5)
    combo_search_dept = tb.Combobox(search_frame, values=[""] + config.DEPARTMENT_LIST, justify='right', state='readonly')
    combo_search_dept.grid(row=1, column=2, sticky=tk.EW, padx=5, pady=5)
    
    search_frame.columnconfigure(2, weight=1); search_frame.columnconfigure(4, weight=1)
    
    tree_frame = tb.Frame(search_win, padding=(15, 5))
    tree_frame.pack(expand=True, fill=tk.BOTH)
    
    tree = tb.Treeview(tree_frame, columns=("id", "visitor_name", "national_id", "employee_to_meet", "department", "entry_time", "shamsi_date", "exit_time", "created_by"), 
                        show='headings', selectmode="browse", bootstyle=PRIMARY)
    
    v_scroll = tb.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    h_scroll = tb.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    tree.pack(expand=True, fill=tk.BOTH)
    
    headings = {"id": "شماره", "visitor_name": "نام مهمان", "national_id": "کد ملی", "employee_to_meet": "ملاقات شونده", 
                "department": "واحد", "entry_time": "ساعت ورود", "shamsi_date": "تاریخ ورود", "exit_time": "ساعت خروج", "created_by": "کاربر ثبت کننده"}
    for col, text in headings.items(): tree.heading(col, text=text)
    
    tree.column("id", width=60, anchor=tk.CENTER); tree.column("visitor_name", width=160, anchor=tk.CENTER)
    tree.column("national_id", width=100, anchor=tk.CENTER); tree.column("employee_to_meet", width=140, anchor=tk.CENTER)
    tree.column("department", width=200, anchor=tk.CENTER); tree.column("entry_time", width=70, anchor=tk.CENTER)
    tree.column("shamsi_date", width=90, anchor=tk.CENTER); tree.column("exit_time", width=70, anchor=tk.CENTER)
    tree.column("created_by", width=130, anchor=tk.CENTER)

    pagination_frame = tb.Frame(search_win, padding=10)
    pagination_frame.pack(fill=tk.X)
    lbl_info = tb.Label(pagination_frame, text="", font=(FONT_MAIN, 11))
    lbl_info.pack(side=tk.RIGHT, padx=(10, 20))
    controls_frame = tb.Frame(pagination_frame)
    controls_frame.pack(side=tk.RIGHT, padx=10)
    lbl_page_num = tb.Label(controls_frame, text="1", font=(FONT_MAIN, 14, "bold"), width=4, anchor="center")
    
    def change_page(action):
        nonlocal current_page
        if action == 'first': current_page = 1
        elif action == 'prev' and current_page > 1: current_page -= 1
        elif action == 'next' and current_page < total_pages: current_page += 1
        elif action == 'last': current_page = total_pages
        fetch_and_display_records(current_filters)

    tb.Button(controls_frame, text="⏭", command=lambda: change_page('first'), bootstyle=(SECONDARY, OUTLINE)).pack(side=tk.RIGHT, padx=2)
    tb.Button(controls_frame, text="▶", command=lambda: change_page('prev'), bootstyle=(SECONDARY, OUTLINE)).pack(side=tk.RIGHT, padx=2)
    lbl_page_num.pack(side=tk.RIGHT, padx=10)
    tb.Button(controls_frame, text="◀", command=lambda: change_page('next'), bootstyle=(SECONDARY, OUTLINE)).pack(side=tk.RIGHT, padx=2)
    tb.Button(controls_frame, text="⏮", command=lambda: change_page('last'), bootstyle=(SECONDARY, OUTLINE)).pack(side=tk.RIGHT, padx=2)

    def fetch_and_display_records(filters=None):
        nonlocal current_page, total_pages
        if filters is None: filters = {}
        
        base_query = " FROM visitors WHERE 1=1"
        params = []
        if filters.get("name"): base_query += " AND visitor_name LIKE ?"; params.append(f"%{filters['name']}%")
        if filters.get("nid"): base_query += " AND national_id LIKE ?"; params.append(f"%{filters['nid']}%")
        if filters.get("dept"): base_query += " AND department = ?"; params.append(filters['dept'])
        
        y, m_name, d = filters.get("year"), filters.get("month_name"), filters.get("day")
        if y: base_query += " AND shamsi_date LIKE ?"; params.append(f"{y}%")
        if m_name in config.PERSIAN_MONTHS: base_query += " AND shamsi_date LIKE ?"; params.append(f"%/{(config.PERSIAN_MONTHS.index(m_name) + 1):02d}/%")
        if d: base_query += " AND shamsi_date LIKE ?"; params.append(f"%/{d.zfill(2)}")

        conn = sqlite3.connect(config.DB_PATH); cursor = conn.cursor()
        cursor.execute("SELECT count(*)" + base_query, params)
        total_records = cursor.fetchone()[0]
        
        import math
        total_pages = max(1, math.ceil(total_records / items_per_page))
        if current_page > total_pages: current_page = total_pages
        
        offset = (current_page - 1) * items_per_page
        params.extend([items_per_page, offset])
        cursor.execute("SELECT id, visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, exit_time, created_by" + base_query + " ORDER BY id DESC LIMIT ? OFFSET ?", params)
        
        for i in tree.get_children(): tree.delete(i)
        for r in cursor.fetchall():
            dt = datetime.strptime(r[5], "%Y-%m-%d %H:%M:%S").strftime("%H:%M") if "-" in r[5] else r[5]
            tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[4], dt, r[6] or "", r[7] or "", r[8] or "---"))
            
        conn.close()
        start_idx = offset + 1 if total_records > 0 else 0
        lbl_info.config(text=f"نمایش {start_idx} تا {min(offset + items_per_page, total_records)} از {total_records} رکورد")
        lbl_page_num.config(text=str(current_page))

    def search_action(): 
        nonlocal current_filters, current_page
        current_page = 1 
        current_filters = {"name": entry_search_name.get(), "nid": entry_search_nid.get(), "year": combo_year.get(), "month_name": combo_month.get(), "day": combo_day.get(), "dept": combo_search_dept.get()}
        fetch_and_display_records(current_filters)

    def reset_action():
        for w in [entry_search_name, entry_search_nid]: w.delete(0, tk.END)
        for w in [combo_year, combo_month, combo_day, combo_search_dept]: w.set("")
        search_action()

    def export_to_excel():
        filters = current_filters
        base_query = " FROM visitors WHERE 1=1"
        params = []
        
        if filters.get("name"): base_query += " AND visitor_name LIKE ?"; params.append(f"%{filters['name']}%")
        if filters.get("nid"): base_query += " AND national_id LIKE ?"; params.append(f"%{filters['nid']}%")
        if filters.get("dept"): base_query += " AND department = ?"; params.append(filters['dept'])
        
        y, m_name, d = filters.get("year"), filters.get("month_name"), filters.get("day")
        if y: base_query += " AND shamsi_date LIKE ?"; params.append(f"{y}%")
        if m_name in config.PERSIAN_MONTHS: base_query += " AND shamsi_date LIKE ?"; params.append(f"%/{(config.PERSIAN_MONTHS.index(m_name) + 1):02d}/%")
        if d: base_query += " AND shamsi_date LIKE ?"; params.append(f"%/{d.zfill(2)}")

        full_query = "SELECT id, visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, exit_time, created_by" + base_query + " ORDER BY id DESC"
        
        try:
            conn = sqlite3.connect(config.DB_PATH)
            cursor = conn.cursor()
            cursor.execute(full_query, params)
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showwarning("هشدار", "رکوردی برای خروجی گرفتن با این فیلترها وجود ندارد", parent=search_win)
                return
                
            columns_export = ["شناسه", "نام مهمان", "کد ملی", "ملاقات شونده", "واحد", "زمان ورود", "تاریخ شمسی", "ساعت خروج", "کاربر ثبت کننده"]
            df = pd.DataFrame(rows, columns=columns_export)
            
            file_path = filedialog.asksaveasfilename(
                parent=search_win,
                defaultextension=".xlsx", 
                filetypes=[("Excel Files", "*.xlsx")], 
                title="ذخیره فایل اکسل"
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("موفق", f"فایل اکسل با موفقیت ذخیره شد:\n{file_path}", parent=search_win)
                
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ایجاد فایل اکسل:\n{str(e)}", parent=search_win)


    def on_tree_double_click(event):
        selected = tree.selection()
        if not selected: return
        vals = tree.item(selected[0], "values")
        visitor_id = vals[0]
        visitor_name = vals[1]
        entry_shamsi_date = vals[6]
        
        if vals[7].strip(): return messagebox.showerror("خطا", "ساعت خروج قبلاً ثبت شده است", parent=search_win)
        
        popup = tb.Toplevel(search_win)
        popup.title("ثبت خروج")
        popup.geometry("500x500")
        try: popup.iconbitmap(utils.resource_path('app_icon.ico'))
        except: pass
        
        p_frame = tb.Frame(popup, padding=30)
        p_frame.pack(fill=tk.BOTH, expand=True)
        tb.Label(p_frame, text="ثبت خروج", font=(FONT_MAIN, 16, "bold"), bootstyle=SUCCESS).pack(pady=(0,5))
        tb.Label(p_frame, text=f": {visitor_name}", font=(FONT_MAIN, 13)).pack(pady=(0,15))
        
        current_shamsi = jdatetime.date.fromgregorian(date=datetime.now().date()).strftime("%Y/%m/%d")
        if entry_shamsi_date != current_shamsi:
            warn_lbl = tb.Label(p_frame, text=f"⚠️ تاریخ ورود: {entry_shamsi_date} (امروز نیست!)", 
                                font=(FONT_MAIN, 11), bootstyle=(WARNING, INVERSE), padding=8, anchor="center")
            warn_lbl.pack(fill=tk.X, pady=(0, 15))
            
        tb.Label(p_frame, text=": ساعت خروج را انتخاب کنید", font=(FONT_MAIN, 12)).pack(anchor="e", pady=(0, 5))
        
        t_frame = tb.Frame(p_frame)
        t_frame.pack(pady=10)
        
        h_var, m_var = tk.StringVar(value=datetime.now().strftime("%H")), tk.StringVar(value=datetime.now().strftime("%M"))
        
        def set_current_time():
            now = datetime.now()
            h_var.set(now.strftime("%H"))
            m_var.set(now.strftime("%M"))
            
        tb.Button(t_frame, text="زمان فعلی", command=set_current_time, bootstyle=INFO).pack(side=tk.RIGHT, padx=(20, 0))
        tb.Combobox(t_frame, textvariable=m_var, values=[str(i).zfill(2) for i in range(0, 60, 5)], width=4, font=(FONT_MAIN, 12), justify='center', state='readonly').pack(side=tk.RIGHT, padx=5)
        tb.Label(t_frame, text=":", font=(FONT_MAIN, 14, "bold")).pack(side=tk.RIGHT)
        tb.Combobox(t_frame, textvariable=h_var, values=[str(i).zfill(2) for i in range(7, 21)], width=4, font=(FONT_MAIN, 12), justify='center', state='readonly').pack(side=tk.RIGHT, padx=5)
        
        try:
            entry_time_str = vals[5]
            entry_time_only = entry_time_str.split(' ')[1][:5] if ' ' in entry_time_str else entry_time_str
            info_lbl = tb.Label(p_frame, text=f"ساعت ورود: {entry_time_only}   |   تاریخ: {entry_shamsi_date}", 
                                font=(FONT_MAIN, 11), bootstyle=(INFO, INVERSE), padding=10, anchor="center")
            info_lbl.pack(fill=tk.X, pady=(20, 10))
        except: pass
        
        def save_exit():
            hour = h_var.get()
            minute = m_var.get()
            if not hour or not minute: return messagebox.showerror("خطا", "لطفاً ساعت و دقیقه را انتخاب کنید", parent=popup)
            
            try:
                if ' ' in vals[5]:
                    entry_h, entry_m = map(int, vals[5].split(' ')[1][:5].split(':'))
                    if (int(hour) * 60 + int(minute)) < (entry_h * 60 + entry_m):
                        if not messagebox.askyesno("هشدار", f"ساعت خروج قبل از ساعت ورود است.\n\nآیا مطمئن هستید؟", parent=popup): return
            except: pass
            
            if entry_shamsi_date != current_shamsi:
                if not messagebox.askyesno("تأیید", "تاریخ ورود با امروز متفاوت است.\n\nآیا مطمئن هستید که می‌خواهید خروج ثبت کنید؟", parent=popup): return
                
            exit_time = f"{hour}:{minute}"
            try:
                with database.DBConnection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE visitors SET exit_time = ? WHERE id = ?",
                        (exit_time, visitor_id)
                    )              
                conn.commit()
                database.log_audit(
                    "visitor_exit_recorded",
                    visitor_id=visitor_id,
                    visitor_name=visitor_name,
                    exit_time=exit_time,
                    entry_shamsi_date=entry_shamsi_date,
                    operator=getattr(app, 'current_username', None)
                )
                popup.destroy(); fetch_and_display_records(current_filters)
                messagebox.showinfo("موفق", f"خروج {visitor_name} ثبت شد", parent=search_win)
            except Exception as e: messagebox.showerror("خطا", str(e), parent=popup)

        btn_frame = tb.Frame(p_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        tb.Button(btn_frame, text="انصراف", command=popup.destroy, bootstyle=(DANGER, OUTLINE)).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5, ipady=5)
        tb.Button(btn_frame, text="تایید خروج", command=save_exit, bootstyle=SUCCESS).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5, ipady=5)


    tree.bind("<Double-1>", on_tree_double_click)

    buttons_frame = tb.Frame(search_win, padding=15); buttons_frame.pack(fill=tk.X)
    tb.Button(buttons_frame, text="جستجو", command=search_action, bootstyle=PRIMARY, width=15).pack(side=tk.RIGHT, padx=5)
    tb.Button(buttons_frame, text="نمایش همه", command=reset_action, bootstyle=(SECONDARY, OUTLINE), width=15).pack(side=tk.RIGHT, padx=5)
    tb.Button(buttons_frame, text="خروجی اکسل", command=export_to_excel, bootstyle=SUCCESS, width=15).pack(side=tk.LEFT, padx=5)
    
    search_action()

def export_audit_log_excel(parent):
    ensure_fonts()

    popup = tb.Toplevel(parent)
    popup.title("خروجی اکسل لاگ حسابرسی")
    popup.geometry("480x340")
    popup.resizable(False, False)
    try:
        popup.iconbitmap(utils.resource_path('app_icon.ico'))
    except Exception:
        pass

    # ─── عنوان ───────────────────────────────────────────────
    tb.Label(
        popup,
        text="بازه تاریخ را وارد کنید",
        font=(FONT_MAIN, 13, "bold"),
        bootstyle=PRIMARY,
        anchor="center",
    ).pack(pady=(24, 16))

    # ─── ردیف تاریخ ─────────────────────────────────
    def _date_row(frm, label_text):
        row = tb.Frame(frm)
        row.pack(fill=tk.X, pady=6, padx=30)

        tb.Label(row, text=label_text, font=(FONT_MAIN, 11), width=10,
                 anchor="e").pack(side=tk.RIGHT)

        years  = [str(y) for y in range(1403, 1420)]
        months = config.PERSIAN_MONTHS
        days   = [str(d).zfill(2) for d in range(1, 32)]

        cb_day   = tb.Combobox(row, values=days,   width=4,  state="readonly",
                               font=(FONT_MAIN, 11))
        cb_month = tb.Combobox(row, values=months, width=8,  state="readonly",
                               font=(FONT_MAIN, 11))
        cb_year  = tb.Combobox(row, values=years,  width=7,  state="readonly",
                               font=(FONT_MAIN, 11))

        cb_day.pack(side=tk.LEFT, padx=3)
        cb_month.pack(side=tk.LEFT, padx=3)
        cb_year.pack(side=tk.LEFT, padx=3)

        import jdatetime
        today = jdatetime.date.today()
        cb_year.set(str(today.year))
        cb_month.set(config.PERSIAN_MONTHS[today.month - 1])
        cb_day.set(str(today.day).zfill(2))

        return cb_year, cb_month, cb_day

    # ─── فریم‌های تاریخ ─────────────────────────────────────
    date_frm = tb.Frame(popup)
    date_frm.pack(fill=tk.X)

    cy_start, cm_start, cd_start = _date_row(date_frm, ": از تاریخ")
    cy_end,   cm_end,   cd_end   = _date_row(date_frm, ": تا تاریخ")

    # ─── دکمه تولید اکسل ─────────────────────────────────────
    def _generate():
        def _month_num(name):
            if name in config.PERSIAN_MONTHS:
                return config.PERSIAN_MONTHS.index(name) + 1
            return 1

        start_str = (
            f"{cy_start.get()}/"
            f"{_month_num(cm_start.get()):02d}/"
            f"{cd_start.get()}"
        )
        end_str = (
            f"{cy_end.get()}/"
            f"{_month_num(cm_end.get()):02d}/"
            f"{cd_end.get()}"
        )

        if start_str > end_str:
            messagebox.showwarning(
                "خطای تاریخ",
                ".تاریخ شروع نمی‌تواند بعد از تاریخ پایان باشد",
                parent=popup,
            )
            return

        rows = database.get_audit_logs(start_str, end_str)

        if not rows:
            messagebox.showwarning(
                "نتیجه‌ای یافت نشد",
                f"هیچ لاگی در بازه\n{start_str}  تا  {end_str}\nوجود ندارد.",
                parent=popup,
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="ذخیره لاگ حسابرسی",
            initialfile=f"audit_{start_str.replace('/', '-')}_to_{end_str.replace('/', '-')}.xlsx",
            parent=popup,
        )
        if not file_path:
            return

        col_names = [
            "شناسه",
            "تاریخ (شمسی)", 
            "ساعت",
            "نوع رویداد",
            "نام کاربر",
            "شناسه مهمان",
            "نام مهمان", 
            "کد ملی",
            "ملاقات‌شونده",
            "واحد",
            "جزئیات",
            "تاریخ ایجاد"
        ]       

        try:
            df = pd.DataFrame(rows, columns=col_names)
            df.to_excel(file_path, index=False)
            messagebox.showinfo(
                "موفقیت",
                f"فایل اکسل با {len(rows)} رکورد ذخیره شد.",
                parent=popup,
            )
            popup.destroy()
        except Exception as e:
            messagebox.showerror(
                "خطا",
                f"خطا در ایجاد فایل اکسل:\n{e}",
                parent=popup,
            )

    tb.Button(
        popup,
        text="📥  تولید و ذخیره اکسل",
        command=_generate,
        bootstyle=SUCCESS,
    ).pack(pady=20, ipadx=10, ipady=6)

def open_change_password_window(parent, username):
    ensure_fonts()
    cp_win = tb.Toplevel(parent)
    cp_win.title("تغییر رمز عبور")
    cp_win.geometry("450x400")
    cp_win.resizable(False, False)
    try:
        cp_win.iconbitmap(utils.resource_path('app_icon.ico'))
    except:
        pass

    bg_path = utils.resource_path("change_password_bg.png")
    if os.path.exists(bg_path):
        try:
            original_img = Image.open(bg_path)
            resized_img = original_img.resize((450, 400), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(resized_img)
            bg_label = tk.Label(cp_win, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception:
            pass

    main_frame = tb.Frame(cp_win, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    tb.Label(
        main_frame,
        text="🔐 تغییر رمز عبور",
        font=(FONT_MAIN, 16, "bold"),
        bootstyle=PRIMARY,
        anchor="center"
    ).pack(pady=(10, 20))

    tb.Label(
        main_frame,
        text=f"کاربر: {username}",
        font=(FONT_MAIN, 12),
        bootstyle=SECONDARY,
        anchor="center"
    ).pack(pady=(0, 20))

    tb.Label(main_frame, text="رمز عبور فعلی:", font=(FONT_MAIN, 12)).pack(anchor="e", pady=(5, 2))
    current_pass_entry = tb.Entry(main_frame, show="●", justify="center", font=(FONT_MAIN, 12))
    current_pass_entry.pack(fill=tk.X, pady=(0, 10))
    current_pass_entry.focus()

    tb.Label(main_frame, text="رمز عبور جدید:", font=(FONT_MAIN, 12)).pack(anchor="e", pady=(5, 2))
    new_pass_entry = tb.Entry(main_frame, show="●", justify="center", font=(FONT_MAIN, 12))
    new_pass_entry.pack(fill=tk.X, pady=(0, 10))

    tb.Label(main_frame, text="تکرار رمز عبور جدید:", font=(FONT_MAIN, 12)).pack(anchor="e", pady=(5, 2))
    confirm_pass_entry = tb.Entry(main_frame, show="●", justify="center", font=(FONT_MAIN, 12))
    confirm_pass_entry.pack(fill=tk.X, pady=(0, 20))

    status_label = tb.Label(main_frame, text="", font=(FONT_MAIN, 11), bootstyle=INFO, anchor="center")
    status_label.pack(pady=(0, 10))

    def do_change():
        current_pw = current_pass_entry.get().strip()
        new_pw = new_pass_entry.get().strip()
        confirm_pw = confirm_pass_entry.get().strip()

        if not current_pw:
            status_label.config(text="❌ لطفاً رمز عبور فعلی را وارد کنید", bootstyle=DANGER)
            return
        if len(new_pw) < 3:
            status_label.config(text="❌ رمز عبور جدید باید حداقل ۳ کاراکتر باشد", bootstyle=DANGER)
            return
        if new_pw != confirm_pw:
            status_label.config(text="❌ تکرار رمز عبور مطابقت ندارد", bootstyle=DANGER)
            return

        success, _, _ = database.authenticate_user(username, current_pw)
        if not success:
            status_label.config(text="❌ رمز عبور فعلی اشتباه است", bootstyle=DANGER)
            return

        if database.change_user_password(username, new_pw):
            database.log_audit("user_password_changed", user=username)
            messagebox.showinfo("موفقیت", "✅ رمز عبور با موفقیت تغییر یافت", parent=cp_win)
            cp_win.destroy()
        else:
            status_label.config(text="❌ خطا در به‌روزرسانی رمز عبور", bootstyle=DANGER)

    # Buttons
    btn_frame = tb.Frame(main_frame)
    btn_frame.pack(fill=tk.X, pady=(10, 0))

    tb.Button(
        btn_frame,
        text="انصراف",
        command=cp_win.destroy,
        bootstyle=(SECONDARY, OUTLINE),
        width=12
    ).pack(side=tk.RIGHT, padx=5)

    tb.Button(
        btn_frame,
        text="تغییر رمز",
        command=do_change,
        bootstyle=SUCCESS,
        width=12
    ).pack(side=tk.RIGHT, padx=5)

    cp_win.bind('<Return>', lambda e: do_change())

def open_developer_mode(app):
    ensure_fonts()
    dev_win = tb.Toplevel(app)
    dev_win.title("پنل مدیریت")
    dev_win.geometry("400x700")
    dev_win.resizable(False,False)
    try: dev_win.iconbitmap(utils.resource_path('app_icon.ico'))
    except: pass

    bg_path = utils.resource_path("developer.png")
    if os.path.exists(bg_path):
        try:
            original_img = Image.open(bg_path)
            resized_img = original_img.resize((400, 700), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(resized_img)
            bg_label = tk.Label(dev_win, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception: pass

    tb.Label(dev_win, text="ابزارهای مدیریت سیستم", font=(FONT_MAIN, 12, "bold"), bootstyle=PRIMARY).pack(pady=(40, 30))
    
    buttons = [
        ("مدیریت کاربران", lambda: open_user_manager(dev_win, app=app, current_user=app.current_username), PRIMARY),
        ("تعداد ورودی/خروجی های ثبت شده", lambda: show_daily_stats_ui(dev_win), INFO),
        ("نمودار تحلیل ترافیک", lambda: show_heatmap_analytics(app), WARNING),
        ("لاگ حسابرسی (خروجی اکسل)",lambda: export_audit_log_excel(dev_win),INFO),
        ("تهیه نسخه پشتیبان", utils.create_backup, SECONDARY),
        ("بازیابی اطلاعات", utils.restore_backup, SECONDARY),
        ("افزودن ۱۰۰ رکورد آزمایشی", database.add_dummy_data, (SUCCESS, OUTLINE)),
        #("حذف رکوردهای آزمایشی", database.delete_dev_records, (DANGER, OUTLINE)), #For deleting test records only.
        ("پاکسازی کامل دیتابیس", database.delete_all_records, DANGER)
    ]
    
    for text, cmd, style in buttons:
        tb.Button(dev_win, text=text, command=cmd, bootstyle=style).pack(fill=tk.X, pady=8, padx=40, ipady=5)
    
    tb.Label(dev_win, text="⚠️ مخصوص راهبر سیستم و پشتیبانی", font=(FONT_MAIN, 10), bootstyle=SECONDARY).pack(side=tk.BOTTOM, pady=10)

#main.py : 

import tkinter as tk
from tkinter import messagebox, font
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import sqlite3
import os
import random
import threading
from datetime import datetime
import jdatetime
from PIL import Image, ImageTk

# Local modules
import config
import database
import utils
import widgets
import windows
import printer

# --- Main Application Setup ---
app = tb.Window(themename="lumen")
app.title(f"سامانه مدیریت ورود و خروج (اداره حراست) - نسخه {config.APP_VERSION}")
app.geometry("1050x600")
app.resizable(False, False)

try:
    icon_path = utils.resource_path('app_icon.ico')
    app.iconbitmap(icon_path)
    app.iconbitmap(default=icon_path)
except Exception: 
    pass

# --- FONT SAFETY CHECK ---
available_fonts = font.families()
FONT_MAIN = "B Titr" if "B Titr" in available_fonts else "Tahoma"
FONT_TABLE = "B Nazanin" if "B Nazanin" in available_fonts else "Tahoma"

# --- BACKGROUND FUNCTION ---
def setup_background(window_root):
    bg_path = utils.resource_path("background.png")
    if not os.path.exists(bg_path): return
    try:
        window_root.original_img = Image.open(bg_path)
        bg_label = tk.Label(window_root)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        def resize_image(event):
            if event.widget == window_root:
                new_w, new_h = event.width, event.height
                if new_w < 50 or new_h < 50: return
                resized = window_root.original_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized)
                bg_label.config(image=photo)
                bg_label.image = photo 
                
        window_root.bind('<Configure>', resize_image)
        bg_label.lower()
    except Exception as e: print(f"Background Error: {e}")

setup_background(app)

# --- LIVE CLOCK & DATE DASHBOARD ---
def update_live_clock():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    j_date = jdatetime.date.fromgregorian(date=now.date())
    persian_date_str = j_date.strftime("%Y/%m/%d")
    
    live_clock_label.config(text=f"{persian_date_str}   -   {current_time}")
    live_clock_label.after(1000, update_live_clock)

live_clock_label = tb.Label(
    app, 
    text="", 
    font=(FONT_MAIN, 14, "bold"),
    bootstyle=PRIMARY       
)
live_clock_label.place(relx=1.0, y=20, anchor="ne", x=-30)
live_clock_label.lift()
update_live_clock()

# --- HELPER UI FUNCTIONS ---
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")

def clear_fields():
    entry_visitor_name.delete(0, tk.END); entry_national_id.delete(0, tk.END)
    entry_employee_to_meet.delete(0, tk.END); combo_department.set("")
    entry_national_id.configure(bootstyle=DEFAULT) 
    entry_visitor_name.configure(bootstyle=DEFAULT)
    entry_national_id.focus()

def auto_fill_department(employee_name):
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT department FROM visitors WHERE employee_to_meet = ? ORDER BY id DESC LIMIT 1", (employee_name,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0]: combo_department.set(result[0])
    except: pass

def update_employee_suggestions():
    try:
        names = database.get_employee_suggestions() 
        entry_employee_to_meet.set_completion_list(names)
    except: pass

def check_returning_visitor(event):
    nid = entry_national_id.get().strip()
    if len(nid) < 5: return
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT visitor_name FROM visitors WHERE national_id = ? ORDER BY id DESC LIMIT 1", (nid,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            if not entry_visitor_name.get():
                entry_visitor_name.delete(0, tk.END)
                entry_visitor_name.insert(0, result[0])
    except: pass

# --- VALIDATION WRAPPERS ---
def validate_national_id_on_exit():
    nid = entry_national_id.get().strip()
    if nid and len(nid) == 10:
        is_valid, error_msg = utils.validate_national_id(nid)
        if not is_valid:
            entry_national_id.configure(bootstyle=WARNING)
            show_status(f"⚠️ {error_msg} (می‌توانید ادامه دهید)", "orange", duration=5000)
        else:
            entry_national_id.configure(bootstyle=SUCCESS)
            check_returning_visitor(None)
    elif nid:
        entry_national_id.configure(bootstyle=WARNING)
        show_status("⚠️ کد ملی باید ۱۰ رقمی باشد (می‌توانید ادامه دهید)", "orange", duration=5000)
    else:
        entry_national_id.configure(bootstyle=DEFAULT)

def validate_visitor_name_on_exit():
    name = entry_visitor_name.get().strip()
    if name and len(name) > 0:
        is_valid, error_msg = utils.validate_persian_name(name)
        if not is_valid and len(name) >= 2:
            entry_visitor_name.configure(bootstyle=DANGER)
            show_status(f"⚠️ {error_msg}", "red", duration=3000)
        else:
            entry_visitor_name.configure(bootstyle=DEFAULT)

def on_national_id_enter(event):
    nid = entry_national_id.get().strip()
    target_widget = entry_visitor_name
    
    if len(nid) >= 5:
        try:
            conn = sqlite3.connect(config.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT visitor_name FROM visitors WHERE national_id = ? ORDER BY id DESC LIMIT 1", (nid,))
            result = cursor.fetchone()
            conn.close()
            if result:
                if not entry_visitor_name.get():
                    entry_visitor_name.delete(0, tk.END)
                    entry_visitor_name.insert(0, result[0])
                target_widget = entry_employee_to_meet
        except: pass
    target_widget.focus_set()
    return "break"

# --- SUBMISSION LOGIC ---
def submit_visitor():
    visitor_name = entry_visitor_name.get().strip()
    national_id = entry_national_id.get().strip()
    employee_to_meet = entry_employee_to_meet.get().strip()
    department = combo_department.get()
    if not all([visitor_name, national_id, employee_to_meet, department]):
        messagebox.showwarning("خطا", "لطفاً تمام اطلاعات را وارد کنید")
        entry_national_id.focus_set() if not national_id else entry_visitor_name.focus_set()
        return
    
    is_valid, error_msg = utils.validate_national_id(national_id)
    if not is_valid:
        response = messagebox.askyesno("هشدار کد ملی", f"{error_msg}\n\nآیا مطمئن هستید که می‌خواهید ادامه دهید؟")
        if not response:
            entry_national_id.focus_set()
            entry_national_id.select_range(0, tk.END)
            return
    
    if len(visitor_name) < 3:
        messagebox.showwarning("خطا", "نام باید حداقل ۳ کاراکتر باشد")
        return

    if len(employee_to_meet) < 3:
        messagebox.showwarning("خطا", "نام ملاقات شونده باید حداقل ۳ کاراکتر باشد")
        return

    current_shamsi_date = jdatetime.date.fromgregorian(date=datetime.now().date()).strftime("%Y/%m/%d")
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM visitors 
            WHERE national_id = ? AND employee_to_meet = ? AND shamsi_date = ? AND (exit_time IS NULL OR exit_time = '') LIMIT 1
        ''', (national_id, employee_to_meet, current_shamsi_date))
        duplicate = cursor.fetchone()
        conn.close()

        if duplicate:
            if not messagebox.askyesno("تکرار ورود", "امروز قبلاً ثبت شده است. آیا مطمئن هستید؟"): return
    except: pass
    now = datetime.now()
    entry_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    shamsi_date_str = jdatetime.date.fromgregorian(date=now.date()).strftime("%Y/%m/%d")
    registrar = getattr(app, 'current_user', 'سیستم') 
    username = getattr(app, 'current_username', 'سیستم')
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO visitors (visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, created_by) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (visitor_name, national_id, employee_to_meet, department, entry_time_str, shamsi_date_str, registrar))
        
        visitor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        database.log_audit(
            "visitor_added",
            user=username,
            visitor_id=visitor_id,
            visitor_name=visitor_name,
            national_id=national_id,
            employee_to_meet=employee_to_meet,
            department=department,
            entry_time=entry_time_str,
            shamsi_date=shamsi_date_str
        )
        
        threading.Thread(target=printer.print_receipt, args=(visitor_id, visitor_name, national_id, employee_to_meet, department, now, shamsi_date_str), daemon=True).start()
        show_success_overlay(card_frame)
        clear_fields()
        show_status(f"✓ ورود مهمان با شماره {visitor_id} با موفقیت ثبت شد", "green", duration=10000)
        update_employee_suggestions()
    except sqlite3.Error as e:
        database.log_audit("visitor_entry_failed",
            visitor_name=visitor_name, 
            national_id=national_id, 
            error=str(e))
        messagebox.showerror("خطای پایگاه داده", f"خطا در ثبت اطلاعات: {e}")

# --- CENTRAL CARD CONTAINER ---
card_frame = tb.Frame(app, padding=15)
card_frame.place(relx=0.5, rely=0.46, anchor="center", width=420, height=480)

header_lbl = tb.Label(card_frame, text="🛡️(سامانه ثبت ورود و خروج (اداره حراست💻", font=(FONT_MAIN, 16, "bold"), anchor="center")
header_lbl.grid(row=0, column=0, columnspan=2, pady=(5, 15), sticky="ew")

labels = {": شماره کارت ملی 🆔": 1, ": نام ملاقات کننده 🙋": 2, ": نام ملاقات شونده 👔": 3, ": امور / واحد مربوطه 🏢": 4}
for text, row in labels.items():
    tb.Label(card_frame, text=text, font=(FONT_MAIN, 12)).grid(row=row, column=1, padx=(10, 20), pady=6, sticky="e")

# 1. Create Widgets
vcmd = (app.register(utils.validate_numeric), '%P')

entry_national_id = tb.Entry(card_frame, justify='right', font=(FONT_MAIN, 12), validate='key', validatecommand=vcmd)
entry_national_id.bind("<FocusOut>", lambda e: (check_returning_visitor(e), validate_national_id_on_exit()))
entry_national_id.bind("<Return>", on_national_id_enter) 

entry_visitor_name = tb.Entry(card_frame, justify='right', font=(FONT_MAIN, 12))
entry_visitor_name.bind("<Return>", focus_next_widget)
entry_visitor_name.bind("<FocusOut>", lambda e: validate_visitor_name_on_exit())

entry_employee_to_meet = widgets.AutocompleteEntry(card_frame, justify='right', font=(FONT_MAIN, 12), selection_callback=auto_fill_department)
combo_department = tb.Combobox(card_frame, values=config.DEPARTMENT_LIST, justify='right', state='readonly', font=(FONT_MAIN, 12))
combo_department.bind("<Return>", focus_next_widget)

# 2. Place Widgets
entry_national_id.grid(row=1, column=0, sticky="ew", padx=(10, 5), pady=6)
entry_visitor_name.grid(row=2, column=0, sticky="ew", padx=(10, 5), pady=6)
entry_employee_to_meet.grid(row=3, column=0, sticky="ew", padx=(10, 5), pady=6)
combo_department.grid(row=4, column=0, sticky="ew", padx=(10, 5), pady=6)
card_frame.grid_columnconfigure(0, weight=1)

# 3. Buttons
btn_frame = tb.Frame(card_frame)
btn_frame.grid(row=5, column=0, columnspan=2, pady=(15, 10), sticky="ew")

tb.Button(btn_frame, text="ثبت و چاپ رسید✅", command=submit_visitor, bootstyle=SUCCESS).pack(pady=4, fill=tk.X)
tb.Button(btn_frame, text="مشاهده و جستجوی سوابق📚", command=lambda: windows.open_search_window(app), bootstyle=PRIMARY).pack(pady=4, fill=tk.X)
tb.Button(btn_frame, text="راهنما📑", command=windows.show_help_popup, bootstyle=SECONDARY).pack(pady=4, fill=tk.X)

# --- LOGIN & MENU SETUP ---
def setup_dashboard(username, role, full_name):
    app.deiconify()
    app.current_user = full_name
    app.current_username = username
    app.title(f"سامانه مدیریت ورود و خروج (اداره حراست)   |   کاربر: {full_name}")
    
    menubar = tk.Menu(app)
    if role == 'admin':
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="پنل مدیریت (Admin)", command=lambda: windows.open_developer_mode(app))
        menubar.add_cascade(label="تنظیمات سیستم", menu=tools_menu)
    
        user_menu = tk.Menu(menubar, tearoff=0)

    def change_password():
        windows.open_change_password_window(app, app.current_username)

    def logout():
        database.log_audit("logout", user=getattr(app, "current_username", None))
        app.withdraw()
        windows.show_login_screen(app, setup_dashboard)

    user_menu.add_command(label="تغییر رمز عبور", command=change_password)
    user_menu.add_separator()
    user_menu.add_command(label="خروج از حساب", command=logout)
    menubar.add_cascade(label=f"حساب کاربری: {full_name}", menu=user_menu)
    app.config(menu=menubar)

try:
    for widget in [entry_visitor_name, combo_department]:
        widget.bind("<Return>", focus_next_widget)
except NameError: pass

# --- STATUS BAR & QUOTE SYSTEM ---
status_bar = tb.Label(
    app, 
    text="  با سلام - به سامانه مدیریت مراجعین (اداره حراست) خوش آمدید", 
    anchor=tk.E, 
    font=(FONT_MAIN, 12), 
    padding=2,
    bootstyle="inverse-light"
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

cycle_timer_id = None
def cycle_cultural_messages():
    global cycle_timer_id
    quote = random.choice(config.CULTURAL_MESSAGES)
    status_bar.config(text=f"  {quote}", foreground="#555555")
    cycle_timer_id = app.after(30000, cycle_cultural_messages)

def start_quote_cycle():
    global cycle_timer_id
    cycle_timer_id = app.after(30000, cycle_cultural_messages)

def show_status(message, color="#555555", duration=10000):
    global cycle_timer_id
    if cycle_timer_id:
        app.after_cancel(cycle_timer_id)
        cycle_timer_id = None
    status_bar.config(text=f"  {message}", foreground=color)
    def return_to_quotes(): cycle_cultural_messages()
    app.after(duration, return_to_quotes)

def show_success_overlay(parent):
    parent.update_idletasks()
    x = parent.winfo_rootx()
    y = parent.winfo_rooty()
    w = parent.winfo_width()
    h = parent.winfo_height()

    overlay = tk.Toplevel(parent)
    overlay.overrideredirect(True)
    overlay.geometry(f"{w}x{h}+{x}+{y}")
    overlay.wm_attributes("-alpha", 0.0)
    overlay.configure(bg="#198754")

    inner = tk.Frame(overlay, bg="#198754")
    inner.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(inner, text="✓", font=("Segoe UI", 52, "bold"),
             bg="#198754", fg="white").pack()
    tk.Label(inner, text="ثبت شد", font=("Segoe UI", 18, "bold"),
             bg="#198754", fg="white").pack(pady=(4, 0))

    #SLOWER ANIMATION :
    def fade(alpha, direction):
        alpha = round(alpha + direction * 0.04, 2)
        if direction == 1 and alpha >= 0.88:
            overlay.wm_attributes("-alpha", 0.88)
            overlay.after(1000, lambda: fade(0.88, -1))
        elif direction == -1 and alpha <= 0.0:
            overlay.destroy()
        else:
            overlay.wm_attributes("-alpha", alpha)
            overlay.after(30, lambda: fade(alpha, direction))

    fade(0.0, 1)

def on_app_close():
    database.log_audit("logout", user=getattr(app, "current_username", None))
    database.log_audit("app_closed", user=getattr(app, "current_username", None))
    app.destroy()
app.protocol("WM_DELETE_WINDOW", on_app_close)

if __name__ == "__main__":
    database.setup_database()
    database.setup_audit_table()
    update_employee_suggestions()
    start_quote_cycle()
    app.withdraw()
    windows.show_login_screen(app, setup_dashboard)
    app.mainloop()