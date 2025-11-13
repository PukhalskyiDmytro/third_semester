from sympy import symbols, Function, dsolve, Eq, exp, sin, cos, I, simplify, diff, solve, Matrix, hessian
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def problem_1():
    x = symbols('x', real=True)
    y = Function('y')
    ode = Eq(y(x).diff(x,2) + 4*y(x).diff(x) + 5*y(x), exp(-2*x))
    sol = dsolve(ode, ics={y(0): 1, y(x).diff(x).subs(x,0): 0})
    print("Problem 1: ODE solution y(x) =")
    sp.pprint(sp.simplify(sol.rhs))
    y_fun = sp.lambdify(x, sp.simplify(sol.rhs), 'numpy')
    xs = np.linspace(-1, 5, 400)
    ys = y_fun(xs)
    plt.figure(figsize=(8,4))
    plt.plot(xs, ys)
    plt.title("Problem 1: Solution of y''+4y'+5y = e^{-2x}, y(0)=1, y'(0)=0")
    plt.xlabel('x')
    plt.ylabel('y(x)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def problem_2():
    t = symbols('t', real=True)
    X = Function('x')(t)
    Y = Function('y')(t)
    eqs = [Eq(sp.diff(X, t), Y - X), Eq(sp.diff(Y, t), -X - Y)]
    sol = dsolve(eqs, ics={X.subs(t,0):1, Y.subs(t,0):0})
    print("\nProblem 2: System solution (x(t), y(t)):")
    for s in sol:
        sp.pprint(s.rhs)
    x_expr = sp.simplify(sol[0].rhs)
    y_expr = sp.simplify(sol[1].rhs)
    xf = sp.lambdify(t, x_expr, 'numpy')
    yf = sp.lambdify(t, y_expr, 'numpy')
    ts = np.linspace(0, 10, 500)
    plt.figure(figsize=(6,6))
    plt.plot(xf(ts), yf(ts))
    plt.scatter([1],[0], color='red')
    plt.title('Problem 2: Phase trajectory (initial (1,0))')
    plt.xlabel('x(t)')
    plt.ylabel('y(t)')
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def problem_3():
    xx, yy = symbols('xx yy', real=True)
    f = sp.exp(-(xx**2 + yy**2))*sp.sin(3*xx)
    x0 = float(sp.pi/6)
    y0 = float(sp.pi/4)
    z0 = float(f.subs({xx: x0, yy: y0}))
    fx = sp.diff(f, xx)
    fy = sp.diff(f, yy)
    fx_val = float(fx.subs({xx: x0, yy: y0}))
    fy_val = float(fy.subs({xx: x0, yy: y0}))
    print('\nProblem 3: Surface and tangent plane at (pi/6, pi/4)')
    print(f'z0 = {z0:.6f}, fx = {fx_val:.6f}, fy = {fy_val:.6f}')
    Xg = np.linspace(-2, 2, 160)
    Yg = np.linspace(-2, 2, 160)
    Xg, Yg = np.meshgrid(Xg, Yg)
    f_num = sp.lambdify((xx, yy), f, 'numpy')
    Z = f_num(Xg, Yg)
    Plane = z0 + fx_val*(Xg - x0) + fy_val*(Yg - y0)
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(Xg, Yg, Z, rstride=6, cstride=6, alpha=0.9)
    ax.plot_surface(Xg, Yg, Plane, rstride=6, cstride=6, alpha=0.5)
    ax.set_title('Problem 3: Surface and tangent plane at (pi/6, pi/4)')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.tight_layout()
    plt.show()

def problem_4():
    t = np.linspace(0, 4*np.pi, 800)
    x_t = np.sin(t)*(1 + np.cos(t))
    y_t = np.cos(t)*(1 - np.sin(t))
    plt.figure(figsize=(6,6))
    plt.plot(x_t, y_t)
    plt.title('Problem 4a: Parametric curve')
    plt.xlabel('x(t)')
    plt.ylabel('y(t)')
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('problem4_parametric.png')
    plt.show()
    xx = np.linspace(-3, 3, 700)
    yy = np.linspace(-3, 3, 700)
    XX, YY = np.meshgrid(xx, yy)
    F = (XX**2 + YY**2)**2 - (2*XX**2 - YY**2)
    plt.figure(figsize=(6,6))
    plt.contour(XX, YY, F, levels=[0])
    plt.title('Problem 4b: Implicit curve (x^2+y^2)^2 = 2x^2 - y^2')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def problem_5():
    x = symbols('x', real=True)
    y1 = x**2 - 1
    y2 = -x + 1
    solx = solve(Eq(y1, y2), x)
    points = [(float(s), float(y1.subs(x, s))) for s in solx]
    print('\nProblem 5: Intersection points:')
    for p in points:
        print(p)
    xs = np.linspace(-3, 3, 400)
    plt.figure(figsize=(6,6))
    plt.plot(xs, xs**2 - 1, label='y = x^2 - 1')
    plt.plot(xs, -xs + 1, label='y = -x + 1')
    for px, py in points:
        plt.scatter([px], [py], color='red')
        plt.text(px+0.05, py+0.05, f'({px:.3g},{py:.3g})')
    plt.legend()
    plt.title('Problem 5: Curves and intersections')
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def problem_6():
    x = symbols('x', real=True)
    expr_trig = sin(x)**4 - 2*sin(x)**2 * cos(x)**2 + cos(x)**4
    simp_trig = simplify(expr_trig)
    expr_complex = (1 + I*x)/(1 - I*x)
    simp_complex = simplify(expr_complex)
    real_part = sp.re(simp_complex)
    imag_part = sp.im(simp_complex)
    print('\nProblem 6: Trig simplification:')
    sp.pprint(simp_trig)
    print('\nComplex simplification:')
    sp.pprint(simp_complex)
    print('\nReal part:')
    sp.pprint(simplify(real_part))
    print('Imag part:')
    sp.pprint(simplify(imag_part))

def problem_7():
    x, y = symbols('x y', real=True)
    f = x**3 - 3*x*y**2
    fx = diff(f, x)
    fy = diff(f, y)
    crit = solve([fx, fy], [x, y])
    H = hessian(f, (x, y))
    print('\nProblem 7: Critical points and Hessian')
    print('Gradient:')
    sp.pprint((fx, fy))
    print('Critical points:')
    sp.pprint(crit)
    print('Hessian:')
    sp.pprint(H)
    for pt in crit:
        H_at = H.subs({x:pt[0], y:pt[1]})
        detH = sp.simplify(H_at.det())
        print(f'At {pt}: Hessian =')
        sp.pprint(H_at)
        print('Determinant =', detH)
        fxx = H_at[0,0]
        if detH.is_zero and detH == 0:
            print('Second derivative test inconclusive (degenerate).')
        else:
            if detH > 0:
                if fxx > 0:
                    print('Local minimum')
                else:
                    print('Local maximum')
            elif detH < 0:
                print('Saddle point')

if __name__ == '__main__':
    problem_1()
    problem_2()
    problem_3()
    problem_4()
    problem_5()
    problem_6()
    problem_7()
