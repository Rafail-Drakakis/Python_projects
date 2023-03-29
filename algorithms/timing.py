import time

#timing.py
def time_function_execution(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken to execute {func.__name__}: {execution_time:.10f} seconds")
    return result
