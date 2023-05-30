import glob
import os
import requests
import time
import pyshorteners
import urllib.request
import shutil

#file_organizer.py
def file_organizer():
    # Get the current working directory
    directory = os.getcwd()

    # Get all files in the directory
    files = os.listdir(directory)

    # Create a dictionary to hold the file extensions and their corresponding folders
    file_types = {}

    # Loop through each file and organize them by extension
    for file in files:
        # Exclude the file_organizer.py file from being moved
        if file == "files_organizer.py":
            continue
        
        # Get the file extension
        file_extension = os.path.splitext(file)[1]

        # If the file extension doesn't exist in the dictionary, create a new folder for it
        if file_extension not in file_types:
            folder_name = file_extension.replace(".", "")
            folder_path = os.path.join(directory, folder_name)
            
            # Check if the folder already exists
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            
            file_types[file_extension] = folder_name

        # Move the file to the corresponding folder
        src_path = os.path.join(directory, file)
        dst_path = os.path.join(directory, file_types[file_extension], file)
        shutil.move(src_path, dst_path)

    print("Files have been organized!")

#link_operator.py
def link_shortener(link):
    shortener = pyshorteners.Shortener()
    short_link = shortener.tinyurl.short(link)
    print(f"Shortened Link: {short_link}")

def link_opener(link):
    shortened_url = urllib.request.urlopen(link)
    real_link = shortened_url.geturl()
    print(f"Real Link: {real_link}")

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
    print(f"Time taken to execute lotto_numbers: {execution_time:.10f} seconds")

#collect_filenames.py
def collect_filenames(file_type):
    directory = os.getcwd()
    files = glob.glob(os.path.join(directory, '*' + file_type))
    
    with open('file_names.txt', 'w') as file:
        file.write('\n'.join(files))
    print("filenames extracted succesfully")
    return files

#test.py
def test():
    print("Please choose an option")
    print("1. Run file organizer")
    print("2. Run link shortener")
    print("3. Run link opener")
    print("4. Run count lines")
    print("5. Run count words ")
    print("6. Run get fact")
    print("7. Create a file with lotto numbers")
    print("8. collect all the filenames of a specific extension")
    print("9.Exit ")

    choice = int(input("Enter your choice (1-8): "))

    if choice == 1:
        file_organizer()
    elif choice == 2:
        link = input("Enter the link to shorten: ")
        link_shortener(link)
    elif choice == 3:
        link = input("Enter the shorten link to show the original: ")
        link_opener(link)
    elif choice == 4:
        filename = input("Enter the name of the file to count the lines inside it: ")
        count_lines(filename)
    elif choice == 5:
        filename = input("Enter the name of the file to count the unique words inside it: ")
        count_words(filename)
    elif choice == 6:
        num = int(input("Enter the number to get an intresting fact for it: "))
        get_fact(num)
    elif choice == 7:
        lotto_numbers("combinations.txt")
    elif choice == 8:
        file_type = input("What type are the files you want to extract? ")
        collect_filenames(file_type)
        os.remove("file_names.txt")
    elif choice == 9:
        print("Exiting the test menu...")
    else:
        print("Invalid choice. Please enter a number from 1 to 8")

test()