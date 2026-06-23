import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import time
import os
import threading

# Initialize globals to satisfy Pylance/Pyright
np = None
Solver3D = None
plotter = None

from ui.setup_dialog import SetupDialog
from ui.control_panel import ControlPanel
from ui.visualization_panel import VisualizationPanel
from ui.log_panel import LogPanel
from ui.theme import Theme

class Laplace3DApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Laplace 3D Explorer")
        self.geometry("1200x700")
        self.configure(bg=Theme.BG_ROOT)
        self.resizable(True, True)
        
        # Create Menu Bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        
        self.show_sidebar = tk.BooleanVar(value=True)
        self.show_terminal = tk.BooleanVar(value=False)
        self.transparent_3d = tk.BooleanVar(value=False)
        self.equal_aspect = tk.BooleanVar(value=False)
        
        view_menu.add_checkbutton(label="Toggle Sidebar", variable=self.show_sidebar, command=self.toggle_panels)
        view_menu.add_checkbutton(label="Toggle Terminal", variable=self.show_terminal, command=self.toggle_panels)
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Transparent 3D Solids", variable=self.transparent_3d, command=self.on_transparency_toggle)
        view_menu.add_checkbutton(label="Equal Aspect Ratio (True Scale)", variable=self.equal_aspect, command=self.on_aspect_ratio_toggle)
        view_menu.add_separator()
        
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Dark Mode", command=lambda: self.switch_theme("Dark"))
        theme_menu.add_command(label="Light Mode", command=lambda: self.switch_theme("Light"))
        
        self.export_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Export", menu=self.export_menu)
        self.export_menu.add_command(label="Export 3D Grid Data (CSV)", command=self.export_csv, state=tk.DISABLED)
        
        self.solver_res = None
        self.coord_sys = "Cartesian"
        self.Lx = 1.0
        self.Ly = 1.0
        self.Lz = 1.0
        
        self.setup_dialog = SetupDialog(self, self.on_setup_submit)
        
        self.loading_frame = tk.Frame(self, bg=Theme.BG_ROOT)
        tk.Label(self.loading_frame, text="Loading Physics Engine & 3D Visualizer...\nPlease wait...", bg=Theme.BG_ROOT, fg=Theme.FG_MAIN, font=Theme.FONT_TITLE, justify=tk.CENTER).pack(pady=50)

    def on_setup_submit(self, coord_sys, val1, val2, val3):
        self.coord_sys = coord_sys
        self.Lx = val1
        self.Ly = val2
        self.Lz = val3
        
        # Ensure loading frame honors current theme
        self.configure(bg=Theme.BG_ROOT)
        self.loading_frame.configure(bg=Theme.BG_ROOT)
        for child in self.loading_frame.winfo_children():
            child.configure(bg=Theme.BG_ROOT, fg=Theme.FG_MAIN)
        
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
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background=Theme.BG_ROOT)
        style.configure('TLabel', background=Theme.BG_ROOT, foreground=Theme.FG_MAIN)
        style.configure('TButton', background=Theme.SUCCESS, foreground=Theme.FG_MAIN, font=Theme.FONT_SMALL)
        
        # Top Ribbon (Control)
        self.control_panel = ControlPanel(self, self.solve_system, self.coord_sys)
        self.control_panel.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Main Vertical Splitter (Top: Viz, Bottom: Log)
        self.v_paned = tk.PanedWindow(self, orient=tk.VERTICAL, opaqueresize=False, bg=Theme.BG_ROOT, sashwidth=4, bd=0, sashrelief=tk.FLAT)
        self.v_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # --- CENTER VISUALIZATION ---
        self.viz_frame = tk.Frame(self.v_paned, bg=Theme.BG_ROOT)
        self.v_paned.add(self.viz_frame, stretch="always")
        
        self.visualization_panel = VisualizationPanel(self.viz_frame, self)
        self.visualization_panel.pack(fill=tk.BOTH, expand=True)
        
        # --- BOTTOM LOG PANEL ---
        self.log_panel = LogPanel(self.v_paned)
        # Terminal hidden by default, so we don't add it initially
        
        # Save references for toggling
        self.main_container = self.v_paned
        
    def toggle_panels(self):
        if self.show_sidebar.get():
            self.control_panel.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, before=self.v_paned)
        else:
            self.control_panel.pack_forget()
            
        if self.show_terminal.get():
            self.v_paned.add(self.log_panel, stretch="never")
        else:
            self.v_paned.forget(self.log_panel)

    def switch_theme(self, mode):
        Theme.set_theme(mode)
        
        # Global configuration
        self.configure(bg=Theme.BG_ROOT)
        
        style = tk.ttk.Style(self)
        style.configure('TFrame', background=Theme.BG_ROOT)
        style.configure('TLabel', background=Theme.BG_ROOT, foreground=Theme.FG_MAIN)
        style.configure('TButton', background=Theme.SUCCESS, foreground=Theme.FG_MAIN, font=Theme.FONT_SMALL)
        
        # Setup Dialog if it exists
        if hasattr(self, 'setup_dialog') and hasattr(self.setup_dialog, 'setup_frame'):
            self.setup_dialog.setup_frame.configure(style='Setup.TFrame')
            # The canvas and inner frames of SetupDialog are harder to update dynamically
            # Usually users don't change theme while in setup dialog.
            
        if hasattr(self, 'loading_frame'):
            self.loading_frame.configure(bg=Theme.BG_ROOT)
            for child in self.loading_frame.winfo_children():
                child.configure(bg=Theme.BG_ROOT, fg=Theme.FG_MAIN)
                
        # Main UI container
        if hasattr(self, 'main_container'):
            if hasattr(self, 'sidebar_frame'):
                self.sidebar_frame.configure(bg=Theme.BG_ROOT)
            if hasattr(self, 'viz_frame'):
                self.viz_frame.configure(bg=Theme.BG_ROOT)
            
            if hasattr(self, 'control_panel'):
                self.control_panel.apply_theme()
            if hasattr(self, 'visualization_panel'):
                self.visualization_panel.apply_theme()
            if hasattr(self, 'log_panel'):
                self.log_panel.apply_theme()

    def on_aspect_ratio_toggle(self):
        if hasattr(self, 'visualization_panel'):
            self.visualization_panel.update_aspect_ratio()
            
    def on_transparency_toggle(self):
        if hasattr(self, 'visualization_panel'):
            self.visualization_panel.render_visualization()

    def solve_system(self):
        try:
            BC = {k: float(self.control_panel.inputs[k].get()) for k in ['left', 'right', 'front', 'back', 'bottom', 'top']}
            dx = float(self.control_panel.inputs['dx'].get())
            
            omega = 1.8
            tol = 1e-6
            max_iter = 2000
            
            print("\n[INFO] Starting Simulation Solver...")
            print(f"[INFO] BCs: {BC}")
            print(f"[INFO] Parameters: dx={dx}, omega={omega}, tol={tol}, max_iter={max_iter}")
            
            self.title("Laplace 3D Explorer - SOLVING...")
            self.control_panel.solve_btn.config(text="SOLVING... PLEASE WAIT", state=tk.DISABLED, bg="#555555")
            self.update()
            
            # Run solver in background thread to avoid freezing UI
            threading.Thread(target=self._execute_solve_thread, args=(BC, dx, omega, tol, max_iter), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.title("Laplace 3D Explorer")
            self.control_panel.solve_btn.config(text="SOLVE", state=tk.NORMAL, bg="#006400")
                
    def _execute_solve_thread(self, BC, dx, omega, tol, max_iter):
        try:
            t0 = time.time()
            solver = Solver3D(self.coord_sys, self.Lx, self.Ly, self.Lz, dx, BC, omega, tol, max_iter)
            solver.solve()
            elapsed = time.time() - t0
            
            print(f"[INFO] Solver finished in {elapsed:.3f} seconds.")
            print(f"[INFO] Total Iterations: {solver.iter}, Final Error: {solver.err:.2e}")
            
            # Marshal the UI update back to the main thread
            self.after(0, lambda: self._on_solve_complete(solver, elapsed))
        except Exception as e:
            self.after(0, lambda err=e: self._on_solve_error(err))
            
    def _on_solve_error(self, e):
        messagebox.showerror("Error", f"Solver Error: {str(e)}")
        self.title("Laplace 3D Explorer")
        self.control_panel.solve_btn.config(text="SOLVE", state=tk.NORMAL, bg="#006400")

    def _on_solve_complete(self, solver, elapsed):
        try:
            self.solver_res = solver
            
            ny, nx, nz = solver.T.shape
            
            # Log metrics instead of updating dashboard
            print(f"Time: {elapsed:.3f} s, Iter: {solver.iter}, Error: {solver.err:.2e}")
            print(f"Max Temp: {np.max(solver.T):.2f}, Min Temp: {np.min(solver.T):.2f}, Center Temp: {solver.T[ny//2, nx//2, nz//2]:.2f}")
            
            # Update Visualization Panel Controls
            self.visualization_panel.z_slider.config(to=nz-1)
            self.visualization_panel.z_spin.config(to=nz-1)
            self.visualization_panel.z_var.set(nz//2)
            self.visualization_panel.vis_cb.config(values=["Domain Geometry", "Heatmap 2D", "Contour 2D", "Surface 2D", "Cutaway 3D", "Scatter 3D", "Isosurface"])
            self.visualization_panel.vis_type.set("Heatmap 2D")
            
            self.title("Laplace 3D Explorer")
            self.control_panel.solve_btn.config(text="SOLVE", state=tk.NORMAL, bg="#006400")
            
            self.visualization_panel.render_visualization()
            
            # Enable export menu after successful solve
            self.export_menu.entryconfig("Export 3D Grid Data (CSV)", state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error updating UI", str(e))
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
