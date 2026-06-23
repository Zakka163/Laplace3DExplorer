import numpy as np
from skimage import measure

def plot_heatmap(ax, X2D, Y2D, T2D):
    ax.clear()
    img = ax.pcolormesh(X2D, Y2D, T2D, shading='auto', cmap='jet')
    ax.set_title("Heatmap 2D", color='white')
    return img

def plot_contour(ax, X2D, Y2D, T2D):
    ax.clear()
    ct = ax.contourf(X2D, Y2D, T2D, levels=20, cmap='jet')
    ax.set_title("Contour 2D", color='white')
    return ct

def plot_surface(ax, X2D, Y2D, T2D):
    ax.clear()
    surf = ax.plot_surface(X2D, Y2D, T2D, cmap='jet', edgecolor='none')
    ax.set_title("Surface 2D", color='white')
    return surf

def plot_scatter3d(ax, X, Y, Z, T):
    ax.clear()
    step = max(1, int(np.ceil(T.size / 5000)))
    Xs, Ys, Zs, Ts = X.flat[::step], Y.flat[::step], Z.flat[::step], T.flat[::step]
    sc = ax.scatter(Xs, Ys, Zs, c=Ts, cmap='jet', alpha=0.6, s=10)
    ax.set_title("Scatter 3D", color='white')
    return sc

def plot_isosurface(ax, X, Y, Z, T):
    ax.clear()
    val = (T.min() + T.max()) / 2.0
    try:
        # skimage marching cubes returns (vertices, faces, normals, values)
        verts, faces, _, _ = measure.marching_cubes(T, val, spacing=(X[0,1,0]-X[0,0,0], Y[1,0,0]-Y[0,0,0], Z[0,0,1]-Z[0,0,0]))
        ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='red', alpha=0.8, edgecolor='none')
        ax.set_title(f"Isosurface (T = {val:.2f})", color='white')
    except Exception as e:
        ax.set_title("Error computing isosurface", color='white')
        print(f"Isosurface Error: {e}")
    return None

def plot_domain_geometry(ax, X, Y, Z):
    ax.clear()
    
    # Draw the bounding surface of the domain
    # Top and Bottom faces
    ax.plot_surface(X[:, :, -1], Y[:, :, -1], Z[:, :, -1], color='cyan', alpha=0.3)
    ax.plot_surface(X[:, :, 0], Y[:, :, 0], Z[:, :, 0], color='cyan', alpha=0.3)
    # Front and Back faces
    ax.plot_surface(X[0, :, :], Y[0, :, :], Z[0, :, :], color='cyan', alpha=0.3)
    ax.plot_surface(X[-1, :, :], Y[-1, :, :], Z[-1, :, :], color='cyan', alpha=0.3)
    # Left and Right faces
    ax.plot_surface(X[:, 0, :], Y[:, 0, :], Z[:, 0, :], color='cyan', alpha=0.3)
    ax.plot_surface(X[:, -1, :], Y[:, -1, :], Z[:, -1, :], color='cyan', alpha=0.3)

    ax.set_title("Domain Geometry", color='white')
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
    
    # 2. Top Face (Z = z_idx)
    surf_top = ax.plot_surface(X[:, :, z_idx], Y[:, :, z_idx], Z[:, :, z_idx], 
                               facecolors=cmap(norm(T[:, :, z_idx])), shade=False)
                     
    # 3. Bottom Face (Z = 0)
    ax.plot_surface(X[:, :, 0], Y[:, :, 0], Z[:, :, 0], 
                    facecolors=cmap(norm(T[:, :, 0])), shade=False)
                
    # 4. Front Face (Y = 0)
    ax.plot_surface(X[0, :, :z_idx+1], Y[0, :, :z_idx+1], Z[0, :, :z_idx+1], 
                    facecolors=cmap(norm(T[0, :, :z_idx+1])), shade=False)
                
    # 5. Back Face (Y = Ly)
    ax.plot_surface(X[-1, :, :z_idx+1], Y[-1, :, :z_idx+1], Z[-1, :, :z_idx+1], 
                    facecolors=cmap(norm(T[-1, :, :z_idx+1])), shade=False)
                
    # 6. Left Face (X = 0)
    ax.plot_surface(X[:, 0, :z_idx+1], Y[:, 0, :z_idx+1], Z[:, 0, :z_idx+1], 
                    facecolors=cmap(norm(T[:, 0, :z_idx+1])), shade=False)
                
    # 7. Right Face (X = Lx)
    ax.plot_surface(X[:, -1, :z_idx+1], Y[:, -1, :z_idx+1], Z[:, -1, :z_idx+1], 
                    facecolors=cmap(norm(T[:, -1, :z_idx+1])), shade=False)
    
    ax.set_xlim3d(X.min(), X.max())
    ax.set_ylim3d(Y.min(), Y.max())
    ax.set_zlim3d(Z.min(), Z.max())
    
    z_val = Z[0, 0, z_idx]
    ax.set_title(f"Cutaway 3D (Z ≤ {z_val:.2f})", color='white')
    
    # Create a mappable for the colorbar
    m = cm.ScalarMappable(cmap=cmap, norm=norm)
    m.set_array(T)
    return m
