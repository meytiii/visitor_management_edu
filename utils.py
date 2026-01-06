import win32ui
import win32print
import win32con
import arabic_reshaper
from tkinter import messagebox
from config import FONT_MAIN

def make_farsi(text):
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        return reshaped_text[::-1]
    except: return text

def validate_numeric(text):
    return text == "" or text.isdigit()

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")

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
            "ساعت خروج :",
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
        
        body_lines = []
        
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
