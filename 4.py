import numpy as np
from math import comb


def d20_experiments(n_trials=1_000_000, seed=20251007):
    rng = np.random.default_rng(seed)
    rolls2 = rng.integers(1, 21, size=(n_trials, 2))
    emp_both20 = np.mean(np.all(rolls2 == 20, axis=1))
    theor_both20 = (1/20) ** 2
    rolls3 = rng.integers(1, 21, size=(n_trials, 3))
    emp_atleast1_20 = np.mean(np.any(rolls3 == 20, axis=1))
    theor_atleast1_20 = 1 - (19/20) ** 3
    rolls5 = rng.integers(1, 21, size=(n_trials, 5))
    emp_exactly2_20 = np.mean(np.sum(rolls5 == 20, axis=1) == 2)
    theor_exactly2_20 = comb(5, 2) * (1/20) ** 2 * (19/20) ** 3
    return [
        ("Two dice (both 20)", emp_both20, theor_both20),
        ("Three dice (>=1 20)", emp_atleast1_20, theor_atleast1_20),
        ("Five dice (exactly 2 20)", emp_exactly2_20, theor_exactly2_20),
    ]


def solve_linear_system():
    A = np.array([[2, 1, -1],
                  [-3, -1, 2],
                  [-2, 1, 2]], dtype=float)
    b = np.array([1, -4, -3], dtype=float)
    x = np.linalg.solve(A, b)
    Ax = A @ x
    check_equals = np.allclose(Ax, b)
    return A, b, x, check_equals


def simulate_ruin(K, N_threshold, r, n_trials=200_000, max_steps=100_000, seed=12345):
    if not (0.0 <= r <= 1.0):
        raise ValueError("r must be between 0 and 1")
    b_unit = K / 100.0
    if b_unit <= 0:
        raise ValueError("K must be positive")
    scale = 1.0 / b_unit
    K_units = int(round(K * scale))
    N_units = int(round(N_threshold * scale))
    up = 2
    down = -1
    caps = np.full(n_trials, K_units, dtype=int)
    active = np.ones(n_trials, dtype=bool)
    rng = np.random.default_rng(seed)
    steps = 0
    while active.any() and steps < max_steps:
        indices = np.nonzero(active)[0]
        n_active = indices.size
        if n_active == 0:
            break
        draws = rng.random(n_active)
        wins = draws < r
        caps[indices[wins]] += up
        caps[indices[~wins]] += down
        absorbed = (caps[indices] <= 0) | (caps[indices] >= N_units)
        active[indices] = ~absorbed
        steps += 1
    ruined = caps <= 0
    ruin_prob = float(np.mean(ruined))
    return ruin_prob, steps, n_trials


def run_ruin_table(K=100.0, N_threshold=200.0, r_values=None, n_trials=120_000, seed_base=1000):
    if r_values is None:
        r_values = np.linspace(0.1, 0.9, 9)
    rows = []
    for r in r_values:
        seed = seed_base + int(round(r * 100))
        ruin_prob, steps, trials = simulate_ruin(K, N_threshold, r, n_trials=n_trials, seed=seed)
        rows.append((float(r), ruin_prob, int(steps), int(trials)))
    return rows


def main(trials=1_000_000, ruin_trials=120_000, seed=20251007, K=100.0, N_threshold=200.0, seed_base=1000):
    df_d20 = d20_experiments(n_trials=trials, seed=seed)
    print("D20 experiments:")
    for event, emp, theo in df_d20:
        print(f"{event}: empirical = {emp:.8f}, theoretical = {theo:.8f}")
    print()
    A, b, x, ok = solve_linear_system()
    print("A =")
    print(A)
    print("b =", b)
    print("x =", x)
    print("A @ x == b? ->", ok)
    print()
    rows = run_ruin_table(K=K, N_threshold=N_threshold, n_trials=ruin_trials, seed_base=seed_base)
    print("Ruin simulation results:")
    print(" r    Estimated_ruin_probability   Steps_used   n_trials")
    for r, prob, steps, trials in rows:
        print(f"{r:.1f}    {prob:.6f}                   {steps:6d}     {trials:6d}")


if __name__ == '__main__':
    main()
