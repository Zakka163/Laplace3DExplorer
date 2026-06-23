import numpy as np
from numba import njit

@njit
def sor_solver_cartesian(T, dx, omega, tol, maxIter):
    ny, nx, nz = T.shape
    T_old = np.copy(T)
    err = 1.0
    iter_count = 0
    while err > tol and iter_count < maxIter:
        err = 0.0
        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                for k in range(1, nz - 1):
                    t_new = (T_old[i+1, j, k] + T[i-1, j, k] + 
                             T_old[i, j+1, k] + T[i, j-1, k] + 
                             T_old[i, j, k+1] + T[i, j, k-1]) / 6.0
                    val = T_old[i, j, k] + omega * (t_new - T_old[i, j, k])
                    diff = abs(val - T_old[i, j, k])
                    if diff > err: err = diff
                    T[i, j, k] = val
        T_old[:] = T[:]
        iter_count += 1
    return iter_count, err

@njit
def sor_solver_cylindrical(T, R_grid, dr, dtheta, dz, omega, tol, maxIter):
    ny, nx, nz = T.shape  # ny=theta, nx=r, nz=z
    T_old = np.copy(T)
    err = 1.0
    iter_count = 0
    while err > tol and iter_count < maxIter:
        err = 0.0
        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                for k in range(1, nz - 1):
                    r_val = R_grid[j]
                    
                    # d2T/dr2 + (1/r)dT/dr
                    t_r = (T_old[i, j+1, k] - 2*T_old[i, j, k] + T[i, j-1, k]) / (dr**2)
                    t_r += (1.0/r_val) * (T_old[i, j+1, k] - T[i, j-1, k]) / (2*dr)
                    
                    # (1/r^2) d2T/dtheta2
                    t_theta = (1.0/(r_val**2)) * (T_old[i+1, j, k] - 2*T_old[i, j, k] + T[i-1, j, k]) / (dtheta**2)
                    
                    # d2T/dz2
                    t_z = (T_old[i, j, k+1] - 2*T_old[i, j, k] + T[i, j, k-1]) / (dz**2)
                    
                    # We solve: t_r + t_theta + t_z = 0 for T[i, j, k]
                    # -2/(dr^2) - 2/(r^2 dtheta^2) - 2/(dz^2)
                    coef_center = -2.0/(dr**2) - 2.0/((r_val*dtheta)**2) - 2.0/(dz**2)
                    
                    sum_others = t_r + t_theta + t_z - coef_center * T_old[i, j, k]
                    t_new = sum_others / (-coef_center)
                    
                    val = T_old[i, j, k] + omega * (t_new - T_old[i, j, k])
                    diff = abs(val - T_old[i, j, k])
                    if diff > err: err = diff
                    T[i, j, k] = val
        T_old[:] = T[:]
        iter_count += 1
    return iter_count, err

@njit
def sor_solver_spherical(T, R_grid, Theta_grid, dr, dtheta, dphi, omega, tol, maxIter):
    ny, nx, nz = T.shape  # ny=theta, nx=r, nz=phi
    T_old = np.copy(T)
    err = 1.0
    iter_count = 0
    while err > tol and iter_count < maxIter:
        err = 0.0
        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                for k in range(1, nz - 1):
                    r_val = R_grid[j]
                    theta_val = Theta_grid[i]
                    sin_t = np.sin(theta_val)
                    if sin_t == 0: sin_t = 1e-9 # avoid division by zero
                    
                    # (1/r^2) d/dr(r^2 dT/dr) = d2T/dr2 + (2/r)dT/dr
                    t_r = (T_old[i, j+1, k] - 2*T_old[i, j, k] + T[i, j-1, k]) / (dr**2)
                    t_r += (2.0/r_val) * (T_old[i, j+1, k] - T[i, j-1, k]) / (2*dr)
                    
                    # (1/(r^2 sin theta)) d/dtheta(sin theta dT/dtheta)
                    # = (1/r^2)[ d2T/dtheta2 + cot(theta) dT/dtheta ]
                    t_theta = (T_old[i+1, j, k] - 2*T_old[i, j, k] + T[i-1, j, k]) / (dtheta**2)
                    t_theta += (1.0/np.tan(theta_val)) * (T_old[i+1, j, k] - T[i-1, j, k]) / (2*dtheta)
                    t_theta *= (1.0/(r_val**2))
                    
                    # (1/(r^2 sin^2 theta)) d2T/dphi2
                    t_phi = (1.0/((r_val*sin_t)**2)) * (T_old[i, j, k+1] - 2*T_old[i, j, k] + T[i, j, k-1]) / (dphi**2)
                    
                    coef_center = -2.0/(dr**2) - 2.0/((r_val*dtheta)**2) - 2.0/((r_val*sin_t*dphi)**2)
                    
                    sum_others = t_r + t_theta + t_phi - coef_center * T_old[i, j, k]
                    t_new = sum_others / (-coef_center)
                    
                    val = T_old[i, j, k] + omega * (t_new - T_old[i, j, k])
                    diff = abs(val - T_old[i, j, k])
                    if diff > err: err = diff
                    T[i, j, k] = val
        T_old[:] = T[:]
        iter_count += 1
    return iter_count, err

