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
    popup.geometry("450x300")
    popup.resizable(False, False)
    
    # Center popup
    x = search_win.winfo_x() + (search_win.winfo_width() // 2) - 225
    y = search_win.winfo_y() + (search_win.winfo_height() // 2) - 150
    popup.geometry(f"+{x}+{y}")
    
    # Main label
    tk.Label(popup, text=f"ثبت خروج برای: {visitor_name}", font=(FONT_MAIN, 12, "bold"), fg="#37474F").pack(pady=(20, 10))
    
    # Date check
    current_shamsi = jdatetime.date.fromgregorian(date=datetime.now().date()).strftime("%Y/%m/%d")
    if entry_shamsi_date != current_shamsi:
        tk.Label(popup, text=f"⚠️ تاریخ ورود: {entry_shamsi_date}\nامروز نیست! فقط برای تصحیح اطلاعات استفاده کنید.", 
                font=(FONT_MAIN, 10), fg="#D32F2F", justify="right").pack(pady=5)
    
    # Time selection frame
    time_frame = tk.Frame(popup)
    time_frame.pack(pady=15)
    
    tk.Label(time_frame, text=":ساعت خروج", font=(FONT_MAIN, 11)).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    
    # Hours dropdown (7-20)
    hours = [str(i).zfill(2) for i in range(7, 21)]  # 07 to 20
    hour_var = tk.StringVar(value=datetime.now().strftime("%H"))
    hour_combo = ttk.Combobox(time_frame, textvariable=hour_var, values=hours, width=4, state="readonly", justify='center')
    hour_combo.grid(row=0, column=1, padx=2)
    
    tk.Label(time_frame, text=":", font=(FONT_MAIN, 11)).grid(row=0, column=0, padx=2)
    
    # Minutes dropdown (00-59)
    minutes = [str(i).zfill(2) for i in range(0, 60, 5)]  # 00, 05, 10, ... 55
    minute_var = tk.StringVar(value=datetime.now().strftime("%M"))
    minute_combo = ttk.Combobox(time_frame, textvariable=minute_var, values=minutes, width=4, state="readonly", justify='center')
    minute_combo.grid(row=0, column=0, padx=(0, 25))
    
    # Set current time button
    def set_current_time():
        now = datetime.now()
        hour_var.set(now.strftime("%H"))
        minute_var.set(now.strftime("%M"))
    
    tk.Button(time_frame, text="زمان حال", command=set_current_time, bg="#2196F3", fg="white", 
              font=(FONT_MAIN, 9), width=8).grid(row=0, column=0, padx=(90, 0), sticky="w")
    
    # Entry time display for reference
    try:
        entry_time_only = item_values[5].split(' ')[1][:5] if ' ' in item_values[5] else item_values[5]
        tk.Label(popup, text=f"ساعت ورود: {entry_time_only}", font=(FONT_MAIN, 10), fg="#666").pack(pady=5)
    except:
        pass
    
    def confirm():
        # Validate time
        hour = hour_var.get()
        minute = minute_var.get()
        
        if not hour or not minute:
            messagebox.showerror("خطا", "لطفاً ساعت و دقیقه را انتخاب کنید", parent=popup)
            return
        
        # Check if exit time is before entry time
        try:
            entry_time_str = item_values[5]
            if ' ' in entry_time_str:
                entry_time_only = entry_time_str.split(' ')[1][:5]
                entry_hour, entry_minute = map(int, entry_time_only.split(':'))
                exit_hour, exit_minute = int(hour), int(minute)
                
                # Convert to minutes for comparison
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
        
        # Validate date if not same day
        if entry_shamsi_date != current_shamsi:
            response = messagebox.askyesno(
                "تأیید تاریخ",
                f"تاریخ ورود ({entry_shamsi_date}) با امروز ({current_shamsi}) متفاوت است.\n\n"
                "آیا مطمئن هستید که می‌خواهید خروج ثبت کنید؟",
                parent=popup
            )
            if not response:
                return
        
        exit_time_str = f"{hour}:{minute}"
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("UPDATE visitors SET exit_time = ? WHERE id = ?", (exit_time_str, visitor_id))
            conn.commit()
            conn.close()
            
            popup.destroy()
            search_win.destroy()
            
            app.deiconify()
            app.focus_set()
            
            msg = f"✓ زمان خروج {exit_time_str} برای {visitor_name} (کدملی: {national_id}) با موفقیت ثبت شد"
            show_status(msg, "#2E7D32", duration=10000)
            
        except Exception as e: 
            messagebox.showerror("خطا", f"خطا در ثبت خروج:\n{str(e)}", parent=popup)

    # Buttons frame
    btn_f = tk.Frame(popup)
    btn_f.pack(pady=20)
    
    tk.Button(btn_f, text="تایید خروج", bg=GREEN_COLOR, fg="white", width=12, 
              font=(FONT_MAIN, 10, "bold"), command=confirm).pack(side=tk.RIGHT, padx=5)
    
    tk.Button(btn_f, text="انصراف", bg=RED_COLOR, fg="white", width=12,
              font=(FONT_MAIN, 10), command=popup.destroy).pack(side=tk.RIGHT, padx=5)
    
    # Set focus to hour combo
    hour_combo.focus_set()
    
    # Bind Enter key to confirm
    popup.bind('<Return>', lambda e: confirm())