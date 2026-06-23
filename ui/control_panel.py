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

        def add_input_pair(parent, label1, val1, label2, val2, key1, key2):
            f = tk.Frame(parent, bg=Theme.BG_PANEL)
            f.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=2)
            
            # Col 1
            f1 = tk.Frame(f, bg=Theme.BG_PANEL)
            f1.pack(side=tk.LEFT, padx=5)
            tk.Label(f1, text=label1, bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, font=Theme.FONT_SMALL, anchor="c").pack(side=tk.TOP, fill=tk.X)
            e1 = tk.Entry(f1, width=8, bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, insertbackground=Theme.FG_MAIN, relief="flat", font=Theme.FONT_SMALL, justify="center")
            e1.insert(0, str(val1))
            e1.pack(side=tk.TOP, pady=2)
            self.inputs[key1] = e1
            
            # Col 2
            f2 = tk.Frame(f, bg=Theme.BG_PANEL)
            f2.pack(side=tk.LEFT, padx=5)
            tk.Label(f2, text=label2, bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, font=Theme.FONT_SMALL, anchor="c").pack(side=tk.TOP, fill=tk.X)
            e2 = tk.Entry(f2, width=8, bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, insertbackground=Theme.FG_MAIN, relief="flat", font=Theme.FONT_SMALL, justify="center")
            e2.insert(0, str(val2))
            e2.pack(side=tk.TOP, pady=2)
            self.inputs[key2] = e2
            
        if self.coord_sys == "Cartesian":
            labels = ["Left (x=0)", "Right (x=Lx)", "Front (y=0)", "Back (y=Ly)", "Bottom (z=0)", "Top (z=Lz)"]
            title1, title2, title3 = "X Boundaries", "Y Boundaries", "Z Boundaries"
        elif self.coord_sys == "Cylindrical":
            labels = ["Inner R (r=\u0394r)", "Outer R (r=R)", "Start \u0398 (\u03B8=0)", "End \u0398 (\u03B8=\u0398)", "Bottom (z=0)", "Top (z=Lz)"]
            title1, title2, title3 = "R Boundaries", "\u0398 Boundaries", "Z Boundaries"
        else: # Spherical
            labels = ["Inner R (r=\u0394r)", "Outer R (r=R)", "Start \u0398 (\u03B8=0)", "End \u0398 (\u03B8=\u0398)", "Start \u03A6 (\u03C6=0)", "End \u03A6 (\u03C6=\u03A6)"]
            title1, title2, title3 = "R Boundaries", "\u0398 Boundaries", "\u03A6 Boundaries"

        def add_separator():
            tk.Frame(self.main_frame, width=1, bg=Theme.BORDER).pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=5)

        grp_x = tk.Frame(self.main_frame, bg=Theme.BG_PANEL)
        grp_x.pack(side=tk.LEFT, padx=5, pady=0, fill=tk.Y)
        tk.Label(grp_x, text=title1, font=('Segoe UI', 9, 'bold'), fg=Theme.FG_SUB, bg=Theme.BG_PANEL).pack(anchor="c", padx=5, pady=(0, 5))
        add_input_pair(grp_x, labels[0], 100, labels[1], 50, 'left', 'right')
        
        add_separator()
        
        grp_y = tk.Frame(self.main_frame, bg=Theme.BG_PANEL)
        grp_y.pack(side=tk.LEFT, padx=5, pady=0, fill=tk.Y)
        tk.Label(grp_y, text=title2, font=('Segoe UI', 9, 'bold'), fg=Theme.FG_SUB, bg=Theme.BG_PANEL).pack(anchor="c", padx=5, pady=(0, 5))
        add_input_pair(grp_y, labels[2], 0, labels[3], 100, 'front', 'back')
        
        add_separator()
        
        grp_z = tk.Frame(self.main_frame, bg=Theme.BG_PANEL)
        grp_z.pack(side=tk.LEFT, padx=5, pady=0, fill=tk.Y)
        tk.Label(grp_z, text=title3, font=('Segoe UI', 9, 'bold'), fg=Theme.FG_SUB, bg=Theme.BG_PANEL).pack(anchor="c", padx=5, pady=(0, 5))
        add_input_pair(grp_z, labels[4], 75, labels[5], 25, 'bottom', 'top')
        
        add_separator()
        
        grp_sim = tk.Frame(self.main_frame, bg=Theme.BG_PANEL)
        grp_sim.pack(side=tk.LEFT, padx=5, pady=0, fill=tk.Y)
        tk.Label(grp_sim, text="Simulation", font=('Segoe UI', 9, 'bold'), fg=Theme.FG_SUB, bg=Theme.BG_PANEL).pack(anchor="c", padx=5, pady=(0, 5))
        
        f_sim_inputs = tk.Frame(grp_sim, bg=Theme.BG_PANEL)
        f_sim_inputs.pack(side=tk.LEFT, pady=2)
        
        # Grid Res
        f_dx = tk.Frame(f_sim_inputs, bg=Theme.BG_PANEL)
        f_dx.pack(side=tk.LEFT, padx=5)
        tk.Label(f_dx, text="Grid Res", bg=Theme.BG_PANEL, fg=Theme.FG_MAIN, font=Theme.FONT_SMALL, anchor="c").pack(side=tk.TOP, fill=tk.X)
        self.inputs['dx'] = tk.Entry(f_dx, width=8, bg=Theme.BG_INPUT, fg=Theme.FG_MAIN, insertbackground=Theme.FG_MAIN, relief="flat", font=Theme.FONT_SMALL, justify="center")
        self.inputs['dx'].insert(0, "0.05")
        self.inputs['dx'].pack(side=tk.TOP, pady=2)
        
        # Center the solve button inside the simulation group
        f_btn = tk.Frame(grp_sim, bg=Theme.BG_PANEL)
        f_btn.pack(side=tk.LEFT, padx=10)
        
        # Load, recolor to white, and resize the play icon
        icon_path = os.path.join("assets", "play_icon.png")
        if os.path.exists(icon_path):
            try:
                img = Image.open(icon_path).convert("RGBA")
                
                # Recolor icon to white (white is 255, 255, 255)
                datas = img.getdata()
                new_data = []
                for item in datas:
                    # If pixel is not fully transparent, make it white but preserve alpha
                    if item[3] > 0:
                        new_data.append((255, 255, 255, item[3]))
                    else:
                        new_data.append(item)
                img.putdata(new_data)
                
                img = img.resize((12, 12), Image.Resampling.LANCZOS)
                self.play_icon = ImageTk.PhotoImage(img)
                self.solve_btn = tk.Button(f_btn, text=" SOLVE", image=self.play_icon, compound=tk.LEFT, bg=Theme.SUCCESS, fg=Theme.SUCCESS_FG, font=Theme.FONT_BOLD, relief="flat", padx=10, pady=4, command=self.solve_callback)
            except Exception:
                self.solve_btn = tk.Button(f_btn, text="▶ SOLVE", bg=Theme.SUCCESS, fg=Theme.SUCCESS_FG, font=Theme.FONT_BOLD, relief="flat", padx=10, pady=4, command=self.solve_callback)
        else:
            self.solve_btn = tk.Button(f_btn, text="▶ SOLVE", bg=Theme.SUCCESS, fg=Theme.SUCCESS_FG, font=Theme.FONT_BOLD, relief="flat", padx=10, pady=4, command=self.solve_callback)
            
        self.solve_btn.pack(side=tk.TOP, pady=5)
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
