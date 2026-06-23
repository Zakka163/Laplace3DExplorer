import numpy as np
from skimage import measure

def plot_heatmap(ax, X2D, Y2D, T2D):
    ax.clear()
    img = ax.imshow(T2D, origin='lower', extent=[X2D.min(), X2D.max(), Y2D.min(), Y2D.max()], cmap='jet', aspect='auto')
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

def plot_domain_geometry(ax, Lx, Ly, Lz):
    ax.clear()
    
    corners = np.array([
        [0, 0, 0], [Lx, 0, 0], [Lx, Ly, 0], [0, Ly, 0],
        [0, 0, Lz], [Lx, 0, Lz], [Lx, Ly, Lz], [0, Ly, Lz]
    ])
    
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    
    faces = [
        [corners[0], corners[1], corners[2], corners[3]], # Bottom
        [corners[4], corners[5], corners[6], corners[7]], # Top
        [corners[0], corners[1], corners[5], corners[4]], # Front
        [corners[3], corners[2], corners[6], corners[7]], # Back
        [corners[0], corners[3], corners[7], corners[4]], # Left
        [corners[1], corners[2], corners[6], corners[5]], # Right
    ]
    
    # Create the Poly3DCollection
    # alpha=0.5 gives it a glass-like solid transparency
    face_collection = Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='white', alpha=0.5)
    ax.add_collection3d(face_collection)
        
    ax.set_title("Domain Geometry", color='white')
    
    ax.set_xlim([-0.1 * Lx, 1.1 * Lx if Lx > 0 else 1.0])
    ax.set_ylim([-0.1 * Ly, 1.1 * Ly if Ly > 0 else 1.0])
    ax.set_zlim([-0.1 * Lz, 1.1 * Lz if Lz > 0 else 1.0])
    
    return None
