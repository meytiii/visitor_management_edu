import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
from datetime import datetime
import os
import shutil
import jdatetime
import random
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- IMPORTS FROM OTHER FILES ---
from config import *
from database import setup_database
from components import AutocompleteEntry
from utils import make_farsi, validate_numeric, focus_next_widget, print_receipt

# --- HELPER LOGIC FUNCTIONS ---

def show_help_popup():
    help_text = f"در صورت بروز هرگونه مشکل یا سوال با شماره زیر تماس بگیرید\n\nخرّم آبادی - 09222550573\n\nنسخه برنامه {APP_VERSION}"
    messagebox.showinfo("راهنما", help_text)

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

def update_employee_suggestions():
    try:
        conn = sqlite3.connect(DB_PATH)
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
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT visitor_name FROM visitors WHERE national_id = ? ORDER BY id DESC LIMIT 1", (nid,))
        result = cursor.fetchone()
        conn.close()
        if result:
            if not entry_visitor_name.get():
                entry_visitor_name.delete(0, tk.END)
                entry_visitor_name.insert(0, result[0])
    except: pass

def clear_fields():
    entry_visitor_name.delete(0, tk.END); entry_national_id.delete(0, tk.END)
    entry_employee_to_meet.delete(0, tk.END); combo_department.set("")
    entry_visitor_name.focus()

# --- STATUS BAR LOGIC ---
def cycle_cultural_messages():
    current_color = status_bar.cget("fg")
    if current_color == "#555555": 
        quote = random.choice(CULTURAL_MESSAGES)
        status_bar.config(text=f"  {quote}", fg="#555555")
    app.after(20000, cycle_cultural_messages)

def show_status(message, color="black", duration=5000):
    status_bar.config(text=f"  {message}", fg=color)
    def return_to_quotes():
        quote = random.choice(CULTURAL_MESSAGES)
        status_bar.config(text=f"  {quote}", fg="#555555")
    app.after(duration, return_to_quotes)

def submit_visitor():
    visitor_name = entry_visitor_name.get()
    national_id = entry_national_id.get()
    employee_to_meet = entry_employee_to_meet.get()
    department = combo_department.get()
    if not all([visitor_name, national_id, employee_to_meet, department]):
        messagebox.showwarning("خطا", "لطفاً تمام اطلاعات را وارد کنید")
        return
    now = datetime.now()
    entry_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    shamsi_date_str = jdatetime.date.fromgregorian(date=now.date()).strftime("%Y/%m/%d")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO visitors (visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date) VALUES (?, ?, ?, ?, ?, ?)',
                       (visitor_name, national_id, employee_to_meet, department, entry_time_str, shamsi_date_str))
        visitor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print_receipt(visitor_id, visitor_name, national_id, employee_to_meet, department, now, shamsi_date_str)
        clear_fields()
        show_status(f"✓ ورود مهمان با شماره {visitor_id} با موفقیت ثبت شد", "#2E7D32")
        update_employee_suggestions()
    except sqlite3.Error as e:
        messagebox.showerror("خطای پایگاه داده", f"خطا در ثبت اطلاعات: {e}")

# --- WINDOW FUNCTIONS ---

