import tkinter as tk
from tkinter import ttk, messagebox
from ui.theme import Theme

class SetupDialog:
    def __init__(self, parent, on_submit_callback):
        self.parent = parent
        self.on_submit_callback = on_submit_callback
        self.setup_inputs = {}
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Setup.TFrame', background=Theme.BG_ROOT)
        style.configure('Setup.TLabel', background=Theme.BG_ROOT, foreground=Theme.FG_MAIN, font=Theme.FONT_REGULAR)
        style.configure('Title.TLabel', background=Theme.BG_ROOT, foreground=Theme.ACCENT_HOVER, font=Theme.FONT_TITLE)
        style.configure('Setup.TCombobox', fieldbackground=Theme.BG_INPUT, background=Theme.BORDER, foreground=Theme.FG_MAIN, font=Theme.FONT_REGULAR)
        
        self.setup_frame = tk.Frame(parent, bg=Theme.BG_PANEL, highlightthickness=1, highlightbackground=Theme.BORDER, padx=40, pady=40)
        self.setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        inner_frame = tk.Frame(self.setup_frame, bg=Theme.BG_PANEL)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(inner_frame, text="Laplace 3D Explorer", style='Title.TLabel', background=Theme.BG_PANEL).pack(pady=(0, 5))
        ttk.Label(inner_frame, text="Define Coordinate System & Domain Size", style='Setup.TLabel', background=Theme.BG_PANEL, font=('Segoe UI', 11, 'italic'), foreground=Theme.FG_SUB).pack(pady=(0, 25))
        
        # Coordinate System Selection
        coord_frame = tk.Frame(inner_frame, bg=Theme.BG_PANEL)
        coord_frame.pack(fill=tk.X, pady=5)
        ttk.Label(coord_frame, text="Coordinate System:", style='Setup.TLabel', background=Theme.BG_PANEL, width=20, anchor="w").pack(side=tk.LEFT)
        
        self.coord_var = tk.StringVar(value="Cartesian")
        self.coord_cb = ttk.Combobox(coord_frame, textvariable=self.coord_var, values=["Cartesian", "Cylindrical", "Spherical"], state="readonly", style='Setup.TCombobox', width=13, font=Theme.FONT_REGULAR)
        self.coord_cb.pack(side=tk.RIGHT)
        self.coord_cb.bind("<<ComboboxSelected>>", self.on_coord_change)
        
        # Dynamic Inputs Frame
        self.inputs_frame = tk.Frame(inner_frame, bg=Theme.BG_PANEL)
        self.inputs_frame.pack(fill=tk.X, pady=10)
        
        self.labels = ["Length X (Lx):", "Length Y (Ly):", "Length Z (Lz):"]
        self.keys = ["dim1", "dim2", "dim3"]
        self.defaults = ["1.0", "1.0", "1.0"]
        self.input_widgets = []
        
        self.build_inputs()
        
        # Custom Modern Button
        btn_frame = tk.Frame(inner_frame, bg=Theme.BG_PANEL)
        btn_frame.pack(pady=30)
        
        self.submit_btn = tk.Button(btn_frame, text="Initialize Environment", bg=Theme.ACCENT, fg=Theme.FG_MAIN, font=Theme.FONT_BOLD, relief="flat", activebackground=Theme.ACCENT_HOVER, activeforeground=Theme.FG_MAIN, cursor="hand2", command=self.on_submit, padx=30, pady=12)
        self.submit_btn.pack()
        
        # Hover effects for button
        self.submit_btn.bind("<Enter>", lambda e: self.submit_btn.config(bg=Theme.ACCENT_HOVER))
        self.submit_btn.bind("<Leave>", lambda e: self.submit_btn.config(bg=Theme.ACCENT))
        
        self.on_coord_change()

    def build_inputs(self):
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        
        self.input_widgets.clear()
        
        for lbl, key, default_val in zip(self.labels, self.keys, self.defaults):
            f = tk.Frame(self.inputs_frame, bg=Theme.BG_PANEL)
            f.pack(fill=tk.X, pady=8)
            ttk.Label(f, text=lbl, style='Setup.TLabel', background=Theme.BG_PANEL, width=26, anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f, width=12, bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, insertbackground=Theme.FG_MAIN, relief="flat", font=Theme.FONT_REGULAR, justify="center")
            e.insert(0, default_val)
            e.pack(side=tk.RIGHT)
            self.input_widgets.append(e)

    def on_coord_change(self, event=None):
        coord = self.coord_var.get()
        if coord == "Cartesian":
            self.labels = ["Length X (Lx):", "Length Y (Ly):", "Length Z (Lz):"]
            self.defaults = ["1.0", "1.0", "1.0"]
        elif coord == "Cylindrical":
            self.labels = ["Radius (R):", "Angle Theta (\u0398) [rad]:", "Height (Lz):"]
            self.defaults = ["1.0", "6.283185", "1.0"]  # 2*pi approx
        elif coord == "Spherical":
            self.labels = ["Radius (R):", "Polar Angle (\u0398) [rad]:", "Azimuthal (\u03A6) [rad]:"]
            self.defaults = ["1.0", "3.14159", "6.283185"]  # pi, 2*pi
            
        self.build_inputs()

    def on_submit(self):
        try:
            val1 = float(self.input_widgets[0].get())
            val2 = float(self.input_widgets[1].get())
            val3 = float(self.input_widgets[2].get())
            
            if val1 <= 0 or val2 <= 0 or val3 <= 0:
                raise ValueError("Dimensions must be positive!")
                
            coord = self.coord_var.get()
            self.setup_frame.place_forget()
            
            # Pass coord system along with dimensions
            self.on_submit_callback(coord, val1, val2, val3)
        except ValueError:
            messagebox.showerror("Error", "Invalid dimensions! Please enter positive numbers.")