class Solver3D:
    def __init__(self, coord_sys, dim1, dim2, dim3, dx, BC, omega=1.8, tol=1e-6, maxIter=5000):
        self.coord_sys = coord_sys
        self.Lx = dim1
        self.Ly = dim2
        self.Lz = dim3
        self.dx = dx
        self.BC = BC
        self.omega = omega
        self.tol = tol
        self.maxIter = maxIter
        
        self.nx = int(np.round(self.Lx / dx)) + 1
        self.ny = int(np.round(self.Ly / dx)) + 1
        self.nz = int(np.round(self.Lz / dx)) + 1
        
        if self.coord_sys == "Cartesian":
            x = np.linspace(0, self.Lx, self.nx)
            y = np.linspace(0, self.Ly, self.ny)
            z = np.linspace(0, self.Lz, self.nz)
        elif self.coord_sys == "Cylindrical":
            x = np.linspace(dx, self.Lx, self.nx)  # Start at dx to avoid r=0
            y = np.linspace(0, self.Ly, self.ny)   # Theta
            z = np.linspace(0, self.Lz, self.nz)   # Z
            self.dr = x[1] - x[0]
            self.dtheta = y[1] - y[0] if self.ny > 1 else 1.0
            self.dz = z[1] - z[0] if self.nz > 1 else 1.0
            self.R_grid = x
        elif self.coord_sys == "Spherical":
            x = np.linspace(dx, self.Lx, self.nx)  # Start at dx to avoid r=0
            y = np.linspace(dx, self.Ly-dx, self.ny)   # Theta (Polar) start at dx to avoid theta=0
            z = np.linspace(0, self.Lz, self.nz)   # Phi (Azimuthal)
            self.dr = x[1] - x[0]
            self.dtheta = y[1] - y[0] if self.ny > 1 else 1.0
            self.dphi = z[1] - z[0] if self.nz > 1 else 1.0
            self.R_grid = x
            self.Theta_grid = y
            
        self.X, self.Y, self.Z = np.meshgrid(x, y, z)
        self.T = np.zeros((self.ny, self.nx, self.nz))
        self.apply_boundary_conditions()
        self.iter = 0
        self.err = 0.0

    def apply_boundary_conditions(self):
        self.T[:, 0, :] = self.BC['left']
        self.T[:, -1, :] = self.BC['right']
        self.T[0, :, :] = self.BC['front']
        self.T[-1, :, :] = self.BC['back']
        self.T[:, :, 0] = self.BC['bottom']
        self.T[:, :, -1] = self.BC['top']

    def solve(self):
        if self.coord_sys == "Cartesian":
            self.iter, self.err = sor_solver_cartesian(self.T, self.dx, self.omega, self.tol, self.maxIter)
        elif self.coord_sys == "Cylindrical":
            self.iter, self.err = sor_solver_cylindrical(self.T, self.R_grid, self.dr, self.dtheta, self.dz, self.omega, self.tol, self.maxIter)
        elif self.coord_sys == "Spherical":
            self.iter, self.err = sor_solver_spherical(self.T, self.R_grid, self.Theta_grid, self.dr, self.dtheta, self.dphi, self.omega, self.tol, self.maxIter)
        return self