def ask_dev_password():
    pwd_win = tk.Toplevel(app)
    pwd_win.title("Security Check"); pwd_win.geometry("300x180")
    try: pwd_win.iconbitmap('app_icon.ico')
    except: pass
    pwd_win.configure(bg=BLUE_COLOR)
    
    x = app.winfo_x() + (app.winfo_width() // 2) - 150
    y = app.winfo_y() + (app.winfo_height() // 2) - 90
    pwd_win.geometry(f"+{x}+{y}")
    tk.Label(pwd_win, text=":رمز عبور را وارد کنید", bg=BLUE_COLOR, fg="white", font=(FONT_MAIN, 11)).pack(pady=15)
    ent_pass = tk.Entry(pwd_win, show="●", justify="center", font=(FONT_MAIN, 11))
    ent_pass.pack(pady=5); ent_pass.focus()
    def check():
        if ent_pass.get() == get_current_password():
            pwd_win.destroy()
            open_developer_mode()
        else:
            messagebox.showerror("Access Denied", "رمز عبور اشتباه است", parent=pwd_win)
            ent_pass.delete(0, tk.END)
    tk.Button(pwd_win, text="ورود", command=check, bg="white", fg=BLUE_COLOR, font=(FONT_MAIN, 10, "bold"), width=10).pack(pady=15)
    pwd_win.bind('<Return>', lambda e: check())

def change_password_ui(parent_win):
    cp_win = tk.Toplevel(parent_win)
    cp_win.title("Change Password"); cp_win.geometry("350x300")
    try: cp_win.iconbitmap('app_icon.ico')
    except: pass
    cp_win.configure(bg=BLUE_COLOR)
    
    def create_field(label_text):
        tk.Label(cp_win, text=label_text, bg=BLUE_COLOR, fg="white", font=(FONT_MAIN, 10)).pack(pady=(10, 0))
        entry = tk.Entry(cp_win, show="●", justify="center", font=(FONT_MAIN, 10))
        entry.pack(pady=5)
        return entry
    ent_old = create_field("رمز عبور فعلی:")
    ent_new = create_field("رمز عبور جدید:")
    ent_confirm = create_field("تکرار رمز عبور جدید:")
    def do_change():
        if ent_old.get() != get_current_password():
            messagebox.showerror("Error", "رمز عبور فعلی اشتباه است", parent=cp_win); return
        if ent_new.get() != ent_confirm.get():
            messagebox.showerror("Error", "تکرار رمز عبور مطابقت ندارد", parent=cp_win); return
        if not ent_new.get():
            messagebox.showerror("Error", "رمز عبور نمی‌تواند خالی باشد", parent=cp_win); return
        set_new_password(ent_new.get())
        messagebox.showinfo("Success", "رمز عبور با موفقیت تغییر یافت", parent=cp_win)
        cp_win.destroy()
    tk.Button(cp_win, text="تغییر رمز", command=do_change, bg="white", fg=BLUE_COLOR, font=(FONT_MAIN, 11, "bold")).pack(pady=20)

def show_daily_stats_ui(parent_win):
    stats_win = tk.Toplevel(parent_win)
    stats_win.title("آمار تردد")
    stats_win.geometry("400x400")
    try: stats_win.iconbitmap('app_icon.ico')
    except: pass
    stats_win.configure(bg=BLUE_COLOR)
    tk.Label(stats_win, text=":تاریخ مورد نظر را وارد کنید", bg=BLUE_COLOR, fg="white", font=(FONT_MAIN, 12, "bold")).pack(pady=(20, 10))
    date_frame = tk.Frame(stats_win, bg=BLUE_COLOR)
    date_frame.pack(pady=5)
    ent_day = tk.Entry(date_frame, justify='center', width=5, font=(FONT_MAIN, 11))
    ent_day.pack(side=tk.RIGHT, padx=2)
    tk.Label(date_frame, text="/", bg=BLUE_COLOR, fg="white", font=(FONT_MAIN, 11)).pack(side=tk.RIGHT)
    ent_month = tk.Entry(date_frame, justify='center', width=5, font=(FONT_MAIN, 11))
    ent_month.pack(side=tk.RIGHT, padx=2)
    tk.Label(date_frame, text="/", bg=BLUE_COLOR, fg="white", font=(FONT_MAIN, 11)).pack(side=tk.RIGHT)
    ent_year = tk.Entry(date_frame, justify='center', width=7, font=(FONT_MAIN, 11))
    ent_year.pack(side=tk.RIGHT, padx=2)
    result_lbl = tk.Label(stats_win, text="", bg=BLUE_COLOR, fg="white", font=(FONT_MAIN, 12), justify="right")
    result_lbl.pack(pady=20)
    def calculate(target_date_str=None):
        if not target_date_str:
            y, m, d = ent_year.get(), ent_month.get(), ent_day.get()
            if not (y and m and d):
                messagebox.showwarning("خطا", "لطفاً سال، ماه و روز را کامل وارد کنید", parent=stats_win)
                return
            target_date_str = f"{y}/{m.zfill(2)}/{d.zfill(2)}"
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM visitors WHERE shamsi_date = ?", (target_date_str,))
            total = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM visitors WHERE shamsi_date = ? AND (exit_time IS NULL OR exit_time = '')", (target_date_str,))
            no_exit = cursor.fetchone()[0]
            conn.close()
            display_text = (f"تاریخ: {target_date_str}\n\n"
                            f"تعداد کل ثبت شده: {total}\n"
                            f"تعداد ثبت شده بدون ساعت خروجی: {no_exit}")
            result_lbl.config(text=display_text)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=stats_win)
    def set_today():
        now_j = jdatetime.date.fromgregorian(date=datetime.now().date())
        ent_year.delete(0, tk.END); ent_year.insert(0, str(now_j.year))
        ent_month.delete(0, tk.END); ent_month.insert(0, str(now_j.month))
        ent_day.delete(0, tk.END); ent_day.insert(0, str(now_j.day))
        calculate(now_j.strftime("%Y/%m/%d"))
    btn_frame = tk.Frame(stats_win, bg=BLUE_COLOR)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="امروز", command=set_today, bg="#FF9800", fg="white", font=(FONT_MAIN, 11, "bold"), relief="flat", width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="محاسبه", command=lambda: calculate(), bg="white", fg=BLUE_COLOR, font=(FONT_MAIN, 11, "bold"), relief="flat", width=10).pack(side=tk.LEFT, padx=10)

