import glob
import os
import requests
import pyshorteners
from itertools import combinations
    
def link_shortner(link):
    """
    The function "link_shortner" takes a long URL as input and returns a shortened URL using the
    pyshorteners library.
    
    :param link: The link parameter is the URL that you want to shorten
    :return: a shortened version of the input link using the pyshorteners library.
    """
    return pyshorteners.Shortener().tinyurl.short(link)

def count_lines(filename):
    """
    The function `count_lines` takes a filename as input, opens the file in read mode, reads all the
    lines into a list, and returns the number of lines in the file.
    
    :param filename: The filename parameter is a string that represents the name of the file you want to
    count the lines of
    :return: the number of lines in the file.
    """
    # Open the file in read mode
    with open(filename, 'r') as f:
        # Read all the lines into a list
        lines = f.readlines()
        # Return the number of lines
        return len(lines)

def count_words(filename):
    """
    The `count_words` function takes a filename as input, reads the file, and returns a dictionary
    containing the count of each word in the file.
    
    :param filename: The filename parameter is a string that represents the name of the file you want to
    count the words in
    :return: a dictionary that contains the counts of each word in the file.
    """
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
        # return the word counts dictionary
        return word_counts

def get_fact(number):
    """
    The function `get_fact` takes a number as input, creates a URL string using the number, sends an
    HTTP GET request to the URL, and returns the response text if the request is successful.
    
    :param number: The input parameter "number" is an integer representing the number for which you want
    to retrieve a fact
    :return: The function `get_fact` is returning the response text from the HTTP GET request made to
    the Numbers API.
    """
    # create a URL string by formatting the input number into the URL
    url = "http://numbersapi.com/{}".format(number)
    # send an HTTP GET request to the URL
    r = requests.get(url)
    # if the request is successful (status code 200), print the response text, otherwise, print an error message with the status code
    if r.status_code == 200:
        return r.text
    else: 
        print("An error occurred, code={}".format(r.status_code))

def lotto_numbers(filename):
    """
    The function "lotto_numbers" generates all possible combinations of 6 numbers from 1 to 49 and
    writes them to a file specified by the "filename" parameter.
    
    :param filename: The filename parameter is the name of the file that will be created to store the
    generated lotto numbers
    :return: the filename of the file that was created.
    """
    with open(filename, 'w') as f:
        for combination in combinations(range(1, 50), 6):
            f.write(' '.join(str(n) for n in combination) + '\n')
    return filename

def collect_filenames(extension):
    """
    The function `collect_filenames` collects all filenames with a given extension in the current
    directory and writes them to a file called "filenames.txt".
    
    :param extension: The "extension" parameter is a string that represents the file extension you want
    to collect filenames for. For example, if you pass "txt" as the extension, the function will collect
    all the filenames with the ".txt" extension
    :return: a file object.
    """
    files = glob.glob(os.path.join(os.getcwd(), f'*{extension}'))
    target_file = "filenames.txt"
    with open(target_file, 'w') as file:
        file.write('\n'.join(files))
    return target_file

def merge_files_by_extension(extension):
    """
    The function `merge_files_by_extension` merges all files in the current directory with a given
    extension into a single file.
    
    :param extension: The "extension" parameter is a string that represents the file extension of the
    files you want to merge. For example, if you want to merge all the text files in a directory, you
    would pass ".txt" as the extension parameter
    :return: the name of the merged file.
    """
    merged_file_name = f"merged{extension}"
    files = [file for file in os.listdir() if file.endswith(extension)]

    with open(merged_file_name, "w") as merged_file:
        for file_name in files:
            with open(file_name, "r") as file:
                merged_file.write(f"// {file_name}\n")
                for line in file:
                    merged_file.write(line)
                merged_file.write("\n")

    return merged_file_name

def main():
    """
    The main function performs various tasks such as shortening a link, counting lines in a file,
    getting a factorial, counting unique words in a file, collecting filenames with a specific
    extension, merging files with a specific extension and generating lotto numbers.
    """
    print("short link:", link_shortner("https://www.youtube.com/watch?v=Un6sYuYTZyI"))
        
    print(get_fact(5))
    
    print("Number of lines in the file:", count_lines("test.txt"))
    print("Unique words in the file:")
    word_counts = count_words("test.txt")
    for word in word_counts:
        print(word, word_counts[word])
    
    print("filenames have been collected:", collect_filenames('.py'))
    os.remove("filenames.txt")
    
    print("Merged file created:", merge_files_by_extension(".py"))
    os.remove("merged.py")
    
    print("lotto numbers are in the file:", lotto_numbers("combinations.txt"))
    os.remove("combinations.txt")

if __name__ == "__main__":    
    main()