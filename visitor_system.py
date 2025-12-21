import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, font
from datetime import datetime
import os
import tempfile
import platform
import jdatetime

import win32ui
import win32print
import win32con

from PIL import Image, ImageTk

APP_VERSION = "1.1.5"
DEPARTMENT_LIST = [
    "حوزه مدیر کل", "معاونت پرورشی", "معاونت تربیت بدنی",
    "معاونت نهضت سواد آموزی", "معاونت آموزش متوسطه", "معاونت آموزش ابتدایی",
    "اداره حراست", "اداره سنجش", "اداره خدمات و پشتیبانی",
    "امور اداری", "اداره فن آوری", "اداره امور مالی و حسابداری",
    "اداره بودجه", "اداره تعاون و رفاه", "اداره استعداد های درخشان",
    "اداره امور شاهد", "اداره بازرسی", "اداره روابط عمومی",
    "اداره حقوقی", "اداره مشارکت ها", "اداره آموزش استثنائی",
    "کارپردازی", "معاونت پژوهش برنامه ریزی و توسعه منابع"
]
PERSIAN_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]

GREEN_COLOR = "#4CAF50"
GREEN_ACTIVE_COLOR = "#45a049"
BLUE_COLOR = "#008CBA"
BLUE_ACTIVE_COLOR = "#007ba7"
RED_COLOR = "#f44336"
RED_ACTIVE_COLOR = "#d32f2f"
DEFAULT_BG_COLOR = "#F0F0F0"

