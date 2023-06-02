import glob, os, time, shutil
import requests, pyshorteners, urllib.request

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
        # Exclude the file_organizer.py file from being moved (assume is the file which contains the code)
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
    
#link_operator.py
def link_shortner(link):
    return pyshorteners.Shortener().tinyurl.short(link)

#count_lines.py
def count_lines(filename):
    # Open the file in read mode
    with open(filename, 'r') as f:
        # Read all the lines into a list
        lines = f.readlines()
        # Return the number of lines
        return len(lines)

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
        # return the word counts dictionary
        return word_counts

#get_fact.py
def get_fact(number):
    # create a URL string by formatting the input number into the URL
    url = "http://numbersapi.com/{}".format(number)
    # send an HTTP GET request to the URL
    r = requests.get(url)
    # if the request is successful (status code 200), print the response text, otherwise, print an error message with the status code
    if r.status_code == 200:
        return r.text
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
    return execution_time

#collect_filenames.py
def collect_filenames(extension):
    files = glob.glob(os.path.join(os.getcwd(), f'*.{extension}'))
    with open('filenames.txt', 'w') as file:
        file.write('\n'.join(files))
    return file

def main():
    print("short link:", link_shortner("https://www.youtube.com/watch?v=Un6sYuYTZyI"))
    print("Number of lines in the file:", count_lines("test.txt"))
    print(get_fact(5))
    print(f'Time taken to execute lotto_numbers: {lotto_numbers("combinations.txt"):.10f} seconds')
    print("files have been organized", file_organizer())

    print("Unique words in the file: ")
    word_counts = count_words("test.txt")
    for word in word_counts:
        print(word, word_counts[word])
    
    collect_filenames('py')
    print("filenames have been collected")

main()