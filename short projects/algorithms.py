import requests
import time

#count_lines.py
def count_lines(filename):
    # Open the file in read mode
    with open(filename, 'r') as f:
        # Read all the lines into a list
        lines = f.readlines()
        # Return the number of lines
        print(f'{len(lines)} lines in the file ')

#count_words.py
def count_words(filename):
    with open(filename, "r") as f:
        all_words = []
        for line in f:
            # split each line into words and add them to the list
            all_words.extend(line.split())  
        # create a dictionary to keep track of the word counts and first occurrences
        word_counts = {}
        first_occurrences = {}
        for i, word in enumerate(all_words):
            if word not in word_counts:
                # add the word to the dictionary with a count of 1 and the current index as its first occurrence
                word_counts[word] = 1
                first_occurrences[word] = i
            else:
                # increment the word count
                word_counts[word] += 1
        # print each word and its count
        print("Unique words in the file: ")
        for word in word_counts:
            print(word, word_counts[word])

#get_fact.py
def get_fact(number):
    # create a URL string by formatting the input number into the URL
    url = "http://numbersapi.com/{}".format(number)
    
    # send an HTTP GET request to the URL
    r = requests.get(url)
    
    # if the request is successful (status code 200), print the response text, otherwise, print an error message with the status code
    if r.status_code == 200:
        print(r.text)
    else: 
        print("An error occurred, code={}".format(r.status_code))

#lotto_numbers.py
def lotto_numbers(filename):
    start_time = time.time()
    
    with open(filename, 'w') as f:
        for combination in combinations(range(1, 50), 6):
            f.write(' '.join(str(n) for n in combination) + '\n')
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken to execute write_combinations_to_file: {execution_time:.10f} seconds")

def test():
	count_lines("test.txt")
	count_words("test.txt")
	get_fact(5)
	#lotto_numbers("combinations.txt")
	#os.remove("combinations.txt")
    
test()