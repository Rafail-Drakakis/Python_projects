import os

import collatz_fibonacci_factorial

collatz_fibonacci_factorial.collatz_sequence(5)
collatz_fibonacci_factorial.fibonacci_sequence(1, 5)
collatz_fibonacci_factorial.factorial_sequence(5)

import count_text

count_text.count_lines("test.txt")
count_text.count_words("test.txt")

import get_fact

get_fact.get_fact(5)

import write_filenames_to_txt

write_filenames_to_txt.write_filenames_to_txt("filenames.txt")
os.remove("filenames.txt")

#import lotto_numbers
#lotto_numbers.time_function_execution(lotto_numbers.write_combinations_to_file, "combinations.txt")
#os.remove("combinations.txt")