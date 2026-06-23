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
