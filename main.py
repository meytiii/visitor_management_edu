import tkinter as tk
from tkinter import ttk, messagebox, font
import sqlite3
import os
import random
import threading
from datetime import datetime
import jdatetime
from PIL import Image, ImageTk

# Import local modules
import config
import database
import utils
import widgets
import windows
import printer

# --- Main Application Setup ---
app = tk.Tk()
app.title(f"سامانه مدیریت ورود و خروج (اداره حراست) - نسخه {config.APP_VERSION}")
app.geometry("1050x600")
app.resizable(False, False)
app.configure(bg=config.DEFAULT_BG_COLOR)
try: app.iconbitmap('app_icon.ico')
except Exception: pass

# --- FONT SAFETY CHECK ---
available_fonts = font.families()
if "B Titr" in available_fonts: FONT_MAIN = "B Titr"
else: FONT_MAIN = "Tahoma"

if "B Nazanin" in available_fonts: FONT_TABLE = "B Nazanin"
else: FONT_TABLE = "Tahoma"

style = ttk.Style(app); style.theme_use("vista")
style.configure(".", font=(FONT_MAIN, 13), background=config.DEFAULT_BG_COLOR)
style.configure("TLabel", anchor="east"); style.configure("TFrame", background=config.DEFAULT_BG_COLOR)

# --- BACKGROUND FUNCTION ---
def setup_background(window_root):
    if not os.path.exists("background.png"): return
    try:
        window_root.original_img = Image.open("background.png")
        bg_label = tk.Label(window_root)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        def resize_image(event):
            if event.widget == window_root:
                new_w, new_h = event.width, event.height
                if new_w < 50 or new_h < 50: return
                resized = window_root.original_img.resize((new_w, new_h), Image.BICUBIC)
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

