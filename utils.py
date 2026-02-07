import os
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