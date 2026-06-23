import tkinter as tk
from ui.theme import Theme

class ControlPanel(tk.LabelFrame):
    def __init__(self, parent, solve_callback, aspect_ratio_callback, coord_sys="Cartesian"):
        super().__init__(parent, text="Control Panel", bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, font=Theme.FONT_BOLD, padx=10, pady=10)
        self.solve_callback = solve_callback
        self.aspect_ratio_callback = aspect_ratio_callback
        self.coord_sys = coord_sys
        self.inputs = {}
        self.build_ui()
        
    def build_ui(self):
        def add_input(label_text, default_val):
            f = tk.Frame(self, bg=Theme.BG_PANEL)
            f.pack(fill=tk.X, pady=3)
            tk.Label(f, text=label_text, width=18, bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, font=Theme.FONT_SMALL, anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f, width=10, bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, insertbackground=Theme.FG_MAIN, relief="flat", font=Theme.FONT_SMALL)
            e.insert(0, str(default_val))
            e.pack(side=tk.RIGHT)
            return e
            
        if self.coord_sys == "Cartesian":
            labels = ["BC Left (x=0):", "BC Right (x=Lx):", "BC Front (y=0):", "BC Back (y=Ly):", "BC Bottom (z=0):", "BC Top (z=Lz):"]
        elif self.coord_sys == "Cylindrical":
            labels = ["Inner R (r=\u0394r):", "Outer R (r=R):", "Start \u0398 (\u03B8=0):", "End \u0398 (\u03B8=\u0398):", "Bottom (z=0):", "Top (z=Lz):"]
        else: # Spherical
            labels = ["Inner R (r=\u0394r):", "Outer R (r=R):", "Start \u0398 (\u03B8=0):", "End \u0398 (\u03B8=\u0398):", "Start \u03A6 (\u03C6=0):", "End \u03A6 (\u03C6=\u03A6):"]

        self.inputs['left'] = add_input(labels[0], 100)
        self.inputs['right'] = add_input(labels[1], 50)
        self.inputs['front'] = add_input(labels[2], 0)
        self.inputs['back'] = add_input(labels[3], 100)
        self.inputs['bottom'] = add_input(labels[4], 75)
        self.inputs['top'] = add_input(labels[5], 25)
        
        tk.Label(self, text="", bg=Theme.BG_PANEL).pack(pady=5)
        
        self.inputs['dx'] = add_input("Grid Resolution:", 0.05)
        
        self.solve_btn = tk.Button(self, text="SOLVE", bg=Theme.SUCCESS, fg=Theme.FG_MAIN, font=Theme.FONT_BOLD, relief="flat", command=self.solve_callback)
        self.solve_btn.pack(fill=tk.X, pady=25)
        self.solve_btn.bind("<Enter>", lambda e: self.solve_btn.config(bg=Theme.SUCCESS_HOVER))
        self.solve_btn.bind("<Leave>", lambda e: self.solve_btn.config(bg=Theme.SUCCESS))
        
        self.equal_aspect_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Equal Aspect Ratio (True 3D Scale)", variable=self.equal_aspect_var, bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, selectcolor=Theme.BG_INPUT, activebackground=Theme.BG_PANEL, activeforeground=Theme.FG_MAIN, font=Theme.FONT_SMALL, command=self.aspect_ratio_callback).pack(anchor="w", pady=5)
