import tkinter as tk
from tkinter import messagebox, filedialog
import time
import os

# Initialize globals to satisfy Pylance/Pyright
np = None
Solver3D = None
plotter = None

from ui.setup_dialog import SetupDialog
from ui.control_panel import ControlPanel
from ui.dashboard_panel import DashboardPanel
from ui.visualization_panel import VisualizationPanel

class Laplace3DApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Laplace 3D Explorer")
        self.geometry("1200x700")
        self.configure(bg="#1E1E1E")
        self.resizable(True, True)
        
        self.solver_res = None
        self.Lx = 1.0
        self.Ly = 1.0
        self.Lz = 1.0
        
        self.setup_dialog = SetupDialog(self, self.on_setup_submit)
        
        self.loading_frame = tk.Frame(self, bg="#1E1E1E")
        tk.Label(self.loading_frame, text="Loading Physics Engine & 3D Visualizer...\nPlease wait...", bg="#1E1E1E", fg="white", font=('Arial', 18, 'italic'), justify=tk.CENTER).pack(pady=50)

    def on_setup_submit(self, Lx, Ly, Lz):
        self.Lx = Lx
        self.Ly = Ly
        self.Lz = Lz
        
        self.loading_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.update()
        
        # Delay heavy load slightly so UI can update the loading text
        self.after(50, self.load_heavy_libraries)
        
    def load_heavy_libraries(self):
        print("[INFO] Loading Machine Learning & Physics Libraries...")
        
        global np, Solver3D, plotter
        import numpy as np
        import matplotlib
        matplotlib.use("TkAgg")
        import matplotlib.backends.backend_tkagg as tkagg
        import matplotlib.figure as fig_mod
        from core.solver import Solver3D
        from visualization import plotter
        
        # Inject lazy loaded modules into visualization panel module
        import ui.visualization_panel as viz_mod
        viz_mod.np = np
        viz_mod.FigureCanvasTkAgg = tkagg.FigureCanvasTkAgg
        viz_mod.NavigationToolbar2Tk = tkagg.NavigationToolbar2Tk
        viz_mod.Figure = fig_mod.Figure
        viz_mod.plotter = plotter
        
        # Inject globals locally
        globals()['np'] = np
        globals()['Solver3D'] = Solver3D
        globals()['plotter'] = plotter
        
        self.loading_frame.place_forget()
        print("[INFO] Building Main GUI...")
        self.build_ui()
        print("[INFO] Application Ready.")
        
        # Render initial domain geometry
        self.visualization_panel.render_visualization()
        
    def build_ui(self):
        # Configure global styles for ttk
        style = tk.ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#1E1E1E')
        style.configure('TLabel', background='#1E1E1E', foreground='white')
        style.configure('TButton', background='#006400', foreground='white', font=('Arial', 10, 'bold'))
        
        main_frame = tk.ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 1. Left Panel (Control Panel)
        self.control_panel = ControlPanel(main_frame, self.solve_system, self.on_aspect_ratio_toggle)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 2. Center Panel (Visualization)
        self.visualization_panel = VisualizationPanel(main_frame, self)
        self.visualization_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # 3. Right Panel (Dashboard)
        self.dashboard_panel = DashboardPanel(main_frame, self.export_csv)
        self.dashboard_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

    def on_aspect_ratio_toggle(self):
        if hasattr(self, 'visualization_panel'):
            self.visualization_panel.update_aspect_ratio()

    def solve_system(self):
        try:
            BC = {k: float(self.control_panel.inputs[k].get()) for k in ['left', 'right', 'front', 'back', 'bottom', 'top']}
            dx = float(self.control_panel.inputs['dx'].get())
            
            omega = 1.8
            tol = 1e-6
            max_iter = 2000
            
            print(f"\n[INFO] Starting Simulation Solver...")
            print(f"[INFO] BCs: {BC}")
            print(f"[INFO] Parameters: dx={dx}, omega={omega}, tol={tol}, max_iter={max_iter}")
            
            self.title("Laplace 3D Explorer - SOLVING...")
            self.control_panel.solve_btn.config(text="SOLVING... PLEASE WAIT", state=tk.DISABLED, bg="#555555")
            self.update()
            
            self.after(50, lambda: self._execute_solve(BC, dx, omega, tol, max_iter))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.title("Laplace 3D Explorer")
            self.control_panel.solve_btn.config(text="SOLVE", state=tk.NORMAL, bg="#006400")
                
    def _execute_solve(self, BC, dx, omega, tol, max_iter):
        try:
            t0 = time.time()
            solver = Solver3D(self.Lx, self.Ly, self.Lz, dx, BC, omega, tol, max_iter)
            solver.solve()
            elapsed = time.time() - t0
            
            print(f"[INFO] Solver finished in {elapsed:.3f} seconds.")
            print(f"[INFO] Total Iterations: {solver.iter}, Final Error: {solver.err:.2e}")
            
            self.solver_res = solver
            
            ny, nx, nz = solver.T.shape
            
            # Update Dashboard
            self.dashboard_panel.update_metrics(
                elapsed, solver.iter, solver.err, 
                np.max(solver.T), np.min(solver.T), solver.T[ny//2, nx//2, nz//2]
            )
            
            # Update Visualization Panel Controls
            self.visualization_panel.z_slider.config(to=nz-1)
            self.visualization_panel.z_spin.config(to=nz-1)
            self.visualization_panel.z_var.set(nz//2)
            self.visualization_panel.vis_cb.config(values=["Domain Geometry", "Heatmap 2D", "Contour 2D", "Surface 2D", "Scatter 3D", "Isosurface"])
            self.visualization_panel.vis_type.set("Heatmap 2D")
            
            self.title("Laplace 3D Explorer")
            self.control_panel.solve_btn.config(text="SOLVE", state=tk.NORMAL, bg="#006400")
            
            self.visualization_panel.render_visualization()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.title("Laplace 3D Explorer")
            self.control_panel.solve_btn.config(text="SOLVE", state=tk.NORMAL, bg="#006400")
            
    def export_csv(self):
        if self.solver_res is None: return
        curr_z = int(float(self.visualization_panel.z_slider.get()))
        f = filedialog.asksaveasfilename(defaultextension=".csv")
        if f:
            print(f"[INFO] Exporting CSV to: {f}")
            np.savetxt(f, self.solver_res.T[:, :, curr_z], delimiter=",")
            print("[INFO] Export Successful!")
            messagebox.showinfo("Export", "CSV Exported Successfully!")

if __name__ == "__main__":
    print("[INFO] Starting Laplace 3D Explorer Process...")
    app = Laplace3DApp()
    app.mainloop()
