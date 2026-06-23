import tkinter as tk
import sys
import queue
from ui.theme import Theme

class LogPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=Theme.BG_PANEL)
        self.log_queue = queue.Queue()
        self.build_ui()
        self.redirect_stdout()
        self.poll_logs()
        
    def build_ui(self):
        # Header
        self.lbl = tk.Label(self, text="Terminal Logs", bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, font=Theme.FONT_BOLD, anchor="w")
        self.lbl.pack(fill=tk.X, padx=5, pady=2)
        
        # Text Area for logs
        self.text_area = tk.Text(self, bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, font=('Consolas', 10), state=tk.DISABLED, wrap=tk.WORD, height=6)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

    def write(self, string):
        self.log_queue.put(string)
        if hasattr(self, 'old_stdout'):
            self.old_stdout.write(string)
            self.old_stdout.flush()

    def flush(self):
        if hasattr(self, 'old_stdout'):
            self.old_stdout.flush()

    def redirect_stdout(self):
        self.old_stdout = sys.stdout
        sys.stdout = self
        
    def restore_stdout(self):
        if hasattr(self, 'old_stdout'):
            sys.stdout = self.old_stdout

    def destroy(self):
        self.restore_stdout()
        super().destroy()

    def poll_logs(self):
        try:
            while not self.log_queue.empty():
                msg = self.log_queue.get_nowait()
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, msg)
                self.text_area.see(tk.END)
                self.text_area.config(state=tk.DISABLED)
        except Exception:
            pass
        self.after(100, self.poll_logs)
        
    def apply_theme(self):
        self.configure(bg=Theme.BG_PANEL)
        self.lbl.configure(bg=Theme.BG_PANEL, fg=Theme.FG_MAIN)
        self.text_area.configure(bg=Theme.BG_INPUT, fg=Theme.FG_MAIN)
