import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import os

class StartupDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Simulation Setup")
        self.geometry("350x250")
        self.configure(bg="#2B2B2B")
        self.resizable(False, False)
        
        self.result = None
        
        tk.Label(self, text="Define Domain Size", bg="#2B2B2B", fg="white", font=('Arial', 14, 'bold')).pack(pady=15)
        
        frame = tk.Frame(self, bg="#2B2B2B")
        frame.pack(pady=10)
        
        self.inputs = {}
        for lbl, key in [("Length X (Lx):", "Lx"), ("Length Y (Ly):", "Ly"), ("Length Z (Lz):", "Lz")]:
            f = tk.Frame(frame, bg="#2B2B2B")
            f.pack(fill=tk.X, pady=5)
            tk.Label(f, text=lbl, bg="#2B2B2B", fg="white", width=15, anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f, width=10, bg="#404040", fg="white", insertbackground="white", relief="flat")
            e.insert(0, "1.0")
            e.pack(side=tk.RIGHT)
            self.inputs[key] = e
            
        tk.Button(self, text="Create Environment", bg="#006400", fg="white", font=('Arial', 10, 'bold'), relief="flat", command=self.on_submit).pack(pady=20)
        
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.transient(master)
        self.grab_set()
        self.wait_window(self)
        
    def on_submit(self):
        try:
            Lx = float(self.inputs["Lx"].get())
            Ly = float(self.inputs["Ly"].get())
            Lz = float(self.inputs["Lz"].get())
            if Lx <= 0 or Ly <= 0 or Lz <= 0:
                raise ValueError("Dimensions must be positive!")
            print(f"[INFO] Environment Created: Lx={Lx}, Ly={Ly}, Lz={Lz}")
            self.result = (Lx, Ly, Lz)
            self.destroy()
        except ValueError:
            print("[ERROR] Invalid dimensions entered.")
            messagebox.showerror("Error", "Invalid dimensions! Please enter positive numbers.")
            
    def on_cancel(self):
        self.result = None
        self.destroy()

