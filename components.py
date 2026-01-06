import tkinter as tk
from tkinter import ttk

class AutocompleteEntry(ttk.Entry):
    def __init__(self, master, completevalues=None, **kwargs):
        super().__init__(master, **kwargs)
        self.completevalues = sorted(completevalues) if completevalues else []
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
            if event and event.widget == self.lb:
                try:
                    index = self.lb.nearest(event.y)
                    self.var.set(self.lb.get(index))
                except: pass
            else:
                try:
                    if self.lb.curselection():
                        self.var.set(self.lb.get(self.lb.curselection()))
                except: pass
            
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