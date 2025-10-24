import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def taylor_partial_sum(x, n):
    s = np.zeros_like(x, dtype=float)
    for k in range(n):
        s += ((-1) ** k) * (x ** (2 * k)) / math.factorial(k)
    return s

def gaussian_wave(x, t, x0, c, sigma):
    return np.exp(-((x - (x0 + c * t)) ** 2) / (sigma ** 2))

def show_taylor_animation(m=15, x_min=-3, x_max=3, x_pts=800, fps=2):
    x = np.linspace(x_min, x_max, x_pts)
    f = np.exp(-x ** 2)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.plot(x, f, label="f(x)=exp(-x^2)", linewidth=2)
    line_poly, = ax.plot([], [], linestyle="--", label="partial sum", linewidth=2)
    title = ax.set_title("Taylor approximation — n = 0")
    ax.legend(loc="upper right")
    def init():
        line_poly.set_data([], [])
        return line_poly, title
    def update(frame):
        n = frame + 1
        p = taylor_partial_sum(x, n)
        line_poly.set_data(x, p)
        title.set_text(f"Taylor approximation — n = {n}")
        return line_poly, title
    ani = animation.FuncAnimation(fig, update, frames=m, init_func=init, interval=1000//fps, blit=False, repeat=False)
    plt.show()

def show_gaussian_animation(frames=100, t0=0.0, t1=60.0, x_min=-10, x_max=10, x_pts=1000, x0=-8.0, c=0.24, sigma=1.0, fps=20):
    x = np.linspace(x_min, x_max, x_pts)
    t_vals = np.linspace(t0, t1, frames)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("x")
    ax.set_ylabel("y(x,t)")
    line, = ax.plot([], [], label="Gaussian wave", linewidth=2)
    title = ax.set_title("Gaussian wave — t = 0.00")
    ax.legend(loc="upper right")
    def init():
        line.set_data([], [])
        return line, title
    def update(i):
        t = t_vals[i]
        y = gaussian_wave(x, t, x0, c, sigma)
        line.set_data(x, y)
        title.set_text(f"Gaussian wave — t = {t:.2f}")
        return line, title
    ani = animation.FuncAnimation(fig, update, frames=frames, init_func=init, interval=1000//fps, blit=False, repeat=False)
    plt.show()

if __name__ == "__main__":
    show_taylor_animation(m=15, fps=2)
    show_gaussian_animation(frames=100, t0=0, t1=60, fps=20)
