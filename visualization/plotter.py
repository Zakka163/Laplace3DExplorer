import numpy as np
from skimage import measure
from ui.theme import Theme

def plot_heatmap(ax, X2D, Y2D, T2D):
    ax.clear()
    img = ax.pcolormesh(X2D, Y2D, T2D, shading='gouraud', cmap='jet')
    ax.set_title("Heatmap 2D", color=Theme.FG_MAIN)
    return img

def plot_contour(ax, X2D, Y2D, T2D):
    ax.clear()
    ct = ax.contourf(X2D, Y2D, T2D, levels=20, cmap='jet')
    ax.set_title("Contour 2D", color=Theme.FG_MAIN)
    return ct

def plot_surface(ax, X2D, Y2D, T2D):
    ax.clear()
    surf = ax.plot_surface(X2D, Y2D, T2D, cmap='jet', edgecolor='none')
    ax.set_title("Surface 2D", color=Theme.FG_MAIN)
    return surf

def plot_scatter3d(ax, X, Y, Z, T):
    ax.clear()
    step = max(1, int(np.ceil(T.size / 5000)))
    Xs, Ys, Zs, Ts = X.flat[::step], Y.flat[::step], Z.flat[::step], T.flat[::step]
    sc = ax.scatter(Xs, Ys, Zs, c=Ts, cmap='jet', alpha=0.6, s=10)
    ax.set_title("Scatter 3D", color=Theme.FG_MAIN)
    return sc

