import tkinter as tk
from tkinter import ttk
import numpy as np
from ui.theme import Theme

# These will be initialized properly during lazy loading in app.py
FigureCanvasTkAgg = None
NavigationToolbar2Tk = None
Figure = None
plotter = None

class VisualizationPanel(tk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, bg=Theme.BG_ROOT)
        self.app = app_controller # We need access to solver_res, Lx, Ly, Lz, etc.
        self._is_rendering = False
        self.current_v_type = None
        self.cb = None
        
        self.build_ui()
        
    def build_ui(self):
        top_center = tk.Frame(self, bg=Theme.BG_ROOT)
        top_center.pack(fill=tk.X, pady=5)
        
        tk.Label(top_center, text="Visual Type:", bg=Theme.BG_ROOT, fg=Theme.FG_MAIN).pack(side=tk.LEFT, padx=5)
        self.vis_type = tk.StringVar(value="Domain Geometry")
        self.vis_cb = ttk.Combobox(top_center, textvariable=self.vis_type, values=["Domain Geometry", "Heatmap 2D", "Contour 2D", "Surface 2D", "Cutaway 3D", "Scatter 3D", "Isosurface"], state="readonly")
        self.vis_cb.pack(side=tk.LEFT, padx=5)
        self.vis_cb.bind("<<ComboboxSelected>>", lambda e: self.render_visualization())
        
        self.lbl_z_slider = tk.Label(top_center, text="Z Height:", bg=Theme.BG_ROOT, fg=Theme.FG_MAIN)
        self.lbl_z_slider.pack(side=tk.LEFT, padx=15)
        
        self.z_var = tk.IntVar(value=0)
        self.z_spin_var = tk.DoubleVar(value=0.0)
        
        self.z_spin = ttk.Spinbox(top_center, from_=0.0, to=10.0, textvariable=self.z_spin_var, width=8, increment=0.1)
        self.z_spin.pack(side=tk.LEFT, padx=2)
        self.z_spin.bind('<Return>', self.on_spinbox_enter)
        
        # We set resolution=1 explicitly so the slider moves in integer steps (index layers)
        self.z_slider = tk.Scale(top_center, from_=0, to=10, orient=tk.HORIZONTAL, bg=Theme.BG_ROOT, fg=Theme.FG_MAIN, highlightthickness=0, variable=self.z_var, showvalue=False, resolution=1, command=lambda v: self.render_visualization())
        self.z_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.fig.patch.set_facecolor(Theme.BG_ROOT)
        self.ax = self.fig.add_subplot(111)
        
        canvas_frame = tk.Frame(self, bg=Theme.BG_ROOT)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, canvas_frame)
        self.toolbar.config(background=Theme.TOOLBAR_BG)
        for child in self.toolbar.winfo_children():
            child.config(background=Theme.TOOLBAR_BG)
        self.toolbar.update()
        
        # Bind mouse scroll for 3D zoom
        self.canvas.mpl_connect('scroll_event', self.on_scroll_zoom)
        
    def on_spinbox_enter(self, event=None):
        if self.app.solver_res is None:
            return
        try:
            target_z = float(self.z_spin_var.get())
            # Clamp to physical bounds
            if target_z < 0: target_z = 0.0
            if target_z > self.app.solver_res.Lz: target_z = self.app.solver_res.Lz
            
            # Find the closest layer index
            Z_1D = self.app.solver_res.Z[0, 0, :]
            closest_idx = (np.abs(Z_1D - target_z)).argmin()
            
            # Set slider, which triggers render_visualization
            self.z_var.set(closest_idx)
            self.render_visualization()
        except ValueError:
            pass # Invalid float

    def on_scroll_zoom(self, event):
        if event.inaxes != self.ax:
            return
            
        scale_factor = 1.1 if event.button == 'down' else 0.9
        
        def zoom_lims(lims, s):
            center = (lims[1] + lims[0]) / 2
            width = lims[1] - lims[0]
            return center - width/2 * s, center + width/2 * s
            
        if hasattr(self.ax, 'get_xlim3d'):
            self.ax.set_xlim3d(zoom_lims(self.ax.get_xlim3d(), scale_factor))
            self.ax.set_ylim3d(zoom_lims(self.ax.get_ylim3d(), scale_factor))
            self.ax.set_zlim3d(zoom_lims(self.ax.get_zlim3d(), scale_factor))
        else:
            self.ax.set_xlim(zoom_lims(self.ax.get_xlim(), scale_factor))
            self.ax.set_ylim(zoom_lims(self.ax.get_ylim(), scale_factor))
            
        self.canvas.draw_idle()

    def get_physical_coordinates(self):
        if not hasattr(self.app, 'solver_res') or self.app.solver_res is None:
            # Generate a dummy grid for initial Domain Geometry rendering
            Lx, Ly, Lz = self.app.Lx, self.app.Ly, self.app.Lz
            nx, ny, nz = 40, 40, 40
            if self.app.coord_sys == "Cartesian":
                x = np.linspace(0, Lx, nx)
                y = np.linspace(0, Ly, ny)
                z = np.linspace(0, Lz, nz)
            elif self.app.coord_sys == "Cylindrical":
                x = np.linspace(0.01, Lx, nx)
                y = np.linspace(0, Ly, ny)
                z = np.linspace(0, Lz, nz)
            elif self.app.coord_sys == "Spherical":
                x = np.linspace(0.01, Lx, nx)
                y = np.linspace(0.01, Ly-0.01, ny)
                z = np.linspace(0, Lz, nz)
            X, Y, Z = np.meshgrid(x, y, z)
        else:
            X = self.app.solver_res.X
            Y = self.app.solver_res.Y
            Z = self.app.solver_res.Z
        
        if self.app.coord_sys == "Cylindrical":
            R, Theta = X, Y
            X_phys = R * np.cos(Theta)
            Y_phys = R * np.sin(Theta)
            return X_phys, Y_phys, Z
        elif self.app.coord_sys == "Spherical":
            R, Theta, Phi = X, Y, Z
            X_phys = R * np.sin(Theta) * np.cos(Phi)
            Y_phys = R * np.sin(Theta) * np.sin(Phi)
            Z_phys = R * np.cos(Theta)
            return X_phys, Y_phys, Z_phys
            
        return X, Y, Z

    def render_visualization(self, event=None):
        if hasattr(self, '_render_timer') and self._render_timer is not None:
            self.after_cancel(self._render_timer)
            
        # Debounce the render call by 150ms
        self._render_timer = self.after(150, self._execute_render_visualization)
        
    def _execute_render_visualization(self):
        if self._is_rendering:
            return
        self._is_rendering = True
        try:
            v_type = self.vis_type.get()
            
            if self.app.solver_res is None and v_type != "Domain Geometry":
                return
                
            print(f"[INFO] Rendering Visual: {v_type}")
            
            if "2D" in v_type or v_type == "Cutaway 3D":
                self.lbl_z_slider.pack(side=tk.LEFT, padx=15)
                self.z_spin.pack(side=tk.LEFT, padx=2)
                self.z_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            else:
                self.lbl_z_slider.pack_forget()
                self.z_spin.pack_forget()
                self.z_slider.pack_forget()
                
            if self.current_v_type != v_type:
                self.fig.clf()
                self.cb = None
                if "3D" in v_type or "Iso" in v_type or "Surface" in v_type or "Geometry" in v_type:
                    self.ax = self.fig.add_subplot(111, projection='3d')
                else:
                    self.ax = self.fig.add_subplot(111)
                self.current_v_type = v_type
            else:
                if v_type in ["Scatter 3D", "Isosurface", "Domain Geometry"]:
                    return # No need to re-render these when Z slider moves
                self.ax.clear()
                
            self.ax.set_facecolor(Theme.BG_ROOT)
            self.ax.tick_params(colors=Theme.FG_MAIN)
                
            if v_type == "Domain Geometry":
                X_phys, Y_phys, Z_phys = self.get_physical_coordinates()
                plotter.plot_domain_geometry(self.ax, X_phys, Y_phys, Z_phys)
                self.ax.set_xlabel('X')
                self.ax.set_ylabel('Y')
                self.ax.set_zlabel('Z')
                self.canvas.draw()
                return
                
            curr_z = self.z_var.get()
            
            T = self.app.solver_res.T
            X, Y, Z = self.get_physical_coordinates()
            
            if curr_z >= Z.shape[2]:
                curr_z = Z.shape[2] - 1
                self.z_var.set(curr_z)
            elif curr_z < 0:
                curr_z = 0
                self.z_var.set(curr_z)
                
            physical_z = Z[0, 0, curr_z]
            # Update spinbox and label with physical Z
            self.z_spin_var.set(round(physical_z, 4))
            self.lbl_z_slider.config(text=f"Z Layer Index: {curr_z}  [Z = {physical_z:.2f}]:")
            
            X2D = X[:, :, curr_z]
            Y2D = Y[:, :, curr_z]
            T2D = T[:, :, curr_z]
            
            if v_type == "Domain Geometry":
                plotter.plot_domain_geometry(self.ax, self.app.solver_res.Lx, self.app.solver_res.Ly, self.app.solver_res.Lz)
            elif v_type == "Heatmap 2D":
                self.cax = plotter.plot_heatmap(self.ax, X2D, Y2D, T2D)
                if not self.cb: self.cb = self.fig.colorbar(self.cax, ax=self.ax)
                else: self.cb.update_normal(self.cax)
            elif v_type == "Contour 2D":
                self.cax = plotter.plot_contour(self.ax, X2D, Y2D, T2D)
                if not self.cb: self.cb = self.fig.colorbar(self.cax, ax=self.ax)
                else: self.cb.update_normal(self.cax)
            elif v_type == "Surface 2D":
                self.cax = plotter.plot_surface(self.ax, X2D, Y2D, T2D)
                if not self.cb: self.cb = self.fig.colorbar(self.cax, ax=self.ax)
                else: self.cb.update_normal(self.cax)
            elif v_type == "Scatter 3D":
                self.cax = plotter.plot_scatter3d(self.ax, X, Y, Z, T)
                if not self.cb: self.cb = self.fig.colorbar(self.cax, ax=self.ax)
                else: self.cb.update_normal(self.cax)
            elif v_type == "Isosurface":
                plotter.plot_isosurface(self.ax, X, Y, Z, T)
            elif v_type == "Cutaway 3D":
                self.cax = plotter.plot_cutaway3d(self.ax, X, Y, Z, T, curr_z, self.app.solver_res.Lx, self.app.solver_res.Ly, self.app.solver_res.Lz)
                if not self.cb: self.cb = self.fig.colorbar(self.cax, ax=self.ax)
                else: self.cb.update_normal(self.cax)
                
            self.update_aspect_ratio()
            
            self.ax.set_xlabel('X Axis', color='white', fontsize=10)
            self.ax.set_ylabel('Y Axis', color='white', fontsize=10)
            if hasattr(self.ax, 'set_zlabel'):
                self.ax.set_zlabel('Z Axis', color='white', fontsize=10)
                
            self.fig.tight_layout()
            self.canvas.draw()
            
        finally:
            self._is_rendering = False

    def update_aspect_ratio(self):
        if not hasattr(self, 'ax'):
            return
            
        v_type = self.vis_type.get()
        if hasattr(self.ax, 'set_box_aspect') and v_type in ["Domain Geometry", "Scatter 3D", "Isosurface", "Cutaway 3D"]:
            # Need to get equal_aspect_var from app controller's control panel
            if hasattr(self.app, 'control_panel') and self.app.control_panel.equal_aspect_var.get():
                if v_type == "Domain Geometry":
                    Lx = self.app.solver_res.Lx if self.app.solver_res else self.app.Lx
                    Ly = self.app.solver_res.Ly if self.app.solver_res else self.app.Ly
                    Lz = self.app.solver_res.Lz if self.app.solver_res else self.app.Lz
                    self.ax.set_box_aspect((Lx, Ly, Lz))
                else:
                    if self.app.solver_res is not None:
                        X = self.app.solver_res.X
                        Y = self.app.solver_res.Y
                        Z = self.app.solver_res.Z
                        self.ax.set_box_aspect((np.ptp(X), np.ptp(Y), np.ptp(Z)))
            else:
                self.ax.set_box_aspect((1, 1, 1)) # Default cube
            
            if not self._is_rendering:
                self.canvas.draw()
