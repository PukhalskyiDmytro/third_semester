import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

def plot_all(show=True):
    rng = np.random.default_rng(20251015) 

    # task 1
    x = np.arange(-10, 10 + 0.01, 0.01)
    y1 = np.sin(x)
    y2 = x * np.sin(x)
    y3 = np.cos(x)

    plt.figure(figsize=(10, 5))
    plt.plot(x, y1, label='$y_1 = \\sin(x)$', linestyle='-', linewidth=1.5)
    plt.plot(x, y2, label='$y_2 = x\\sin(x)$', linestyle='--', linewidth=1.2)
    plt.plot(x, y3, label='$y_3 = \\cos(x)$', linestyle='-.', linewidth=1.2)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title(r'Plot of $\sin(x)$, $x\sin(x)$ and $\cos(x)$ on $[-10,10]$', fontsize=14)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    if show:
        plt.show()

    # task 2
    n = 2000
    A = rng.normal(loc=0.0, scale=1.0, size=n)           
    B = rng.normal(loc=2.0, scale=np.sqrt(0.5), size=n)  

    min_all = min(A.min(), B.min())
    max_all = max(A.max(), B.max())
    bins = np.linspace(min_all, max_all, 31)  

    plt.figure(figsize=(8, 5))
    plt.hist(A, bins=bins, density=True, alpha=0.6, label='A ~ N(0,1)')
    plt.hist(B, bins=bins, density=True, alpha=0.6, label='B ~ N(2,0.5)')
    plt.xlabel('Value', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.title('Overlaid histograms (density, bins=30) of A and B', fontsize=14)
    plt.legend(frameon=True)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    if show:
        plt.show()

    # task 3
    X_vals = np.linspace(-6, 6, 200)
    Y_vals = np.linspace(-6, 6, 200)
    X, Y = np.meshgrid(X_vals, Y_vals)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, linewidth=0, antialiased=True)
    ax.contour(X, Y, Z, zdir='z', offset=-1, levels=12)
    ax.set_zlim(-1, 1)
    ax.set_xlabel('X', fontsize=12, labelpad=8)
    ax.set_ylabel('Y', fontsize=12, labelpad=8)
    ax.set_zlabel('Z = sin(sqrt(X^2 + Y^2))', fontsize=12, labelpad=10)
    ax.set_title(r'3D surface: $z = \sin(\sqrt{x^2 + y^2})$ with contours at $z=-1$', fontsize=14)
    fig.colorbar(surf, shrink=0.6, aspect=12, pad=0.1)
    plt.tight_layout()
    if show:
        plt.show()

if __name__ == '__main__':
    plot_all(show=True)
