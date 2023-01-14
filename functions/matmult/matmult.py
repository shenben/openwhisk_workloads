import numpy as np
from time import time

def matmul(N):
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)

    start = time()
    C = np.matmul(A, B)
    latency = time() - start

    return latency

def main(params):
    N = params['N']
    latency = matmul(N)
    ret_val = {}
    ret_val['latency'] = latency
    return ret_val
#print(main({'N':10}))
