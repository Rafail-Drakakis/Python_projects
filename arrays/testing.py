from timing import finish_time

#testing.py
def test_algorithm(algorithm_name, algorithm_func, array, *args):
    result = finish_time(algorithm_func, algorithm_name, array, *args)
    return result

