import math
from time import time

def float_operations(N):
    start = time()
    for i in range(0, N):
        sin_i = math.sin(i)
        cos_i = math.cos(i)
        sqrt_i = math.sqrt(i)
    latency = time() - start
    return latency

def main(params):
    N = int(params['N'])
    ret_val = {}
    ret_val['latency'] = float_operations(N)
    return ret_val
