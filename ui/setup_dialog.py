import tkinter as tk
from tkinter import ttk, messagebox
from ui.theme import Theme

class SetupDialog(tk.Toplevel):
    def __init__(self, parent, on_submit_callback, is_initial=False):
        super().__init__(parent)
        self.parent = parent
        self.on_submit_callback = on_submit_callback
        self.is_initial = is_initial
        self.setup_inputs = {}
        
        self.title("Environment Settings")
        self.configure(bg=Theme.BG_PANEL)
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center relative to parent
        self.center_window()
        
        # Handle close window button ('X')
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        inner_frame = tk.Frame(self, bg=Theme.BG_PANEL, padx=30, pady=30)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure styles
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Setup.TFrame', background=Theme.BG_ROOT)
        style.configure('Setup.TLabel', background=Theme.BG_PANEL, foreground=Theme.FG_MAIN, font=Theme.FONT_REGULAR)
        style.configure('Title.TLabel', background=Theme.BG_PANEL, foreground=Theme.ACCENT_HOVER, font=Theme.FONT_TITLE)
        style.configure('Setup.TCombobox', fieldbackground=Theme.BG_INPUT, background=Theme.BORDER, foreground=Theme.FG_MAIN, font=Theme.FONT_REGULAR)
        
        ttk.Label(inner_frame, text="Laplace 3D Explorer", style='Title.TLabel').pack(pady=(0, 5))
        ttk.Label(inner_frame, text="Define Coordinate System & Domain Size", style='Setup.TLabel', font=('Segoe UI', 11, 'italic'), foreground=Theme.FG_SUB).pack(pady=(0, 20))
        
        # Coordinate System Selection
        coord_frame = tk.Frame(inner_frame, bg=Theme.BG_PANEL)
        coord_frame.pack(fill=tk.X, pady=5)
        ttk.Label(coord_frame, text="Coordinate System:", style='Setup.TLabel', width=20, anchor="w").pack(side=tk.LEFT)
        
        # Pre-populate with current values if available
        current_coord = self.parent.coord_sys if hasattr(self.parent, 'coord_sys') else "Cartesian"
        self.coord_var = tk.StringVar(value=current_coord)
        self.coord_cb = ttk.Combobox(coord_frame, textvariable=self.coord_var, values=["Cartesian", "Cylindrical", "Spherical"], state="readonly", style='Setup.TCombobox', width=13, font=Theme.FONT_REGULAR)
        self.coord_cb.pack(side=tk.RIGHT)
        self.coord_cb.bind("<<ComboboxSelected>>", self.on_coord_change)
        
        # Dynamic Inputs Frame
        self.inputs_frame = tk.Frame(inner_frame, bg=Theme.BG_PANEL)
        self.inputs_frame.pack(fill=tk.X, pady=10)
        
        self.input_widgets = []
        self.on_coord_change()
        
        # Custom Modern Buttons
        self.btn_frame = tk.Frame(inner_frame, bg=Theme.BG_PANEL)
        self.btn_frame.pack(pady=20)
        
        self.submit_btn = tk.Button(self.btn_frame, text="Initialize Environment", bg=Theme.ACCENT, fg=Theme.FG_MAIN, font=Theme.FONT_BOLD, relief="flat", activebackground=Theme.ACCENT_HOVER, activeforeground=Theme.FG_MAIN, cursor="hand2", command=self.on_submit, padx=20, pady=10)
        
        self.cancel_btn = tk.Button(self.btn_frame, text="Cancel", bg=Theme.BORDER, fg=Theme.FG_MAIN, font=Theme.FONT_BOLD, relief="flat", activebackground=Theme.BORDER, activeforeground=Theme.FG_MAIN, cursor="hand2", command=self.on_cancel, padx=20, pady=10)
        
        if not self.is_initial:
            self.cancel_btn.pack(side=tk.LEFT, padx=10)
            self.submit_btn.pack(side=tk.LEFT, padx=10)
        else:
            self.submit_btn.pack(side=tk.TOP, padx=10)
            
        # Hover effects
        self.submit_btn.bind("<Enter>", lambda e: self.submit_btn.config(bg=Theme.ACCENT_HOVER))
        self.submit_btn.bind("<Leave>", lambda e: self.submit_btn.config(bg=Theme.ACCENT))
        
        self.cancel_btn.bind("<Enter>", lambda e: self.cancel_btn.config(bg=Theme.FG_SUB))
        self.cancel_btn.bind("<Leave>", lambda e: self.cancel_btn.config(bg=Theme.BORDER))

    def center_window(self):
        self.update_idletasks()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        
        width = 450
        height = 420
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def build_inputs(self):
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        
        self.input_widgets.clear()
        
        for lbl, default_val in zip(self.labels, self.defaults):
            f = tk.Frame(self.inputs_frame, bg=Theme.BG_PANEL)
            f.pack(fill=tk.X, pady=8)
            ttk.Label(f, text=lbl, style='Setup.TLabel', width=26, anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f, width=12, bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, insertbackground=Theme.FG_MAIN, relief="flat", font=Theme.FONT_REGULAR, justify="center")
            e.insert(0, default_val)
            e.pack(side=tk.RIGHT)
            self.input_widgets.append(e)

    def on_coord_change(self, event=None):
        coord = self.coord_var.get()
        if coord == "Cartesian":
            self.labels = ["Length X (Lx):", "Length Y (Ly):", "Length Z (Lz):"]
            # Pre-populate with parent dimensions if coordinate system matches
            if hasattr(self.parent, 'coord_sys') and self.parent.coord_sys == "Cartesian":
                self.defaults = [str(self.parent.Lx), str(self.parent.Ly), str(self.parent.Lz)]
            else:
                self.defaults = ["1.0", "1.0", "1.0"]
        elif coord == "Cylindrical":
            self.labels = ["Radius (R):", "Angle Theta (\u0398) [rad]:", "Height (Lz):"]
            if hasattr(self.parent, 'coord_sys') and self.parent.coord_sys == "Cylindrical":
                self.defaults = [str(self.parent.Lx), str(self.parent.Ly), str(self.parent.Lz)]
            else:
                self.defaults = ["1.0", "6.283185", "1.0"]
        elif coord == "Spherical":
            self.labels = ["Radius (R):", "Polar Angle (\u0398) [rad]:", "Azimuthal (\u03A6) [rad]:"]
            if hasattr(self.parent, 'coord_sys') and self.parent.coord_sys == "Spherical":
                self.defaults = [str(self.parent.Lx), str(self.parent.Ly), str(self.parent.Lz)]
            else:
                self.defaults = ["1.0", "3.14159", "6.283185"]
            
        self.build_inputs()

    def on_cancel(self):
        self.grab_release()
        self.destroy()

    def on_submit(self):
        try:
            val1 = float(self.input_widgets[0].get())
            val2 = float(self.input_widgets[1].get())
            val3 = float(self.input_widgets[2].get())
            
            if val1 <= 0 or val2 <= 0 or val3 <= 0:
                raise ValueError("Dimensions must be positive!")
                
            coord = self.coord_var.get()
            self.grab_release()
            self.destroy()
            
            # Pass coord system along with dimensions
            self.on_submit_callback(coord, val1, val2, val3)
        except ValueError:
            messagebox.showerror("Error", "Invalid dimensions! Please enter positive numbers.")
