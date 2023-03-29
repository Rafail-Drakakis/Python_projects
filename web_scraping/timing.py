import time

# Function to print the elapsed time
def print_elapsed_time(start_time):
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"Elapsed time: {elapsed_time} seconds")

