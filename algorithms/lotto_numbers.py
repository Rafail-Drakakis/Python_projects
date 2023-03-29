from itertools import combinations

#lotto_numbers.py
def write_combinations_to_file(filename):
    with open(filename, 'w') as f:
        for combination in combinations(range(1, 50), 6):
            f.write(' '.join(str(n) for n in combination) + '\n')
