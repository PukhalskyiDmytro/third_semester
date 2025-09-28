import numpy as np

def task1(seed=42):
    np.random.seed(seed)
    arr = np.random.randint(50, 101, size=20)
    transformed = np.where(arr < 75, 50, 100)
    return arr, transformed

def task2(seed=42):
    np.random.seed(seed)
    mat = np.random.uniform(0, 10, size=(7,3))
    col_means = mat.mean(axis=0)
    centered = mat - col_means
    return mat, col_means, centered

def task3():
    arr = np.arange(0, 51)
    mult7 = arr[arr % 7 == 0]
    mult3_gt20 = arr[(arr % 3 == 0) & (arr > 20)]
    return arr, mult7, mult3_gt20

def task4():
    x = np.linspace(0, 2*np.pi, 50)
    y = np.sin(x)
    z = np.cos(x)
    return x, y, z, y.max(), z.min()

def task5(seed=42):
    np.random.seed(seed)
    temps = np.random.uniform(-5, 10, size=30)
    neg_days = np.sum(temps < 0)
    pos_temps = temps[temps > 0]
    mean_pos = pos_temps.mean() if pos_temps.size > 0 else np.nan
    max_val, min_val = temps.max(), temps.min()
    max_indices = np.where(temps == max_val)[0]
    min_indices = np.where(temps == min_val)[0]
    return temps, neg_days, mean_pos, max_val, max_indices, min_val, min_indices

if __name__ == "__main__":
    print("Task 1:", task1())
    print("Task 2:", task2())
    print("Task 3:", task3())
    print("Task 4:", task4())
    print("Task 5:", task5())
