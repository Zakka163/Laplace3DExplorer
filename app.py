import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import time
import os

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from core.solver import Solver3D
from visualization import plotter

class Laplace3DApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Laplace 3D Explorer")
        self.geometry("1200x700")
        self.configure(bg="#1E1E1E")
        
        self.solver_res = None
        self.build_ui()
        
    def build_ui(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#1E1E1E')
        style.configure('TLabel', background='#1E1E1E', foreground='white')
        style.configure('TButton', background='#006400', foreground='white', font=('Arial', 10, 'bold'))
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # LEFT PANEL
        left_panel = ttk.Frame(main_frame, width=280)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Label(left_panel, text="Control Panel", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.inputs = {}
        def add_input(label_text, default_val):
            f = ttk.Frame(left_panel)
            f.pack(fill=tk.X, pady=2)
            ttk.Label(f, text=label_text, width=15).pack(side=tk.LEFT)
            e = ttk.Entry(f, width=10)
            e.insert(0, str(default_val))
            e.pack(side=tk.RIGHT)
            return e
            
        self.inputs['left'] = add_input("BC Left:", 100)
        self.inputs['right'] = add_input("BC Right:", 50)
        self.inputs['front'] = add_input("BC Front:", 0)
        self.inputs['back'] = add_input("BC Back:", 100)
        self.inputs['bottom'] = add_input("BC Bottom:", 75)
        self.inputs['top'] = add_input("BC Top:", 25)
        
        ttk.Label(left_panel, text="").pack()
        
        self.inputs['dx'] = add_input("Grid dx:", 0.05)
        self.inputs['omega'] = add_input("Omega:", 1.8)
        self.inputs['tol'] = add_input("Tolerance:", 1e-6)
        self.inputs['maxIter'] = add_input("Max Iter:", 2000)
        
        solve_btn = ttk.Button(left_panel, text="SOLVE", command=self.solve_system)
        solve_btn.pack(fill=tk.X, pady=20)
        
        # CENTER PANEL
        center_panel = ttk.Frame(main_frame)
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        top_center = ttk.Frame(center_panel)
        top_center.pack(fill=tk.X, pady=5)
        
        ttk.Label(top_center, text="Visual Type:").pack(side=tk.LEFT, padx=5)
        self.vis_type = tk.StringVar(value="Heatmap 2D")
        vis_cb = ttk.Combobox(top_center, textvariable=self.vis_type, values=["Heatmap 2D", "Contour 2D", "Surface 2D", "Scatter 3D", "Isosurface"])
        vis_cb.pack(side=tk.LEFT, padx=5)
        vis_cb.bind("<<ComboboxSelected>>", lambda e: self.render_visualization())
        
        ttk.Label(top_center, text="Z Layer:").pack(side=tk.LEFT, padx=10)
        self.z_slider = ttk.Scale(top_center, from_=0, to=10, orient=tk.HORIZONTAL, command=lambda v: self.render_visualization())
        self.z_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.fig.patch.set_facecolor('#1E1E1E')
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=center_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # RIGHT PANEL
        right_panel = ttk.Frame(main_frame, width=250)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        ttk.Label(right_panel, text="Dashboard", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.labels = {}
        for lbl in ["Time", "Iter", "Error", "Max Temp", "Min Temp", "Center Temp"]:
            self.labels[lbl] = ttk.Label(right_panel, text=f"{lbl}: -")
            self.labels[lbl].pack(anchor=tk.W, pady=5)
            
        ttk.Button(right_panel, text="Export CSV", command=self.export_csv).pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
    def solve_system(self):
        try:
            BC = {k: float(self.inputs[k].get()) for k in ['left', 'right', 'front', 'back', 'bottom', 'top']}
            dx = float(self.inputs['dx'].get())
            omega = float(self.inputs['omega'].get())
            tol = float(self.inputs['tol'].get())
            max_iter = int(self.inputs['maxIter'].get())
            
            self.title("Laplace 3D Explorer - SOLVING...")
            self.update()
            
            t0 = time.time()
            solver = Solver3D(1.0, 1.0, 1.0, dx, BC, omega, tol, max_iter)
            solver.solve()
            elapsed = time.time() - t0
            
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
            
    def render_visualization(self):
        if self.solver_res is None: return
        
        self.fig.clf()
        v_type = self.vis_type.get()
        
        if "3D" in v_type or "Iso" in v_type or "Surface" in v_type:
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.ax = self.fig.add_subplot(111)
            
        self.ax.set_facecolor('#1E1E1E')
        self.ax.tick_params(colors='white')
        
        self.ax.set_xlabel('X Axis', color='white')
        self.ax.set_ylabel('Y Axis', color='white')
        if hasattr(self.ax, 'set_zlabel'):
            self.ax.set_zlabel('Z Axis', color='white')
            
        curr_z = int(float(self.z_slider.get()))
        
        T = self.solver_res.T
        X = self.solver_res.X
        Y = self.solver_res.Y
        Z = self.solver_res.Z
        
        X2D = X[:, :, curr_z]
        Y2D = Y[:, :, curr_z]
        T2D = T[:, :, curr_z]
        
        if v_type == "Heatmap 2D":
            plotter.plot_heatmap(self.ax, X2D, Y2D, T2D)
        elif v_type == "Contour 2D":
            plotter.plot_contour(self.ax, X2D, Y2D, T2D)
        elif v_type == "Surface 2D":
            plotter.plot_surface(self.ax, X2D, Y2D, T2D)
        elif v_type == "Scatter 3D":
            plotter.plot_scatter3d(self.ax, X, Y, Z, T)
        elif v_type == "Isosurface":
            plotter.plot_isosurface(self.ax, X, Y, Z, T)
            
        self.canvas.draw()
        
    def export_csv(self):
        if self.solver_res is None: return
        curr_z = int(float(self.z_slider.get()))
        f = filedialog.asksaveasfilename(defaultextension=".csv")
        if f:
            np.savetxt(f, self.solver_res.T[:, :, curr_z], delimiter=",")
            messagebox.showinfo("Export", "CSV Exported Successfully!")

if __name__ == "__main__":
    app = Laplace3DApp()
    app.mainloop()
