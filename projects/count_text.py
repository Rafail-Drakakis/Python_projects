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