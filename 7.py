import sympy as sp
x, y, a = sp.symbols('x y a')

def task1_algebra():
    F = (x**3 - y**3)/(x**2 - y**2) + 1/(x - y) - 1/(x + y)
    return {
        'F': F,
        'expand': sp.expand(F),
        'factor': sp.factor(F),
        'cancel': sp.cancel(F),
        'together': sp.simplify(sp.together(F)),
        'apart': sp.apart(F, x),
        'collect_y': sp.collect(F, y)
    }

def task2_subs():
    g = sp.exp(a*x) - sp.sqrt(1+x)
    expr_exact = g.subs({x: sp.Rational(1,5), a: sp.log(3)})
    expr_num = sp.N(expr_exact, 40)
    expr_ns = sp.nsimplify(expr_num)
    return {'g': g, 'exact': expr_exact, 'numeric_40': expr_num, 'nsimplify': expr_ns}

def task3_limits():
    limit_a = sp.limit((sp.tan(x) - x)/x**3, x, 0)
    limit_b = sp.limit(sp.log(1+x)/sp.sqrt(x), x, sp.oo)
    limit_c = sp.limit(x**x, x, 0, dir='+')
    return {'lim_a': limit_a, 'lim_b': limit_b, 'lim_c': limit_c}

def task4_diff_int():
    h = sp.exp(-x)*sp.cos(2*x)
    h1 = sp.diff(h, x)
    h2 = sp.diff(h, x, 2)
    integral_h = sp.integrate(h, (x, 0, sp.pi))
    return {'h': h, "h'": h1, "h''": h2, 'integral': integral_h}

def task5_taylor():
    f = sp.log(1-x) + sp.sqrt(1+x)
    series_f = sp.series(f, x, 0, 7).removeO()
    exact_val = f.subs(x, sp.Rational(1,3))
    approx_val = series_f.subs(x, sp.Rational(1,3))
    error = sp.N(exact_val - approx_val, 20)
    return {'f': f, 'series_x6': series_f, 'exact_at_1_3': exact_val, 'approx_at_1_3': approx_val, 'error': error}

def task6_equations():
    eq1 = x**3 - 5*x + 1
    roots_exact = sp.solve(eq1, x)
    roots_numeric = sp.nroots(eq1)
    equation2 = sp.exp(-x) - x**2
    sol1 = sp.nsolve(equation2, 0)
    sol2 = sp.nsolve(equation2, 1)
    sol3 = sp.nsolve(equation2, 3)
    return {'eq1_exact_roots': roots_exact, 'eq1_numeric_roots': roots_numeric, 'nsolve_0': sol1, 'nsolve_1': sol2, 'nsolve_3': sol3}

def task7_matrices():
    A = sp.Matrix([[3, -1, 2],[0, 2, -2],[1, 1, 1]])
    b = sp.Matrix([4, -2, 3])
    rank_A = A.rank()
    det_A = A.det()
    inv_A = A.inv() if det_A != 0 else None
    x_sol = A.LUsolve(b)
    check = A*x_sol - b
    return {'A': A, 'b': b, 'rank': rank_A, 'det': det_A, 'inv': inv_A, 'solution': x_sol, 'check': check}

def main():
    r1 = task1_algebra()
    print('Task 1 results:')
    for k, v in r1.items():
        print(k, '=', v)
    r2 = task2_subs()
    print('\nTask 2 results:')
    for k, v in r2.items():
        print(k, '=', v)
    r3 = task3_limits()
    print('\nTask 3 results:')
    for k, v in r3.items():
        print(k, '=', v)
    r4 = task4_diff_int()
    print('\nTask 4 results:')
    for k, v in r4.items():
        print(k, '=', v)
    r5 = task5_taylor()
    print('\nTask 5 results:')
    for k, v in r5.items():
        print(k, '=', v)
    r6 = task6_equations()
    print('\nTask 6 results:')
    for k, v in r6.items():
        print(k, '=', v)
    r7 = task7_matrices()
    print('\nTask 7 results:')
    for k, v in r7.items():
        print(k, '=', v)

if __name__ == '__main__':
    main()
