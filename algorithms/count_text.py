import requests 
import sys

#count_lines.py
def count_lines_menu():
    file_name = input("Enter the file name: ")
    num_lines = count_lines(file_name)
    print(f"Number of lines in the file: {num_lines}")

def count_lines(filename):
    # Open the file in read mode
    with open(filename, 'r') as f:
        # Read all the lines into a list
        lines = f.readlines()
        # Return the number of lines
        return len(lines)

#count_words.py
def count_words(file):
    words = 0
    for line in file:
        words += len(line.split())
    file.seek(0)  # reset the file pointer to the beginning of the file
    return words

# Function to count the number of times a given word appears in a list of words
def word_appearances(word, all_words):
    return all_words.count(word)

# Function to find the index of the first occurrence of a given word in a list of words
def first_occurrence(word, all_words):
    return all_words.index(word)

# Main function to read the input file and process the words
def words():
    filename = input("Enter the file name: ")
    with open(filename, "r") as f:
        all_words = []
        for line in f:
            all_words.extend(line.split())  # split each line into words and add them to the list
        printed_words = set()  # create a set to keep track of which words have already been printed
        for word in all_words:
            if word not in printed_words:
                # print the word and its count if it hasn't been printed before
                print(word, word_appearances(word, all_words))
                printed_words.add(word)  # add the word to the set of printed words
                
def count_text_menu():
    choice = int(input("Enter\n1.For count the lines in a file \n2.For count unique words in a file: "))
    if choice == 1:
        count_lines_menu()
    elif choice == 2:
        words()
