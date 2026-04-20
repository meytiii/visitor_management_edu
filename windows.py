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
        if len(u) < 3 or len(p) < 3: return messagebox.showwarning("خطا", "نام کاربری و رمز عبور باید حداقل ۳ حرف باشند", parent=um_win)
        if len(fname) < 2: return messagebox.showwarning("خطا", "لطفاً نام و نام خانوادگی را وارد کنید", parent=um_win)
        
        ok, msg = database.create_user(u, p, fname, r)
        if ok:
            messagebox.showinfo("موفق", f"کاربر {fname} با موفقیت ایجاد شد", parent=um_win)
            for ent in [new_fullname_ent, new_user_ent, new_pass_ent]: ent.delete(0, tk.END)
            refresh_list()
        else: messagebox.showerror("خطا", msg, parent=um_win)

    tb.Button(action_frame, text="ثبت کاربر", command=add_user, bootstyle=SUCCESS).pack(fill=tk.X, pady=15, padx=20)
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
    cp_win.geometry("400x700")
    cp_win.resizable(False, False)
    try:
        cp_win.iconbitmap(utils.resource_path('app_icon.ico'))
    except:
        pass

    # --- Canvas for background and overlay ---
    canvas = tk.Canvas(cp_win, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Load and display background image
    bg_path = utils.resource_path("change_password_bg.png")
    bg_image = None
    if os.path.exists(bg_path):
        try:
            pil_img = Image.open(bg_path)
            # Resize to window size
            pil_img = pil_img.resize((400, 700), Image.Resampling.LANCZOS)
            bg_image = ImageTk.PhotoImage(pil_img)
            canvas.create_image(0, 0, image=bg_image, anchor="nw")
            # Keep reference
            canvas.bg_image = bg_image
        except Exception as e:
            print(f"Background error: {e}")

    # --- Semi-transparent card background ---
    # Draw a rounded rectangle with stipple for transparency effect
    card_x1, card_y1 = 30, 50
    card_x2, card_y2 = 370, 650
    radius = 20

    # Create rounded rectangle using a polygon approximation
    # We'll use a white fill with stipple to make it semi-transparent
    points = [
        card_x1 + radius, card_y1,
        card_x2 - radius, card_y1,
        card_x2, card_y1,
        card_x2, card_y1 + radius,
        card_x2, card_y2 - radius,
        card_x2, card_y2,
        card_x2 - radius, card_y2,
        card_x1 + radius, card_y2,
        card_x1, card_y2,
        card_x1, card_y2 - radius,
        card_x1, card_y1 + radius,
        card_x1, card_y1,
    ]
    # Smooth approximation (simple polygon; you can refine with more points if needed)
    canvas.create_polygon(points, fill="white", stipple="gray50", outline="#cccccc", width=1, smooth=True)

    # --- Place widgets on canvas ---
    # We'll create a frame as a window item for easier layout
    form_frame = tk.Frame(canvas, bg='', highlightthickness=0)  # transparent
    canvas.create_window(200, 350, window=form_frame, width=320, height=520)

    # Title
    tb.Label(
        form_frame,
        text="🔐 تغییر رمز عبور",
        font=(FONT_MAIN, 16, "bold"),
        bootstyle=PRIMARY,
        anchor="center",
        background=''  # transparent label background (ttk themes may override, but we try)
    ).pack(pady=(10, 15))

    tb.Label(
        form_frame,
        text=f"{username} : کاربر",
        font=(FONT_MAIN, 12),
        bootstyle=SECONDARY,
        anchor="center",
        background=''
    ).pack(pady=(0, 15))

    # Current password
    tb.Label(form_frame, text=": رمز عبور فعلی", font=(FONT_MAIN, 12), background='').pack(anchor="e", pady=(5, 2))
    current_pass_entry = tb.Entry(form_frame, show="●", justify="center", font=(FONT_MAIN, 12))
    current_pass_entry.pack(fill=tk.X, pady=(0, 10))
    current_pass_entry.focus()

    # New password
    tb.Label(form_frame, text=": رمز عبور جدید", font=(FONT_MAIN, 12), background='').pack(anchor="e", pady=(5, 2))
    new_pass_entry = tb.Entry(form_frame, show="●", justify="center", font=(FONT_MAIN, 12))
    new_pass_entry.pack(fill=tk.X, pady=(0, 10))

    # Confirm password
    tb.Label(form_frame, text=": تکرار رمز عبور جدید", font=(FONT_MAIN, 12), background='').pack(anchor="e", pady=(5, 2))
    confirm_pass_entry = tb.Entry(form_frame, show="●", justify="center", font=(FONT_MAIN, 12))
    confirm_pass_entry.pack(fill=tk.X, pady=(0, 15))

    # Status label
    status_label = tb.Label(form_frame, text="", font=(FONT_MAIN, 11), bootstyle=INFO, anchor="center", background='')
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
    btn_frame = tb.Frame(form_frame)
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