class Laplace3DApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.after(10, self.show_startup)
        
    def show_startup(self):
        dialog = StartupDialog(self)
        if not dialog.result:
            self.destroy()
            return
            
        self.Lx, self.Ly, self.Lz = dialog.result
        
        print("[INFO] Loading Machine Learning & Physics Libraries... Please Wait...")
        self.update()
        
        global np, FigureCanvasTkAgg, Figure, Solver3D, plotter
        import numpy as np
        import matplotlib
        matplotlib.use("TkAgg")
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        from core.solver import Solver3D
        from visualization import plotter
        
        self.title("Laplace 3D Explorer")
        self.geometry("1200x700")
        self.configure(bg="#1E1E1E")
        
        self.solver_res = None
        
        print("[INFO] Building Main GUI...")
        self.build_ui()
        self.deiconify()
        print("[INFO] Application Ready.")
        
    def build_ui(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#1E1E1E')
        style.configure('TLabel', background='#1E1E1E', foreground='white')
        style.configure('TButton', background='#006400', foreground='white', font=('Arial', 10, 'bold'))
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # LEFT PANEL
        left_panel = tk.LabelFrame(main_frame, text="Control Panel", bg="#2B2B2B", fg="white", font=('Arial', 12, 'bold'), padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.inputs = {}
        def add_input(label_text, default_val):
            f = tk.Frame(left_panel, bg="#2B2B2B")
            f.pack(fill=tk.X, pady=3)
            tk.Label(f, text=label_text, width=15, bg="#2B2B2B", fg="white", anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f, width=10, bg="#404040", fg="white", insertbackground="white", relief="flat")
            e.insert(0, str(default_val))
            e.pack(side=tk.RIGHT)
            return e
            
        self.inputs['left'] = add_input("BC Left:", 100)
        self.inputs['right'] = add_input("BC Right:", 50)
        self.inputs['front'] = add_input("BC Front:", 0)
        self.inputs['back'] = add_input("BC Back:", 100)
        self.inputs['bottom'] = add_input("BC Bottom:", 75)
        self.inputs['top'] = add_input("BC Top:", 25)
        
        tk.Label(left_panel, text="", bg="#2B2B2B").pack(pady=5)
        
        self.inputs['dx'] = add_input("Grid dx:", 0.05)
        
        solve_btn = tk.Button(left_panel, text="SOLVE", bg="#006400", fg="white", font=('Arial', 10, 'bold'), relief="flat", command=self.solve_system)
        solve_btn.pack(fill=tk.X, pady=25)
        
        # CENTER PANEL
        center_panel = tk.Frame(main_frame, bg="#1E1E1E")
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        top_center = tk.Frame(center_panel, bg="#1E1E1E")
        top_center.pack(fill=tk.X, pady=5)
        
        tk.Label(top_center, text="Visual Type:", bg="#1E1E1E", fg="white").pack(side=tk.LEFT, padx=5)
        self.vis_type = tk.StringVar(value="Domain Geometry")
        vis_cb = ttk.Combobox(top_center, textvariable=self.vis_type, values=["Domain Geometry", "Heatmap 2D", "Contour 2D", "Surface 2D", "Scatter 3D", "Isosurface"], state="readonly")
        vis_cb.pack(side=tk.LEFT, padx=5)
        vis_cb.bind("<<ComboboxSelected>>", lambda e: self.render_visualization())
        
        self.lbl_z_slider = tk.Label(top_center, text="Z Layer:", bg="#1E1E1E", fg="white")
        self.lbl_z_slider.pack(side=tk.LEFT, padx=15)
        self.z_slider = tk.Scale(top_center, from_=0, to=10, orient=tk.HORIZONTAL, bg="#1E1E1E", fg="white", highlightthickness=0, command=lambda v: self.render_visualization())
        self.z_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.fig.patch.set_facecolor('#1E1E1E')
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=center_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # RIGHT PANEL
        right_panel = tk.LabelFrame(main_frame, text="Dashboard & Export", bg="#2B2B2B", fg="white", font=('Arial', 12, 'bold'), padx=10, pady=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        self.labels = {}
        for lbl in ["Time", "Iter", "Error", "Max Temp", "Min Temp", "Center Temp"]:
            self.labels[lbl] = tk.Label(right_panel, text=f"{lbl}: -", bg="#2B2B2B", fg="white", anchor="w", font=('Consolas', 10))
            self.labels[lbl].pack(fill=tk.X, pady=8)
            
        tk.Button(right_panel, text="Export CSV", bg="#333333", fg="white", relief="flat", command=self.export_csv).pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
    def solve_system(self):
        try:
            BC = {k: float(self.inputs[k].get()) for k in ['left', 'right', 'front', 'back', 'bottom', 'top']}
            dx = float(self.inputs['dx'].get())
            
            # Internal Advanced Solver Settings
            omega = 1.8
            tol = 1e-6
            max_iter = 2000
            
            print(f"\n[INFO] Starting Simulation Solver...")
            print(f"[INFO] BCs: {BC}")
            print(f"[INFO] Parameters: dx={dx}, omega={omega}, tol={tol}, max_iter={max_iter}")
            
            self.title("Laplace 3D Explorer - SOLVING...")
            self.update()
            
            t0 = time.time()
            solver = Solver3D(self.Lx, self.Ly, self.Lz, dx, BC, omega, tol, max_iter)
            solver.solve()
            elapsed = time.time() - t0
            
            print(f"[INFO] Solver finished in {elapsed:.3f} seconds.")
            print(f"[INFO] Total Iterations: {solver.iter}, Final Error: {solver.err:.2e}")
            
            self.solver_res = solver
            
            self.labels["Time"].config(text=f"Time: {elapsed:.3f} s")
            self.labels["Iter"].config(text=f"Iter: {solver.iter}")
            self.labels["Error"].config(text=f"Error: {solver.err:.2e}")
            self.labels["Max Temp"].config(text=f"Max Temp: {np.max(solver.T):.2f}")
            self.labels["Min Temp"].config(text=f"Min Temp: {np.min(solver.T):.2f}")
            
            ny, nx, nz = solver.T.shape
            self.labels["Center Temp"].config(text=f"Center Temp: {solver.T[ny//2, nx//2, nz//2]:.2f}")
            
            self.z_slider.config(to=nz-1)
            self.z_slider.set(nz//2)
            
            self.title("Laplace 3D Explorer")
            self.render_visualization()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.title("Laplace 3D Explorer")
            
    def render_visualization(self, event=None):
        if self.solver_res is None: return
        
        v_type = self.vis_type.get()
        print(f"[INFO] Rendering Visual: {v_type}")
        
        # Toggle slider visibility
        if "2D" in v_type:
            self.lbl_z_slider.pack(side=tk.LEFT, padx=15)
            self.z_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        else:
            self.lbl_z_slider.pack_forget()
            self.z_slider.pack_forget()
            
        self.fig.clf()
        
        if "3D" in v_type or "Iso" in v_type or "Surface" in v_type or "Geometry" in v_type:
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.ax = self.fig.add_subplot(111)
            
        self.ax.set_facecolor('#1E1E1E')
        self.ax.tick_params(colors='white')
            
        curr_z = int(float(self.z_slider.get()))
        
        T = self.solver_res.T
        X = self.solver_res.X
        Y = self.solver_res.Y
        Z = self.solver_res.Z
        
        X2D = X[:, :, curr_z]
        Y2D = Y[:, :, curr_z]
        T2D = T[:, :, curr_z]
        
        if v_type == "Domain Geometry":
            plotter.plot_domain_geometry(self.ax, self.solver_res.Lx, self.solver_res.Ly, self.solver_res.Lz)
        elif v_type == "Heatmap 2D":
            plotter.plot_heatmap(self.ax, X2D, Y2D, T2D)
        elif v_type == "Contour 2D":
            plotter.plot_contour(self.ax, X2D, Y2D, T2D)
        elif v_type == "Surface 2D":
            plotter.plot_surface(self.ax, X2D, Y2D, T2D)
        elif v_type == "Scatter 3D":
            plotter.plot_scatter3d(self.ax, X, Y, Z, T)
        elif v_type == "Isosurface":
            plotter.plot_isosurface(self.ax, X, Y, Z, T)
            
        self.ax.set_xlabel('X Axis', color='white', fontsize=10)
        self.ax.set_ylabel('Y Axis', color='white', fontsize=10)
        if hasattr(self.ax, 'set_zlabel'):
            self.ax.set_zlabel('Z Axis', color='white', fontsize=10)
            
        self.fig.tight_layout()
        self.canvas.draw()
        
    def export_csv(self):
        if self.solver_res is None: return
        curr_z = int(float(self.z_slider.get()))
        f = filedialog.asksaveasfilename(defaultextension=".csv")
        if f:
            print(f"[INFO] Exporting CSV to: {f}")
            np.savetxt(f, self.solver_res.T[:, :, curr_z], delimiter=",")
            print("[INFO] Export Successful!")
            messagebox.showinfo("Export", "CSV Exported Successfully!")

if __name__ == "__main__":
    app = Laplace3DApp()
    app.mainloop()
