import tkinter as tk
from ui.theme import Theme

class DashboardPanel(tk.LabelFrame):
    def __init__(self, parent, export_callback):
        super().__init__(parent, text="Dashboard & Export", bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, font=Theme.FONT_BOLD, padx=10, pady=10)
        self.export_callback = export_callback
        self.labels = {}
        self.build_ui()
        
    def build_ui(self):
        for lbl in ["Time", "Iter", "Error", "Max Temp", "Min Temp", "Center Temp"]:
            self.labels[lbl] = tk.Label(self, text=f"{lbl}: -", bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, anchor="w", font=('Consolas', 10))
            self.labels[lbl].pack(fill=tk.X, pady=8)
            
        export_btn = tk.Button(self, text="Export CSV", bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, relief="flat", font=Theme.FONT_SMALL, command=self.export_callback)
        export_btn.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        export_btn.bind("<Enter>", lambda e: export_btn.config(bg=Theme.BORDER))
        export_btn.bind("<Leave>", lambda e: export_btn.config(bg=Theme.BG_INPUT))
        
    def update_metrics(self, elapsed_time, iter_count, error, max_t, min_t, center_t):
        self.labels["Time"].config(text=f"Time: {elapsed_time:.3f} s")
        self.labels["Iter"].config(text=f"Iter: {iter_count}")
        self.labels["Error"].config(text=f"Error: {error:.2e}")
        self.labels["Max Temp"].config(text=f"Max Temp: {max_t:.2f}")
        self.labels["Min Temp"].config(text=f"Min Temp: {min_t:.2f}")
        self.labels["Center Temp"].config(text=f"Center Temp: {center_t:.2f}")
