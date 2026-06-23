import tkinter as tk
from PIL import Image, ImageTk
import os
from ui.theme import Theme

class ControlPanel(tk.LabelFrame):
    def __init__(self, parent, solve_callback, coord_sys="Cartesian"):
        super().__init__(parent, text="Control Panel", bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, font=Theme.FONT_BOLD, padx=10, pady=10, relief="flat", bd=0)
        self.solve_callback = solve_callback
        self.coord_sys = coord_sys
        self.inputs = {}
        self.build_ui()
        
    def build_ui(self):
        self.main_frame = tk.Frame(self, bg=Theme.BG_PANEL)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        def add_input(parent, label_text, default_val):
            f = tk.Frame(parent, bg=Theme.BG_PANEL)
            f.pack(side=tk.TOP, fill=tk.X, pady=2, padx=5)
            tk.Label(f, text=label_text, width=14, bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, font=Theme.FONT_SMALL, anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f, width=8, bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, insertbackground=Theme.FG_MAIN, relief="flat", font=Theme.FONT_SMALL, justify="center")
            e.insert(0, str(default_val))
            e.pack(side=tk.RIGHT)
            return e
            
        if self.coord_sys == "Cartesian":
            labels = ["Left (x=0):", "Right (x=Lx):", "Front (y=0):", "Back (y=Ly):", "Bottom (z=0):", "Top (z=Lz):"]
            title1, title2, title3 = "X Boundaries", "Y Boundaries", "Z Boundaries"
        elif self.coord_sys == "Cylindrical":
            labels = ["Inner R (r=\u0394r):", "Outer R (r=R):", "Start \u0398 (\u03B8=0):", "End \u0398 (\u03B8=\u0398):", "Bottom (z=0):", "Top (z=Lz):"]
            title1, title2, title3 = "R Boundaries", "\u0398 Boundaries", "Z Boundaries"
        else: # Spherical
            labels = ["Inner R (r=\u0394r):", "Outer R (r=R):", "Start \u0398 (\u03B8=0):", "End \u0398 (\u03B8=\u0398):", "Start \u03A6 (\u03C6=0):", "End \u03A6 (\u03C6=\u03A6):"]
            title1, title2, title3 = "R Boundaries", "\u0398 Boundaries", "\u03A6 Boundaries"

        def add_separator():
            tk.Frame(self.main_frame, width=1, bg=Theme.BORDER).pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=5)

        grp_x = tk.Frame(self.main_frame, bg=Theme.BG_PANEL)
        grp_x.pack(side=tk.LEFT, padx=5, pady=0, fill=tk.Y)
        tk.Label(grp_x, text=title1, font=('Segoe UI', 9, 'bold'), fg=Theme.FG_SUB, bg=Theme.BG_PANEL).pack(anchor="w", padx=5)
        self.inputs['left'] = add_input(grp_x, labels[0], 100)
        self.inputs['right'] = add_input(grp_x, labels[1], 50)
        
        add_separator()
        
        grp_y = tk.Frame(self.main_frame, bg=Theme.BG_PANEL)
        grp_y.pack(side=tk.LEFT, padx=5, pady=0, fill=tk.Y)
        tk.Label(grp_y, text=title2, font=('Segoe UI', 9, 'bold'), fg=Theme.FG_SUB, bg=Theme.BG_PANEL).pack(anchor="w", padx=5)
        self.inputs['front'] = add_input(grp_y, labels[2], 0)
        self.inputs['back'] = add_input(grp_y, labels[3], 100)
        
        add_separator()
        
        grp_z = tk.Frame(self.main_frame, bg=Theme.BG_PANEL)
        grp_z.pack(side=tk.LEFT, padx=5, pady=0, fill=tk.Y)
        tk.Label(grp_z, text=title3, font=('Segoe UI', 9, 'bold'), fg=Theme.FG_SUB, bg=Theme.BG_PANEL).pack(anchor="w", padx=5)
        self.inputs['bottom'] = add_input(grp_z, labels[4], 75)
        self.inputs['top'] = add_input(grp_z, labels[5], 25)
        
        add_separator()
        
        grp_sim = tk.Frame(self.main_frame, bg=Theme.BG_PANEL)
        grp_sim.pack(side=tk.LEFT, padx=5, pady=0, fill=tk.Y)
        tk.Label(grp_sim, text="Simulation", font=('Segoe UI', 9, 'bold'), fg=Theme.FG_SUB, bg=Theme.BG_PANEL).pack(anchor="w", padx=5)
        self.inputs['dx'] = add_input(grp_sim, "Grid Res:", 0.05)
        
        # Center the solve button inside the simulation group
        btn_frame = tk.Frame(grp_sim, bg=Theme.BG_PANEL)
        btn_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)
        
        # Load and resize the play icon
        icon_path = os.path.join("assets", "play_icon.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((14, 14), Image.Resampling.LANCZOS)
            self.play_icon = ImageTk.PhotoImage(img)
            self.solve_btn = tk.Button(btn_frame, text=" SOLVE", image=self.play_icon, compound=tk.LEFT, bg=Theme.SUCCESS, fg=Theme.SUCCESS_FG, font=Theme.FONT_BOLD, relief="flat", command=self.solve_callback)
        else:
            self.solve_btn = tk.Button(btn_frame, text="▶ SOLVE", bg=Theme.SUCCESS, fg=Theme.SUCCESS_FG, font=Theme.FONT_BOLD, relief="flat", command=self.solve_callback)
            
        self.solve_btn.pack(fill=tk.X)
        self.solve_btn.bind("<Enter>", lambda e: self.solve_btn.config(bg=Theme.SUCCESS_HOVER))
        self.solve_btn.bind("<Leave>", lambda e: self.solve_btn.config(bg=Theme.SUCCESS))

    def apply_theme(self):
        self.configure(bg=Theme.BG_PANEL, fg=Theme.FG_MAIN)
        
        def update_widgets(parent):
            for widget in parent.winfo_children():
                if isinstance(widget, tk.Frame) or isinstance(widget, tk.LabelFrame):
                    widget.configure(bg=Theme.BG_PANEL)
                    if isinstance(widget, tk.LabelFrame):
                        widget.configure(fg=Theme.FG_SUB)
                    update_widgets(widget)
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=Theme.BG_PANEL, fg=Theme.FG_MAIN)
                elif isinstance(widget, tk.Entry):
                    widget.configure(bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, insertbackground=Theme.FG_MAIN)
                    
        update_widgets(self)
        self.solve_btn.configure(bg=Theme.SUCCESS, fg=Theme.SUCCESS_FG)
