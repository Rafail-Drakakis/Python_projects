import sys

def count_words(file):
    words = 0
    counter = file.read(1)
    while counter != "" :
        if counter == '\n' or counter == ' ' or counter == '\t':
            words += 1
        counter = file.read(1)
    file.seek(0)
    return words

def word_appearances(word, all_words):
    appearances = 0
    for w in all_words:
        if w == word:
            appearances += 1
    return appearances

def first_occurrence(word, all_words):
    pos = 0
    for i in range(len(all_words)):
        if all_words[i] == word:
            pos = i
            break
    return pos

def words():
    filename = input("Enter the file name: ")
    with open(filename, "r") as f:
        words = count_words(f)
        all_words = []
        f.seek(0)
        for i in range(words):
            word = ""
            while True:
                counter = f.read(1)
                if counter == ' ' or counter == '\n' or counter == '\t' or counter == '':
                    break
                word += counter
            all_words.append(word)
        for i in range(words):
            if first_occurrence(all_words[i], all_words) == i:
                print(all_words[i], word_appearances(all_words[i], all_words))
