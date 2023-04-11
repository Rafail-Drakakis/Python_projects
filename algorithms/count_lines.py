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

