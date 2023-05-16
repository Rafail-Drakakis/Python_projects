#lotto_numbers.py
from itertools import combinations
import time

def time_function_execution(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken to execute {func.__name__}: {execution_time:.10f} seconds")
    return result

def write_combinations_to_file(filename):
    with open(filename, 'w') as f:
        for combination in combinations(range(1, 50), 6):
            f.write(' '.join(str(n) for n in combination) + '\n')