from googlesearch import search
import webbrowser

def search_google(query):
    """
    The function `search_google` takes a query as input and uses the `search` function to search Google
    for the query, printing the top 5 results.
    
    :param query: The query parameter is a string that represents the search query you want to perform
    on Google. It can be any keyword or phrase that you want to search for
    """
    try:
        for j in search(query, num_results=5):
            print(j)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def search_youtube(query):
    """
    The function `search_youtube` takes a query as input and opens a new tab in the web browser with the
    YouTube search results for that query.
    
    :param query: The query parameter is the search term or keywords that you want to search for on
    YouTube. It can be a single word or a phrase
    """
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open_new_tab(search_url)
    
def search_with_each_line(file_path):
    """
    The function reads each line from a file, prompts the user to choose between searching on Google or
    YouTube for each line, and then performs the corresponding search.
    
    :param file_path: The file path is the location of the file that you want to read and search
    through. It should be a string that specifies the path to the file, including the file name and
    extension. For example, "C:/Users/username/Documents/file.txt" or "my_folder/my_file.txt"
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                query = line.strip()
                print(f"Searching for: {query}")
                choice = int(input("Enter \n1.To search on google\n2.To search on youtube: "))
                if choice == 1:
                    search_google(query)
                elif choice == 2:
                    search_youtube(query)
                print()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    file_path = input("Enter the file name: ")
    search_with_each_line(file_path)

if __name__ == "__main__":
    main()