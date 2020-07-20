import time
import pymp
import numpy as np
import numba
from numba import njit, prange

N = int(1e7)
A = np.ones(N)*1
B = np.ones(N)*2

def check_solution(expected, actual):
    if abs(expected - actual)/expected > 1e-5:
        print(f"Incorrect solution\nExpected {expected}, got {actual}")

dot_product = 0.
start_time = time.time()
for i in range(0,N):
    dot_product += A[i] * B[i]
end_time = time.time()
serial_time = end_time - start_time
answer = dot_product
print(f"Serial code took {serial_time} seconds")
print("----------------------------------------")

start_time = time.time()
dot_product = A @ B
end_time = time.time()
numpy_time = end_time - start_time
check_solution(answer, dot_product)
print(f"Numpy magic took {numpy_time} seconds")
print(f"Speedup: {serial_time/numpy_time}")
print("----------------------------------------")

@njit
def numba_test(A,B,N):
    dot_product = 0
    for i in range(0, N):
        dot_product += A[i] * B[i]
    return dot_product


@njit(parallel=True)
def pnumba_test(A,B,N):
    dot_product = 0
    for i in prange(0, N):
        dot_product += A[i] * B[i]
    return dot_product

start_time = time.time()
dot_product = numba_test(A,B,N)
end_time = time.time()
numba_time = end_time - start_time
check_solution(answer, dot_product)
print(f"Serial numba took {numba_time} seconds")
print(f"Speedup: {serial_time/numba_time}")
print("----------------------------------------")

start_time = time.time()
dot_product = pnumba_test(A,B,N)
end_time = time.time()
pnumba_time = end_time - start_time
check_solution(answer, dot_product)
print(f"Parallel numba took {pnumba_time} seconds with {numba.config.NUMBA_NUM_THREADS} threads")
print(f"Speedup: {serial_time/pnumba_time}")
print("----------------------------------------")

THREADS = pymp.config.num_threads[0] # gets the value from OMP_NUM_THREADS
dot_product_unreduced = pymp.shared.array(THREADS)
start_time = time.time()
with pymp.Parallel(THREADS) as p:
    for i in p.range(0, N):
        dot_product_unreduced[p.thread_num] += A[i] * B[i]
dot_product = np.sum(dot_product_unreduced)
end_time = time.time()
parallel_time = end_time - start_time
check_solution(answer, dot_product)
print(f"Parallel code took {parallel_time} seconds using {THREADS} threads")
print(f"Speedup: {serial_time/parallel_time}")
print("----------------------------------------")

dot_product_unreduced = pymp.shared.array(THREADS)
start_time = time.time()
with pymp.Parallel(THREADS) as p:
    n = p.thread_num
    start = int(n*N/THREADS)
    end   = int((n+1)*N/THREADS) if n < THREADS-1 else N
    dot_product_unreduced[p.thread_num] = A[start:end] @ B[start:end]
dot_product = np.sum(dot_product_unreduced)
end_time = time.time()
parallel_time = end_time - start_time
check_solution(answer, dot_product)
print(f"Parallel numpy code took {parallel_time} seconds using {THREADS} threads")
print(f"Speedup: {serial_time/parallel_time}")
print("----------------------------------------")
