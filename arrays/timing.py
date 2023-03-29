import time

#timing.py
def finish_time(function, algorithm_name, *positional_args, **keyword_args):
    start_time = time.time()
    result = function(*positional_args, **keyword_args)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The {algorithm_name} algorithm took {execution_time:.6f} seconds \n{algorithm_name}, {result}")
    return result
