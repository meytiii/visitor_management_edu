import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import sqlite3
import pandas as pd
from datetime import datetime
import jdatetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from PIL import Image, ImageTk

# Import local modules
import config
import database
import utils
import widgets

# --- Configuration & Styles ---
FONT_MAIN = "Tahoma"
FONT_TABLE = "Tahoma"
_fonts_checked = False

def ensure_fonts():
    """Checks for Persian fonts only when needed (requires Tk root to be active)."""
    global FONT_MAIN, FONT_TABLE, _fonts_checked
    if _fonts_checked: return
    try:
        available = font.families()
        if "B Titr" in available: FONT_MAIN = "B Titr"
        if "B Nazanin" in available: FONT_TABLE = "B Nazanin"
        _fonts_checked = True
    except: pass

def show_help_popup():
    help_text = f"در صورت بروز هرگونه مشکل یا سوال با شماره زیر تماس بگیرید\n\nخرّم آبادی - 09222550573\n\nنسخه برنامه {config.APP_VERSION}"
    messagebox.showinfo("راهنما", help_text)

def show_login_screen(app, on_success_callback):
    """
    Shows a login window using a Canvas for transparent text over the background image.
    """
    ensure_fonts()
    login_win = tk.Toplevel(app)
    login_win.title("ورود به سیستم")
    
    # Window Geometry
    width, height = 400, 350
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    login_win.geometry(f"{width}x{height}+{x}+{y}")
    login_win.resizable(False, False)

    # --- CANVAS SETUP ---
    canvas = tk.Canvas(login_win, width=width, height=height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # --- BACKGROUND IMAGE ---
    canvas.configure(bg="#59A552") 
    
    if os.path.exists("login.png"):
        try:
            pil_image = Image.open("login.png")
            pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
            bg_image_obj = ImageTk.PhotoImage(pil_image)
            canvas.create_image(0, 0, image=bg_image_obj, anchor="nw")
            login_win.bg_image_obj = bg_image_obj 
        except Exception as e:
            print(f"Error loading login background: {e}")

    # --- ICON ---
    try: login_win.iconbitmap('app_icon.ico')
    except: pass

    # --- DRAWING TEXT ---
    canvas.create_text(200, 40, text="سامانه مدیریت مراجعین", fill="#D0F8FF", font=(FONT_MAIN, 16, "bold"))
    
    canvas.create_text(200, 90, text=":نام کاربری", fill="#FFF9D7", font=(FONT_MAIN, 12))
    ent_user = tk.Entry(login_win, justify='center', font=(FONT_MAIN, 12))
    canvas.create_window(200, 120, window=ent_user, width=200, height=30)
    
    canvas.create_text(200, 160, text=":رمز عبور", fill="#FFF9D7", font=(FONT_MAIN, 12))
    ent_pass = tk.Entry(login_win, show="●", justify='center', font=(FONT_MAIN, 12))
    canvas.create_window(200, 190, window=ent_pass, width=200, height=30)
    
    # --- LOGIN LOGIC ---
    def do_login():
        u = ent_user.get().strip()
        p = ent_pass.get().strip()
        
        success, role, full_name = database.authenticate_user(u, p)
        
        if success:
            login_win.destroy()
            on_success_callback(u, role, full_name)
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است", parent=login_win)
            ent_pass.delete(0, tk.END)

    # Login Button
    btn_login = widgets.RoundedButton(
        login_win,
        text="ورود",
        command=do_login,
        bg="white",
        fg=config.BLUE_COLOR,
        hover_bg="#E0E0E0",
        width=150
    )
    canvas.create_window(200, 260, window=btn_login, width=150, height=44)
    
    def on_close():
        app.destroy()

    login_win.protocol("WM_DELETE_WINDOW", on_close)
    login_win.bind('<Return>', lambda e: do_login())
    ent_user.focus()

# --- USER MANAGER (ADMIN ONLY) ---
def open_user_manager(parent):
    ensure_fonts()
    um_win = tk.Toplevel(parent)
    um_win.title("مدیریت کاربران")
    um_win.geometry("750x550")
    um_win.configure(bg="white")
    
    # --- FIX: Set Icon ---
    try: um_win.iconbitmap('app_icon.ico')
    except: pass

    # --- NEW: Background Image ---
    if os.path.exists("user_management.png"):
        try:
            original_img = Image.open("user_management.png")
            resized_img = original_img.resize((750, 550), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(resized_img)
            
            bg_label = tk.Label(um_win, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception as e:
            print(f"Error loading user_management background: {e}")
    # -----------------------------
    
    # List Frame (Left Side)
    list_frame = tk.Frame(um_win, bg="white", width=280) 
    list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
    list_frame.pack_propagate(False)

    
    tk.Label(list_frame, text="لیست کاربران", font=(FONT_MAIN, 14, "bold"), bg="white", fg=config.BLUE_COLOR).pack(anchor="e")
    
    # Styled Listbox
    user_list = tk.Listbox(list_frame, font=(FONT_TABLE, 12), bd=2, relief="groove", justify='right')
    user_list.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def refresh_list():
        user_list.delete(0, tk.END)
        users = database.get_all_users() # [(user, role, full_name), ...]
        for u, r, fname in users:
            role_fa = "مدیر" if r == 'admin' else "نگهبان"
            display_name = fname if fname else "---"
            # Format: [Role] Full Name (username)
            user_list.insert(tk.END, f"[{role_fa}]  {display_name}  ({u})")
            
    refresh_list()
    
    # Action Frame (Right Side)
    action_frame = tk.Frame(um_win, bg="#F5F5F5", width=300, bd=1, relief="solid")
    action_frame.pack(side=tk.RIGHT, fill=tk.Y)
    action_frame.pack_propagate(False)
    
    tk.Label(action_frame, text="افزودن کاربر جدید", bg="#F5F5F5", fg="#333", font=(FONT_MAIN, 13, "bold")).pack(pady=(25, 15))
    
    # Helper to create inputs
    def create_input(label_text, show=None):
        tk.Label(action_frame, text=label_text, bg="#F5F5F5", font=(FONT_MAIN, 11)).pack(pady=(5, 0))
        entry = tk.Entry(action_frame, justify='center', font=(FONT_MAIN, 11), show=show, width=22)
        entry.pack(pady=2)
        return entry

    new_fullname_ent = create_input(":نام و نام خانوادگی")
    new_user_ent = create_input(":نام کاربری")
    new_pass_ent = create_input(":رمز عبور") 
    
    # Role Selection
    tk.Label(action_frame, text=":نقش کاربری", bg="#F5F5F5", font=(FONT_MAIN, 11)).pack(pady=(10, 5))
    role_var = tk.StringVar(value="guard")
    
    radio_frame = tk.Frame(action_frame, bg="#F5F5F5")
    radio_frame.pack()
    
    tk.Radiobutton(radio_frame, text="نگهبان", variable=role_var, value="guard", bg="#F5F5F5", font=(FONT_MAIN, 10)).pack(side=tk.RIGHT, padx=5)
    tk.Radiobutton(radio_frame, text="مدیر", variable=role_var, value="admin", bg="#F5F5F5", font=(FONT_MAIN, 10)).pack(side=tk.RIGHT, padx=5)
    
    def add_user():
        fname = new_fullname_ent.get().strip()
        u = new_user_ent.get().strip()
        p = new_pass_ent.get().strip()
        r = role_var.get()
        
        if len(u) < 3 or len(p) < 3:
            messagebox.showwarning("خطا", "نام کاربری و رمز عبور باید حداقل ۳ حرف باشند", parent=um_win)
            return
        
        if len(fname) < 2:
            messagebox.showwarning("خطا", "لطفاً نام و نام خانوادگی را وارد کنید", parent=um_win)
            return
        
        ok, msg = database.create_user(u, p, fname, r)
        if ok:
            messagebox.showinfo("موفق", f"کاربر {fname} با موفقیت ایجاد شد", parent=um_win)
            new_fullname_ent.delete(0, tk.END)
            new_user_ent.delete(0, tk.END)
            new_pass_ent.delete(0, tk.END)
            refresh_list()
        else:
            messagebox.showerror("خطا", msg, parent=um_win)

    # Add Button
    widgets.RoundedButton(
        action_frame, 
        text="ثبت کاربر", 
        command=add_user, 
        width=180, height=40, 
        bg=config.GREEN_COLOR, 
        hover_bg=config.GREEN_ACTIVE_COLOR,
        font=(FONT_MAIN, 12, "bold")
    ).pack(pady=20)
    
    tk.Label(action_frame, text="------------------------", bg="#F5F5F5", fg="#CCC").pack(pady=10)
    
    def delete_selected():
        sel = user_list.curselection()
        if not sel: return
        
        text = user_list.get(sel[0]) 
        username = text.split("  (")[-1].replace(")", "").strip()
        
        if messagebox.askyesno("حذف", f"آیا از حذف کاربر {username} مطمئن هستید؟", parent=um_win):
            ok, msg = database.delete_user(username)
            if ok:
                refresh_list()
            else:
                messagebox.showerror("خطا", msg, parent=um_win)

    # Delete Button
    widgets.RoundedButton(
        action_frame, 
        text="حذف کاربر انتخاب شده", 
        command=delete_selected, 
        width=180, height=40, 
        bg=config.RED_COLOR, 
        hover_bg=config.RED_ACTIVE_COLOR,
        font=(FONT_MAIN, 12, "bold")
    ).pack(pady=5)

def show_daily_stats_ui(parent_win):
    """Popup to show daily entry/exit counts."""
    ensure_fonts()
    stats_win = tk.Toplevel(parent_win)
    stats_win.title("آمار تردد")
    stats_win.geometry("400x400")
    try: stats_win.iconbitmap('app_icon.ico')
    except: pass
    stats_win.configure(bg=config.BLUE_COLOR)
    
    tk.Label(stats_win, text=":تاریخ مورد نظر را وارد کنید", bg=config.BLUE_COLOR, fg="white", font=(FONT_MAIN, 12, "bold")).pack(pady=(20, 10))
    
    date_frame = tk.Frame(stats_win, bg=config.BLUE_COLOR)
    date_frame.pack(pady=5)
    
    ent_day = tk.Entry(date_frame, justify='center', width=5, font=(FONT_MAIN, 11))
    ent_day.pack(side=tk.RIGHT, padx=2)
    tk.Label(date_frame, text="/", bg=config.BLUE_COLOR, fg="white", font=(FONT_MAIN, 11)).pack(side=tk.RIGHT)
    
    ent_month = tk.Entry(date_frame, justify='center', width=5, font=(FONT_MAIN, 11))
    ent_month.pack(side=tk.RIGHT, padx=2)
    tk.Label(date_frame, text="/", bg=config.BLUE_COLOR, fg="white", font=(FONT_MAIN, 11)).pack(side=tk.RIGHT)
    
    ent_year = tk.Entry(date_frame, justify='center', width=7, font=(FONT_MAIN, 11))
    ent_year.pack(side=tk.RIGHT, padx=2)
    result_lbl = tk.Label(stats_win, text="", bg=config.BLUE_COLOR, fg="white", font=(FONT_MAIN, 12), justify="right")
    result_lbl.pack(pady=20)

    def calculate(target_date_str=None):
        if not target_date_str:
            y, m, d = ent_year.get(), ent_month.get(), ent_day.get()
            if not (y and m and d):
                messagebox.showwarning("خطا", "لطفاً سال، ماه و روز را کامل وارد کنید", parent=stats_win)
                return
            target_date_str = f"{y}/{m.zfill(2)}/{d.zfill(2)}"
        
        try:
            conn = sqlite3.connect(config.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM visitors WHERE shamsi_date = ?", (target_date_str,))
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM visitors WHERE shamsi_date = ? AND (exit_time IS NULL OR exit_time = '')", (target_date_str,))
            no_exit = cursor.fetchone()[0]
            
            conn.close()
            
            display_text = (
                f"تاریخ: {target_date_str}\n\n"
                f"تعداد کل ثبت شده: {total}\n"
                f"تعداد ثبت شده بدون ساعت خروجی: {no_exit}"
            )
            result_lbl.config(text=display_text)
            
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=stats_win)

    def set_today():
        now_j = jdatetime.date.fromgregorian(date=datetime.now().date())
        ent_year.delete(0, tk.END); ent_year.insert(0, str(now_j.year))
        ent_month.delete(0, tk.END); ent_month.insert(0, str(now_j.month))
        ent_day.delete(0, tk.END); ent_day.insert(0, str(now_j.day))
        calculate(now_j.strftime("%Y/%m/%d"))

    btn_frame = tk.Frame(stats_win, bg=config.BLUE_COLOR)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="امروز", command=set_today, bg="#FF9800", fg="white", font=(FONT_MAIN, 11, "bold"), relief="flat", width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="محاسبه", command=lambda: calculate(), bg="white", fg=config.BLUE_COLOR, font=(FONT_MAIN, 11, "bold"), relief="flat", width=10).pack(side=tk.LEFT, padx=10)

def show_heatmap_analytics(app):
    ensure_fonts()
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
    cb_month = ttk.Combobox(filter_frame, values=[""] + config.PERSIAN_MONTHS, width=10, state="readonly", justify='center')
    cb_month.pack(side=tk.RIGHT, padx=2)
    tk.Label(filter_frame, text="ماه", bg="#E3F2FD").pack(side=tk.RIGHT)
    cb_year = ttk.Combobox(filter_frame, values=[""] + years, width=5, state="readonly", justify='center')
    cb_year.pack(side=tk.RIGHT, padx=2)
    tk.Label(filter_frame, text="سال", bg="#E3F2FD").pack(side=tk.RIGHT)
    chart_container = tk.Frame(analytics_win, bg="white")
    chart_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def update_chart():
        for widget in chart_container.winfo_children():
            widget.destroy()
        y, m_name, d = cb_year.get(), cb_month.get(), cb_day.get()
        
        query = "SELECT strftime('%H', entry_time) as hour, COUNT(*) FROM visitors WHERE 1=1"
        params = []
        
        title_context = "کل ادوار" 
        if y:
            query += " AND shamsi_date LIKE ?"
            params.append(f"{y}%")
            title_context = f"سال {y}"
        
        if m_name in config.PERSIAN_MONTHS:
            m_idx = config.PERSIAN_MONTHS.index(m_name) + 1
            m_str = f"{m_idx:02d}"
            query += " AND shamsi_date LIKE ?"
            params.append(f"%/{m_str}/%")
            title_context += f" - {m_name}"
            
        if d:
            d_str = d.zfill(2)
            query += " AND shamsi_date LIKE ?"
            params.append(f"%/{d_str}")
            title_context += f" - روز {d}"
        query += " GROUP BY hour ORDER BY hour"
        try:
            conn = sqlite3.connect(config.DB_PATH)
            cursor = conn.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall()
            conn.close()
        except Exception as e:
            tk.Label(chart_container, text=f"خطای دیتابیس: {e}", fg="red", bg="white").pack()
            return
        if not data:
            tk.Label(chart_container, text="اطلاعاتی با این فیلتر یافت نشد", font=(FONT_MAIN, 14), bg="white", fg="#777").pack(pady=50)
            return
        hours_found = [row[0] for row in data]
        counts_found = [row[1] for row in data]
        
        full_hours = [f"{h:02d}" for h in range(7, 20)] 
        full_counts = []
        for h in full_hours:
            if h in hours_found:
                idx = hours_found.index(h)
                full_counts.append(counts_found[idx])
            else:
                full_counts.append(0)
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        bars = ax.bar(full_hours, full_counts, color='#3F51B5', width=0.6, zorder=3)
        
        final_title = f"تحلیل تردد - {title_context}"
        ax.set_title(utils.make_farsi(final_title), fontsize=14, fontname=FONT_TABLE)
        ax.set_xlabel(utils.make_farsi("ساعت ورود"), fontsize=12, fontname=FONT_TABLE)
        ax.set_ylabel(utils.make_farsi("تعداد مراجعین"), fontsize=12, fontname=FONT_TABLE)
        
        ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontsize=10)
        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def reset_filters():
        cb_year.set("")
        cb_month.set("")
        cb_day.set("")
        update_chart()

    tk.Button(filter_frame, text="نمایش نمودار", command=update_chart, bg=config.BLUE_COLOR, fg="white", font=(FONT_MAIN, 11), width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(filter_frame, text="حذف فیلترها", command=reset_filters, bg=config.RED_COLOR, fg="white", font=(FONT_MAIN, 11), width=12).pack(side=tk.LEFT, padx=10)
    update_chart()

def open_shift_log_window(app):
    ensure_fonts()
    log_win = tk.Toplevel(app)
    log_win.title("دفتر ثبت وقایع و گزارشات")
    log_win.geometry("700x550")
    try: log_win.iconbitmap('app_icon.ico')
    except: pass
    log_win.configure(bg="#ECEFF1")
    # --- LIST SECTION ---
    list_frame = ttk.LabelFrame(log_win, text="سوابق وقایع ثبت شده", padding=(10, 10))
    list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
    log_list = tk.Listbox(list_frame, font=(FONT_TABLE, 12), height=10, yscrollcommand=scrollbar.set, justify='right')
    scrollbar.config(command=log_list.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    log_list.pack(fill=tk.BOTH, expand=True)
    # --- INPUT SECTION ---
    input_frame = ttk.LabelFrame(log_win, text="ثبت گزارش جدید", padding=(10, 10))
    input_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)
    tk.Label(input_frame, text=":شرح واقعه", font=(FONT_MAIN, 11)).pack(anchor=tk.E)
    
    txt_input = tk.Text(input_frame, height=3, font=(FONT_MAIN, 11))
    txt_input.tag_configure("right", justify='right')
    txt_input.pack(fill=tk.X, pady=5)
    txt_input.insert("1.0", "") 
    
    def align_text(event): txt_input.tag_add("right", "1.0", "end")
    txt_input.bind("<KeyRelease>", align_text)
    def load_logs():
        log_list.delete(0, tk.END)
        try:
            conn = sqlite3.connect(config.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT shamsi_date, created_at, event_text FROM shift_logs ORDER BY id DESC")
            records = cursor.fetchall()
            conn.close()
            for row in records:
                s_date = row[0]
                time_only = row[1].split(' ')[1][:5]
                text = row[2]
                display_text = f"{text}   |   [{s_date} - {time_only}]"
                log_list.insert(tk.END, display_text)
        except Exception as e: messagebox.showerror("Error", str(e))
    def save_log():
        text = txt_input.get("1.0", tk.END).strip()
        if len(text) < 2: return
        now = datetime.now()
        created_at = now.strftime("%Y-%m-%d %H:%M:%S")
        s_date = jdatetime.date.fromgregorian(date=now.date()).strftime("%Y/%m/%d")
        try:
            conn = sqlite3.connect(config.DB_PATH); cursor = conn.cursor()
            cursor.execute("INSERT INTO shift_logs (event_text, created_at, shamsi_date) VALUES (?, ?, ?)", (text, created_at, s_date))
            conn.commit(); conn.close()
            txt_input.delete("1.0", tk.END)
            load_logs()
            messagebox.showinfo("موفق", "گزارش در دفتر وقایع ثبت شد")
        except Exception as e: messagebox.showerror("Error", str(e))
    tk.Button(input_frame, text="ثبت گزارش", bg=config.BLUE_COLOR, fg="white", font=(FONT_MAIN, 11), command=save_log).pack(anchor=tk.W)
    load_logs()

def open_search_window(app):
    ensure_fonts()
    search_win = tk.Toplevel(app)
    try: search_win.iconbitmap('app_icon.ico')
    except Exception: pass
    search_win.title("مشاهده و جستجوی سوابق")
    search_win.geometry("1300x800") 
    
    # --- STATE VARIABLES ---
    current_page = 1
    items_per_page = 50
    total_pages = 1
    current_filters = {} 
    
    # --- FILTER FRAME ---
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
    combo_month = ttk.Combobox(search_frame, values=[""] + config.PERSIAN_MONTHS, justify='center', width=10, state='readonly')
    combo_month.grid(row=1, column=4, sticky=tk.E, padx=(0, 55))
    years = [str(i) for i in range(1400, 1411)] 
    combo_year = ttk.Combobox(search_frame, values=[""] + years, justify='center', width=5, state='readonly')
    combo_year.grid(row=1, column=4, sticky=tk.W, padx=(0, 0))
    ttk.Label(search_frame, text=": واحد").grid(row=1, column=3, sticky=tk.E, padx=(15, 5), pady=5)
    combo_search_dept = ttk.Combobox(search_frame, values=[""] + config.DEPARTMENT_LIST, justify='right', state='readonly')
    combo_search_dept.grid(row=1, column=2, sticky=tk.EW, padx=5, pady=5)
    search_frame.columnconfigure(2, weight=1); search_frame.columnconfigure(4, weight=1)
    
    # --- TREEVIEW (TABLE) SETUP ---
    tree_frame = ttk.Frame(search_win, padding=(10, 5))
    tree_frame.pack(expand=True, fill=tk.BOTH)
    v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
    h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
    
    columns = ("id", "visitor_name", "national_id", "employee_to_meet", "department", "entry_time", "shamsi_date", "exit_time", "created_by")
    
    style = ttk.Style()
    style.configure("Custom.Treeview", font=(FONT_TABLE, 12, "bold"), rowheight=35)
    style.configure("Custom.Treeview.Heading", font=(FONT_MAIN, 12))
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="browse", style="Custom.Treeview", 
                        yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    
    v_scroll.config(command=tree.yview)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    h_scroll.config(command=tree.xview)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    
    tree.pack(expand=True, fill=tk.BOTH)
    
    headings = {
        "id": "شماره", "visitor_name": "نام مهمان", "national_id": "کد ملی", "employee_to_meet": "ملاقات شونده", 
        "department": "واحد", "entry_time": "ساعت ورود", "shamsi_date": "تاریخ ورود", "exit_time": "ساعت خروج", "created_by": "کاربر ثبت کننده"
    }
    for col, text in headings.items(): tree.heading(col, text=text)
    
    tree.column("id", width=60, anchor=tk.CENTER, minwidth=50)
    tree.column("visitor_name", width=160, anchor=tk.E, minwidth=140) 
    tree.column("national_id", width=100, anchor=tk.CENTER, minwidth=90)
    tree.column("employee_to_meet", width=140, anchor=tk.E, minwidth=130)
    tree.column("department", width=120, anchor=tk.E, minwidth=110)
    tree.column("entry_time", width=70, anchor=tk.CENTER, minwidth=60)
    tree.column("shamsi_date", width=90, anchor=tk.CENTER, minwidth=80)
    tree.column("exit_time", width=70, anchor=tk.CENTER, minwidth=60)
    tree.column("created_by", width=130, anchor=tk.CENTER, minwidth=100)

    # --- PAGINATION CONTROLS ---
    pagination_frame = tk.Frame(search_win, bg=config.DEFAULT_BG_COLOR, pady=10)
    pagination_frame.pack(fill=tk.X)
    
    # Info Label (Far Right)
    lbl_info = tk.Label(pagination_frame, text="", font=(FONT_MAIN, 11), bg=config.DEFAULT_BG_COLOR)
    lbl_info.pack(side=tk.RIGHT, padx=(10, 20))
    
    # Controls Group (Packed to the Right, to be next to the info label)
    controls_frame = tk.Frame(pagination_frame, bg=config.DEFAULT_BG_COLOR)
    controls_frame.pack(side=tk.RIGHT, padx=10)
    
    # Page Number Display
    lbl_page_num = tk.Label(controls_frame, text="1", font=(FONT_MAIN, 14, "bold"), bg=config.DEFAULT_BG_COLOR, width=4)
    
    def change_page(action):
        nonlocal current_page
        if action == 'first':
            if current_page == 1: return
            current_page = 1
        elif action == 'prev':
            if current_page <= 1: return
            current_page -= 1
        elif action == 'next':
            if current_page >= total_pages: return
            current_page += 1
        elif action == 'last':
            if current_page == total_pages: return
            current_page = total_pages
            
        fetch_and_display_records(current_filters)

    icon_font = ("Segoe UI Symbol", 14) 
    btn_conf = {"width": 45, "height": 35, "radius": 15, "bg": "#B4B4B4", "hover_bg": "#919191", "font": icon_font}
    
    # LAYOUT ORDER (PACKING RIGHT TO LEFT)
    # [Last >>|]  [Next >]   [ 1 ]   [Prev <]  [First |<<]
    
    # 1. Last Page (⏭)
    widgets.RoundedButton(controls_frame, text="⏭", command=lambda: change_page('first'), **btn_conf).pack(side=tk.RIGHT, padx=2)
    
    # 2. Next Page (▶)
    widgets.RoundedButton(controls_frame, text="▶", command=lambda: change_page('prev'), **btn_conf).pack(side=tk.RIGHT, padx=2)
    
    # 3. Page Number
    lbl_page_num.pack(side=tk.RIGHT, padx=10)
    
    # 4. Prev Page (◀)
    widgets.RoundedButton(controls_frame, text="◀", command=lambda: change_page('next'), **btn_conf).pack(side=tk.RIGHT, padx=2)
    
    # 5. First Page (⏮)
    widgets.RoundedButton(controls_frame, text="⏮", command=lambda: change_page('last'), **btn_conf).pack(side=tk.RIGHT, padx=2)

    # --- CORE FUNCTIONS ---
    def get_query_and_params(filters, count_only=False):
        base_query = "SELECT count(*)" if count_only else "SELECT id, visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date, exit_time, created_by"
        base_query += " FROM visitors WHERE 1=1"
        
        params = []
        if filters.get("name"): base_query += " AND visitor_name LIKE ?"; params.append(f"%{filters['name']}%")
        if filters.get("nid"): base_query += " AND national_id LIKE ?"; params.append(f"%{filters['nid']}%")
        if filters.get("dept"): base_query += " AND department = ?"; params.append(filters['dept'])
        
        y, m_name, d = filters.get("year"), filters.get("month_name"), filters.get("day")
        if y: base_query += " AND shamsi_date LIKE ?"; params.append(f"{y}%")
        if m_name in config.PERSIAN_MONTHS:
            m_index = config.PERSIAN_MONTHS.index(m_name) + 1
            m = f"{m_index:02d}"
            base_query += " AND shamsi_date LIKE ?"; params.append(f"%/{m}/%")
        if d:
            d_padded = d.zfill(2)
            base_query += " AND shamsi_date LIKE ?"; params.append(f"%/{d_padded}")
            
        return base_query, params

    def populate_tree(records):
        for i in tree.get_children(): tree.delete(i)
        for record in records:
            try:
                dt_obj = datetime.strptime(record[5], "%Y-%m-%d %H:%M:%S")
                display_time = dt_obj.strftime("%H:%M")
            except: display_time = record[5]
            
            registrar = record[8] if len(record) > 8 and record[8] else "---"
            
            display_record = (
                record[0], record[1], record[2], record[3], record[4], 
                display_time, record[6] or "", record[7] or "", 
                registrar
            )
            tree.insert("", tk.END, values=display_record)

    def fetch_and_display_records(filters=None):
        nonlocal current_page, total_pages
        if filters is None: filters = {}
        
        conn = sqlite3.connect(config.DB_PATH); cursor = conn.cursor()
        
        # 1. Get Total Count
        count_query, count_params = get_query_and_params(filters, count_only=True)
        cursor.execute(count_query, count_params)
        total_records = cursor.fetchone()[0]
        
        # Calculate Total Pages
        import math
        total_pages = math.ceil(total_records / items_per_page)
        if total_pages < 1: total_pages = 1
        
        # Ensure current page is valid
        if current_page > total_pages: current_page = total_pages
        
        # 2. Get Data
        query, params = get_query_and_params(filters, count_only=False)
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        
        offset = (current_page - 1) * items_per_page
        params.extend([items_per_page, offset])
        
        cursor.execute(query, params)
        records = cursor.fetchall()
        
        populate_tree(records)
        conn.close()
        
        # Update UI Labels
        start_idx = offset + 1 if total_records > 0 else 0
        end_idx = min(offset + items_per_page, total_records)
        lbl_info.config(text=f"نمایش {start_idx} تا {end_idx} از {total_records} رکورد")
        lbl_page_num.config(text=str(current_page))

    def search_action(): 
        nonlocal current_filters, current_page
        current_page = 1 
        current_filters = {
            "name": entry_search_name.get(), "nid": entry_search_nid.get(), 
            "year": combo_year.get(), "month_name": combo_month.get(), 
            "day": combo_day.get(), "dept": combo_search_dept.get()
        }
        fetch_and_display_records(current_filters)

    def reset_action():
        entry_search_name.delete(0, tk.END); entry_search_nid.delete(0, tk.END)
        combo_year.set(""); combo_month.set(""); combo_day.set(""); combo_search_dept.set("")
        search_action()

    # --- EXCEL EXPORT ---
    def export_to_excel():
        conn = sqlite3.connect(config.DB_PATH); cursor = conn.cursor()
        query, params = get_query_and_params(current_filters, count_only=False)
        query += " ORDER BY id DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            messagebox.showwarning("هشدار", "رکوردی برای خروجی گرفتن وجود ندارد")
            return
        
        columns_export = ["شناسه", "نام مهمان", "کد ملی", "ملاقات شونده", "واحد", "زمان ورود (میلادی)", "تاریخ شمسی", "ساعت خروج", "کاربر ثبت کننده"]
        try:
            df = pd.DataFrame(rows, columns=columns_export)
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")], title="ذخیره فایل اکسل")
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("موفق", f"فایل اکسل ذخیره شد:\n{file_path}")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ایجاد فایل اکسل:\n{e}")

    # --- EXIT TIME POPUP ---
    def on_tree_double_click(event):
        selected_item = tree.selection()
        if not selected_item: return
        item_values = tree.item(selected_item, "values")
        
        visitor_id = item_values[0]
        visitor_name = item_values[1]
        national_id = item_values[2]
        entry_shamsi_date = item_values[6]
        existing_exit = item_values[7]
        if existing_exit and existing_exit.strip():
            messagebox.showerror("خطا", "ساعت خروج قبلاً ثبت شده است", parent=search_win)
            return
        popup = tk.Toplevel(search_win)
        popup.title("ثبت خروج")
        popup.geometry("500x500")
        popup.resizable(False, False)
        try: popup.iconbitmap('app_icon.ico')
        except: pass
        
        x = search_win.winfo_x() + (search_win.winfo_width() // 2) - 250
        y = search_win.winfo_y() + (search_win.winfo_height() // 2) - 250
        popup.geometry(f"+{x}+{y}")
        
        POPUP_BG_COLOR = "#1E3A5F"
        CARD_BG_COLOR = "#FFFFFF"
        popup.configure(bg=POPUP_BG_COLOR)
        
        card_frame = tk.Frame(popup, bg=CARD_BG_COLOR, bd=2, relief="ridge")
        card_frame.place(relx=0.5, rely=0.5, anchor="center", width=460, height=480)
        
        header_frame = tk.Frame(card_frame, bg=CARD_BG_COLOR)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        
        tk.Label(header_frame, text="ثبت خروج", font=(FONT_MAIN, 16, "bold"), 
                bg=CARD_BG_COLOR, fg="#2E7D32").pack()
        
        tk.Label(header_frame, text=f": {visitor_name}", font=(FONT_MAIN, 13), 
                bg=CARD_BG_COLOR, fg="#37474F").pack()
        
        current_shamsi = jdatetime.date.fromgregorian(date=datetime.now().date()).strftime("%Y/%m/%d")
        if entry_shamsi_date != current_shamsi:
            warning_frame = tk.Frame(card_frame, bg="#FFF3CD", bd=1, relief="solid")
            warning_frame.pack(fill=tk.X, padx=20, pady=10)
            tk.Label(warning_frame, text=f"⚠️ تاریخ ورود: {entry_shamsi_date} (امروز نیست!)", 
                    font=(FONT_MAIN, 10), bg="#FFF3CD", fg="#856404", justify="right").pack(pady=8)
        
        time_frame = tk.Frame(card_frame, bg=CARD_BG_COLOR)
        time_frame.pack(pady=15)
        
        tk.Label(time_frame, text=": ساعت خروج را انتخاب کنید", font=(FONT_MAIN, 12), 
                bg=CARD_BG_COLOR, fg="#37474F").grid(row=0, column=0, columnspan=5, pady=(0, 15), sticky="e")
        
        hours = [str(i).zfill(2) for i in range(7, 21)]
        hour_var = tk.StringVar(value=datetime.now().strftime("%H"))
        hour_combo = ttk.Combobox(time_frame, textvariable=hour_var, values=hours, 
                                width=5, state="readonly", justify='center', font=(FONT_MAIN, 12))
        hour_combo.grid(row=1, column=0, padx=(0, 5))
        
        tk.Label(time_frame, text=":", font=(FONT_MAIN, 14), bg=CARD_BG_COLOR).grid(row=1, column=1, padx=5)
        
        minutes = [str(i).zfill(2) for i in range(0, 60, 5)]
        minute_var = tk.StringVar(value=datetime.now().strftime("%M"))
        minute_combo = ttk.Combobox(time_frame, textvariable=minute_var, values=minutes, 
                                width=5, state="readonly", justify='center', font=(FONT_MAIN, 12))
        minute_combo.grid(row=1, column=2, padx=(5, 15))
        
        def set_current_time():
            now = datetime.now()
            hour_var.set(now.strftime("%H"))
            minute_var.set(now.strftime("%M"))
        
        current_time_btn = widgets.RoundedButton(
            time_frame,
            text="زمان فعلی",
            command=set_current_time,
            width=120,
            height=36,
            radius=18,
            bg="#1976D2",
            hover_bg="#1565C0",
            fg="white",
            font=(FONT_MAIN, 11)
        )
        current_time_btn.grid(row=1, column=4, padx=(20, 0))
        
        try:
            entry_time_only = item_values[5].split(' ')[1][:5] if ' ' in item_values[5] else item_values[5]
            info_frame = tk.Frame(card_frame, bg="#E3F2FD", bd=1, relief="solid")
            info_frame.pack(fill=tk.X, padx=20, pady=15)
            tk.Label(info_frame, text=f"ساعت ورود: {entry_time_only}   |   تاریخ: {entry_shamsi_date}", 
                    font=(FONT_MAIN, 11), bg="#E3F2FD", fg="#1565C0").pack(pady=8)
        except:
            pass
        
        def confirm():
            hour = hour_var.get()
            minute = minute_var.get()
            
            if not hour or not minute:
                messagebox.showerror("خطا", "لطفاً ساعت و دقیقه را انتخاب کنید", parent=popup)
                return
            
            try:
                entry_time_str = item_values[5]
                if ' ' in entry_time_str:
                    entry_time_only = entry_time_str.split(' ')[1][:5]
                    entry_hour, entry_minute = map(int, entry_time_only.split(':'))
                    exit_hour, exit_minute = int(hour), int(minute)
                    
                    entry_total = entry_hour * 60 + entry_minute
                    exit_total = exit_hour * 60 + exit_minute
                    
                    if exit_total < entry_total:
                        response = messagebox.askyesno(
                            "هشدار",
                            f"ساعت خروج ({hour}:{minute}) قبل از ساعت ورود ({entry_hour:02d}:{entry_minute:02d}) است.\n\n"
                            "آیا مطمئن هستید که می‌خواهید ادامه دهید؟",
                            parent=popup
                        )
                        if not response:
                            return
            except:
                pass
            
            if entry_shamsi_date != current_shamsi:
                response = messagebox.askyesno(
                    "تأیید تاریخ متفاوت",
                    f"تاریخ ورود ({entry_shamsi_date}) با امروز ({current_shamsi}) متفاوت است.\n\n"
                    "آیا مطمئن هستید که می‌خواهید خروج ثبت کنید?\n"
                    "(فقط برای تصحیح اطلاعات قبلی استفاده شود)",
                    parent=popup
                )
                if not response:
                    return
            
            exit_time_str = f"{hour}:{minute}"
            
            try:
                conn = sqlite3.connect(config.DB_PATH)
                cursor = conn.cursor()
                cursor.execute("UPDATE visitors SET exit_time = ? WHERE id = ?", (exit_time_str, visitor_id))
                conn.commit()
                conn.close()
                
                popup.destroy()
                fetch_and_display_records(current_filters)
                messagebox.showinfo("موفق", f"خروج {visitor_name} در ساعت {exit_time_str} ثبت شد", parent=search_win)
                
            except Exception as e: 
                messagebox.showerror("خطا", f"خطا در ثبت خروج:\n{str(e)}", parent=popup)

        btn_frame = tk.Frame(card_frame, bg=CARD_BG_COLOR)
        btn_frame.pack(pady=20)
        
        cancel_btn = widgets.RoundedButton(
            btn_frame,
            text="انصراف",
            command=popup.destroy,
            width=120,
            height=40,
            radius=20,
            bg="#f44336",
            hover_bg="#d32f2f",
            fg="white",
            font=(FONT_MAIN, 12)
        )
        cancel_btn.pack(side=tk.RIGHT, padx=15)
        
        confirm_btn = widgets.RoundedButton(
            btn_frame,
            text="تایید خروج",
            command=confirm,
            width=120,
            height=40,
            radius=20,
            bg="#4CAF50",
            hover_bg="#388E3C",
            fg="white",
            font=(FONT_MAIN, 12, "bold")
        )
        confirm_btn.pack(side=tk.RIGHT, padx=15)
        
        hour_combo.focus_set()
        popup.bind('<Return>', lambda e: confirm())

    tree.bind("<Double-1>", on_tree_double_click)

    # --- BUTTONS ---
    buttons_frame = ttk.Frame(search_win, padding=(10, 10)); buttons_frame.pack(fill=tk.X)
    
    tk.Button(buttons_frame, text="جستجو", command=search_action, bg=config.BLUE_COLOR, fg="white", font=(FONT_MAIN, 12), width=10).pack(side=tk.RIGHT, padx=5)
    tk.Button(buttons_frame, text="نمایش همه", command=reset_action, font=(FONT_MAIN, 12), width=10).pack(side=tk.RIGHT, padx=5)
    
    tk.Button(buttons_frame, text="خروجی اکسل", command=export_to_excel, bg="#2E7D32", fg="white", font=(FONT_MAIN, 12, "bold"), width=15).pack(side=tk.LEFT, padx=5)
    
    search_action()

def open_developer_mode(app):
    ensure_fonts()
    dev_win = tk.Toplevel(app)
    dev_win.title("پنل مدیریت")
    dev_win.geometry("400x700")
    try:
        dev_win.iconbitmap('app_icon.ico')
    except:
        pass
    dev_win.configure(bg=config.BLUE_COLOR)

    # --- NEW: Background Image ---
    if os.path.exists("developer.png"):
        try:
            original_img = Image.open("developer.png")
            resized_img = original_img.resize((400, 700), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(resized_img)
            
            bg_label = tk.Label(dev_win, image=bg_photo)
            bg_label.image = bg_photo # Keep reference
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception as e:
            print(f"Error loading developer background: {e}")
    # -----------------------------
    
    tk.Label(
        dev_win,
        text="ابزارهای مدیریت سیستم",
        font=(FONT_MAIN, 14, "bold"),
        bg=config.BLUE_COLOR,
        fg="white"
    ).pack(pady=20)
    
    # --- Buttons ---
    
    widgets.RoundedButton(
        dev_win,
        text="مدیریت کاربران",
        command=lambda: open_user_manager(dev_win),
        bg="#FF5722",
        hover_bg="#E64A19",
        font=(FONT_MAIN, 14, "bold"),
        width=250
    ).pack(pady=6)
    
    widgets.RoundedButton(
        dev_win,
        text="افزودن ۱۰۰ رکورد آزمایشی",
        command=database.add_dummy_data,
        bg=config.GREEN_COLOR,
        hover_bg=config.GREEN_ACTIVE_COLOR,
        font=(FONT_MAIN, 14),
        width=250
    ).pack(pady=6)
    widgets.RoundedButton(
        dev_win,
        text="پاکسازی کامل دیتابیس",
        command=database.delete_all_records,
        bg=config.RED_COLOR,
        hover_bg=config.RED_ACTIVE_COLOR,
        font=(FONT_MAIN, 14),
        width=250
    ).pack(pady=6)
    widgets.RoundedButton(
        dev_win,
        text="تعداد ورودی/خروجی های ثبت شده",
        command=lambda: show_daily_stats_ui(dev_win),
        bg="#673AB7",
        hover_bg="#5E35B1",
        font=(FONT_MAIN, 13),
        width=250
    ).pack(pady=6)
    widgets.RoundedButton(
        dev_win,
        text="نمودار تحلیل ترافیک",
        command=lambda: show_heatmap_analytics(app),
        bg="#E91E63",
        hover_bg="#D81B60",
        font=(FONT_MAIN, 13),
        width=250
    ).pack(pady=6)
    widgets.RoundedButton(
        dev_win,
        text="تهیه نسخه پشتیبان",
        command=utils.create_backup,
        bg="#009688",
        hover_bg="#00796B",
        font=(FONT_MAIN, 13),
        width=250
    ).pack(pady=6)
    widgets.RoundedButton(
        dev_win,
        text="بازیابی اطلاعات",
        command=utils.restore_backup,
        bg="#795548",
        hover_bg="#6D4C41",
        font=(FONT_MAIN, 13),
        width=250
    ).pack(pady=6)
    
    tk.Label(
        dev_win,
        text="⚠️ مخصوص راهبر سیستم و پشتیبانی",
        font=(FONT_MAIN, 10),
        bg=config.BLUE_COLOR, 
        fg="#E0E0E0"
    ).pack(side=tk.BOTTOM, pady=10)