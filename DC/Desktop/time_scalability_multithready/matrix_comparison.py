import time
import random
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def generate_matrix(size):
    return [[random.random() for _ in range(size)] for _ in range(size)]

def matrix_multiply_sequential(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def compute_row(i, A, B):
    n = len(A)
    row = [0] * n
    for j in range(n):
        for k in range(n):
            row[j] += A[i][k] * B[k][j]
    return row

def matrix_multiply_parallel(A, B, executor_class, max_workers=None):
    n = len(A)
    with executor_class(max_workers=max_workers) as executor:
        futures = [executor.submit(compute_row, i, A, B) for i in range(n)]
        results = [future.result() for future in futures]
    return results

def time_function(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return end - start, result

def main():
    sizes = [50, 100, 500, 1000]
    methods = {
        'Sequential': lambda A, B: matrix_multiply_sequential(A, B),
        'Multithreading': lambda A, B: matrix_multiply_parallel(A, B, ThreadPoolExecutor, max_workers=4),
        'Multiprocessing': lambda A, B: matrix_multiply_parallel(A, B, ProcessPoolExecutor, max_workers=4)
    }

    for size in sizes:
        print(f"\nMatrix size: {size}x{size}")
        A = generate_matrix(size)
        B = generate_matrix(size)

        for method_name, method_func in methods.items():
            elapsed, _ = time_function(method_func, A, B)
            print(f"{method_name}: {elapsed:.4f} seconds")

if __name__ == "__main__":
    main()