live_clock_label = tk.Label(
    app, 
    text="", 
    font=(FONT_MAIN, 14, "bold"),
    bg=config.DEFAULT_BG_COLOR,
    fg="#00695C"       
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
    entry_national_id.focus()

def auto_fill_department(employee_name):
    """Finds the most recent department for the selected employee and fills the combobox."""
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT department FROM visitors WHERE employee_to_meet = ? ORDER BY id DESC LIMIT 1", (employee_name,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            combo_department.set(result[0])
    except: pass

def update_employee_suggestions():
    """Reads employee names, sorted by how often they receive visitors (Popularity)."""
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT employee_to_meet, COUNT(*) as cnt 
            FROM visitors 
            WHERE employee_to_meet != '' 
            GROUP BY employee_to_meet 
            ORDER BY cnt DESC
        ''')
        names = [row[0] for row in cursor.fetchall()]
        conn.close()
        
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
    """Validate national ID when field loses focus - WARN but don't block"""
    nid = entry_national_id.get().strip()
    
    if nid and len(nid) == 10:
        is_valid, error_msg = utils.validate_national_id(nid)
        
        if not is_valid:
            entry_national_id.configure(foreground="orange")
            show_status(f"⚠️ {error_msg} (می‌توانید ادامه دهید)", "#FF9800", duration=5000)
        else:
            entry_national_id.configure(foreground="green")
            check_returning_visitor(None)
    elif nid:
        entry_national_id.configure(foreground="orange")
        show_status("⚠️ کد ملی باید ۱۰ رقمی باشد (می‌توانید ادامه دهید)", "#FF9800", duration=5000)
    else:
        entry_national_id.configure(foreground="black")

def validate_visitor_name_on_exit():
    """Validate visitor name when field loses focus"""
    name = entry_visitor_name.get().strip()
    if name and len(name) > 0:
        is_valid, error_msg = utils.validate_persian_name(name)
        
        if not is_valid and len(name) >= 2:
            entry_visitor_name.configure(foreground="red")
            show_status(f"⚠️ {error_msg}", "#D32F2F", duration=3000)
        else:
            entry_visitor_name.configure(foreground="black")

def on_national_id_enter(event):
    """
    Handles Enter Key on National ID:
    - FOUND: Auto-fill Name -> Jump to Employee (Skip Name)
    - NEW: Jump to Visitor Name
    """
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
        response = messagebox.askyesno(
            "هشدار کد ملی",
            f"{error_msg}\n\nآیا مطمئن هستید که می‌خواهید ادامه دهید؟\n\n"
            f"✅ اگر کد ملی درست است، ادامه دهید\n"
            f"❌ اگر اشتباه وارد کرده‌اید، لغو کنید و اصلاح نمایید"
        )
        if not response:
            entry_national_id.focus_set()
            entry_national_id.select_range(0, tk.END)
            return
    
    if len(visitor_name) < 3:
        messagebox.showwarning("خطا", "نام باید حداقل ۳ کاراکتر باشد")
        entry_visitor_name.focus_set()
        entry_visitor_name.select_range(0, tk.END)
        return
    
    if len(employee_to_meet) < 3:
        messagebox.showwarning("خطا", "نام ملاقات شونده باید حداقل ۳ کاراکتر باشد")
        entry_employee_to_meet.focus_set()
        entry_employee_to_meet.select_range(0, tk.END)
        return
    
    current_shamsi_date = jdatetime.date.fromgregorian(date=datetime.now().date()).strftime("%Y/%m/%d")
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM visitors 
            WHERE national_id = ? 
            AND employee_to_meet = ? 
            AND shamsi_date = ?
            AND (exit_time IS NULL OR exit_time = '')
            LIMIT 1
        ''', (national_id, employee_to_meet, current_shamsi_date))
        duplicate = cursor.fetchone()
        conn.close()
        
        if duplicate:
            response = messagebox.askyesno(
                "تکرار ورود",
                f"آیا مطمئن هستید که می‌خواهید ورود مجدد ثبت کنید؟\n\n"
                f"کد ملی {national_id} برای ملاقات با {employee_to_meet}\n"
                f"امروز قبلاً ثبت شده است (ثبت شماره {duplicate[0]})."
            )
            if not response:
                return
    except:
        pass
    
    now = datetime.now()
    entry_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    shamsi_date_str = jdatetime.date.fromgregorian(date=now.date()).strftime("%Y/%m/%d")
    
    # --- GET CURRENT USER ---
    registrar = getattr(app, 'current_user', 'سیستم') 
    
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        # --- UPDATED SQL TO INCLUDE created_by ---
        cursor.execute('''
            INSERT INTO visitors (visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, created_by) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (visitor_name, national_id, employee_to_meet, department, entry_time_str, shamsi_date_str, registrar))
        
        visitor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # --- Run printing in background thread ---
        print_thread = threading.Thread(
            target=printer.print_receipt, 
            args=(visitor_id, visitor_name, national_id, employee_to_meet, department, now, shamsi_date_str),
            daemon=True
        )
        print_thread.start()
        # -----------------------------------------
        
        clear_fields()
        
        show_status(f"✓ ورود مهمان با شماره {visitor_id} با موفقیت ثبت شد", "#2E7D32", duration=10000)
        update_employee_suggestions()
    except sqlite3.Error as e:
        messagebox.showerror("خطای پایگاه داده", f"خطا در ثبت اطلاعات: {e}")

# --- CENTRAL CARD CONTAINER ---
card_frame = tk.Frame(app, bg=config.CARD_BG_COLOR, bd=2, relief="groove")
card_frame.place(relx=0.5, rely=0.5, anchor="center", width=410, height=530)
header_lbl = tk.Label(card_frame, text="(سامانه ثبت ورود و خروج (اداره حراست", font=(FONT_MAIN, 16, "bold"), bg=config.CARD_BG_COLOR, fg="#37474F")
header_lbl.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky="ew")

labels = {": شماره کارت ملی": 1, ": نام ملاقات کننده": 2, ": نام ملاقات شونده": 3, ": امور / واحد مربوطه": 4}
for text, row in labels.items():
    tk.Label(card_frame, text=text, font=(FONT_MAIN, 13), bg=config.CARD_BG_COLOR, fg="black", anchor="e").grid(row=row, column=1, padx=(10, 30), pady=10, sticky="e")

# 1. Create Widgets
vcmd = (app.register(utils.validate_numeric), '%P')

entry_national_id = ttk.Entry(card_frame, justify='right', font=(FONT_MAIN, 13), validate='key', validatecommand=vcmd)
entry_national_id.bind("<FocusOut>", lambda e: (check_returning_visitor(e), validate_national_id_on_exit()))
entry_national_id.bind("<Return>", on_national_id_enter) 

entry_visitor_name = ttk.Entry(card_frame, justify='right', font=(FONT_MAIN, 13))
entry_visitor_name.bind("<Return>", focus_next_widget)
entry_visitor_name.bind("<FocusOut>", lambda e: validate_visitor_name_on_exit())

entry_employee_to_meet = widgets.AutocompleteEntry(
    card_frame, 
    justify='right', 
    font=(FONT_MAIN, 13),
    selection_callback=auto_fill_department
)

combo_department = ttk.Combobox(card_frame, values=config.DEPARTMENT_LIST, justify='right', state='readonly', font=(FONT_MAIN, 12))
combo_department.bind("<Return>", focus_next_widget)

# 2. Place Widgets (Grid)
entry_national_id.grid(row=1, column=0, sticky="ew", padx=(30, 5), pady=10)      # Top
entry_visitor_name.grid(row=2, column=0, sticky="ew", padx=(30, 5), pady=10)     # Second
entry_employee_to_meet.grid(row=3, column=0, sticky="ew", padx=(30, 5), pady=10) # Third
combo_department.grid(row=4, column=0, sticky="ew", padx=(30, 5), pady=10)       # Fourth
card_frame.grid_columnconfigure(0, weight=1)

# 3. Buttons
btn_frame = tk.Frame(card_frame, bg=config.CARD_BG_COLOR)
btn_frame.grid(row=5, column=0, columnspan=2, pady=(30, 20), sticky="ew")

widgets.RoundedButton(
    btn_frame,
    text="ثبت و چاپ رسید",
    command=submit_visitor,
    bg=config.GREEN_COLOR,
    hover_bg=config.GREEN_ACTIVE_COLOR,
    font=(FONT_MAIN, 13, "bold")
).pack(pady=6)

widgets.RoundedButton(
    btn_frame,
    text="مشاهده و جستجوی سوابق",
    command=lambda: windows.open_search_window(app),
    bg=config.BLUE_COLOR,
    hover_bg=config.BLUE_ACTIVE_COLOR,
    font=(FONT_MAIN, 12)
).pack(pady=6)

widgets.RoundedButton(
    btn_frame,
    text="راهنما",
    command=windows.show_help_popup,
    bg="#607D8B",
    hover_bg="#546E7A",
    font=(FONT_MAIN, 12)
).pack(pady=6)

# --- LOGIN & MENU SETUP ---
def setup_dashboard(username, role, full_name):
    """
    Called after successful login.
    """
    app.deiconify()
    
    app.current_user = full_name 
    
    app.title(f"سامانه مدیریت ورود و خروج (اداره حراست)   |   کاربر: {full_name}")
    
    menubar = tk.Menu(app)
    
    # 1. Admin Menu (Only for Admins)
    if role == 'admin':
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="پنل مدیریت (Admin)", command=lambda: windows.open_developer_mode(app))
        menubar.add_cascade(label="تنظیمات سیستم", menu=tools_menu)
    
    # 2. Guard Menu (For Everyone)
    guard_menu = tk.Menu(menubar, tearoff=0)
    guard_menu.add_command(label="دفتر ثبت وقایع", command=lambda: windows.open_shift_log_window(app))
    menubar.add_cascade(label="امور نگهبانی", menu=guard_menu)
    
    # 3. Logout Option
    user_menu = tk.Menu(menubar, tearoff=0)
    
    def logout():
        for widget in app.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        
        app.withdraw()
        windows.show_login_screen(app, setup_dashboard)
        
    user_menu.add_command(label="خروج از حساب", command=logout)
    menubar.add_cascade(label=f"حساب کاربری: {full_name}", menu=user_menu)

    app.config(menu=menubar)

# --- QoL: Press Enter to move to next field ---
try:
    for widget in [entry_visitor_name, combo_department]:
        widget.bind("<Return>", focus_next_widget)
except NameError: pass

# --- STATUS BAR & QUOTE SYSTEM ---
status_bar = tk.Label(
    app, 
    text="", 
    bd=1, 
    relief=tk.SUNKEN, 
    anchor=tk.E, 
    font=(FONT_MAIN, 11), 
    bg="#E0E0E0",
    padx=10,
    fg="#555555"
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)
status_bar.config(text="  با سلام - به سامانه مدیریت مراجعین (اداره حراست) خوش آمدید")

cycle_timer_id = None
def cycle_cultural_messages():
    """Updates the status bar with a random quote and resets the 30s timer."""
    global cycle_timer_id
    quote = random.choice(config.CULTURAL_MESSAGES)
    status_bar.config(text=f"  {quote}", fg="#555555")
    cycle_timer_id = app.after(30000, cycle_cultural_messages)

def start_quote_cycle():
    """Starts the initial delay for quotes."""
    global cycle_timer_id
    cycle_timer_id = app.after(30000, cycle_cultural_messages)

def show_status(message, color="black", duration=10000):
    """Displays a priority message."""
    global cycle_timer_id
    if cycle_timer_id:
        app.after_cancel(cycle_timer_id)
        cycle_timer_id = None
    status_bar.config(text=f"  {message}", fg=color)
    def return_to_quotes():
        cycle_cultural_messages()
    app.after(duration, return_to_quotes)

# --- QoL: ACTIVE FIELD HIGHLIGHTING ---
def on_focus_in(event):
    event.widget.configure(bg="#E3F2FD")
def on_focus_out(event):
    event.widget.configure(bg="white")

all_inputs = [entry_visitor_name, entry_national_id, entry_employee_to_meet, combo_department]
for widget in all_inputs:
    widget.bind("<FocusIn>", on_focus_in, add="+")
    widget.bind("<FocusOut>", on_focus_out, add="+")

if __name__ == "__main__":
    database.setup_database()
    
    update_employee_suggestions()
    start_quote_cycle()
    
    app.withdraw()
    
    windows.show_login_screen(app, setup_dashboard)
    
    app.mainloop()