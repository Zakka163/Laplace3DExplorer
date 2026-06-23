import numpy as np
from numba import njit

@njit
def sor_solver(T, dx, omega, tol, maxIter):
    ny, nx, nz = T.shape
    
    T_old = np.copy(T)
    err = 1.0
    iter_count = 0
    
    while err > tol and iter_count < maxIter:
        err = 0.0
        # Iterate over interior points
        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                for k in range(1, nz - 1):
                    t_new = (T_old[i+1, j, k] + T[i-1, j, k] + 
                             T_old[i, j+1, k] + T[i, j-1, k] + 
                             T_old[i, j, k+1] + T[i, j, k-1]) / 6.0
                    
                    val = T_old[i, j, k] + omega * (t_new - T_old[i, j, k])
                    
                    diff = abs(val - T_old[i, j, k])
                    if diff > err:
                        err = diff
                        
                    T[i, j, k] = val
                    
        T_old[:] = T[:]
        iter_count += 1
        
    return iter_count, err

class Solver3D:
    def __init__(self, Lx, Ly, Lz, dx, BC, omega=1.8, tol=1e-6, maxIter=5000):
        self.Lx = Lx
        self.Ly = Ly
        self.Lz = Lz
        self.dx = dx
        self.BC = BC
        self.omega = omega
        self.tol = tol
        self.maxIter = maxIter
        
        self.nx = int(np.round(Lx / dx)) + 1
        self.ny = int(np.round(Ly / dx)) + 1
        self.nz = int(np.round(Lz / dx)) + 1
        
        # Grid
        x = np.linspace(0, Lx, self.nx)
        y = np.linspace(0, Ly, self.ny)
        z = np.linspace(0, Lz, self.nz)
        self.X, self.Y, self.Z = np.meshgrid(x, y, z)
        
        # Initialize T
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
        self.iter, self.err = sor_solver(self.T, self.dx, self.omega, self.tol, self.maxIter)
        return self