def open_search_window():
    search_win = tk.Toplevel(app)
    try: search_win.iconbitmap('app_icon.ico')
    except Exception: pass
    search_win.title("مشاهده و جستجوی سوابق")
    search_win.geometry("1200x750")
    
    search_frame = ttk.LabelFrame(search_win, text="فیلترهای جستجو", padding=(10, 10))
    search_frame.pack(fill=tk.X, padx=10, pady=5)
    
    ttk.Label(search_frame, text=": نام مهمان").grid(row=0, column=5, sticky=tk.E, padx=(15, 5), pady=5)
    entry_search_name = ttk.Entry(search_frame, justify='right')
    entry_search_name.grid(row=0, column=4, sticky=tk.EW, padx=5, pady=5)
    ttk.Label(search_frame, text=": کد ملی").grid(row=0, column=3, sticky=tk.E, padx=(15, 5), pady=5)
    entry_search_nid = ttk.Entry(search_frame, justify='right')
    entry_search_nid.grid(row=0, column=2, sticky=tk.EW, padx=5, pady=5)
    
    ttk.Label(search_frame, text=": تاریخ").grid(row=1, column=5, sticky=tk.E, padx=(15, 5), pady=5)
    days = [str(i) for i in range(1, 32)]
    combo_day = ttk.Combobox(search_frame, values=[""] + days, justify='center', width=3, state='readonly')
    combo_day.grid(row=1, column=4, sticky=tk.E, padx=(0, 5))
    combo_month = ttk.Combobox(search_frame, values=[""] + PERSIAN_MONTHS, justify='center', width=10, state='readonly')
    combo_month.grid(row=1, column=4, sticky=tk.E, padx=(0, 55))
    years = [str(i) for i in range(1400, 1411)] 
    combo_year = ttk.Combobox(search_frame, values=[""] + years, justify='center', width=5, state='readonly')
    combo_year.grid(row=1, column=4, sticky=tk.W, padx=(0, 0))
    
    ttk.Label(search_frame, text=": واحد").grid(row=1, column=3, sticky=tk.E, padx=(15, 5), pady=5)
    combo_search_dept = ttk.Combobox(search_frame, values=[""] + DEPARTMENT_LIST, justify='right', state='readonly')
    combo_search_dept.grid(row=1, column=2, sticky=tk.EW, padx=5, pady=5)
    search_frame.columnconfigure(2, weight=1); search_frame.columnconfigure(4, weight=1)
    
    tree_frame = ttk.Frame(search_win, padding=(10, 5))
    tree_frame.pack(expand=True, fill=tk.BOTH)
    v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
    h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
    columns = ("id", "visitor_name", "national_id", "employee_to_meet", "department", "entry_time", "shamsi_date", "exit_time")
    
    style.configure("Custom.Treeview", font=(FONT_TABLE, 12, "bold"), rowheight=35)
    style.configure("Custom.Treeview.Heading", font=(FONT_MAIN, 12))
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="browse", style="Custom.Treeview", 
                        yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    v_scroll.config(command=tree.yview); v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    h_scroll.config(command=tree.xview); h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.pack(expand=True, fill=tk.BOTH)
    
    headings = {"id": "شماره", "visitor_name": "نام مهمان", "national_id": "کد ملی", "employee_to_meet": "ملاقات شونده", "department": "واحد", "entry_time": "ساعت ورود", "shamsi_date": "تاریخ ورود", "exit_time": "ساعت خروج"}
    for col, text in headings.items(): tree.heading(col, text=text)
    tree.column("id", width=60, anchor=tk.CENTER, minwidth=50)
    tree.column("visitor_name", width=180, anchor=tk.E, minwidth=150) 
    tree.column("national_id", width=110, anchor=tk.CENTER, minwidth=100)
    tree.column("employee_to_meet", width=160, anchor=tk.E, minwidth=140)
    tree.column("department", width=140, anchor=tk.E, minwidth=120)
    tree.column("entry_time", width=80, anchor=tk.CENTER, minwidth=70)
    tree.column("shamsi_date", width=100, anchor=tk.CENTER, minwidth=90)
    tree.column("exit_time", width=80, anchor=tk.CENTER, minwidth=70)
    
    def get_query_and_params(filters):
        query = "SELECT id, visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, exit_time FROM visitors WHERE 1=1"
        params = []
        if filters.get("name"): query += " AND visitor_name LIKE ?"; params.append(f"%{filters['name']}%")
        if filters.get("nid"): query += " AND national_id LIKE ?"; params.append(f"%{filters['nid']}%")
        if filters.get("dept"): query += " AND department = ?"; params.append(filters['dept'])
        y, m_name, d = filters.get("year"), filters.get("month_name"), filters.get("day")
        if y: query += " AND shamsi_date LIKE ?"; params.append(f"{y}%")
        if m_name in PERSIAN_MONTHS:
            m_index = PERSIAN_MONTHS.index(m_name) + 1
            m = f"{m_index:02d}"
            query += " AND shamsi_date LIKE ?"; params.append(f"%/{m}/%")
        if d:
            d_padded = d.zfill(2)
            query += " AND shamsi_date LIKE ?"; params.append(f"%/{d_padded}")
        return query, params
    def populate_tree(records):
        for i in tree.get_children(): tree.delete(i)
        for record in records:
            try:
                dt_obj = datetime.strptime(record[5], "%Y-%m-%d %H:%M:%S")
                display_time = dt_obj.strftime("%H:%M")
            except: display_time = record[5]
            display_record = (record[0], record[1], record[2], record[3], record[4], display_time, record[6] or "", record[7] or "")
            tree.insert("", tk.END, values=display_record)
    def fetch_and_display_records(filters=None):
        if filters is None: filters = {}
        conn = sqlite3.connect(DB_PATH); cursor = conn.cursor()
        query, params = get_query_and_params(filters)
        query += " ORDER BY id DESC"
        cursor.execute(query, params)
        populate_tree(cursor.fetchall())
        conn.close()
    def search_action(): 
        fetch_and_display_records({"name": entry_search_name.get(), "nid": entry_search_nid.get(), "year": combo_year.get(), "month_name": combo_month.get(), "day": combo_day.get(), "dept": combo_search_dept.get()})
    def reset_action():
        entry_search_name.delete(0, tk.END); entry_search_nid.delete(0, tk.END)
        combo_year.set(""); combo_month.set(""); combo_day.set(""); combo_search_dept.set("")
        fetch_and_display_records({})
    def export_to_excel():
        filters = {"name": entry_search_name.get(), "nid": entry_search_nid.get(), "year": combo_year.get(), "month_name": combo_month.get(), "day": combo_day.get(), "dept": combo_search_dept.get()}
        conn = sqlite3.connect(DB_PATH); cursor = conn.cursor()
        query, params = get_query_and_params(filters)
        query += " ORDER BY id DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        if not rows: messagebox.showwarning("هشدار", "رکوردی برای خروجی گرفتن وجود ندارد"); return
        columns_export = ["شناسه", "نام مهمان", "کد ملی", "ملاقات شونده", "واحد", "زمان ورود (میلادی)", "تاریخ شمسی", "ساعت خروج"]
        try:
            df = pd.DataFrame(rows, columns=columns_export)
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")], title="ذخیره فایل اکسل")
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("موفق", f"فایل اکسل ذخیره شد:\n{file_path}")
        except Exception as e: messagebox.showerror("خطا", f"خطا در ایجاد فایل اکسل:\n{e}")
    def on_tree_double_click(event):
        selected_item = tree.selection()
        if not selected_item: return
        item_values = tree.item(selected_item, "values")
        visitor_id, visitor_name, entry_shamsi_date, existing_exit = item_values[0], item_values[1], item_values[6], item_values[7]
        if existing_exit and existing_exit.strip():
            messagebox.showerror("خطا", "ساعت خروج قبلاً ثبت شده است", parent=search_win); return
        popup = tk.Toplevel(search_win)
        popup.title("ثبت خروج"); popup.geometry("350x200")
        x = search_win.winfo_x() + (search_win.winfo_width() // 2) - 175
        y = search_win.winfo_y() + (search_win.winfo_height() // 2) - 100
        popup.geometry(f"+{x}+{y}")
        tk.Label(popup, text=f"ثبت خروج برای: {visitor_name}", font=(FONT_MAIN, 12, "bold")).pack(pady=20)
        def confirm():
            current_shamsi = jdatetime.date.fromgregorian(date=datetime.now().date()).strftime("%Y/%m/%d")
            if entry_shamsi_date != current_shamsi:
                messagebox.showerror("خطا", "ثبت خروج فقط در تاریخ ورود امکان‌پذیر است", parent=popup); return
            try:
                conn = sqlite3.connect(DB_PATH); cursor = conn.cursor()
                cursor.execute("UPDATE visitors SET exit_time = ? WHERE id = ?", (datetime.now().strftime("%H:%M"), visitor_id))
                conn.commit(); conn.close()
                popup.destroy(); search_action()
                messagebox.showinfo("موفق", "خروج ثبت شد", parent=search_win)
            except Exception as e: messagebox.showerror("Error", str(e))
        btn_f = tk.Frame(popup); btn_f.pack(pady=10)
        tk.Button(btn_f, text="تایید خروج", bg=GREEN_COLOR, fg="white", width=12, command=confirm).pack(side=tk.RIGHT, padx=5)
        tk.Button(btn_f, text="انصراف", bg=RED_COLOR, fg="white", width=12, command=popup.destroy).pack(side=tk.RIGHT, padx=5)
    tree.bind("<Double-1>", on_tree_double_click)
    buttons_frame = ttk.Frame(search_win, padding=(10, 10)); buttons_frame.pack(fill=tk.X)
    tk.Button(buttons_frame, text="جستجو", command=search_action, bg=BLUE_COLOR, fg="white", font=(FONT_MAIN, 12), width=10).pack(side=tk.RIGHT, padx=5)
    tk.Button(buttons_frame, text="نمایش همه", command=reset_action, font=(FONT_MAIN, 12), width=10).pack(side=tk.RIGHT, padx=5)
    tk.Button(buttons_frame, text="خروجی اکسل", command=export_to_excel, bg="#2E7D32", fg="white", font=(FONT_MAIN, 12, "bold"), width=15).pack(side=tk.LEFT, padx=5)
    reset_action()

def show_heatmap_analytics():
    analytics_win = tk.Toplevel(app)
    analytics_win.title("تحلیل آماری تردد")
    analytics_win.geometry("900x650")
    try: analytics_win.iconbitmap('app_icon.ico')
    except: pass
    analytics_win.configure(bg="white")
    filter_frame = tk.Frame(analytics_win, bg="#E3F2FD", bd=1, relief="solid")
    filter_frame.pack(fill=tk.X, padx=10, pady=10)
    tk.Label(filter_frame, text=":فیلتر زمانی", bg="#E3F2FD", font=(FONT_MAIN, 12, "bold")).pack(side=tk.RIGHT, padx=10, pady=10)
    years = [str(i) for i in range(1400, 1411)]
    days = [str(i) for i in range(1, 32)]
    cb_day = ttk.Combobox(filter_frame, values=[""] + days, width=3, state="readonly", justify='center')
    cb_day.pack(side=tk.RIGHT, padx=2)
    tk.Label(filter_frame, text="روز", bg="#E3F2FD").pack(side=tk.RIGHT)
    cb_month = ttk.Combobox(filter_frame, values=[""] + PERSIAN_MONTHS, width=10, state="readonly", justify='center')
    cb_month.pack(side=tk.RIGHT, padx=2)
    tk.Label(filter_frame, text="ماه", bg="#E3F2FD").pack(side=tk.RIGHT)
    cb_year = ttk.Combobox(filter_frame, values=[""] + years, width=5, state="readonly", justify='center')
    cb_year.pack(side=tk.RIGHT, padx=2)
    tk.Label(filter_frame, text="سال", bg="#E3F2FD").pack(side=tk.RIGHT)
    chart_container = tk.Frame(analytics_win, bg="white")
    chart_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    def update_chart():
        for widget in chart_container.winfo_children(): widget.destroy()
        y, m_name, d = cb_year.get(), cb_month.get(), cb_day.get()
        query = "SELECT strftime('%H', entry_time) as hour, COUNT(*) FROM visitors WHERE 1=1"
        params = []
        title_context = "کل ادوار" 
        if y: query += " AND shamsi_date LIKE ?"; params.append(f"{y}%"); title_context = f"سال {y}"
        if m_name in PERSIAN_MONTHS:
            m_idx = PERSIAN_MONTHS.index(m_name) + 1; m_str = f"{m_idx:02d}"
            query += " AND shamsi_date LIKE ?"; params.append(f"%/{m_str}/%"); title_context += f" - {m_name}"
        if d:
            d_str = d.zfill(2); query += " AND shamsi_date LIKE ?"; params.append(f"%/{d_str}"); title_context += f" - روز {d}"
        query += " GROUP BY hour ORDER BY hour"
        try:
            conn = sqlite3.connect(DB_PATH); cursor = conn.cursor(); cursor.execute(query, params)
            data = cursor.fetchall(); conn.close()
        except Exception as e: tk.Label(chart_container, text=f"خطای دیتابیس: {e}", fg="red", bg="white").pack(); return
        if not data: tk.Label(chart_container, text="اطلاعاتی با این فیلتر یافت نشد", font=(FONT_MAIN, 14), bg="white", fg="#777").pack(pady=50); return
        hours_found = [row[0] for row in data]; counts_found = [row[1] for row in data]
        full_hours = [f"{h:02d}" for h in range(7, 20)]; full_counts = []
        for h in full_hours:
            if h in hours_found: idx = hours_found.index(h); full_counts.append(counts_found[idx])
            else: full_counts.append(0)
        fig = Figure(figsize=(8, 5), dpi=100); ax = fig.add_subplot(111)
        bars = ax.bar(full_hours, full_counts, color='#3F51B5', width=0.6, zorder=3)
        final_title = f"تحلیل تردد - {title_context}"
        ax.set_title(make_farsi(final_title), fontsize=14, fontname=FONT_TABLE)
        ax.set_xlabel(make_farsi("ساعت ورود"), fontsize=12, fontname=FONT_TABLE)
        ax.set_ylabel(make_farsi("تعداد مراجعین"), fontsize=12, fontname=FONT_TABLE)
        ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
        for bar in bars:
            height = bar.get_height()
            if height > 0: ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom', fontsize=10)
        canvas = FigureCanvasTkAgg(fig, master=chart_container); canvas.draw(); canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    def reset_filters(): cb_year.set(""); cb_month.set(""); cb_day.set(""); update_chart()
    tk.Button(filter_frame, text="نمایش نمودار", command=update_chart, bg=BLUE_COLOR, fg="white", font=(FONT_MAIN, 11), width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(filter_frame, text="حذف فیلترها", command=reset_filters, bg=RED_COLOR, fg="white", font=(FONT_MAIN, 11), width=12).pack(side=tk.LEFT, padx=10)
    update_chart()

def add_dummy_data():
    try:
        first_names = ["علی", "محمد", "رضا", "حسین", "محسن", "احمد", "مهدی", "سارا", "مریم", "زهرا", "فاطمه", "نرگس", "نیما", "کاوه", "امید", "پیمان", "سعید"]
        last_names = ["محمدی", "حسینی", "رضایی", "کریمی", "احمدی", "موسوی", "جعفری", "صادقی", "رحیمی", "عباسی", "باقری", "زاهدی", "میرزایی", "غفاری"]
        dummy_records = []
        for _ in range(100):
            full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            nid = str(random.randint(1000000000, 9999999999))
            year = random.choice([1403, 1404]); month = random.randint(1, 12)
            if month <= 6: day = random.randint(1, 31)
            elif month <= 11: day = random.randint(1, 30)
            else: day = random.randint(1, 29)
            shamsi_date = f"{year}/{month:02d}/{day:02d}"
            hour = random.randint(8, 13); minute = random.randint(0, 59); second = random.randint(0, 59)
            time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
            g_date = jdatetime.date(year, month, day).togregorian()
            entry_time_gregorian = f"{g_date.year}-{g_date.month:02d}-{g_date.day:02d} {time_str}"
            dept = random.choice(DEPARTMENT_LIST)
            dummy_records.append({"visitor_name": full_name, "national_id": nid, "employee_to_meet": "-", "department": dept, "entry_time": entry_time_gregorian, "shamsi_date": shamsi_date})
        dummy_records.sort(key=lambda x: x['entry_time'])
        conn = sqlite3.connect(DB_PATH); cursor = conn.cursor()
        for r in dummy_records:
            cursor.execute('''INSERT INTO visitors (visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date) VALUES (?, ?, ?, ?, ?, ?)''', (r['visitor_name'], r['national_id'], r['employee_to_meet'], r['department'], r['entry_time'], r['shamsi_date']))
        conn.commit(); conn.close()
        messagebox.showinfo("Developer Mode", "100 Random Records Added Successfully!")
    except Exception as e: messagebox.showerror("Error", f"Failed to generate data: {e}")

def delete_all_records():
    if not messagebox.askyesno("Danger Zone", "Are you sure you want to DELETE ALL records?\n\nThis cannot be undone!"): return
    try:
        conn = sqlite3.connect(DB_PATH); cursor = conn.cursor()
        cursor.execute("DELETE FROM visitors")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='visitors'")
        conn.commit(); conn.close()
        messagebox.showinfo("Developer Mode", "Database has been completely cleared.")
    except Exception as e: messagebox.showerror("Error", f"Failed to delete data: {e}")

def create_backup():
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_visitor_log_{timestamp}.db"
        destination_path = os.path.join(os.getcwd(), backup_filename)
        if not os.path.exists(DB_PATH): messagebox.showerror("خطا", ".فایل پایگاه داده یافت نشد! اطلاعاتی برای پشتیبان‌گیری وجود ندارد"); return
        shutil.copy2(DB_PATH, destination_path)
        messagebox.showinfo("عملیات موفق", f":نسخه پشتیبان با موفقیت ایجاد شد و در مسیر زیر ذخیره گردید\n\n{destination_path}")
    except Exception as e: messagebox.showerror("خطا در پشتیبان‌گیری", f":خطایی در حین عملیات رخ داد\n{e}")

def restore_backup():
    backup_path = filedialog.askopenfilename(title="انتخاب فایل پشتیبان", filetypes=[("Database Files", "*.db"), ("All Files", "*.*")])
    if not backup_path: return
    try:
        bk_conn = sqlite3.connect(backup_path); bk_cursor = bk_conn.cursor()
        try: bk_cursor.execute("SELECT visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, exit_time FROM visitors"); records_to_import = bk_cursor.fetchall()
        except sqlite3.DatabaseError: bk_conn.close(); raise Exception("Invalid Schema")
        bk_conn.close()
        if not records_to_import: messagebox.showinfo("اطلاعات", "فایل انتخاب شده خالی است"); return
        conn = sqlite3.connect(DB_PATH); cursor = conn.cursor()
        imported_count = 0; duplicate_count = 0
        for row in records_to_import:
            cursor.execute("SELECT 1 FROM visitors WHERE national_id = ? AND entry_time = ?", (row[1], row[4]))
            if cursor.fetchone(): duplicate_count += 1
            else:
                cursor.execute('''INSERT INTO visitors (visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, exit_time) VALUES (?, ?, ?, ?, ?, ?, ?)''', row)
                imported_count += 1
        conn.commit(); conn.close()
        msg = f"{imported_count} : تعداد رکورد های جدید  "
        if duplicate_count > 0: msg += f"\n\n(همچنین {duplicate_count} رکورد تکراری نادیده گرفته شد)"
        messagebox.showinfo("نتیجه بازیابی", msg)
    except Exception: messagebox.showerror("خطا", "فایل انتخاب شده معتبر نیست\nلطفاً از صحیح بودن فایل پشتیبان اطمینان حاصل کنید")

def open_developer_mode():
    dev_win = tk.Toplevel(app)
    dev_win.title("پنل مدیریت")
    dev_win.geometry("400x680")
    try: dev_win.iconbitmap('app_icon.ico')
    except: pass
    dev_win.configure(bg=BLUE_COLOR)
    tk.Label(dev_win, text="ابزارهای مدیریت سیستم", font=(FONT_MAIN, 14, "bold"), bg=BLUE_COLOR, fg="white").pack(pady=20)
    tk.Button(dev_win, text="افزودن ۱۰۰ رکورد آزمایشی", command=add_dummy_data, bg="white", fg=BLUE_COLOR, font=(FONT_MAIN, 12, "bold"), relief="flat", padx=20, pady=5).pack(pady=5)
    tk.Button(dev_win, text="پاکسازی کامل دیتابیس", command=delete_all_records, bg=RED_COLOR, fg="white", font=(FONT_MAIN, 12, "bold"), relief="flat", padx=20, pady=5).pack(pady=5)
    tk.Button(dev_win, text="تغییر رمز عبور", command=lambda: change_password_ui(dev_win), bg="#FF9800", fg="white", font=(FONT_MAIN, 12, "bold"), relief="flat", padx=20, pady=5).pack(pady=5)
    tk.Button(dev_win, text="تعداد ورودی/خروجی های ثبت شده", command=lambda: show_daily_stats_ui(dev_win), bg="#673AB7", fg="white", font=(FONT_MAIN, 12, "bold"), relief="flat", padx=20, pady=5).pack(pady=5)
    tk.Button(dev_win, text="نمودار تحلیل ترافیک (Heatmap)", command=show_heatmap_analytics, bg="#E91E63", fg="white", font=(FONT_MAIN, 12, "bold"), relief="flat", padx=20, pady=5).pack(pady=5)
    tk.Button(dev_win, text="تهیه نسخه پشتیبان (Backup)", command=create_backup, bg="#009688", fg="white", font=(FONT_MAIN, 12, "bold"), relief="flat", padx=20, pady=5).pack(pady=5)
    tk.Button(dev_win, text="بازیابی اطلاعات (Import)", command=restore_backup, bg="#795548", fg="white", font=(FONT_MAIN, 12, "bold"), relief="flat", padx=20, pady=5).pack(pady=5)
    tk.Label(dev_win, text="⚠️ مخصوص راهبر سیستم و پشتیبانی", font=(FONT_MAIN, 10), bg=BLUE_COLOR, fg="#E0E0E0").pack(side=tk.BOTTOM, pady=10)

# --- APP SETUP ---
app = tk.Tk()
app.title(f"سامانه مدیریت ورود و خروج (اداره حراست) - نسخه {APP_VERSION}")
app.geometry("1050x600")
app.resizable(False, False)
app.configure(bg=DEFAULT_BG_COLOR)
try: app.iconbitmap('app_icon.ico')
except Exception: pass

available_fonts = font.families()
if "B Titr" in available_fonts: FONT_MAIN = "B Titr"
else: FONT_MAIN = "Tahoma"
if "B Nazanin" in available_fonts: FONT_TABLE = "B Nazanin"
else: FONT_TABLE = "Tahoma"
style = ttk.Style(app); style.theme_use("vista")
style.configure(".", font=(FONT_MAIN, 13), background=DEFAULT_BG_COLOR)
style.configure("TLabel", anchor="east"); style.configure("TFrame", background=DEFAULT_BG_COLOR)

setup_background(app)

# --- LIVE CLOCK ---
def update_live_clock():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    j_date = jdatetime.date.fromgregorian(date=now.date())
    persian_date_str = j_date.strftime("%Y/%m/%d")
    live_clock_label.config(text=f"{persian_date_str}   -   {current_time}")
    live_clock_label.after(1000, update_live_clock)
live_clock_label = tk.Label(app, text="", font=(FONT_MAIN, 14, "bold"), bg=DEFAULT_BG_COLOR, fg="#00695C")
live_clock_label.place(relx=1.0, y=20, anchor="ne", x=-30)
live_clock_label.lift()
update_live_clock()

# --- CENTRAL CARD ---
card_frame = tk.Frame(app, bg=CARD_BG_COLOR, bd=2, relief="groove")
card_frame.place(relx=0.5, rely=0.5, anchor="center", width=410, height=530)
header_lbl = tk.Label(card_frame, text="(سامانه ثبت ورود و خروج (اداره حراست", font=(FONT_MAIN, 16, "bold"), bg=CARD_BG_COLOR, fg="#37474F")
header_lbl.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky="ew")
labels = {": شماره کارت ملی": 1, ": نام ملاقات کننده": 2, ": نام ملاقات شونده": 3, ": امور / واحد مربوطه": 4}
for text, row in labels.items():
    tk.Label(card_frame, text=text, font=(FONT_MAIN, 13), bg=CARD_BG_COLOR, fg="black", anchor="e").grid(row=row, column=1, padx=(10, 30), pady=10, sticky="e")

vcmd = (app.register(validate_numeric), '%P')
entry_national_id = ttk.Entry(card_frame, justify='right', font=(FONT_MAIN, 13), validate='key', validatecommand=vcmd)
entry_national_id.bind("<FocusOut>", check_returning_visitor)
entry_national_id.bind("<Return>", focus_next_widget)
entry_employee_to_meet = AutocompleteEntry(card_frame, justify='right', font=(FONT_MAIN, 13))
entry_visitor_name = ttk.Entry(card_frame, justify='right', font=(FONT_MAIN, 13))
entry_visitor_name.bind("<Return>", focus_next_widget)
combo_department = ttk.Combobox(card_frame, values=DEPARTMENT_LIST, justify='right', state='readonly', font=(FONT_MAIN, 12))
combo_department.bind("<Return>", focus_next_widget)

entry_national_id.grid(row=1, column=0, sticky="ew", padx=(30, 5), pady=10)
entry_visitor_name.grid(row=2, column=0, sticky="ew", padx=(30, 5), pady=10)
entry_employee_to_meet.grid(row=3, column=0, sticky="ew", padx=(30, 5), pady=10)
combo_department.grid(row=4, column=0, sticky="ew", padx=(30, 5), pady=10)
card_frame.grid_columnconfigure(0, weight=1)

btn_frame = tk.Frame(card_frame, bg=CARD_BG_COLOR)
btn_frame.grid(row=5, column=0, columnspan=2, pady=(30, 20), sticky="ew")
submit_button = tk.Button(btn_frame, text="ثبت و چاپ رسید", command=submit_visitor, bg=GREEN_COLOR, fg="white", activebackground=GREEN_ACTIVE_COLOR, activeforeground="white", font=(FONT_MAIN, 13, "bold"), relief="flat", borderwidth=0)
submit_button.pack(fill="x", padx=30, pady=5)
search_db_button = tk.Button(btn_frame, text="مشاهده و جستجوی سوابق", command=open_search_window, bg=BLUE_COLOR, fg="white", activebackground=BLUE_ACTIVE_COLOR, activeforeground="white", font=(FONT_MAIN, 12), relief="flat", borderwidth=0)
search_db_button.pack(fill="x", padx=30, pady=5)
help_button = tk.Button(btn_frame, text="راهنما", command=show_help_popup, bg="#607D8B", fg="white", activebackground="#546E7A", activeforeground="white", font=(FONT_MAIN, 12), relief="flat", borderwidth=0)
help_button.pack(fill="x", padx=30, pady=5)

menubar = tk.Menu(app)
tools_menu = tk.Menu(menubar, tearoff=0)
tools_menu.add_command(label="پنل مدیریت", command=ask_dev_password)
menubar.add_cascade(label="امکانات", menu=tools_menu)
app.config(menu=menubar)

try:
    for widget in [entry_visitor_name, entry_national_id, combo_department]:
        widget.bind("<Return>", focus_next_widget)
except NameError: pass

if __name__ == "__main__":
    setup_database()
    update_employee_suggestions()
    status_bar = tk.Label(app, text="", bd=1, relief=tk.SUNKEN, anchor=tk.E, font=(FONT_MAIN, 11), bg="#E0E0E0", padx=10, fg="#555555")
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    status_bar.config(text="  با سلام - به سامانه مدیریت مراجعین (اداره حراست) خوش آمدید")
    app.after(30000, cycle_cultural_messages)
    def on_focus_in(event): event.widget.configure(bg="#E3F2FD")
    def on_focus_out(event): event.widget.configure(bg="white")
    all_inputs = [entry_visitor_name, entry_national_id, entry_employee_to_meet, combo_department]
    for widget in all_inputs:
        widget.bind("<FocusIn>", on_focus_in, add="+")
        widget.bind("<FocusOut>", on_focus_out, add="+")
    app.mainloop()