def plot_isosurface(ax, X, Y, Z, T):
    ax.clear()
    val = (T.min() + T.max()) / 2.0
    try:
        # Downsample to ~40x40x40 to prevent UI freeze
        ny, nx, nz = T.shape
        sy = max(1, ny // 40)
        sx = max(1, nx // 40)
        sz = max(1, nz // 40)
        
        T_sub = T[::sy, ::sx, ::sz]
        X_sub = X[::sy, ::sx, ::sz]
        Y_sub = Y[::sy, ::sx, ::sz]
        Z_sub = Z[::sy, ::sx, ::sz]
        
        # We need spacing for the sub-grid. This is an approximation for curvilinear grids.
        dx = X_sub[0,1,0]-X_sub[0,0,0] if X_sub.shape[1] > 1 else 1.0
        dy = Y_sub[1,0,0]-Y_sub[0,0,0] if Y_sub.shape[0] > 1 else 1.0
        dz = Z_sub[0,0,1]-Z_sub[0,0,0] if Z_sub.shape[2] > 1 else 1.0
        # Fallback to avoid zero spacing
        if dx == 0: dx = 1.0
        if dy == 0: dy = 1.0
        if dz == 0: dz = 1.0
        
        verts, faces, _, _ = measure.marching_cubes(T_sub, val, spacing=(dx, dy, dz))
        
        # Center the isosurface to physical space
        verts[:, 0] += X_sub.min()
        verts[:, 1] += Y_sub.min()
        verts[:, 2] += Z_sub.min()
        
        ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='red', alpha=0.8, edgecolor='none')
        ax.set_title(f"Isosurface (T = {val:.2f})", color=Theme.FG_MAIN)
    except Exception as e:
        ax.set_title("Error computing isosurface", color=Theme.FG_MAIN)
        print(f"Isosurface Error: {e}")
    return None

def plot_domain_geometry(ax, X, Y, Z):
    ax.clear()
    
    # Draw the bounding surface of the domain with a visible wireframe representing the grid
    # Top and Bottom faces
    ax.plot_surface(X[:, :, -1], Y[:, :, -1], Z[:, :, -1], color='cyan', alpha=0.3, edgecolor=Theme.FG_SUB, linewidth=0.5, antialiased=True)
    ax.plot_surface(X[:, :, 0], Y[:, :, 0], Z[:, :, 0], color='cyan', alpha=0.3, edgecolor=Theme.FG_SUB, linewidth=0.5, antialiased=True)
    # Front and Back faces
    ax.plot_surface(X[0, :, :], Y[0, :, :], Z[0, :, :], color='cyan', alpha=0.3, edgecolor=Theme.FG_SUB, linewidth=0.5, antialiased=True)
    ax.plot_surface(X[-1, :, :], Y[-1, :, :], Z[-1, :, :], color='cyan', alpha=0.3, edgecolor=Theme.FG_SUB, linewidth=0.5, antialiased=True)
    # Left and Right faces
    ax.plot_surface(X[:, 0, :], Y[:, 0, :], Z[:, 0, :], color='cyan', alpha=0.3, edgecolor=Theme.FG_SUB, linewidth=0.5, antialiased=True)
    ax.plot_surface(X[:, -1, :], Y[:, -1, :], Z[:, -1, :], color='cyan', alpha=0.3, edgecolor=Theme.FG_SUB, linewidth=0.5, antialiased=True)

    ax.set_title("Domain Geometry", color=Theme.FG_MAIN)
    ax.set_xlim([X.min(), X.max()])
    ax.set_ylim([Y.min(), Y.max()])
    ax.set_zlim([Z.min(), Z.max()])
    
def plot_cutaway3d(ax, X, Y, Z, T, z_idx, Lx, Ly, Lz):
    ax.clear()
    
    import matplotlib.cm as cm
    import matplotlib.colors as mcolors
    
    vmin, vmax = T.min(), T.max()
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.jet
    
    # Calculate strides to downsample grids to max ~60x60 patches for smoother rendering
    ny, nx, nz = T.shape
    sy = max(1, ny // 60)
    sx = max(1, nx // 60)
    sz = max(1, (z_idx + 1) // 60)
    
    # 2. Top Face (Z = z_idx)
    surf_top = ax.plot_surface(X[::sy, ::sx, z_idx], Y[::sy, ::sx, z_idx], Z[::sy, ::sx, z_idx], 
                               facecolors=cmap(norm(T[::sy, ::sx, z_idx])), shade=False, linewidth=0, antialiased=True)
                     
    # 3. Bottom Face (Z = 0)
    ax.plot_surface(X[::sy, ::sx, 0], Y[::sy, ::sx, 0], Z[::sy, ::sx, 0], 
                    facecolors=cmap(norm(T[::sy, ::sx, 0])), shade=False, linewidth=0, antialiased=True)
                
    # 4. Front Face (Y = 0)
    ax.plot_surface(X[0, ::sx, :z_idx+1:sz], Y[0, ::sx, :z_idx+1:sz], Z[0, ::sx, :z_idx+1:sz], 
                    facecolors=cmap(norm(T[0, ::sx, :z_idx+1:sz])), shade=False, linewidth=0, antialiased=True)
                
    # 5. Back Face (Y = Ly)
    ax.plot_surface(X[-1, ::sx, :z_idx+1:sz], Y[-1, ::sx, :z_idx+1:sz], Z[-1, ::sx, :z_idx+1:sz], 
                    facecolors=cmap(norm(T[-1, ::sx, :z_idx+1:sz])), shade=False, linewidth=0, antialiased=True)
                
    # 6. Left Face (X = 0)
    ax.plot_surface(X[::sy, 0, :z_idx+1:sz], Y[::sy, 0, :z_idx+1:sz], Z[::sy, 0, :z_idx+1:sz], 
                    facecolors=cmap(norm(T[::sy, 0, :z_idx+1:sz])), shade=False, linewidth=0, antialiased=True)
                
    # 7. Right Face (X = Lx)
    ax.plot_surface(X[::sy, -1, :z_idx+1:sz], Y[::sy, -1, :z_idx+1:sz], Z[::sy, -1, :z_idx+1:sz], 
                    facecolors=cmap(norm(T[::sy, -1, :z_idx+1:sz])), shade=False, linewidth=0, antialiased=True)
    
    ax.set_xlim3d(X.min(), X.max())
    ax.set_ylim3d(Y.min(), Y.max())
    ax.set_zlim3d(Z.min(), Z.max())
    
    z_val = Z[0, 0, z_idx]
    ax.set_title(f"Cutaway 3D (Z \u2264 {z_val:.2f})", color=Theme.FG_MAIN)
    
    # Create a mappable for the colorbar
    m = cm.ScalarMappable(cmap=cmap, norm=norm)
    m.set_array(T)
    return m
