import tkinter as tk

class ControlPanel(tk.LabelFrame):
    def __init__(self, parent, solve_callback, aspect_ratio_callback, coord_sys="Cartesian"):
        super().__init__(parent, text="Control Panel", bg="#2B2B2B", fg="white", font=('Arial', 12, 'bold'), padx=10, pady=10)
        self.solve_callback = solve_callback
        self.aspect_ratio_callback = aspect_ratio_callback
        self.coord_sys = coord_sys
        self.inputs = {}
        self.build_ui()
        
    def build_ui(self):
        def add_input(label_text, default_val):
            f = tk.Frame(self, bg="#2B2B2B")
            f.pack(fill=tk.X, pady=3)
            tk.Label(f, text=label_text, width=15, bg="#2B2B2B", fg="white", anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f, width=10, bg="#404040", fg="white", insertbackground="white", relief="flat")
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
        
        tk.Label(self, text="", bg="#2B2B2B").pack(pady=5)
        
        self.inputs['dx'] = add_input("Grid Resolution:", 0.05)
        
        self.solve_btn = tk.Button(self, text="SOLVE", bg="#006400", fg="white", font=('Arial', 10, 'bold'), relief="flat", command=self.solve_callback)
        self.solve_btn.pack(fill=tk.X, pady=25)
        
        self.equal_aspect_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Equal Aspect Ratio (True 3D Scale)", variable=self.equal_aspect_var, bg="#2B2B2B", fg="white", selectcolor="#404040", activebackground="#2B2B2B", activeforeground="white", command=self.aspect_ratio_callback).pack(anchor="w", pady=5)