# --- Database and Core Logic ---
def setup_database():
    conn = sqlite3.connect('visitor_log.db')
    cursor = conn.cursor()
    try: cursor.execute("ALTER TABLE visitors ADD COLUMN shamsi_date TEXT;")
    except sqlite3.OperationalError: pass
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT, visitor_name TEXT NOT NULL,
            national_id TEXT NOT NULL, employee_to_meet TEXT NOT NULL,
            department TEXT NOT NULL, entry_time TEXT NOT NULL,
            shamsi_date TEXT, exit_time TEXT
        )''')
    conn.commit(); conn.close()

def show_help_popup():
    help_text = f"در صورت بروز هرگونه مشکل یا سوال با شماره زیر تماس بگیرید\n\nخرّم آبادی - 09222550573\n\nنسخه برنامه {APP_VERSION}"
    messagebox.showinfo("راهنما", help_text)

def submit_visitor():
    visitor_name, national_id, employee_to_meet, department = (entry_visitor_name.get(), entry_national_id.get(), entry_employee_to_meet.get(), combo_department.get())
    if not all([visitor_name, national_id, employee_to_meet, department]):
        messagebox.showwarning("خطا", "لطفاً تمام اطلاعات را وارد کنید"); return
    now = datetime.now()
    entry_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    shamsi_date_str = jdatetime.date.fromgregorian(date=now.date()).strftime("%Y/%m/%d")
    try:
        conn = sqlite3.connect('visitor_log.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO visitors (visitor_name, national_id, employee_to_meet, department, entry_time, shamsi_date) VALUES (?, ?, ?, ?, ?, ?)',(visitor_name, national_id, employee_to_meet, department, entry_time_str, shamsi_date_str))
        visitor_id = cursor.lastrowid
        conn.commit(); conn.close()
        print_receipt(visitor_id, visitor_name, national_id, employee_to_meet, department, now, shamsi_date_str)
        clear_fields()
        messagebox.showinfo("موفق", f"ورود مهمان با شماره {visitor_id} ثبت شد")
    except sqlite3.Error as e: messagebox.showerror("خطای پایگاه داده", f"خطا در ثبت اطلاعات: {e}")

def print_receipt(visitor_id, name, nid, emp, dept, entry_dt, shamsi_date):
    try:
        printer_name = win32print.GetDefaultPrinter()
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        hDC.StartDoc("Visitor Receipt")
        hDC.StartPage()

        page_width = hDC.GetDeviceCaps(win32con.HORZRES)
        
        x_center = page_width // 2
        x_right_margin = page_width - 10
        y = 10
        line_height = 50

        font_data = {"name": "B Titr", "height": 45, "weight": 700} 
        f = win32ui.CreateFont(font_data)
        hDC.SelectObject(f)

        headers = [
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
            f"ملاقات شونده: {emp}",
            f"واحد: {dept}",
            "--------------------------------",
            "* حداکثر زمان حضور 2 ساعت می باشد *",
            "",
            "امضاء نگهبان",
            "",
            "امضاء ملاقات شونده",
            "",
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


def clear_fields():
    entry_visitor_name.delete(0, tk.END); entry_national_id.delete(0, tk.END)
    entry_employee_to_meet.delete(0, tk.END); combo_department.set("")
    entry_visitor_name.focus()

# --- UPDATED BACKGROUND FUNCTION (Full Visibility + Auto-Resizing) ---
def setup_background(window_frame):
    """
    Loads 'background.png', sets up dynamic resizing, 
    and displays the image fully visible (no fading/transparency).
    """
    if not os.path.exists("background.png"):
        return

    try:
        # 1. Load the original image
        window_frame.original_img = Image.open("background.png")

        # 2. Create the Label that will hold the image
        bg_label = tk.Label(window_frame)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower() # Send to back

        # 3. Define the resize logic
        def resize_image(event):
            # Get the new window size
            new_w, new_h = event.width, event.height
            
            # Prevent errors if window is too small during startup
            if new_w < 50 or new_h < 50: return

            # Resize the image directly
            resized = window_frame.original_img.resize((new_w, new_h), Image.BICUBIC)

            # Convert to Tkinter PhotoImage and display
            photo = ImageTk.PhotoImage(resized)
            bg_label.config(image=photo)
            bg_label.image = photo # Keep reference

        # 4. Bind the resize event
        window_frame.bind('<Configure>', resize_image)

    except Exception as e:
        print(f"Background Error: {e}")


def open_search_window():
    search_win = tk.Toplevel(app)
    try: search_win.iconbitmap('app_icon.ico')
    except Exception: pass
    search_win.title("مشاهده و جستجوی سوابق")
    search_win.geometry("1150x700")
    
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
    combo_search_dept = ttk.Combobox(search_frame, values=[""] + DEPARTMENT_LIST, justify='right', state='readonly'); combo_search_dept.grid(row=1, column=2, sticky=tk.EW, padx=5, pady=5)
    search_frame.columnconfigure(2, weight=1); search_frame.columnconfigure(4, weight=1)
    
    tree_frame = ttk.Frame(search_win, padding=(10, 5)); tree_frame.pack(expand=True, fill=tk.BOTH)
    columns = ("id", "visitor_name", "national_id", "employee_to_meet", "department", "entry_time", "shamsi_date", "exit_time")
    
    style.configure("Custom.Treeview", font=(FONT_TABLE, 13, "bold"), rowheight=35)
    style.configure("Custom.Treeview.Heading", font=(FONT_MAIN, 12))

    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="browse", style="Custom.Treeview")
    headings = {"id": "شماره", "visitor_name": "نام مهمان", "national_id": "کد ملی", "employee_to_meet": "ملاقات شونده", "department": "واحد", "entry_time": "ساعت ورود", "shamsi_date": "تاریخ ورود", "exit_time": "ساعت خروج"}
    for col, text in headings.items(): tree.heading(col, text=text)
    for col in columns: tree.column(col, anchor=tk.CENTER)
    widths = {"id": 60, "visitor_name": 150, "national_id": 100, "employee_to_meet": 150, "department": 120, "entry_time": 80, "shamsi_date": 100, "exit_time": 80}
    for col, width in widths.items(): tree.column(col, width=width)
    
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set); scrollbar.pack(side=tk.RIGHT, fill=tk.Y); tree.pack(expand=True, fill=tk.BOTH)

    def populate_tree(records):
        for i in tree.get_children(): tree.delete(i)
        for record in records:
            display_record = (record[0], record[1], record[2], record[3], record[4], datetime.strptime(record[5], "%Y-%m-%d %H:%M:%S").strftime("%H:%M"), record[6] or "", record[7] or "")
            tree.insert("", tk.END, values=display_record)
            
    def fetch_and_display_records(filters=None):
        if filters is None: filters = {}
        conn = sqlite3.connect('visitor_log.db'); cursor = conn.cursor()
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
        
        query += " ORDER BY id DESC"; cursor.execute(query, params); populate_tree(cursor.fetchall()); conn.close()

    def search_action(): fetch_and_display_records({"name": entry_search_name.get(), "nid": entry_search_nid.get(), "year": combo_year.get(), "month_name": combo_month.get(), "day": combo_day.get(), "dept": combo_search_dept.get()})
    def reset_action():
        entry_search_name.delete(0, tk.END); entry_search_nid.delete(0, tk.END)
        combo_year.set(""); combo_month.set(""); combo_day.set(""); combo_search_dept.set(""); fetch_and_display_records({})

    def on_tree_double_click(event):
        selected_item = tree.selection()
        if not selected_item: return
        item_values = tree.item(selected_item, "values")
        visitor_id = item_values[0]
        visitor_name = item_values[1]
        existing_exit_time = item_values[7]

        if existing_exit_time and existing_exit_time.strip():
             messagebox.showerror("خطا", "ساعت خروج برای این مهمان ثبت شده و امکان ثبت ساعت جدید نمی باشد!", parent=search_win)
             return

        popup = tk.Toplevel(search_win)
        popup.title("ثبت خروج")
        popup.geometry("400x250")
        popup.resizable(False, False)
        try: popup.iconbitmap('app_icon.ico')
        except: pass
        x = search_win.winfo_x() + (search_win.winfo_width() // 2) - 175
        y = search_win.winfo_y() + (search_win.winfo_height() // 2) - 90
        popup.geometry(f"+{x}+{y}")

        tk.Label(popup, text=f":ثبت خروج برای\n{visitor_name}", font=(FONT_MAIN, 13, "bold")).pack(pady=10)
        tk.Label(popup, text="ساعت خروج برای مهمان انتخاب شده ثبت شود؟", font=(FONT_MAIN, 12)).pack(pady=5)

        def confirm_exit():
            exit_time_str = datetime.now().strftime("%H:%M")
            try:
                conn = sqlite3.connect('visitor_log.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE visitors SET exit_time = ? WHERE id = ?", (exit_time_str, visitor_id))
                conn.commit(); conn.close()
                popup.destroy()
                search_action()
                messagebox.showinfo("موفق", "ساعت خروج با موفقیت ثبت شد", parent=search_win)
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در ثبت ساعت خروج: {e}", parent=search_win)

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="بله", bg=GREEN_COLOR, fg="white", width=10, font=(FONT_MAIN, 12, "bold"), command=confirm_exit).pack(side=tk.RIGHT, padx=10)
        tk.Button(btn_frame, text="خیر", bg=RED_COLOR, fg="white", width=10, font=(FONT_MAIN, 12, "bold"), command=popup.destroy).pack(side=tk.RIGHT, padx=10)

    tree.bind("<Double-1>", on_tree_double_click)
    buttons_frame = ttk.Frame(search_win, padding=(10, 10)); buttons_frame.pack(fill=tk.X)
    tk.Button(buttons_frame, text="جستجو", command=search_action, bg=BLUE_COLOR, fg="white", font=(FONT_MAIN, 12), activebackground=BLUE_ACTIVE_COLOR, activeforeground="white", relief="flat", borderwidth=0, width=12).pack(side=tk.RIGHT, padx=5, ipady=2)
    tk.Button(buttons_frame, text="نمایش همه", command=reset_action, font=(FONT_MAIN, 12), relief="flat", borderwidth=0, width=12).pack(side=tk.RIGHT, padx=5, ipady=2)
    reset_action()

# --- Main Application Setup ---
app = tk.Tk()
app.title(f"سامانه مدیریت ورود و خروج (اداره حراست) - نسخه {APP_VERSION}")
app.geometry("650x600")
app.resizable(False, False)
app.configure(bg=DEFAULT_BG_COLOR)
try: app.iconbitmap('app_icon.ico')
except Exception: pass

# --- FONT SAFETY CHECK ---
available_fonts = font.families()
if "B Titr" in available_fonts: FONT_MAIN = "B Titr"
else: FONT_MAIN = "Tahoma"

if "B Nazanin" in available_fonts: FONT_TABLE = "B Nazanin"
else: FONT_TABLE = "Tahoma"

style = ttk.Style(app); style.theme_use("vista")
style.configure(".", font=(FONT_MAIN, 13), background=DEFAULT_BG_COLOR)
style.configure("TLabel", anchor="east"); style.configure("TFrame", background=DEFAULT_BG_COLOR)

frame = ttk.Frame(app, padding=(20, 15)); frame.pack(expand=True, fill=tk.BOTH)

# --- APPLY BACKGROUND IMAGE ---
# Ensure 'background.jpg' is in the same folder
setup_background(frame)

labels = {": نام ملاقات کننده": 0, ": شماره کارت ملی": 1, ": نام ملاقات شونده": 2, ": امور / واحد مربوطه": 3}
for text, row in labels.items(): ttk.Label(frame, text=text).grid(row=row, column=1, padx=10, pady=10, sticky="e")

entry_visitor_name = ttk.Entry(frame, justify='right', font=(FONT_MAIN, 13))
entry_national_id = ttk.Entry(frame, justify='right', font=(FONT_MAIN, 13))
entry_employee_to_meet = ttk.Entry(frame, justify='right', font=(FONT_MAIN, 13))
combo_department = ttk.Combobox(frame, values=DEPARTMENT_LIST, justify='right', state='readonly', font=(FONT_MAIN, 13))

entry_visitor_name.grid(row=0, column=0, sticky="ew", padx=10, pady=10); entry_national_id.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
entry_employee_to_meet.grid(row=2, column=0, sticky="ew", padx=10, pady=10); combo_department.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

frame.grid_columnconfigure(0, weight=1)

submit_button = tk.Button(frame, text="ثبت و چاپ رسید", command=submit_visitor, bg=GREEN_COLOR, fg="white", activebackground=GREEN_ACTIVE_COLOR, activeforeground="white", font=(FONT_MAIN, 14, "bold"), relief="flat", borderwidth=0)
submit_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=(20, 5), ipady=8)

search_db_button = tk.Button(frame, text="مشاهده و جستجوی سوابق", command=open_search_window, bg=BLUE_COLOR, fg="white", activebackground=BLUE_ACTIVE_COLOR, activeforeground="white", font=(FONT_MAIN, 13), relief="flat", borderwidth=0)
search_db_button.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5, ipady=4)

help_button = tk.Button(frame, text="راهنما", command=show_help_popup, bg="#607D8B", fg="white", activebackground="#546E7A", activeforeground="white", font=(FONT_MAIN, 13), relief="flat", borderwidth=0)
help_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=(5,0), ipady=4)

version_label = ttk.Label(frame, text=f"نسخه برنامه : {APP_VERSION}", font=(FONT_MAIN, 11), foreground="#808080")
version_label.grid(row=7, column=0, columnspan=2, pady=(10, 0))

if __name__ == "__main__":
    setup_database()
    app.mainloop()